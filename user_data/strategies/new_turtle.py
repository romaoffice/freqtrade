
# --- Do not remove these libs ---
from freqtrade.strategy import IStrategy
from typing import Dict, List
from functools import reduce
from pandas import DataFrame
# --------------------------------

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class Strategy001(IStrategy):

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi"
    minimal_roi = {
        "60":  0.01,
        "30":  0.03,
        "20":  0.04,
        "0":  0.05
    }

    # Optimal stoploss designed for the strategy
    # This attribute will be overridden if the config file contains "stoploss"
    stoploss = -0.10

    # Optimal timeframe for the strategy
    timeframe = '1m'

    # trailing stoploss
    trailing_stop = False
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.02

    # run "populate_indicators" only for new candle
    process_only_new_candles = False

    # Experimental settings (configuration will overide these if set)
    use_sell_signal = True
    sell_profit_only = False
    ignore_roi_if_buy_signal = False
    
    # Optional order type mapping
    order_types = {
        'buy': 'market',
        'sell': 'market',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    length = 28
    Multiplier = 3.11
    bardelay = 2
    trailingmenu = "Normal"#options=["Normal","Re-entries","None"]
    trailinmode = "Auto"#options=["Auto","Custom"]
    usetrail = True if trailingmenu!="None" else False
    longTrailPerc = 5*0.01
    shortTrailPerc = 5 * 0.01

    def informative_pairs(self):
        """
        Define additional, informative pair/interval combinations to be cached from the exchange.
        These pair/interval combinations are non-tradeable, unless they are part
        of the whitelist as well.
        For more information, please consult the documentation
        :return: List of tuples in the format (pair, interval)
            Sample: return [("ETH/USDT", "5m"),
                            ("BTC/USDT", "15m"),
                            ]
        """
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds several different TA indicators to the given DataFrame

        Performance Note: For the best performance be frugal on the number of indicators
        you are using. Let uncomment only the indicator you are using in your strategies
        or your hyperopt configuration, otherwise you will waste your memory and CPU usage.
        """

        dataframe['avgTR'] = ta.ATR(dataframe, timeperiod=self.Length)

        dataframe['highestC'] = dataframe['high'].rolling(self.Length).max()
        dataframe['lowestC'] = dataframe['low'].rolling(self.Length).min()

        dataframe['hiLimit'] = dataframe['highestC']-dataframe['avgTR']*self.Multiplier
        dataframe['loLimit'] = dataframe['lowestC']+dataframe['avgTR']*self.Multiplier
        
        dataframe.loc[0, 'ret'] = df.loc[0, 'loLimit']
        for i in range(1, len(dataframe)):
            if dataframe.loc[i,'close']>dataframe.loc[i,'hiLimit'] and \
               dataframe.loc[i,'close']>dataframe.loc[i,'loLimit'] :
               dataframe.loc[i,'ret'] = dataframe.loc[i,'hiLimit']
            else:
                if dataframe.loc[i,'close']<dataframe.loc[i,'hiLimit'] and \
                   dataframe.loc[i,'close']<dataframe.loc[i,'loLimit'] :
                   dataframe.loc[i,'ret'] = dataframe.loc[i,'loLimit']
                else:
                    if i==1 :
                     dataframe.loc[i,'ret'] = dataframe.loc[i,'close']
                    else:
                     dataframe.loc[i,'ret'] = dataframe.loc[i-1,'ret']

        dataframe.loc[0, 'pos'] = df.loc[0, 'ret']
        for i in range(1, len(dataframe)):
            if dataframe.loc[i,'close']>dataframe.loc[i,'ret']:
               dataframe.loc[i,'pos'] = 1
            else:
                if dataframe.loc[i,'close']<dataframe.loc[i,'ret']:
                   dataframe.loc[i,'pos'] = -1
                else:
                    if i==1 :
                     dataframe.loc[i,'pos'] = 0
                    else:
                     dataframe.loc[i,'pos'] = dataframe.loc[i-1,'pos']

        dataframe.loc[0, 'enterLong'] = df.loc[0, 'pos']
        for i in range(1+self.bardelay, len(dataframe)):
            rising = True
            falling = True
            dataframe.loc[i,'enterLong']=False        
            dataframe.loc[i,'enterShort']=False        
            for j in range(1,self.bardelay):
                if(dataframe.loc[i,'close']<dataframe.loc[i-j,'close']):
                    rising = False
                if(dataframe.loc[i,'close']>dataframe.loc[i-j,'close']):
                    falling = False
            if dataframe.loc[i,'pos'] ==  1 and \
               (self.trailingmenu!="Normal" or (i>1 and dataframe.loc[i,'pos']!=dataframe.loc[i-1,'pos'] ) and \
               rising:
               dataframe.loc[i,'enterLong']=True        
            
            if dataframe.loc[i,'pos'] ==  -1 and \
               (self.trailingmenu!="Normal" or (i>1 and dataframe.loc[i,'pos']!=dataframe.loc[i-1,'pos'] ) and \
               falling:
               dataframe.loc[i,'enterShort']=True        

        retrun dataframe


    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the entry signal for the given dataframe
        :param dataframe: DataFrame
        :return: DataFrame with entry column , 1: long, -1:short
        """
        dataframe.loc[
            (
                dataframe['enterLong']
            ),
            'entry'] = 1#-1.1
        dataframe.loc[
            (
                dataframe['enterShort']
            ),
            'entry'] = -1#-1.1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the exit signal for the given dataframe
        :param dataframe: DataFrame
        :return: DataFrame with exit column
        """
        dataframe.loc[
            (
                dataframe['enterLong'] or dataframe['enterShort']
            ),
            'exit'] = 1#-1.1
        return dataframe
