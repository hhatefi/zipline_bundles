# imports
from zipline.api import (symbol, set_benchmark, order_target_percent,
                         schedule_function, time_rules)
from zipline.finance import commission
#import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def initialize(context):
    context.set_commission(commission.PerShare(cost=0.0, min_trade_cost=0))
    set_benchmark(symbol('SPY'))
    context.asset = symbol('AAPL')
    context.has_ordered = False

    schedule_function(place_order, None,
                      time_rules.market_open())

def place_order(context, data):
    if not context.has_ordered:
        order_target_percent(context.asset, 1.0)
        context.has_ordered = True

def analyze(context, perf):
    fig = plt.figure(figsize=(12,8))
    perf.algorithm_period_return.plot(x='strategy return', legend=True)
    perf.benchmark_period_return.plot(legend=True)
    plt.show()
