from openbb_terminal.sdk import openbb

## StockScreen Functions
"""
def stocks_quote(symbol):
    df = openbb.stocks.quote(symbol)
    df = df.to_dict()
    first_key = list(df.keys())[0]
    df = df[first_key]
    return df
"""

def fa_overview(symbol):
    df = openbb.stocks.fa.overview(symbol)
    df = df.to_dict()
    df = df[0]
    df['Book total']= hum_format(float(df['Book value'])*(num_format(df['Shares outstanding'])))
    return df

## Requires API_KEY_FINANCIALMODELINGPREP
def fa_metrics(symbol):
    df = openbb.stocks.fa.metrics(symbol, 1, False)
    df = df.to_dict()
    first_key = list(df.keys())[0]
    df = df[first_key]
    return df

def fa_income(symbol):
    df = openbb.stocks.fa.income(symbol, False, False, "YahooFinance", 1)
    df = df.iloc[:, 0]
    df = df.to_dict()
    df = (df['Total revenue'] - df['Net income'])
    df = hum_format(df) 
    return df

## Requires API_KEY_FINANCIALMODELINGPREP
def fa_growth(symbol):
    df = openbb.stocks.fa.growth(symbol, 1, False)
    df = df.to_dict()
    first_key = list(df.keys())[0]
    df = df[first_key]   
    return df

## MacroDash Functions
def usbonds():
    bonds = openbb.economy.usbonds()
    bonds = bonds[::-1]
    bonds['Yld (%)'] = bonds['Yld (%)'].astype(float)
    return bonds

## Formating functions
def hum_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
    
def num_format(num):
    if type(num) == float or type(num) == int:
        return num
    if 'K' in num:
        if len(num) > 1:
            return float(num.replace('K', '')) * 1000
        return 1000.0
    if 'M' in num:
        if len(num) > 1:
            return float(num.replace('M', '')) * 1000000
        return 1000000.0
    if 'B' in num:
        return float(num.replace('B', '')) * 1000000000
    return 0.0