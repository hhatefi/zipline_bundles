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
convert it to the format required by zipline. The module is usually
added in `zipline.data.bundles` package.

2. registering the ingester module as a new data bundle.

The latter is usually done in `.zipline/extension.py` file located in
user's home directory. An example of such a registration is given by
[extension.py](lib/extension.py). There is a bundle called
`yahoo_csv`, which can read price data from csv files downloaded from
[yahoo! finance](https://finance.yahoo.com/).

Our [extension.py](lib/extension.py) assumes that the ingester module
is accessible from `zipline.data.bundles` package. It can of course be
changed by users to their desired location.

