import math
import numpy as np


def signal_strength(product, trends_data: dict) -> float:
    """
    Signal strength from company sales data + Google Trends data.
    Accepts a Product or NewProduct. Sales fields may be None for new products.
    Returns normalized score 0–1.
    """

    # ── 1. SALES COMPONENT ──────────────────────────────────────────────────

    order_count   = product.order_count or 0
    total_qty     = product.total_qty_shipped or 0
    total_revenue = product.total_revenue or 0
    avg_unit_cost = product.avg_unit_cost or 1

    implied_revenue_per_unit = total_revenue / max(total_qty, 1)
    margin_ratio = implied_revenue_per_unit / max(avg_unit_cost, 1)
    margin_score = min(max((margin_ratio - 1) / 4.0, 0.0), 1.0)

    order_score  = min(math.log1p(order_count) / math.log1p(1000), 1.0)
    volume_score = min(math.log1p(total_qty) / math.log1p(1_000_000), 1.0)

    sales_score = (margin_score * 0.5) + (order_score * 0.25) + (volume_score * 0.25)

    # ── 2. TRENDS TIME SERIES COMPONENT ─────────────────────────────────────

    time_series = trends_data.get('interest_over_time', {})
    if time_series and isinstance(list(time_series.values())[0], dict):
        time_series = list(time_series.values())[0]

    values = [v for _, v in sorted(time_series.items(), key=lambda x: int(x[0]))]

    if len(values) >= 2:
        recent  = values[-8:]
        earlier = values[:-8]

        recent_avg  = sum(recent) / len(recent)
        earlier_avg = sum(earlier) / len(earlier) if earlier else recent_avg
        trend_direction = (recent_avg - earlier_avg) / max(earlier_avg, 1)
        trend_score = min(max((trend_direction + 1) / 2, 0.0), 1.0)

        x = np.arange(len(recent))
        slope = np.polyfit(x, recent, 1)[0]
        momentum_score = min(max((slope + 10) / 20, 0.0), 1.0)

        std = np.std(values)
        mean = np.mean(values)
        cv = std / max(mean, 1)
        volatility_penalty = min(cv, 1.0)

        peak_idx = values.index(max(values))
        peak_recency_score = peak_idx / max(len(values) - 1, 1)

        time_score = (
            trend_score          * 0.35 +
            momentum_score       * 0.35 +
            peak_recency_score   * 0.20 +
            (1 - volatility_penalty) * 0.10
        )
    else:
        time_score = 0.5

    # ── 3. QUERY INTENT COMPONENT ────────────────────────────────────────────

    related        = trends_data.get('related_queries', {})
    top_queries    = related.get('top', [])
    rising_queries = related.get('rising', [])

    top_score = 0.0
    if top_queries:
        top_values = sorted([q['value'] for q in top_queries], reverse=True)
        weighted = sum(v / (i + 1) for i, v in enumerate(top_values))
        top_score = min(weighted / 300.0, 1.0)

    rising_score = 0.0
    if rising_queries:
        numeric = [q['value'] for q in rising_queries if isinstance(q['value'], (int, float))]
        if numeric:
            rising_score = min(sum(numeric) / len(numeric) / 500.0, 1.0)

    query_score = (top_score * 0.65) + (rising_score * 0.35)

    # ── 4. FINAL WEIGHTED COMBINATION ────────────────────────────────────────

    # New products have no sales data so we redistribute that weight to trends
    has_sales = product.order_count is not None
    if has_sales:
        weights = {'sales': 0.40, 'trends': 0.35, 'queries': 0.25}
    else:
        weights = {'sales': 0.00, 'trends': 0.60, 'queries': 0.40}

    final = (
        weights['sales']   * sales_score  +
        weights['trends']  * time_score   +
        weights['queries'] * query_score
    )

    return round(min(max(final, 0.0), 1.0), 4)


def socialmedia_signal_strength(data: dict) -> float:
    """
    Computes a normalized signal strength score (0–1) from social/ad keyword data.
    """

    def parse_num(val):
        if isinstance(val, (int, float)):
            return float(val)
        val = str(val).replace('%', '').replace('USD', '').replace(',', '').strip()
        multiplier = 1_000_000 if val.endswith('M') else 1_000 if val.endswith('K') else 1
        val = val.rstrip('KM').strip()
        return float(val) * multiplier

    popularity   = parse_num(data.get('popularity', 0))
    pop_change   = parse_num(data.get('popularity_change', 0))
    ctr          = parse_num(data.get('ctr', 0))
    cvr          = parse_num(data.get('cvr', 0))
    cpa          = parse_num(data.get('cpa', 0))
    cost         = parse_num(data.get('cost', 0))
    impressions  = parse_num(data.get('impressions', 0))
    view_rate_6s = parse_num(data.get('6s_view_rate', 0))
    likes        = parse_num(data.get('likes', 0))
    shares       = parse_num(data.get('shares', 0))
    comments     = parse_num(data.get('comments', 0))
    rank         = parse_num(data.get('rank', 99))

    engagement       = likes + (shares * 3) + (comments * 2)
    engagement_score = 1 - math.exp(-engagement / 2000)
    reach_score      = min(math.log1p(impressions) / math.log1p(500_000), 1.0)
    conv_score       = min((ctr * cvr) / 20.0, 1.0)
    efficiency_score = 1 - min((cpa / (cost + 1e-9)) / 50.0, 1.0)
    momentum_score   = min(max((popularity / 200.0) * (1 + pop_change / 100.0), 0.0), 1.0)
    attention_score  = min(view_rate_6s / 15.0, 1.0)
    rank_score       = 1.0 / rank

    weights = {
        'engagement': 0.20, 'reach':      0.15, 'conversion': 0.25,
        'efficiency': 0.20, 'momentum':   0.10, 'attention':  0.05, 'rank': 0.05,
    }

    final = (
        weights['engagement']  * engagement_score +
        weights['reach']       * reach_score      +
        weights['conversion']  * conv_score        +
        weights['efficiency']  * efficiency_score  +
        weights['momentum']    * momentum_score    +
        weights['attention']   * attention_score   +
        weights['rank']        * rank_score
    )

    return round(min(max(final, 0.0), 1.0), 4)
