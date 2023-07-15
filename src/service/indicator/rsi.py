import plotly.graph_objects as go
import numpy as np

def calRsi(self, period: int):
    df = self.df.copy()
    df["delta"] = df["close_price"] - df["close_price"].shift(1)
    df["gain"] = np.where(df["delta"] >= 0, df["delta"], 0)
    df["loss"] = np.where(df["delta"] < 0, abs(df["delta"]), 0)
    avg_gain = []
    avg_loss = []
    
    gain = df["gain"].tolist()
    loss = df["loss"].tolist()
    
    for i in range(len(df)):
        if i < period:
            avg_gain.append(np.NaN)
            avg_loss.append(np.NaN)
        elif i == period:
            avg_gain.append(df["gain"].rolling(period).mean().tolist()[period])
            avg_loss.append(df["loss"].rolling(period).mean().tolist()[period])
        elif i > period:
            avg_gain.append(((period - 1) * avg_gain[i - 1] + gain[i]) / period)
            avg_loss.append(((period - 1) * avg_loss[i - 1] + loss[i]) / period)
    
    df["avg_gain"] = np.array(avg_gain)
    df["avg_loss"] = np.array(avg_loss)
    df["rs"] = df["avg_gain"] / df["avg_loss"]
    df["rsi"] = 100 - (100 / (1 + df["rs"]))
    
    self.rsi = df.dropna()
    return self

def drawRsi(self, plot):
    #delete volumne plot and add rsi plot
    plot.fig.for_each_trace(lambda trace: trace.update(visible=False) if trace.name == "volume" else ())
    plot.fig.add_trace(
        go.Scatter(
            x=self.rsi.index,
            y=self.rsi["rsi"],
            name="rsi",
            line=dict(color="blue")
        ), row=2, col=2)
    
    plot.fig.add_shape(
            type="rect",
            x0=self.rsi.index[0],
            y0=30,
            x1=self.rsi.index[-1],
            y1=70,
            line=dict(width=0),
            fillcolor='rgba(181, 181, 181, 0.2)',
            row=2, col=2
        )


    
    return self