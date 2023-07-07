import src.service.indicator.vp as VP
import src.service.indicator.ema as EMA


class Indicator:
    def __init__(self, df, dtf):
        self.df = df
        self.dtf = dtf
        self.emas = {}

    # vap
    def calVpActionArea(self, vp):
        return VP.calVpActionArea(self, vp)

    def drawVpPlot(self, plot):
        return VP.drawVpPlot(self, plot)

    # ema
    def ema(self, period: int):
        return EMA.ema(self, period)

    def drawEmasPlot(self, period: int, plot):
        return EMA.drawEmasPlot(self, period, plot)
