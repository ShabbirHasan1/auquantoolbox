from datetime import timedelta
from instrumentFeatures.instrument_feature_config import InstrumentFeatureConfig
from dataSource.auquan_data_source import AuquanDataSource
from marketFeatures.market_feature_config import MarketFeatureConfig
from executionSystem.simple_execution_system import SimpleExecutionSystem
from orderPlacer.backtesting_order_placer import BacktestingOrderPlacer
from backtester.constants import *


class TradingSystemParameters(object):
    def __init__(self):
        self.__instrumentFeatureConfigs = {}
        instrumentFeatureConfigDicts = self.getInstrumentFeatureConfigDicts()
        for instrumentType in instrumentFeatureConfigDicts:
            self.__instrumentFeatureConfigs[instrumentType] = map(lambda x: InstrumentFeatureConfig(x), instrumentFeatureConfigDicts[instrumentType])
        self.__marketFeatureConfigs = map(lambda x: MarketFeatureConfig(x), self.getMarketFeatureConfigDicts())

    #####################################################################
    ###      START OF OVERRIDING METHODS
    #####################################################################

    '''
    Returns an instance of class DataParser
    '''
    def getDataParser(self):
        raise NotImplementedError
        return None

    '''
    Returns a timedetla object to indicate frequency of updates to features
    Any updates within this frequncy to instruments do not trigger feature updates.
    Consequently any trading decisions that need to take place happen with the same
    frequency
    '''
    def getFrequencyOfFeatureUpdates(self):
        return timedelta(0, 60)

    '''
    Returns a dictionary with:
    key: string representing instrument type. Right now INSTRUMENT_TYPE_OPTION, INSTRUMENT_TYPE_STOCK, INSTRUMENT_TYPE_FUTURE
    value: Array of instrument feature config dictionaries
        feature config Dictionary has the following keys:
        featureId: a string representing the type of feature you want to use
        featureKey: {optional} a string representing the key you will use to access the value of this feature.
                    If not present, will just use featureId
        params: {optional} A dictionary with which contains other optional params if needed by the feature
    Example:
    positionConfigDict = {'featureId': 'position'}
    vwapConfigDict = {'featureKey': 'price',
                          'featureId': 'vwap'}
    movingAvg_30Dict = {'featureKey': 'mv_avg_30',
                          'featureId': 'moving_average',
                          'params': {'days': 30}}
    movingAvg_90Dict = {'featureKey': 'mv_avg_90',
                          'featureId': 'moving_average',
                          'params': {'days': 90}}
    return {INSTRUMENT_TYPE_FUTURE: [positionConfigDict, vwapConfigDict],
            INSTRUMENT_TYPE_STOCK: [positionConfigDict, movingAvg_30Dict, movingAvg_90Dict]}

    For each future instrument, you will have features keyed by position and price.
    For each stock instrument, you will have features keyed by position, mv_avg_30, mv_avg_90
    '''
    def getInstrumentFeatureConfigDicts(self):
        return {}

    '''
    Returns an array of market feature config dictionaries
        market feature config Dictionary has the following keys:
        featureId: a string representing the type of feature you want to use
        featureKey: a string representing the key you will use to access the value of this feature.this
        params: A dictionary with which contains other optional params if needed by the feature
    '''
    def getMarketFeatureConfigDicts(self):
        return []

    '''
    A function that returns your predicted value based on your heuristics. 
    If you are just trading one asset like a stock, it could be the predicted value of the stock.
    If you are doing pair trading, the prediction could be the difference in the prices of the stocks.
    Arguments:
    time - When this prediction is being calculated
    currentMarketFeatures - Dictionary of market features which have been calculated at this update cycle.
    instrumentManager - Holder for all instruments and everything else if you need.
    '''
    def getPrediction(self, time, currentMarketFeatures, instrumentManager):
        return 0.0

    '''
    Returns the type of execution system we want to use. Its an implementation of the class ExecutionSystem
    Basically, it converts prediction to intended positions for different instruments.
    '''
    def getExecutionSystem(self):
        return SimpleExecutionSystem(longLimit=12000, shortLimit=12000)

    '''
    Returns the type of order placer we want to use. its an implementation of the class OrderPlacer.
    It helps place an order, and also read confirmations of orders being placed.
    For Backtesting, you can just use the BacktestingOrderPlacer, which places the order which you want, and automatically confirms it too.
    '''
    def getOrderPlacer(self):
        return BacktestingOrderPlacer()

    '''
    Returns the amount of lookback data you want for your calculations. The historical market features and instrument features are only
    stored upto this amount.
    This number is the number of times we have updated our features. 
    '''
    def getLookbackSize(self):
        return 500

    #####################################################################
    ###      END OF OVERRIDING METHODS
    #####################################################################

    def getFeatureConfigsForInstrumentType(self, instrumentType):
        if instrumentType in self.__instrumentFeatureConfigs:
            return self.__instrumentFeatureConfigs[instrumentType]
        else:
            return []

    def getMarketFeatureConfigs(self):
        return self.__marketFeatureConfigs