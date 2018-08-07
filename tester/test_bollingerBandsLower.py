import numpy as np
import sys
sys.path.append(r'''C:\Users\tejaswini\Desktop\auquantoolbox''')
from backtester.features.bollinger_bands_lower_feature import BollingerBandsLowerFeature
from backtester.instruments_manager import *
from backtester.instruments_lookback_data import *
from backtester.modelLearningManagers.feature_manager import FeatureManager
from unittest.mock import Mock, MagicMock
from tester.initialize import Initialize
import math
import pandas as pd
import pytest

@pytest.fixture
def mockInstrumentManager():
    return Mock(spec=InstrumentManager)
@pytest.fixture
def mockFeatureManager():
    return Mock(spec=FeatureManager)
@pytest.fixture
def mockInstrumentLookbackData():
	return Mock(spec=InstrumentsLookbackData)

def test_bollinger_bands_lower( mockInstrumentManager, mockFeatureManager, mockInstrumentLookbackData):
    for i in range(1,4):
        dataSet = Initialize.getDataSet(i)
        mockInstrumentManager.getLookbackInstrumentFeatures.return_value = mockInstrumentLookbackData
        mockInstrumentLookbackData.getFeatureDf.return_value=dataSet["data"]
        resultInstrument = BollingerBandsLowerFeature.computeForInstrument(i, "", dataSet["featureParams"], "ma_m",  mockInstrumentManager)
        mockInstrumentManager.getDataDf.return_value = dataSet["data"]
        resultMarket = BollingerBandsLowerFeature.computeForMarket(i, "", dataSet["featureParams"], "ma_m", {},  mockInstrumentManager)
        mockFeatureManager.getFeatureDf.return_value = dataSet["data"]
        resultInstrumentData = BollingerBandsLowerFeature.computeForInstrumentData(i, dataSet["featureParams"], "ma_m", mockFeatureManager )
        assert round(resultMarket,2) == round(dataSet['bblf'][-1],2)
        assert round(resultInstrument['open'],2) == round(dataSet['bblf'][-1],2)
        assert round(resultInstrumentData.iat[-1,0],2) == round(dataSet['bblf'][-1],2)
    for i in range(4,5):
        dataSet = Initialize.getDataSet(i)
        mockInstrumentManager.getLookbackInstrumentFeatures.return_value = mockInstrumentLookbackData
        mockInstrumentLookbackData.getFeatureDf.return_value=dataSet["data"]
        with pytest.raises(ValueError):
        	BollingerBandsLowerFeature.computeForInstrument(i, "", dataSet["featureParams"], "ma_m",  mockInstrumentManager)
        mockInstrumentManager.getDataDf.return_value = dataSet["data"]
        with pytest.raises(ValueError):
        	BollingerBandsLowerFeature.computeForMarket(i, "", dataSet["featureParams"], "ma_m", {},  mockInstrumentManager)
        mockFeatureManager.getFeatureDf.return_value = dataSet["data"]
        with pytest.raises(ValueError):
        	BollingerBandsLowerFeature.computeForInstrumentData(i, dataSet["featureParams"], "ma_m", mockFeatureManager )
    for i in range(5,6):
        dataSet = Initialize.getDataSet(i)
        mockInstrumentManager.getLookbackInstrumentFeatures.return_value = mockInstrumentLookbackData
        mockInstrumentLookbackData.getFeatureDf.return_value=dataSet["data"]
        with pytest.raises(ValueError):
        	BollingerBandsLowerFeature.computeForInstrument(i, "", dataSet["featureParams"], "ma_m",  mockInstrumentManager)
        mockInstrumentManager.getDataDf.return_value = dataSet["data"]
        with pytest.raises(ValueError):
        	BollingerBandsLowerFeature.computeForMarket(i, "", dataSet["featureParams"], "ma_m", {},  mockInstrumentManager)
        mockFeatureManager.getFeatureDf.return_value = dataSet["data"]
        with pytest.raises(ValueError):
            BollingerBandsLowerFeature.computeForInstrumentData(i, dataSet["featureParams"], "ma_m", mockFeatureManager )