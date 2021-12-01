import ccxt
print('CCXT version:', ccxt.__version__)  # requires CCXT version > 1.20.31
exchange = ccxt.binance({
    'apiKey': 'iALoKUiAKslA8at6xlKkYTfHLrFGsB2TupQVPd1Rzn9HFdcfPOps0yM5iJurhl77',
    'secret': 'nIrwG5etQTlz2RgRhreXXl7oU7PlKT6yi3q0nrxaCst2gheidjPAcWibc5UkISMF',
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future',  # ←-------------- quotes and 'future'
    },
})

exchange.load_markets()
print(exchange.symbols)