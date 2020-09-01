from pandas import Timestamp
from iexfinance.stocks import get_historical_data

def get_downloader(start_date,
               end_date,):
    """returns a downloader closure for iex cloud
    :param start_date: the first day on which dat are downloaded
    :param end_date: the last day on which data are downloaded
    :type start_date: str in format YYYY-MM-DD
    :type end_date: str in format YYYY-MM-DD
    """
    dt_start=Timestamp(start_date).date()
    dt_end=Timestamp(end_date).date()

    def downloader(symbol):
        """downloads symbol price data using iex cloud API
        :param symbol: the symbol name
        :type symbol: str
        """
        df = get_historical_data(symbol, dt_start, dt_end, output_format='pandas')

        return df

    return downloader
