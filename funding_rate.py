from datetime import datetime
from exchange_interface import FtxClient
from logzero import logger
from time import gmtime, strftime

import time
import os
import settings
import telegram

# Environment variables
FUTURES = os.getenv('LIST_OF_FUTURES')
DELAY = int(os.getenv('UPDATE_DELAY'))
OUTPUT_NUMBER = int(os.getenv('OUTPUT_NUMBER'))
OUTPUT_THRESHOLD = int(os.getenv('OUTPUT_THRESHOLD'))
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

fundings = {}
send_telegram = True if TELEGRAM_TOKEN else False

ftx = FtxClient()

if(send_telegram):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)


def get_top_bottom():
    for future in get_futures():
        fundings[future] = ftx.get_funding_rate(future)

    ordered_fundings = {k: v for k, v in sorted(
        fundings.items(), key=lambda item: item[1])}

    total = len(ordered_fundings)
    bottom = {k: ordered_fundings[k]
              for k in list(ordered_fundings)[:OUTPUT_NUMBER]}
    top = {k: ordered_fundings[k] for k in list(
        ordered_fundings)[total - OUTPUT_NUMBER:]}

    send_message(f'{strftime("%Y-%m-%d - %H:%M:%S", gmtime())}')
    send_message(f'Top {OUTPUT_NUMBER}:')
    for k, v in top.items():
        if(abs(v) < OUTPUT_THRESHOLD):
            continue
        send_message(f'{k} ({v})')

    send_message(f'Bottom {OUTPUT_NUMBER}:')
    for k, v in bottom.items():
        if(abs(v) < OUTPUT_THRESHOLD):
            continue
        send_message(f'{k} ({v})')


def send_message(message):
    if(send_telegram):
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    logger.info(message)


def get_futures():
    if(FUTURES == 'all'):
        return ftx.get_all_futures()
    else:
        return FUTURES.split(',')


while True:
    start_time = time.time()
    get_top_bottom()
    execution_time = time.time() - start_time
    # Discount execution time from DELAY
    time.sleep(DELAY - int(execution_time))
