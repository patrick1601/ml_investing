import pandas as pd
import sys

pd.set_option('display.max_columns', None)

if __name__ == '__main__':
    # import data
    x = pd.read_csv('Annual_Stock_Price_Fundamentals.csv', index_col=0)
    y = pd.read_csv('Annual_Stock_Price_Performance.csv', index_col=0)

    # remove rows where no share price
    bool_list = ~y['Open Price'].isnull()
    y=y[bool_list]
    x=x[bool_list]

    # remove rows where no listed number of shares
    bool_list = ~x['Shares (Diluted)_x'].isnull()
    y=y[bool_list]
    x=x[bool_list]

    # remove rows where there is low/no volume
    bool_list = ~((y['Volume']<1e4) | (y['Volume2']<1e4))
    y=y[bool_list]
    x=x[bool_list]

    # remove rows with missing dates (also removes latest data which we cannot use)
    bool_list = ~y['Date2'].isnull()
    y=y[bool_list]
    x=x[bool_list]

    y=y.reset_index(drop=True)
    x=x.reset_index(drop=True)

    # create market cap feature
    x['Market Cap'] = y['Open Price']*x['Shares (Diluted)_x']

    print(x.shape)
    print(y.shape)

    x.to_csv('Annual_Stock_Price_Fundamentals_Filtered.csv')
    y.to_csv('Annual_Stock_Price_Performance_Filtered.csv')