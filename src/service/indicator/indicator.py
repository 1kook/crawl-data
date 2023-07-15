import src.service.indicator.vp as VP
import src.service.indicator.ma as MA
import src.service.indicator.atr as ATR
import src.service.indicator.bb as BB
import src.service.indicator.rsi as RSI
import src.service.indicator.adx as ADX
import src.service.indicator.obv as OBV

class Indicator:
    def __init__(self, df):
        self.df = df
        self.ma = {}

    # vap
    def calVpActionArea(self, vp):
        return VP.calVpActionArea(self, vp)

    def drawVpPlot(self, plot):
        return VP.drawVpPlot(self, plot)

    # ema
    def calMa(self, period: int):
        return MA.calMa(self, period)

    def calMacd(self, fast: int, slow: int, signal: int):
        return MA.calMacd(self, fast, slow, signal)

    def drawMacd(self, plot):
        return MA.drawMacd(self, plot)
    
    #atr
    def calAtr(self, period: int):
        return ATR.calAtr(self, period)
    
    def drawAtr(self, plot):
        return ATR.drawAtr(self, plot)
    
    #bb
    def calBB(self, period: int, std: int):
        return BB.calBB(self, period, std)
    
    def drawBB(self, plot):
        return BB.drawBB(self, plot)
    
    #rsi
    def calRsi(self, period: int):
        return RSI.calRsi(self, period)
    
    def drawRsi(self, plot):
        return RSI.drawRsi(self, plot)

    #adx
    def calAdx(self, period: int):
        return ADX.calAdx(self, period)
    
    def drawAdx(self, plot):
        return ADX.drawAdx(self, plot)
    
    #obv
    def calObv(self):
        return OBV.calObv(self)
    
    def drawObv(self, plot):
        return OBV.drawObv(self, plot)