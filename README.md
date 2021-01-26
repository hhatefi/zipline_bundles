Zipline Bundles
===============

This repository contains some zipline data bundles, which are used to
download and extract historical price data for backtesting in zipline
platform. [zipline](https://www.zipline.io/) is a backtesting
framework written in python, which can be used to test, analyze and
visualize trading strategies. It currently powers
[Quantopian](https://www.quantopian.com/), a free rich community
centered hosted platform for trading strategy development and many
more.

## Quick start

You have already cloned the repository and switched the working
directory to the repository root. Then, in an environment where
zipline is installed and working, adding all data bundles can be done
by

```sh
python install.py
```

Note that the installer complains if there already exist python
modules with the same name. To force the installer to overwrite the
existing modules, add `-f`. Apart from `zipline` itself and its
dependencies, there are additional dependencies used by each
bundle. To install them all run

```sh
pip install -r requirements.txt
```

You can check if the installation is complete by running:
```sh
zipline bundles
```

You should see new bundles are added to the list:

```bash
csvdir <no ingestions>
iex <no ingestions>
quandl <no ingestions>
quantopian-quandl <no ingestions>
yahoo_csv <no ingestions>
yahoo_direct <no ingestions>
```

To test the installation, a simple strategy backtest can be executed
over price data read by one of the bundles. For this, `yahoo_csv`
bundle is used, which reads data from a directory containing csv files
that are downloaded from yahoo finance. First, ingest price data
stored in [data](data) directory:

```bash
YAHOO_CSVDIR=./data/ zipline ingest -b yahoo_csv
```

Then backtest buy and hold strategy over the ingested data:

```bash
zipline run -f tests/buy_and_hold.py -b yahoo_csv --start 2019-07-02 --end 2020-07-02
```

The cumulative return of the strategy will be depicted in a plot after
backtesting.

## Bundles

The following bundles are currently defined by the repository.

| Bundle        | Data Source                                                    | Dependency | Module  |
| :-----        | ----------                                                     | :----------| ------- |
| `yahoo_csv`   | csv files downloaded from [yahoo finance](https://finance.yahoo.com) | none | none    |
| `yahoo_direct`| [yahoo finance](https://finance.yahoo.com) | [`yahoofinancials`](https://pypi.org/project/yahoofinancials/) | [yahoo.py](lib/yahoo.py) |
| `iex`       |  [IEX cloud](https://iexcloud.io) | [`iexfinance`](https://pypi.org/project/iexfinance/) | [iex.py](lib/iex.py) |

`yahoo_csv` bundle takes data from CSV files downloaded from yahoo
finance. Each file contains price data of a single asset and shall be
named as `assert_name.csv`. The bundle reads all the csv files located
in a directory given by environment variable `YAHOO_CSVDIR`:

```bash
YAHOO_CSVDIR=/path/to/csvdir zipline ingest -b yahoo_csv
```

`yahoo_direct` directly downloads price data from yahoo finance. The
bundle extracts asset names from environment variable `YAHOO_SYM_LST`,
which holds a comma separated list of asset names. For example:

```bash
YAHOO_SYM_LST=SPY,AAPL zipline ingest -b yahoo_direct
```

ingests price data of assets `SPY` and `AAPL`. The start and the end
date of ingestion can be set into variables `start_date` and
`end_date`, respectively. These variables are passed to function
`get_downloader` where the bundle is registered in
`$HOME/.zipline/extension.py`. Here is how the registration may look
like:

```python
register('yahoo_direct', # bundle's name
         direct_ingester('YAHOO',
                         every_min_bar=False,
                         symbol_list_env='YAHOO_SYM_LST', # the environment variable holding the comma separated list of assert names
                         downloader=yahoo.get_downloader(start_date='2010-01-01',
                                                         end_date='2020-01-01'
                         ),
         ),
         calendar_name='NYSE',
)
```

In addition to the start and the end date, the environment variable
name holding price data can be set here. `direct_ingester` can
additionally takes callable `filter_cb`. It takes as a parameter a
data frame that is just retured from the downloader and returns a new
data frame. It is useful when the downloaded price data needs
additional prepossessing.

`iex` downloads price data from IEX cloud. Its usage is fairly similar
to that of `yahoo_direct`. Fetching price data from IEX cloud however
requires passing a valid API token, which is stored in environment
variable `IEX_TOKEN`. Moreover, the environment variable storing asset
names is called `IEX_SYM_LST`.

## Manual installation
[install.py](install.py) takes the following steps to add the bundles:

* copy [extension.py](lib/extension.py) into `~/.zipline/`,

* add [ingester.py](lib/ingester.py) as well as the proper module for
  each bundle listed in above table into package
  `zipline.data.bundles`, i.e. copy the modules into where the package
  is located. Package location differs depending on the way zipline is
  installed. One way to find out the location in an environment with
  zipline installed is to run the following code:
  
  ```bash
  python -c 'import zipline.data.bundles as bdl; print(bdl.__path__)'
  ```

If only a subset of bundles is needed, one way is to keep their
registration in [extension.py](lib/extension.py), their dependency in
[requirements.txt](requirements.txt) and their related modules in
variable `src_ing` inside [install.py](install.py). Then, use the
installation script!

## Adding new bundles

It is possible to define new data bundles using the structures
provided by this repository. The process is explained in [this
post](https://hhatefi.github.io/posts/zipline_bundles/) in more
detail.