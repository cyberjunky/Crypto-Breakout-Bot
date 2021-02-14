from datetime import datetime
import numpy as np
import util


def computeRange(i_highes, i_lowes) -> float:
    """ Compute the normalized distance between the past lowest and highest points """
    highes = i_highes.copy()
    lowes = i_lowes.copy()
    highes.sort()
    lowes.sort()
    return (highes[-3] - highes[3]) / highes[3] # use the 3rd highest and lowest


def isPumping5m(closes, volumes) -> bool:
    """ Check if is pumping: volume and price increase """
    priceIncreasing = closes[-1] > closes[-10:-1].max() # price is the highest in the past 50 mins (assuming 5m candles are used)
    volumeIncreasing = volumes[-3:].mean() > volumes[:-3].mean() # use the average of the last 3 candles (assuming 5m candles are used)
    return priceIncreasing and volumeIncreasing


def computeATRHour(closes, highes, lowes) -> float:
    """ Assuming is receiving 1h candles """
    ATR = 0 #  Average True Range: measure of the past volatility
    N = len(closes)
    for i in range(1,N):
        tmpATR = max(highes[i]-lowes[i],
                     abs(highes[i]-closes[i-1]),
                     abs(lowes[i]-closes[i-1])
        )
        tmpATR /= lowes[i] * 100 # normalize
        ATR += tmpATR
    return ATR/N


def check_status(fsym):
    """ Check if is consolidating and pumping """

    # define timestamps in milliseconds
    windowTsMs = 3600 * 24 * 3 * 1000  # window of 3 days
    nowTsMs = int(datetime.timestamp(datetime.now()) * 1000)
    startTsMs = int(nowTsMs - windowTsMs)

    # get 5m symbol candles
    df = util.get_symbol_data(fsym, startTsMs, nowTsMs)
    highes = np.array(df['high']).astype(np.float64)
    lowes = np.array(df['low']).astype(np.float64)
    closes = np.array(df['close']).astype(np.float64)
    volumes = np.array(df['volume']).astype(np.float64)

    # get 1h symbol candles (faster to convert from 5m candles than making another query)
    highes1h, lowes1h, closes1h, _ = util.convert_candles_5m_to_1h(highes, lowes, closes, volumes)

    # criteria under which the coin is breaking out

    # is consolidating
    lowVolatility = computeATRHour(closes1h, highes1h, lowes1h) < 0.0005
    isNarrowRange = computeRange(highes, lowes) < 0.2
    isConsolidating = lowVolatility and isNarrowRange

    # price and volume are increasing
    isPumping = isPumping5m(closes, volumes)

    return isConsolidating, isPumping