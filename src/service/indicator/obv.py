import plotly.graph_objects as go
import numpy as np

def calObv(self):
    df = self.df.copy()
    
    df["direction"] = np.where(df["close_price"] > df["close_price"].shift(1), 1, np.where(df["close_price"] < df["close_price"].shift(1), -1, 0))
    df["direction"][0] = 0
    df["vol_adj"] = df["volume"] * df["direction"]
    df["obv"] = df["vol_adj"].cumsum()
    
    
    self.obv = df.dropna()
    return self

def drawObv(self, plot):
    plot.fig.add_trace(
        go.Scatter(
            x=self.obv.index,
            y=self.obv["obv"],
            name="obv",
            line=dict(color="white",)
        ), row=2, col=2)
        
    
    return self