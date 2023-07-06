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

queue = []
MAX_QUEUE = 61
TOTAL = 0
# load checkpoint from file txt
checkpoint = 0
with open('checkpoint.txt', 'r') as f:
    checkpoint = int(f.read())

exchange = ccxt.binance()

while True:
    try:
        kline = exchange.fetch_ohlcv('BTC/USDT', '1m', since=checkpoint)
    except:
        print('Error')
        time.sleep(60)
        continue
    
    if len(kline) > 1:
        kline = kline[:-1]
        for el in kline:
            data = {
                'open_time': pd.to_datetime(el[0], unit='ms', utc=False),
                'open': float(el[1]),
                'high': float(el[2]),
                'low': float(el[3]),
                'close': float(el[4]),
                'volume': float(el[5]),
                'close_time': pd.to_datetime(el[0]+60*1000, unit='ms'),
            }

            print(data)
            if len(queue) < MAX_QUEUE:
                queue.append(data)
                TOTAL += data['close']
            else:
                queue.pop(0)
                queue.append(data)

                frame_5 = queue[-1]['close'] - queue[-6]['close']
                frame_15 = queue[-1]['close'] - queue[-16]['close']
                frame_30 = queue[-1]['close'] - queue[-31]['close']
                frame_60 = queue[-1]['close'] - queue[-61]['close']

                if frame_5 > 200 and frame_15 > 200 and frame_30 > 200 and frame_60 > 200:
                    print('BUY')
                    bot.send_message(os.getenv('CHAT_ID'), "🚨 BUY signal 🟢 \nCurrent price: {} \n5m: {} \n15m: {} \n30m: {} \n60m: {} \nTime (UTC): {}".format(queue[-1]["close"], frame_5, frame_15, frame_30, frame_60, queue[-1]["close_time"]), parse_mode='Markdown')
                    queue = queue[2:]
                elif frame_5 < -200 and frame_15 < -200 and frame_30 < -200 and frame_60 < -200:
                    print('SELL')
                    bot.send_message(os.getenv('CHAT_ID'), "🚨 SELL signal 🔴 \nCurrent price: {} \n5m: {} \n15m: {} \n30m: {} \n60m: {} \nTime (UTC): {}".format(queue[-1]["close"], frame_5, frame_15, frame_30, frame_60, queue[-1]["close_time"]), parse_mode='Markdown')
                    queue = queue[15:]
            cursor = conn.cursor()
            cursor.execute("INSERT INTO btc_price (open_time, open_price, high_price, low_price, close_price, volume, close_time, quote_asset_volume) VALUES (%(open_time)s, %(open)s, %(high)s, %(low)s, %(close)s, %(volume)s, %(close_time)s, 0)", data)
            conn.commit()

            checkpoint = el[0]+1*60*1000
            with open('checkpoint.txt', 'w') as f:
                f.write(str(checkpoint))
        time.sleep(10)