export const TOP5 = [
  { rank: 1, name: 'Ginger Chew Candy',        cat: 'Confections', signal: 10, bar: 100, color: '#1B3A5C', badge: 'hot', approved: true,  icon: '🍬' },
  { rank: 2, name: 'Asian Ginseng Root Powder', cat: 'Ginseng',     signal: 9,  bar: 97,  color: '#2557A7', badge: 'hot', approved: true,  icon: '🌾' },
  { rank: 3, name: 'Chrysanthemum Tea Bags',    cat: 'Teas',        signal: 8,  bar: 88,  color: '#3A7BD5', badge: 'hot', approved: true,  icon: '🌸' },
]

export const KEYWORDS = [
  { text: 'ginseng',          tier: 'hot', size: 'xl' },
  { text: 'ginger',           tier: 'hot', size: 'xl' },
  { text: 'adaptogen',        tier: 'hot', size: 'lg' },
  { text: 'turmeric',         tier: 'hot', size: 'lg' },
  { text: 'mushroom blend',   tier: 'hot', size: 'md' },
  { text: "lion's mane",      tier: 'hot', size: 'md' },
  { text: 'ashwagandha',      tier: 'hot', size: 'md' },
  { text: 'ginseng shot',     tier: 'hot', size: 'md' },
  { text: 'matcha',           tier: 'mid', size: 'lg' },
  { text: 'probiotic',        tier: 'mid', size: 'md' },
  { text: 'herbal tea',       tier: 'mid', size: 'md' },
  { text: 'tiger balm',       tier: 'mid', size: 'md' },
  { text: 'collagen',         tier: 'mid', size: 'sm' },
  { text: 'immune support',   tier: 'mid', size: 'sm' },
  { text: 'kombucha',         tier: 'mid', size: 'sm' },
  { text: 'elderberry',       tier: 'mid', size: 'sm' },
  { text: 'herbal gummy',     tier: 'mid', size: 'sm' },
  { text: 'chrysanthemum',    tier: 'low', size: 'sm' },
  { text: 'functional snack', tier: 'low', size: 'sm' },
  { text: 'mooncake',         tier: 'low', size: 'sm' },
]

export const KEYWORD_POSITIONS = [
  { top: '32%', left: '49%' }, { top: '26%', left: '37%' },
  { top: '38%', left: '66%' }, { top: '21%', left: '68%' },
  { top: '50%', left: '47%' }, { top: '46%', left: '78%' },
  { top: '62%', left: '29%' }, { top: '57%', left: '57%' },
  { top: '18%', left: '52%' }, { top: '74%', left: '51%' },
  { top: '37%', left: '16%' }, { top: '29%', left: '81%' },
  { top: '79%', left: '69%' }, { top: '23%', left: '26%' },
  { top: '68%', left: '79%' }, { top: '54%', left: '17%' },
  { top: '71%', left: '39%' }, { top: '42%', left: '23%' },
  { top: '79%', left: '21%' }, { top: '49%', left: '86%' },
]

export const OPPS = [
  { icon: '🍬', name: 'Kombucha-Ginger Chew',       sub: 'Ginger + fermented trend',        badge: 'Develop',    bc: '#EAF5EE', bt: '#2E7D52' },
  { icon: '🌱', name: 'Ginseng-Adaptogen Snack Bar', sub: 'Adaptogens + PoP ginseng line',   badge: 'Develop',    bc: '#EAF5EE', bt: '#2E7D52' },
  { icon: '🍵', name: "Lion's Mane Herbal Tea",      sub: 'Distribute existing product',     badge: 'Distribute', bc: '#EBF3FD', bt: '#185FA5' },
  { icon: '⚡', name: 'Ginseng Energy Shot',          sub: 'Functional beverage white space', badge: 'Develop',    bc: '#EAF5EE', bt: '#2E7D52' },
  { icon: '✨', name: 'Tiger Balm Ginseng Serum',    sub: 'Expand Tiger Balm into skincare', badge: 'Develop',    bc: '#FEF6E6', bt: '#854F0B' },
]

export const ALERTS = [
  { color: '#C05621', html: '<strong>Tariff watch:</strong> Chinese herb imports face potential 15% increase — monitor ginseng sourcing costs.' },
  { color: '#2557A7', html: "<strong>Rising demand:</strong> Lion's mane mushroom supplement searches up 340% YoY on Google Trends." },
  { color: '#2E7D52', html: '<strong>Shelf life clear:</strong> All top-5 recommendations exceed 12-month shelf life requirement.' },
  { color: '#C9963A', html: '<strong>TikTok signal:</strong> "herbal gummy" and "ginseng shot" trending in wellness category this week.' },
]

export const PRODUCTS = [
  { name: 'Ginger Chew Candy',           cat: 'ginger',          signal: 10, badge: 'hot',    approved: true,  icon: '🍬', type: 'distribute' },
  { name: 'Asian Ginseng Root Powder',   cat: 'asianginseng',    signal: 9,  badge: 'hot',    approved: true,  icon: '🌾', type: 'develop'    },
  { name: 'Chrysanthemum Tea Bags',      cat: 'teas',            signal: 8,  badge: 'hot',    approved: true,  icon: '🌸', type: 'distribute' },
  { name: 'Tiger Balm Sport Roll-On',    cat: 'tigerbalm',       signal: 8,  badge: 'hot',    approved: true,  icon: '🐯', type: 'distribute' },
  { name: "Lion's Mane Capsules",        cat: 'personalcare',    signal: 8,  badge: 'new',    approved: true,  icon: '🧠', type: 'distribute' },
  { name: 'American Ginseng Slices',     cat: 'americanginseng', signal: 8,  badge: 'hot',    approved: true,  icon: '🌱', type: 'distribute' },
  { name: 'Dark Chocolate Ginger',       cat: 'chocolates',      signal: 8,  badge: 'hot',    approved: true,  icon: '🍫', type: 'develop'    },
  { name: 'Herbal Throat Drops',         cat: 'personalcare',    signal: 8,  badge: 'hot',    approved: true,  icon: '🌿', type: 'distribute' },
  { name: 'Turmeric Supplement',         cat: 'personalcare',    signal: 8,  badge: 'hot',    approved: true,  icon: '💊', type: 'distribute' },
  { name: 'Ginseng Energy Shot',         cat: 'americanginseng', signal: 7,  badge: 'rising', approved: true,  icon: '⚡', type: 'develop'    },
  { name: 'Oolong Loose Leaf Tea',       cat: 'teas',            signal: 7,  badge: 'rising', approved: true,  icon: '🍵', type: 'distribute' },
  { name: 'Matcha Latte Mix',            cat: 'teas',            signal: 7,  badge: 'new',    approved: true,  icon: '🫖', type: 'distribute' },
  { name: 'Probiotic Blend',             cat: 'personalcare',    signal: 7,  badge: 'rising', approved: true,  icon: '🫙', type: 'distribute' },
  { name: 'Almond Sesame Brittle',       cat: 'candies',         signal: 7,  badge: 'rising', approved: true,  icon: '🥜', type: 'distribute' },
  { name: 'Instant Pho Kit',             cat: 'instantfood',     signal: 7,  badge: 'hot',    approved: true,  icon: '🍜', type: 'distribute' },
  { name: 'Herbal Muscle Rub',           cat: 'personalcare',    signal: 7,  badge: 'rising', approved: true,  icon: '💪', type: 'develop'    },
  { name: 'Green Tea Extract',           cat: 'teas',            signal: 7,  badge: 'rising', approved: false, icon: '🌿', type: 'develop'    },
  { name: 'Ginger Candy Assortment',     cat: 'ginger',          signal: 7,  badge: 'rising', approved: true,  icon: '🍡', type: 'distribute' },
  { name: 'Ginseng Honey Sticks',        cat: 'asianginseng',    signal: 6,  badge: 'rising', approved: true,  icon: '🍯', type: 'develop'    },
  { name: 'Ginseng-Adaptogen Snack',     cat: 'asianginseng',    signal: 6,  badge: 'rising', approved: false, icon: '🌾', type: 'develop'    },
  { name: 'Ginger Kombucha Mix',         cat: 'ginger',          signal: 6,  badge: 'new',    approved: false, icon: '🧪', type: 'develop'    },
  { name: 'Mooncake — Red Bean',         cat: 'mooncakes',       signal: 6,  badge: 'rising', approved: true,  icon: '🥮', type: 'distribute' },
  { name: 'Ginseng Face Serum',          cat: 'americanginseng', signal: 6,  badge: 'new',    approved: true,  icon: '✨', type: 'develop'    },
  { name: 'Dried Lychee Fruit',          cat: 'nutsfruits',      signal: 6,  badge: 'new',    approved: true,  icon: '🍈', type: 'distribute' },
]

export const PRODUCT_DETAILS = {
  'Ginger Chew Candy': {
    shelfLife: 18, origin: 'Thailand / USA',
    ingredients: 'Ginger extract, cane sugar, natural flavors',
    keywords: ['ginger', 'great deal', 'limited time'],
    status: 'New Product - Develop', statusColor: '#2E7D52',
  },
  'Asian Ginseng Root Powder': {
    shelfLife: 24, origin: 'South Korea',
    ingredients: '100% Pure Korean Red Ginseng Root Powder',
    keywords: ['ginseng', 'adaptogen', 'immune support'],
    status: 'Existing - Expand Distribution', statusColor: '#185FA5',
  },
  'Chrysanthemum Tea Bags': {
    shelfLife: 36, origin: 'China',
    ingredients: 'Dried Chrysanthemum flowers',
    keywords: ['herbal tea', 'chrysanthemum'],
    status: 'Existing - Distribute', statusColor: '#185FA5',
  },
  'Tiger Balm Sport Roll-On': {
    shelfLife: 36, origin: 'Singapore',
    ingredients: 'Camphor, Menthol, Cajuput Oil, Cassia Oil',
    keywords: ['tiger balm', 'summer'],
    status: 'Existing - Expand Line', statusColor: '#185FA5',
  },
  "Lion's Mane Capsules": {
    shelfLife: 24, origin: 'USA / China',
    ingredients: "Lion's Mane Mushroom Extract, Vegetable Capsule",
    keywords: ["lion's mane", 'mushroom blend', 'adaptogen'],
    status: 'New Product - Develop', statusColor: '#2E7D52',
  },
}

export const DEFAULT_DETAILS = {
  shelfLife: 24, origin: 'Multiple', ingredients: 'Proprietary blend',
  keywords: ['wellness'], status: 'New Product', statusColor: '#2E7D52',
}

export const CATEGORIES = [
  { key: 'all',           label: 'All',                      color: '#993C1D' },
  { key: 'americanginseng', label: 'American Ginseng',       color: 'var(--navy)' },
  { key: 'asianginseng',  label: 'Asian Ginseng',            color: '#2557A7' },
  { key: 'candies',       label: 'Candies',                  color: '#2E7D52' },
  { key: 'chocolates',    label: 'Chocolates',               color: '#C9963A' },
  { key: 'cookies',       label: 'Cookies',                  color: '#993556' },
  { key: 'ginger',        label: 'Ginger',                   color: '#534AB7' },
  { key: 'instantfood',   label: 'Instant food / seasonings',color: '#993C1D' },
  { key: 'nutsfruits',    label: 'Ginseng',                  color: '#2557A7' },
  { key: 'personalcare',  label: 'Teas',                     color: '#2E7D52' },
  { key: 'teas',          label: 'Confections',              color: '#C9963A' },
  { key: 'tigerbalm',     label: 'Wellness',                 color: '#993556' },
  { key: 'other',         label: 'Personal care',            color: '#534AB7' },
]
