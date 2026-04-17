import numpy as np


class SuggestionModel:
    column_indexes = {
        "product_name": 0,
        "signal_strength": 1
    }

    # Identifies trending products in the dataset and assigns tags based on various business objectives
    def __init__(self, data):
        self.data = data
    
    # Sorts products by "key" and picks the top "count", only including rows meeting "filters" if provided
    def get_suggestions(self, count=5, key=None, filters=None):
        filtered_data = self.data[filters,:] if filters else self.data
        return self.data[filtered_data[:,(key if key else SuggestionModel.column_indexes["signal_strength"])].argsort(axis=0)[:-count-1],:]

    # Standardize column indices. Usage:
    # SuggestionModel.clean_data(data, product_name=0, signal_strength=4, ...)
    # Returns a new array with standardized column indices
    # Missing columns are filled with NaN
    def clean_data(data, **kwargs):
        keys = [-1] * len(SuggestionModel.column_indexes)
        for key, val in SuggestionModel.column_indexes.items():
            keys[val] = key
        return np.hstack((data[:,kwargs[key]] if key in kwargs else np.full((data.shape[0],1), np.nan) for key in keys))
