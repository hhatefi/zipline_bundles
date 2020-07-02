import os
import sys
import numpy as np
import pandas as pd
import datetime as dt
#
from logbook import Logger
#
from zipline.utils.cli import maybe_show_progress

log = Logger(__name__)

class ingester_base:
    """
    data bundle reader base
    """
    def __init__(self, exchange, every_min_bar):
        """initializes an ingester instance

        :param exchange: the name of the exchange providing price data

        :param every_min_bar: The price time series given to an
        ingester may have 1-day or 1-minute frequency. This variable
        being `True` means the frequency is 1-minute, otherwise the
        price is provided daily.

        :type exchange: str
        :type every_min_bar: bool

        """
        self._exchange=exchange
        self._every_min_bar=every_min_bar

    def __call__(self,
                 environ,
                 asset_db_writer,
                 minute_bar_writer,
                 daily_bar_writer,
                 adjustment_writer,
                 calendar,
                 start_session,
                 end_session,
                 cache,
                 show_progress,
                 output_dir):
        """implements the ingest function

        For in detail parameter description see https://www.zipline.io/bundles.html#writing-a-new-bundle
        """
        raise NotImplementedError

    def _read_and_convert(self):
        """reads price data from the source and convert it to the format readable from zipline
        """
        raise NotImplementedError

    def _filter(self, df):
        """applies filter on price data read by ingestor

        This method is called within `self._read_and_convert`. All the
        operations must be done on `df` inplace.

        :param df: the price dataframe to be filtered
        :type df: pandas.DataFrame
        """
        raise NotImplementedError

class csv_ingester(ingester_base):
    """inegester from csv files
    """
    def __init__(self, exchange, every_min_bar, csvdir, csvdir_env, index_column='date', column_mapper=None):
        """creates an instance of csv ingester

        :param exchange: an arbitrary name for the exchange providing
        price data

        :param every_min_bar: The price time series given to an
        ingester may have 1-day or 1-minute frequency. This variable
        being `True` means the frequency is 1-minute, otherwise the
        price is provided daily.

        :param csvdir: The path to the directory containing csv
        files. For each symbol there must be a single file of name
        '<symbolname>.csv'

        :param csvdir_env: The envireonment variable used to locate
        the csv directory containing the csv files. After setting this
        parameter, for example by
        `csv_ingester(...,csvdir_env='CSV_DIR'...)`, the user can pass
        a csv directory via
        `ENV_VAR=/path/to/csv/dir zipline bundles -b <bundle_name>`

        :param index_column: the label of the column in csv file that is
        interpreted as index. It reports the timestamp of the
        corrsponding price information. Its default value is 'date'.

        :param column_mapper: a dictionary that maps column labels
        read from csv file to the ones expected from zipline. Zipline
        accepts csv files in OHLCD format, which contains columns
        'date', 'open', 'high', 'low', 'close' , 'volume', 'dividend'
        and 'split'. For example, a mapper passed by
        column_mapper={'Date': 'date'}, renames column label 'Date' to
        'date' in all symbol dataframes read by the ingester. The
        default value is `None`, which means no renaming will happen.

        :type exchange: str
        :type every_min_bar: bool
        :type csvdir: str
        :type csvdir_env: str
        :type index_column: str
        :type column_mapper: dict mapping str to str

        """
        super().__init__(exchange, every_min_bar)
        self._csvdir = csvdir
        self._csvdir_env = csvdir_env
        self._index_column=index_column
        self._column_mapper=column_mapper

    def _get_csvdir(self, show_progress=False):
        """returns the csv directory to read csv files from

        It tries first to set the csv directory from environment
        variable. If no environment variable is given, or it is not
        set by the user, it will check self._csvdir for a valid
        directory. If that fails then `sys.exit()` will be called.

        :param show_progress: if `True`, it will be verbose
        :type show_progress: bool

        :return: the path to csv directory
        :rtype: str
        """
        if self._csvdir_env:
            path = os.environ.get(self._csvdir_env)
            if path and os.path.isdir(path):
                if show_progress:
                    log.info('csv directory is set to \'{}\''.format(path))
                return path
            elif show_progress:
                log.debug('\'{}\' is not a valid directory'.format(path))
        if self._csvdir and os.path.isdir(self._csvdir):
            if show_progress:
                log.info('csv directory is set to \'{}\''.format(self._csvdir))
            return self._csvdir
        error_msg="csv directory is not valid"
        if self._csvdir_env:
            error_msg="{}. It can be set via environment variable '{}'".format(error_msg, self._csvdir_env)
        if error_msg[-1] == "'":
            error_msg="{}. It can also be set inside '.zipline/extension.py' where the bundle is registered by setting argument 'csvdir'".format(error_msg)
        else:
            error_msg="{}. It can be set inside '.zipline/extension.py' where the bundle is registered by setting argument 'csvdir'".format(error_msg)
        log.error("{}.".format(error_msg))
        sys.exit(1)

    def _extract_symbols(self):
        """returns the list of (symbol, csv_file_path) pair from the csv directory path

        This function extracts the list symbols from csv files located
        in `self._get_csvdir`. The assumption is that the price data
        of each asset is stored in `symbol_name.csv` within the csv
        directory.

        :return: the list of symbols
        :rtype: list of str
        """
        return [csv_file_path.split('.csv')[0] # symbol name
                for csv_file_path in os.listdir(self._get_csvdir()) if csv_file_path.endswith('.csv')]

    def _create_metadata(self, nsymbols):
        """creates metadata dataframe with appropriate columns with length of `nsymbols`

        An empty dataframe is created for symbols' metadata. It is
        stored in `self._df_metadata`.

        :param nsymbols: the number of symbols
        :type nsymbols: int
        """
        self._df_metadata = pd.DataFrame(np.empty(nsymbols, dtype=[
            ('start_date', 'datetime64[ns]'),
            ('end_date', 'datetime64[ns]'),
            ('auto_close_date', 'datetime64[ns]'),
            ('symbol', 'object'),
            ('exchange', 'object'),]))

    def _update_symbol_metadata(self, symbol_index, symbol, df):
        """update metadata for the given symbol

        Metadata are extracted from the given dataframe `df`, which is
        the price data read from csv file or downloaded via the firm
        API. They are stored in `self._df_metadata[symbol_index]`

        :param symbol_index: the symbol index
        :param symbol: the symbol name
        :param df: the dataframe storing symbol's price data

        :type symbol_index: int
        :type symbol: str
        :type df: pandas.DataFrame
        """
        start_date = df.index[0]
        end_date = df.index[-1]
        autoclose_date = end_date + pd.Timedelta(days=1)
        self._df_metadata.iloc[symbol_index] = start_date, end_date, autoclose_date, symbol, self._exchange

    def _read_and_convert(self, symbols, show_progress):
        """returns the generator of symbol index and the dataframe storing its price data
        """
        path = self._get_csvdir(show_progress)
        with maybe_show_progress(symbols, show_progress, label='Loading csv files: ') as it:
            for symbol_index, symbol in enumerate(it):
                file_path = '{0}/{1}.csv'.format(path, symbol)
                if os.path.exists(file_path):
                    # read data from csv file and set the index
                    df_data = pd.read_csv(file_path, index_col=self._index_column, parse_dates=True, dtype={"Volumn": np.uint64}).sort_index()
                    # rename columns if necessary
                    if self._column_mapper:
                        df_data.rename(columns=self._column_mapper, inplace=True)
                    self._filter(df_data)
                    self._update_symbol_metadata(symbol_index, symbol, df_data)
                    yield symbol_index, df_data

    def _filter(self, df):
        """applies filter on price dataframe read by ingestor

        This method is called within `self._read_and_convert`, after
        the column mapping is done. It checks if the dataframe has
        `split` and `dividend` column, if not it creates them and
        assigns their default value.

        :param df: the price dataframe to be filtered
        :type df: pandas.DataFrame

        """
        if 'dividend' not in df.columns:
            df['dividend'] = 0;
        if 'split' not in df.columns:
            df['split'] = 1

    def __call__(self,
                 environ,
                 asset_db_writer,
                 minute_bar_writer,
                 daily_bar_writer,
                 adjustment_writer,
                 calendar,
                 start_session,
                 end_session,
                 cache,
                 show_progress,
                 output_dir):
        """implements the actual ingest function

        The order of calls are as follows
        1. `self._extract_symbols()`
        2. `self._create_metadata()`
        3. `self._read_and_convert()`
        """
        symbols = self._extract_symbols()
        if show_progress:
            log.info('symbols are: {0}'.format(symbols))
        self._create_metadata(len(symbols))
        if show_progress:
            log.info('writing data...')
        if self._every_min_bar:
            minute_bar_write.write(self._read_and_convert(symbols, show_progress), show_progress=show_progress)
        else:
            daily_bar_writer.write(self._read_and_convert(symbols, show_progress), show_progress=show_progress)
        if show_progress:
            log.info('meta data:\n{0}'.format(self._df_metadata))
        asset_db_writer.write(equities=self._df_metadata)
        adjustment_writer.write()
        if show_progress:
            log.info('writing completed')
