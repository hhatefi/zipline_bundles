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

## Data bundles 

Zipline runs a trading stretegy by executing its buy and cell order
over historical price data. The price data are provided by zipline
data bundles. They can basically read price data from CSV files or
directly download them from the firm website via a set of designated
API calls. In either cases, the price data are usually required to be
preprocessed before feeding into the zipline price database. The
reason is because zipline expect a certain format for price data. For
instance, it expects csv files to comply with OHLCV format with
certain column labels. Visit https://www.zipline.io/bundles.html for
more details.

## Writing a new data bundle

In order to add a new data bundle, two steps need to be taken:
1. writing a module to get price data from a source and convert it to
the format required by Zipline,
2. registering the module as new data bundle.

The latter is usually done in `.zipline/extension.py` file located in
user's home directory. An example of such a registration is given by
[extension.py](lib/extension.py). There is a bundle called
`yahoo_csv`, which can read price data from csv files downloaded from
[yahoo! finance](https://finance.yahoo.com/).

The former should be accesible via a module
imported from `zipline.data.bundles` directory. This directory differs
depending on the way zipline is installed.

