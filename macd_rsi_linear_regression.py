import QuantConnect
import pandas as pd
import numpy as np
from AlgorithmImports import *
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from datetime import timedelta


class ScikitLearnLinearRegressionAlgorithm(QCAlgorithm):
    def Initialize(self) -> None:
        self.SetStartDate(2019, 8, 21)  # Set Start Date
        self.SetEndDate(2021, 11, 26)
        self.SetCash(100000)  # Set Strategy Cash
        self.btc = self.AddCrypto("BTCUSD", Resolution.Hour).Symbol
        # self.bb = self.BB(symbol=self.btc, period=20, k=2, movingAverageType=MovingAverageType.Simple, resolution=Resolution.Daily)
        self.rsi = self.RSI(self.btc, 14, MovingAverageType.Simple, Resolution.Hour)
        self.macd = self.MACD(symbol=self.btc, fastPeriod=10, slowPeriod=30, signalPeriod=2,
                              type=MovingAverageType.Simple, resolution=Resolution.Hour)
        self.SetWarmup(timedelta(720))
        self.prevprice = float(0)
        self.rsivals = []
        self.macdvals = []
        self.pricevals = []
        self.assetData = dict
        self.assetDataFrame = pd.DataFrame
        self.priceDataFrame = pd.DataFrame
        self.warmup = False
        self.price = 0
        self.valueReturned = False
        self.LR = LinearRegression()
        self.model = None
        self.testerdata = None

    def OnWarmupFinished(self):
        self.trainingData = {
            "priceChange": self.pricevals,
            "rsi": self.rsivals,
            "macd": self.macdvals
        }
        self.testingData = {
            "rsi": self.rsivals,
            "macd": self.macdvals
        }
        self.resultData = {
            "priceChange": self.pricevals
        }

        self.assetDataFrame = pd.DataFrame(self.testingData)
        self.priceDataFrame = pd.DataFrame(self.resultData)
        '''self.Log("PRICE")
        self.Log(len(self.pricevals))
        self.Log(self.pricevals)
        self.Log("RSI")
        self.Log(len(self.rsivals))
        self.Log(self.rsivals)
        self.Log("MACD")
        self.Log(len(self.macdvals))
        self.Log(self.macdvals)'''
        self.valueReturned = False
        self.warmup = True

    def duringWarming(self):
        if self.rsi.IsReady and self.macd.IsReady:
            if self.Time.time().hour == 6:
                rsiv = (self.rsi.Current.Value)
                macdv = (self.macd.Current.Value)
                self.rsivals.append(rsiv)
                self.macdvals.append(macdv)
                self.price = self.Securities[self.btc].Price
                self.valueReturned = True
            elif self.Time.time().hour == 11 and self.valueReturned == True:
                pricechange = (self.price) - (self.prevprice)
                self.pricevals.append(pricechange)
                self.prevprice = (self.price)
        else:
            self.Log("vars not ready")

    def ML(self, macd, rsi):
        if self.valueReturned == False:
            x = self.assetDataFrame
            y = self.priceDataFrame
            self.testerdata = x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
            self.model = self.LR.fit(x_train, y_train)
            y_prediction = self.LR.predict(x_test)
            score = r2_score(y_test, y_prediction)
            self.Log('score' + str(score))
            self.Log('mean squared error' + str(mean_squared_error(y_test, y_prediction)))
            self.Log('distance from error' + str(np.sqrt(mean_squared_error(y_test, y_prediction))))
            data = pd.DataFrame({
                "rsi": rsi,
                "macd": macd
            }, index=[1])
            value = self.LR.predict(data)
            if value > 0:
                self.SetHoldings(self.btc, 1)
            else:
                self.Liquidate()

    def trade(self, macd, rsi):
        x = self.assetDataFrame
        y = self.priceDataFrame
        data = pd.DataFrame({
            "rsi": rsi,
            "macd": macd
        }, index=[1])
        x_train, x_test, y_train, y_test = self.testerdata
        self.LR.fit(x_train, y_train)


    def OnData(self, slice: QuantConnect.Data.Slice) -> None:
        if self.warmup == False:
            self.duringWarming()
        elif self.warmup == True:
            rsiv = (self.rsi.Current.Value)
            macdv = (self.macd.Current.Value)
            self.ML(rsiv, macdv)
