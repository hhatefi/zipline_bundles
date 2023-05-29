#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from zipline.data.bundles import register
from zipline.data.bundles.ingester import csv_ingester # ingester.py need to be placed in zipline.data.bundles

_DEFAULT_PATH = str(Path.home() / '.zipline/csv/yahoo')

register(
    'yahoo_csv',
    csv_ingester('YAHOO',
                 every_min_bar=False, # the price is daily
                 csvdir_env='YAHOO_CSVDIR',
                 csvdir=_DEFAULT_PATH,
                 index_column='Date',
                 column_mapper={'Open': 'open',
                                'High': 'high',
                                'Low': 'low',
                                'Close': 'close',
                                'Volume': 'volume',
                                'Adj Close': 'price',
                 },
    ),
    calendar_name='NYSE',
)

from zipline.data.bundles.ingester import direct_ingester

from zipline.data.bundles import yahoo
register('yahoo_direct', # bundle's name
         direct_ingester('YAHOO',
                         every_min_bar=False,
                         symbol_list_env='YAHOO_SYM_LST', # the environemnt variable holding the comma separated list of assert names
                         downloader=yahoo.get_downloader(start_date='2010-01-01',
                                                         end_date='2020-01-01'
                         ),
         ),
         calendar_name='NYSE',
)

from zipline.data.bundles import iex
import trading_calendars as tc

cal=tc.get_calendar('NYSE')
register('iex', # bundle's name
         direct_ingester('IEX Cloud',
                         every_min_bar=False,
                         symbol_list_env='IEX_SYM_LST', # the environemnt variable holding the comma separated list of assert names
                         downloader=iex.get_downloader(start_date='2020-01-01',
                                                       end_date='2020-01-05'
                         ),
                         filter_cb=lambda df: df[[cal.is_session(dt) for dt in df.index]]
         ),
         calendar_name='NYSE',
)

from zipline.data.bundles import binance

register('binance_daily', # bundle's name
         direct_ingester('Binance Exchange',
                         every_min_bar=False,
                         symbol_list_env='BINANCE_SYM_LST', # the environemnt variable holding the comma separated list of assert names
                         downloader=binance.get_downloader(start_date='2020-01-01',
                                                           end_date='2020-01-05',
                                                           every_min_bar=False # True for minute price, False for dailyprice
                         ),
         ),
         calendar_name='24/7',
)

register('binance_min', # bundle's name
         direct_ingester('Binance Exchange',
                         every_min_bar=True,
                         symbol_list_env='BINANCE_SYM_LST', # the environemnt variable holding the comma separated list of assert names
                         downloader=binance.get_downloader(start_date='2020-01-01',
                                                           end_date='2020-01-05',
                                                           every_min_bar=True # True for minute price, False for dailyprice
                         ),
         ),
         calendar_name='24/7',
)
