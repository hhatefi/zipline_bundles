Zipline Bundles
===============

This repository contains some zipline data bundles, which are used to
download and extract historical price data for backtesting in zipline
platform. [Zipline](https://www.zipline.io/) is a backtesting
framework written in python, which can be used to test, analyze and
visualize trading strategies. It currently powers
[Quantopian](https://www.quantopian.com/), a free rich community
centered hosted platform for trading strategy development and many
more.

## Quick start

To add the bundles defined in this repository, the following steps should be taken:

* copy [extension.py](lib/extension.py) into `~/.zipline/`, or if the
  extension file already exists, append its content into
  `~/.zipline/extension.py`

* find where package `zipline.data.bundles` is located and add module
  [ingester.py](lib/ingester.py) into it. Where the package is located
  differs depending on the way zipline is installed. One way to detect
  the location of this package in an environment with zipline
  installed is to run the following code:
  ```bash
  python -c 'import zipline.data.bundles as bdl; print(bdl.__path__)'
  ```

## Data bundles 

Zipline runs a trading stretegy by executing its buy and cell order
over historical price data. Price data are provided by zipline data
bundles. Data bundles can basically read price data from CSV files or
directly download them from the firm website via a set of designated
API calls. In either cases, the price data are usually required to be
preprocessed before feeding into the zipline price database. The
reason is because zipline expect a certain format for price data. For
instance, it requires price time series to comply with OHLCV format
with certain column labels. Visit https://www.zipline.io/bundles.html
for more details.

## Writing a new data bundle

In order to add a new data bundle, two steps need to be taken:

1. writing an ingester module that gets price data from a source and
converts it to the format required by zipline. The module is usually
added in `zipline.data.bundles` package.

2. registering the ingester module as a new data bundle.

The latter is usually done in `.zipline/extension.py` file located in
user's home directory. An example of such a registration is given by
[extension.py](lib/extension.py). Our [extension.py](lib/extension.py)
assumes that the ingester module is accessible from
`zipline.data.bundles` package. It can of course be changed by users
to their desired location. 

### Adding a csv bundle 

An ingester capable of reading csv files with different formats is
defined by class `csv_ingester` inside module
[ingester.py](lib/ingester.py). Price data are read from a directory
containing csv files. For each symbol a csv file with name
`<symbol-name>.csv` is expected. Price data are read from the files
and converted to `pandas.DataFrame` objects with certain columns
before feeding into zipline price database. `csv_ingester` can be
configured according to the shape of the csv file it reads from. An
example of this configuration can be seen where bundle `yahoo_csv` is
registered in [extension.py](lib/extension.py):

```python
register(
    'yahoo_csv',
    csv_ingester('YAHOO',
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
```

`csv_yahoo` can read csv files downloaded from [yahoo!
finance](https://finance.yahoo.com/). Let's have a closer look into
its registration.

* `'yahoo_csv'` is the name of the bundle,

* `csv_ingester` is the ingester class name,

* `'YAHOO'` is an arbitrary name for the exchange, from which the
  price data are downloaded,

* `csvdir_env` is the name of environment variable pointing to the
  directory containing csv files. It gives the opportunity of passing
  the csv directory at runtime via setting the environment
  variable. For `yahoo_csv` bundle, e.g
  ```python
  YAHOO_CSVDIR=/path/to/csv/dir zipline ingest -b yahoo_csv
  ```

* `csvdir` is the path to the csv directory. The path set by
   envirenment variable defined by `csvdir_env` takes precedence over
   this value,

* `index_column` is the column label in the csv file to be considered
  as `pandas.DataFrame` index,

* `column_mapper` is a dictionary mapping the column labels in the csv
  file to the one in `pandas.DataFrame`,

* `calendar_name` is the calendar used by the exchange.