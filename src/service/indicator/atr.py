import plotly.graph_objects as go

def calAtr(self, period: int):
    df = self.df.copy()
    df["H-L"] = abs(df["high_price"] - df["low_price"])
    df["H-PC"] = abs(df["high_price"] - df["close_price"].shift(1))
    df["L-PC"] = abs(df["low_price"] - df["close_price"].shift(1))
    df["TR"] = df[["H-L", "H-PC", "L-PC"]].max(axis=1, skipna=False)
    df["ATR"] = df["TR"].rolling(period).mean()
    
    self.atr = df.dropna()
    return self

def drawAtr(self, plot):
    #delete volumne plot and add atr plot
    plot.fig.for_each_trace(lambda trace: trace.update(visible=False) if trace.name == "volume" else ())
    plot.fig.add_trace(
        go.Scatter(
            x=self.atr["ATR"].index,
            y=self.atr["ATR"],
            name="atr",
            line=dict(color="blue",)
        ), row=2, col=2)
    
    return self
    