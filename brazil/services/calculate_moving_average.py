import pandas as pd


def calculate_moving_average(data, window_size):
    """
    Calculates the moving average of list of data
    """
    data_series = pd.Series(data)
    windows = data_series.rolling(window_size)
    moving_averages = windows.mean()
    moving_averages = moving_averages.fillna(0)
    moving_averages = moving_averages.round(decimals=2)
    moving_averages_list = moving_averages.tolist()
    return moving_averages_list
