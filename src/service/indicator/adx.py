import numpy as np
import plotly.graph_objects as go

def calAdx(self, period: int):
    df = self.df.copy()
    self.calAtr(period)
    
    df["+DX"] = np.where((df["high_price"] - df["high_price"].shift(1)) > (df["low_price"].shift(1) - df["low_price"]), df["high_price"] - df["high_price"].shift(1), 0)
    df["-DX"] = np.where((df["low_price"].shift(1) - df["low_price"]) > (df["high_price"] - df["high_price"].shift(1)), df["low_price"].shift(1) - df["low_price"], 0)
    
    df["S+DM"] = df["+DX"].ewm(span=period, adjust=False).mean()
    df["S-DM"] = df["-DX"].ewm(span=period, adjust=False).mean()
    df["+DMI"] = (df["S+DM"] / self.atr["ATR"]) * 100
    df["-DMI"] = (df["S-DM"] / self.atr["ATR"]) * 100
    
    df["DX"] = abs(df["+DMI"] - df["-DMI"]) / (df["+DMI"] + df["-DMI"]) * 100
    df["ADX"] = df["DX"].ewm(span=period, adjust=False).mean()
    
    self.adx = df.dropna()
    
    return self

def drawAdx(self, plot):
    #delete volumne plot and add atr plot
    plot.fig.for_each_trace(lambda trace: trace.update(visible=False) if trace.name == "volume" else ())
    
    for i in range(0, 100, 25):
        plot.fig.add_shape(
            type="rect",
            x0=self.adx["ADX"].index[0],
            y0=i,
            x1=self.adx["ADX"].index[-1],
            y1=i+25,
            line=dict(
                width=0,
            ),
            fillcolor=f"rgba({255-i*255/100}, {i/100*128}, 0, 0.5)",
            row = 2, col = 2
        )
    
    plot.fig.add_trace(
        go.Scatter(
            x=self.adx["ADX"].index,
            y=self.adx["ADX"],
            name="adx",
            line=dict(color="white",)
        ), row=2, col=2)
    
            
    
    return self
    