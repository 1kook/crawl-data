import time
import os
import psycopg2
from dotenv import load_dotenv
import pandas as pd
import ccxt
import telebot
import pandas as pd
from scipy import stats, signal
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import datetime


load_dotenv()
DB_CON = psycopg2.connect(os.getenv('CONNECTION'))
DAYS = 10
TIME_FRAME=30

def getData(days=14):
    fromDate = datetime.datetime.now() - datetime.timedelta(days=days)

    df = pd.read_sql_query(
        'SELECT * FROM btc_price WHERE open_time > %s', DB_CON, params=(fromDate,))
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms', utc=False)
    df['close_time'] = pd.to_datetime(df['close_time'], unit='ms', utc=False)
    df = df.set_index('open_time')
    df = df.resample('1MIN').ffill()

    return df

def resampleTimeframe(df, tf):
    df = df.copy()

    last_index_minute = df.index[-1].minute
    minutes_to_adjust = (tf - (last_index_minute + 1) % tf) % tf

    if minutes_to_adjust > 0:
        last_row = df.iloc[-1]
        for _ in range(minutes_to_adjust):
            df.loc[df.index[-1] + pd.Timedelta(minutes=1)] = last_row

    dtf = df.resample(str(tf)+'Min').agg({
        'open_price': 'first',
        'high_price': 'max',
        'low_price': 'min',
        'volume': 'sum',
        'close_price': lambda x: x.iloc[-1],
        'close_time': lambda x: x.iloc[-1]
    }).dropna()

    return dtf

# def calVolumeProfile(data, bin_size=10):
#     vap = pd.DataFrame(columns=['price', 'volume'])
#     vap.set_index('price')

#     for i in range(0, len(data)-1):
#         price = data.iloc[i]['close_price']
#         volume = data.iloc[i]['volume']
#         vap.loc[len(vap)] = [price, volume]

#     # cal histogram
#     bins = np.arange(vap['price'].min(), vap['price'].max(), bin_size)
#     vap['bin'] = pd.cut(vap['price'], bins)
#     vap = vap.groupby('bin').sum()

#     new_index = []
#     for index in vap.index:
#         new_index.append(index.mid)

#     vap.index = new_index

#     return vap

def calVolumeProfile(data, bin_size=10):
    price = data['close_price']
    volume = data['volume']
    
    # Calculate histogram
    bins = np.arange(price.min(), price.max(), bin_size)
    bin_labels = pd.cut(price, bins)

    vap = pd.DataFrame({'price': price, 'volume': volume, 'bin': bin_labels})
    vap = vap.groupby('bin').sum()

    # Update index
    new_index = [bin.mid for bin in vap.index]
    vap.index = new_index

    return vap

def calActionArea(df, vp):
    kde_factor = 0.05
    num_samples = 500
    kde = stats.gaussian_kde(
    df["close_price"], weights=df["volume"], bw_method=kde_factor)
    xr = np.linspace(df["close_price"].min(),
                    df["close_price"].max(), num_samples)
    kdy = kde(xr)

    peaks, peaks_props = signal.find_peaks(kdy)
    pkx = xr[peaks]
    pky = kdy[peaks]

    scaleY = vp["volume"].max() / kdy.max()

    kdy = kdy * scaleY
    peaks, peaks_props = signal.find_peaks(
        kdy, prominence=kdy.max() * 0.3, width=1)
    pkx = xr[peaks]
    pky = kdy[peaks]

    ticks_per_sample = (xr.max() - xr.min()) / num_samples

    left_base = peaks_props["left_bases"]
    right_base = peaks_props["right_bases"]
    line_x = pkx
    line_y0 = pky
    line_y1 = pky - peaks_props['prominences']

    left_ips = peaks_props['left_ips']
    right_ips = peaks_props['right_ips']
    width_x0 = xr.min() + (left_ips * ticks_per_sample)
    width_x1 = xr.min() + (right_ips * ticks_per_sample)
    width_y = peaks_props['width_heights']
    
    return line_x, line_y0, line_y1, width_x0, width_x1, width_y

def drawVapPlot(df, vp, line_x, line_y0, line_y1, width_x0, width_x1, width_y):
    fig = make_subplots(
        rows=2,
        cols=2,
        vertical_spacing=0.07,
        subplot_titles=('VAP', 'OHLC', '', 'Volume'),
        row_width=[0.2, 0.7],
        column_widths=[0.2, 0.7],
        horizontal_spacing=0.01,
        shared_yaxes='rows'
    )

    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['open_price'],
            high=df['high_price'],
            low=df['low_price'],
            close=df['close_price'],
            name='market data'
        ),
        row=1, col=2
    )

    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df['volume'],
            name='volume',
            marker={
                "color": "rgba(128,128,128,0.5)",
            }),
        row=2, col=2
    )

    # draw vap
    fig.add_trace(
        go.Bar(
            x=vp.volume,
            y=vp.index,
            text=np.around(vp.volume, 2),
            textposition='auto',
            orientation='h',
        ),
        row=1, col=1
    )

    for x, y0, y1 in zip(line_x, line_y0, line_y1):
        fig.add_shape(
            type='line',
            xref='x', yref='y',
            x0=y0, y0=x, x1=y1, y1=x,
            line=dict(
                color='red',
                width=2,
            ),
            row=1, col=1
        )

    for x0, x1, y in zip(width_x0, width_x1, width_y):
        fig.add_shape(
            type='line',
            xref='x', yref='y',
            x0=y, y0=x0, x1=y, y1=x1,
            line=dict(
                color='red',
                width=2,
            ),
            row=1, col=1
        )

        fig.add_shape(
            type="rect",
            x0=df.index.min(), y0=x0, x1=df.index.max()+pd.Timedelta(minutes=120), y1=x1,
            line=dict(width=0),
            fillcolor='rgba(136,112,185,0.3)',
            row=1, col=2
        )

    fig.update_layout(
        title_text='BTC/USDT',
        yaxis2=dict(
            title="Price (USD)",
            side="right"
        ),
        xaxis=dict(rangeslider=dict(visible=False)),
        xaxis2=dict(rangeslider=dict(visible=False))
    )

    fig.update_layout(height=800)
    return fig.to_html(full_html=True)

def vapHandler(days, timeframe):
    df = getData(days)
    dtf = resampleTimeframe(df, timeframe)
    vp = calVolumeProfile(df, 50)
    line_x, line_y0, line_y1, width_x0, width_x1, width_y = calActionArea(df,vp)
    return drawVapPlot(dtf, vp, line_x, line_y0, line_y1, width_x0, width_x1, width_y)
# draw candlestick and vap
