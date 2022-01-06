 freqtrade trade --strategy new_turtle
 - check backtest with btcusd daily. from 2017

freqtrade download-data --exchange binance --pairs BTC/USDT --timeframe 1d --timerange=20170101-20211211
freqtrade backtesting --strategy new_turtle --pairs BTC/USDT --dry-run-wallet 100000 --timeframe 1d --timerange 20190907- --export trades --export-filename=backtest_turtle.json
