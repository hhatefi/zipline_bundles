import os
from pandas import Timestamp, DataFrame
from binance.client import Client

API_KEY_ENV='BINANCE_API_KEY'
SECRET_KEY_ENV='BINANCE_SECRET_KEY'


def klines2ohlcv(klines):
    """converts klines downloaded from binace via python binance module
    into pandas dataframe complaint with OHLCV
    :param klines: The list of klines
    :type klines: list of price data, see https://sammchardy
    """
    ohlcv=[(Timestamp(l[0], unit='ms'),  # timestamp
            float(l[1]),                   # open
            float(l[2]),                   # high
            float(l[3]),                   # low
            float(l[4]),                   # close
            float(l[5])                    # volume
            )
        for l in klines]

    df=DataFrame(ohlcv, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df.set_index('date', inplace=True)

    return df

def get_downloader(start_date, end_date, every_min_bar):
    """returns a downloader closure for iex cloud
    :param start_date: the first day on which dat are downloaded
    :param end_date: the last day on which data are downloaded
    :type start_date: str in format YYYY-MM-DD
    :type end_date: str in format YYYY-MM-DD
    :param every_min_bar: True if the the price time series must be
    downloaded for every minute. Otherwise the daily price is fetched.
    :type every_min_bar: bool
    """
    dt_start=int(Timestamp(start_date).timestamp()*1000)
    dt_end=int(Timestamp(end_date).timestamp()*1000)

    def downloader(symbol):
        """downloads symbol price data using iex cloud API
        :param symbol: the symbol name
        :type symbol: str
        """
        api_key=os.environ.get(API_KEY_ENV)
        secret_key=os.environ.get(SECRET_KEY_ENV)
        if api_key is None or secret_key is None:
            raise Exception('Both {} and {} environment variables must be defined'.format(API_KEY_ENV, SECRET_KEY_ENV))
        cl=Client(api_key, secret_key)
        freq=Client.KLINE_INTERVAL_1MINUTE if every_min_bar else Client.KLINE_INTERVAL_1DAY
        klines=cl.get_historical_klines(symbol, freq, dt_start, dt_end)

        df=klines2ohlcv(klines)
        return df

    return downloader
