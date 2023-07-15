import plotly.graph_objects as go
import numpy as np

def calMa(self, period):
    self.ma[period] = self.df["close_price"].ewm(
        span=period, min_periods=period).mean()
    return self


def calMacd(self, fast, slow, signal):
    df = self.df[['close_price']].copy()
    self.calMa(fast)
    self.calMa(slow)
    
    df["fast"] = self.ma[fast]
    df["slow"] = self.ma[slow]
    df["macd"] = (df["fast"] - df["slow"]).dropna()
    df["macd_signal"] = df["macd"].ewm(
        span=signal, min_periods=signal).mean().dropna()
    
    self.macd = df.dropna()

    return self


def drawMacd(self, plot):
    # draw macd
    plot.fig.for_each_trace(lambda trace: trace.update(visible=False) if trace.name == "volume" else ())
    
    #draw and fill green and red bar    
    plot.fig.add_trace(
        go.Bar(
            x=self.macd.index,
            y=self.macd["macd"].where(self.macd["macd"] > 0),
            name="macd",
            marker={
                "color": "green",
            },
            visible=True,
        ), row=2, col=2
    )
    
    plot.fig.add_trace(
        go.Bar(
            x=self.macd.index,
            y=self.macd["macd"].where(self.macd["macd"] < 0),
            name="macd",
            marker={
                "color": "red",
            },
            visible=True,
        ), row=2, col=2
    )
    
    #draw macd signal
    plot.fig.add_trace(
        go.Scatter(
            x=self.macd.index,
            y=self.macd["macd_signal"],
            name="macd signal",
            line=dict(color="white",),
            visible=True,
        ), row=2, col=2
    )

    return self
