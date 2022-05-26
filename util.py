import pandas as pd
import requests
import numpy as np


FIAT = ['EUR', 'GBP']
STABLES = ['BUSD', 'DAI', 'PAX', 'SUSD', 'TUSD', 'USDC', 'USDS', 'USDSB', 'USDT']
SYMBOLS_TO_AVOID = FIAT + STABLES + ['BCC', 'BCHABC', 'BCHSV', 'BKRW', 'ERD', 'HC', 'LEND', 'MCO', 'PAXG', 'STORM', 'STRAT', 'VEN', 'XZC']


def get_all_symbols():
    """ Get a list of all Binance symbols against USDT """
    url = "https://api.binance.com/api/v3/ticker/price"
    res = requests.get(url)
    allTickers = res.json()

    allSymbols = []
    for tmp in allTickers:
        symbol = tmp['symbol']
        if symbol[-4:] == 'USDT': # look only for coins against USDT
            symbol = symbol[:-4] # take only the coin instead of coinUSDT
            if symbol[-2:] == 'UP' or symbol[-4:] in ['BEAR', 'BULL', 'DOWN'] or symbol in SYMBOLS_TO_AVOID: # ignore there coins
                continue
            allSymbols.append(symbol)

    allSymbols.sort() # sort alphabetically
    return allSymbols



def get_symbol_data(fsym, startTsMs, endTsMs=None, interval='5m'):
    """ Get the OHLC data for the given symbol starting from the given timestamp (in milliseconds) """

    # e.g. of query https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=5m&startTime=1&limit=1000
    baseUrl = 'https://api.binance.com/api/v3/klines'
    if endTsMs is None:
        url = baseUrl + f'?symbol={fsym}USDT&interval={interval}&startTime={startTsMs}&limit=1000'
    else:
        if endTsMs < startTsMs:
            print(f"{fsym} end time is less than start time")
            return None
        url = baseUrl + f'?symbol={fsym}USDT&interval={interval}&startTime={startTsMs}&endTime={endTsMs}&limit=1000'

    res = requests.get(url)
    if res.status_code != 200:
        print(f"{fsym} error in request {url}")
        return None
    res = res.json() # convert to json
    if res:
        df = pd.DataFrame.from_dict(res)
        df = df.loc[:, :5]
        df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        df.set_index('timestamp', inplace=True) # set timestamp as dataframe index
        return df
    else:
        return None


def convert_candles_5m_to_1h(highes, lowes, closes, volumes):
    """ Convert 5m candles to 1h candles """
    N = len(highes)
    highes1h = []
    lowes1h = []
    closes1h = []
    volumes1h = []
    for i in range(0, N, 15): # 1 hour contains 15 5mins
        if i+15 >= N:
            break
        highes1h.append(max(highes[i:i+15]))
        lowes1h.append(min(lowes[i:i+15]))
        closes1h.append(closes[i+15])
        volumes1h.append(sum(volumes[i:i+15]))
    return np.array(highes1h), np.array(lowes1h), np.array(closes1h), np.array(volumes1h)
