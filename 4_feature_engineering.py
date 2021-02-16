import pandas as pd

pd.set_option('display.max_columns', None)

def fixNansInX():
    '''Replace null values in given keys with 0'''
    for key in x_.keys():
        if key in keyCheckNullList:
            x_.loc[x_[key].isnull(), key]=0


def addColsToX():
    '''add enterprise value (EV) and EBIT columns to x dataframe'''
    # add EV
    x_["EV"] = x_["Market Cap"] + x_["Long Term Debt"] + x_["Short Term Debt"] - x_["Cash, Cash Equivalents & Short Term Investments"]

    # add EBIT
    x_["EBIT"] = x_["Net Income"] - x_["Interest Expense, Net"] - x_["Income Tax (Expense) Benefit, Net"]


# Make new X with ratios to learn from.
def getXRatios():
    '''add ratios we want to a new x dataframe which will be eventually fed to the machine
    learning model'''

    # make new x dataframe which will contain all of the features we want to train on
    x = pd.DataFrame()

    # EV/EBIT
    x["EV/EBIT"] = x_["EV"] / x_["EBIT"]

    # Op. In./(NWC+FA)
    x["Op. In./(NWC+FA)"] = x_["Operating Income (Loss)"] /\
                            (x_["Total Current Assets"] - x_["Total Current Liabilities"] + x_["Property, Plant & Equipment, Net"])

    # P/E
    x["P/E"] = x_["Market Cap"] / x_["Net Income"]

    # P/B
    x["P/B"] = x_["Market Cap"] / x_["Total Equity"]

    # P/S
    x["P/S"] = x_["Market Cap"] / x_["Revenue"]

    # Op. In./Interest Expense
    x["Op. In./Interest Expense"] = x_["Operating Income (Loss)"] / - x_["Interest Expense, Net"]

    # Working Capital Ratio
    x["Working Capital Ratio"] = x_["Total Current Assets"] / x_["Total Current Liabilities"]

    # Return on Equity
    x["RoE"] = x_["Net Income"] / x_["Total Equity"]

    # Return on Capital Employed
    x["ROCE"] = x_["EBIT"] / (x_["Total Assets"] - x_["Total Current Liabilities"])

    # Debt/Equity
    x["Debt/Equity"] = x_["Total Liabilities"] / x_["Total Equity"]

    # Debt Ratio
    x["Debt Ratio"] = x_["Total Assets"] / x_["Total Liabilities"]

    # Cash Ratio
    x["Cash Ratio"] = x_["Cash, Cash Equivalents & Short Term Investments"] / x_["Total Current Liabilities"]

    # Asset Turnover
    x["Asset Turnover"] = x_["Revenue"] / x_["Property, Plant & Equipment, Net"]

    # Gross Profit Margin
    x["Gross Profit Margin"] = x_["Gross Profit"] / x_["Revenue"]

    ### Altman ratios ###
    # (CA-CL)/TA
    x["(CA-CL)/TA"] = (x_["Total Current Assets"] - x_["Total Current Liabilities"])\
                      / x_["Total Assets"]

    # RE/TA
    x["RE/TA"] = x_["Retained Earnings"] / x_["Total Assets"]

    # EBIT/TA
    x["EBIT/TA"] = x_["EBIT"] / x_["Total Assets"]

    # Book Equity/TL
    x["Book Equity/TL"] = x_["Total Equity"] / x_["Total Liabilities"]

    return x

def maxMinRatio(m, text, max, min):
    '''define maximum values in dataframe by column so there are no inf values'''
    m.loc[x[text]>max,text]=max
    m.loc[x[text]<min,text]=min

if __name__ == '__main__':
    # import data
    x_ = pd.read_csv('Annual_Stock_Price_Fundamentals_Filtered.csv.csv', index_col=0)
    y_ = pd.read_csv('Annual_Stock_Price_Performance_Filtered.csv.csv', index_col=0)

    # keys in x dataframe we want to replace null values with 0
    keyCheckNullList = ["Short Term Debt", "Long Term Debt", "Interest Expense, Net",
                        "Income Tax (Expense) Benefit, Net",
                        "Cash, Cash Equivalents & Short Term Investments",
                        "Property, Plant & Equipment, Net", "Revenue", "Gross Profit"]