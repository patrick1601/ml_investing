import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix

pd.set_option('display.max_columns', None)

if __name__ == '__main__':
    x = pd.read_csv('Annual_Stock_Price_Fundamentals.csv', index_col=0)
    y = pd.read_csv('Annual_Stock_Price_Performance.csv', index_col=0)

    # scatter plot of revenue and net income
    attributes = ['Revenue', 'Net Income']
    scatter_matrix(x[attributes])
    plt.show()

    # filter for shares that have less than 10,000 shares volume
    print(y[(y['Volume']<1e4) | (y['Volume']<1e4)])