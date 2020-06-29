Zipline Bundles
===============

This repository contains some zipline data bundles, which are used to
download and extract historical price data for backtesting in zipline
platform.

## Adding new bundles
Zipline bundles can in general read price data from CSV files or
directly download them from the firm website via its provided API
calls. In either cases, the price data are usually required to be
preprocessed before feeding into the zipline pipeline. The reason is
because zipline expect a certain format for price data.

In order to add a new data bundle, two steps need to be taken:
1. writing a module to get price data from a source and convert it to
the format required by Zipline,
2. registering the module as new data bundle.

The latter is usually done in `.zipline/extension.py` file located in
user's home directory. The former should be accesible via a module
imported from `zipline.data.bundles` directory.



