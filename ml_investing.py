import numpy as np
import pandas as pd

pd.set_option('display.max_columns', None)

# Data from https://simfin.com/
def getXDataMerged():
    a = pd.read_csv('us-income-annual.csv', delimiter=';')
    b = pd.read_csv('us-balance-annual.csv', delimiter=';')
    c = pd.read_csv('us-cashflow-annual.csv', delimiter=';')

    print('Income Statement csv is: ', a.shape)
    print('Balance Sheet csv is: ', b.shape)
    print('Cash Flow csv is: ', c.shape)

    result = pd.merge(a, b, on=['Ticker', 'SimFinId', 'Currency', 'Fiscal Year', 'Report Date',
                                'Publish Date'])
    result = pd.merge(result, c, on=['Ticker', 'SimFinId', 'Currency', 'Fiscal Year', 'Report Date',
                                     'Publish Date'])

    result['Report Date'] = pd.to_datetime(result['Report Date'])
    result['Publish Date'] = pd.to_datetime(result['Publish Date'])

    print('Merged X data matrix shape is: ', result.shape)

    return result

def getYRawData():
    d = pd.read_csv('us-shareprices-daily.csv', delimiter = ';')

    d['Date']=pd.to_datetime(d['Date'])
    print('Stock Price data matrix is: ', d.shape)

    return d

def getYPriceDataNearDate(ticker, date, modifier, d):
    '''return just the y price and volume near date (as we have missing data).
    want the volume data returned to remove stocks with near 0 volume later.
    d is just the raw Y data.
    modifier just modifies the date to look between'''
    windowDays = 5

    rows = d[(d['Date'].between(pd.to_datetime(date) + pd.Timedelta(days=modifier),
                                pd.to_datetime(date) + pd.Timedelta(days=windowDays+modifier)))
    & (d['Ticker']==ticker)]

    if rows.empty:
        return [ticker, np.float("NaN"), np.datetime64('NaT'), np.float('NaN')]
    else:
        # take the first item of the list of days that falls in the window of accepted days
        return [ticker, rows.iloc[0]['Open'], rows.iloc[0]['Date'],
                rows.iloc[0]['Volume']*rows.iloc[0]['Open']]

def getYPricesReportDateDateAndTargetDate(x, d, modifier=365):
    '''modifier is effectively the hold period for a stock.
    x is the vector of company data.
    d is the Y raw data (stock price and date for all days)'''
    i = 0

    # Pre allocation list of list of 2
    # [(price at date) (price at date + modifier)]
    y = [[None]*8 for i in range(len(x))]

    # or 'Report Date' is the performance date from->to. Want this to be publish date
    # Because of time lag between report date (which can't be actioned on) and publish date (data we can trade on)
    whichDateCol = 'Publish Date'

    for index in range(len(x)):
        y[i] = (getYPriceDataNearDate(x['Ticker'].iloc[index],
                                      x[whichDateCol].iloc[index],
                                      0,
                                      d) +
                getYPriceDataNearDate(x['Ticker'].iloc[index],
                                      x[whichDateCol].iloc[index],
                                      modifier,
                                      d))
        i=i+1
    return y


if __name__ == '__main__':
    x = getXDataMerged()
    x.to_csv('Annual_Stock_Price_Fundamentals.csv')

    d = getYRawData()
    y = getYPricesReportDateDateAndTargetDate(x, d, 365)

    y=pd.DataFrame(y, columns=['Ticker', 'Open Price', 'Date', 'Volume',
                               'Ticker2', 'Open Price2', 'Date2', 'Volume2'])
    y.to_csv('Annual_Stock_Price_Performance.csv')