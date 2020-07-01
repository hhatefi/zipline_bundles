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
