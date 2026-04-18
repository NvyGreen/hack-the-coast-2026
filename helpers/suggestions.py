import numpy as np
import json
from pathlib import Path


class SuggestionModel:
    column_indexes = {
        "product_name": 0,
        "signal_strength": 1
    }

    # Identifies trending products in the dataset and assigns tags based on various business objectives
    def __init__(self, data, trends_file="datasets/trends_data.json"):
        self.data = data
        self.trends_data = self.load_trends_data(trends_file)
    
    def load_trends_data(self, file_path):
        """Load trends data from JSON file."""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Trends file {file_path} not found. Proceeding without trends.")
            return {}
    
    def get_trend_score(self, category):
        """Compute a trend score for a category based on recent interest."""
        if category not in self.trends_data:
            return 0
        
        trends = json.loads(self.trends_data[category])
        # Remove isPartial
        trends.pop('isPartial', None)
        
        # Get the latest values for each keyword
        latest_scores = []
        for keyword, data in trends.items():
            if data:  # Check if data is not empty
                # Get the last timestamp's value
                timestamps = list(data.keys())
                if timestamps:
                    latest_value = data[timestamps[-1]]
                    latest_scores.append(latest_value)
        
        # Average of latest scores, or 0 if no data
        return np.mean(latest_scores) if latest_scores else 0
    
    # Sorts products by "key" and picks the top "count", only including rows meeting "filters" if provided
    # what is the format for filters? who knows!
    def get_suggestions(self, count=5, key=None, filters=None, use_trends=False):
        filtered_data = self.filter_data(filters)
        
        if use_trends and self.trends_data:
            # Add trend scores to signal strength
            scores = []
            for row in filtered_data:
                category = row[self.column_indexes["product_name"]]
                base_score = row[self.column_indexes["signal_strength"]]
                trend_score = self.get_trend_score(category)
                combined_score = base_score + trend_score  # Simple addition, can be weighted
                scores.append(combined_score)
            scores = np.array(scores)
            top_indices = scores.argsort()[-count:][::-1]  # Top count in descending order
        else:
            sort_key = key if key is not None else self.column_indexes["signal_strength"]
            top_indices = filtered_data[:, sort_key].argsort()[-count:][::-1]
        
        return filtered_data[top_indices]
    
    # goofy filtering function
    def filter_data(self, filters=None):
        return self.data[filters,:] if filters else self.data

    # Standardize column indices. Usage:
    # SuggestionModel.clean_data(data, product_name=0, signal_strength=4, ...)
    # Returns a new array with standardized column indices
    # Missing columns are filled with NaN
    def clean_data(data, **kwargs):
        keys = [-1] * len(SuggestionModel.column_indexes)
        for key, val in self.column_indexes.items():
            keys[val] = key
        return np.hstack((data[:,kwargs[key]] if key in kwargs else np.full((data.shape[0],1), np.nan) for key in keys))
