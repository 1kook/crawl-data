import asyncio
import time
import os
import psycopg2
from dotenv import load_dotenv
import pandas as pd
import ccxt
import telebot

load_dotenv()
conn = psycopg2.connect(os.getenv('CONNECTION'))
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

# bot.send_message(os.getenv('CHAT_ID'), 'App started')
# load checkpoint from file txt
def crawlPrice(symbol, stopThreads):
    checkpoint = 0
    #get last checkpoint from db
    cursor = conn.cursor()
    cursor.execute(f"SELECT close_time  AT TIME ZONE 'UTC' FROM {symbol.lower()}_price ORDER BY open_time DESC LIMIT 1")
    if cursor.rowcount > 0:
        checkpoint = cursor.fetchone()[0]
        #convert to timestamp
        checkpoint = int(checkpoint.timestamp() * 1000)
    else:
        checkpoint = 1546300800000
    cursor.close()

    exchange = ccxt.binance()

    while True:
        try:
            kline = exchange.fetch_ohlcv(f"{symbol.upper()}/USDT", '1m', since=checkpoint)
        except Exception as e:
            print(e)
            time.sleep(10)
            continue
        
        if len(kline) > 1:
            kline = kline[:-1]
            for el in kline:
                if stopThreads[0]:
                    return
                print(el)
                data = {
                    'open_time': pd.to_datetime(el[0], unit='ms', utc=False),
                    'open': float(el[1]),
                    'high': float(el[2]),
                    'low': float(el[3]),
                    'close': float(el[4]),
                    'volume': float(el[5]),
                    'close_time': pd.to_datetime(el[0]+60*1000, unit='ms'),
                }
                
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO {symbol.lower()}_price (open_time, open_price, high_price, low_price, close_price, volume, close_time, quote_asset_volume) VALUES ('{data['open_time']}', {data['open']}, {data['high']}, {data['low']}, {data['close']}, {data['volume']}, '{data['close_time']}', 0)")
                conn.commit()
                cursor.close()

                checkpoint = data["close_time"]
                print(f"{symbol} - {data['open_time']} - {data['close_time']}")