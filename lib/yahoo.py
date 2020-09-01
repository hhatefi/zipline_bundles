from yahoofinancials import YahooFinancials
import pandas as pd
import datetime as dt


def get_downloader(start_date,
               end_date,
               granularity='daily',):
    """returns a downloader closure for oanda
    :param start_date: the first day on which dat are downloaded
    :param end_date: the last day on which data are downloaded
    :param granularity: the frequency of price data, 'D' for daily and 'M1' for 1-minute data
    :type start_date: str in format YYYY-MM-DD
    :type end_date: str in format YYYY-MM-DD
    :type granularity: str
    """

    def downloader(symbol):
        """downloads symbol price data using oanda REST API
        :param symbol: the symbol name
        :type symbol: str
        """
        yf = YahooFinancials(symbol)

        res = yf.get_historical_price_data(str(start_date), str(end_date), granularity)

        if not res or symbol not in res or 'prices' not in res[symbol]:
            ValueError('Fetching price data for "{}" failed.'.format(symbol))

        prices=res[symbol]['prices']
        df = pd.DataFrame({'open': [p['open'] for p in prices],
                           'close': [p['close'] for p in prices],
                           'low': [p['low'] for p in prices],
                           'high': [p['high'] for p in prices],
                           'volume': [p['volume'] for p in prices],}, index=[pd.Timestamp(d['formatted_date']) for d in prices])
        if 'dividend' in prices:
            df['dividend'] = [p['dividend'] for p in prices]
        else:
            df['dividend'] = 0

        if 'split' in prices:
            df['split'] = [p['split'] for p in prices]
        else:
            df['split'] = 1

        print(df.head(3))

        return df

    return downloader
