# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import tempfile
import os
from pathlib import Path
import sys
from config import Config
from record import Record as Trecord
from Telegram import Telegram as TTelegram


# получить настройки
file_json = "config.json"
if len(sys.argv) > 1:
    file_json = sys.argv[1]
config = Config(__file__, file_json).read()
if config is None:
    print("Config file not exists")
    sys.exit()

# глобальный словарь для всех потоков
PARAMS = {

    'tg-bot': config['tg-bot'],
    'tg-group': config['tg-group'],
    'audio-threshold-on': config['audio-threshold-on'],
    'audio-threshold-off': config['audio-threshold-off'],
    'audio-time-low': config['audio-time-low'],
    'audio-time-hi': config['audio-time-hi'],
    'path-sound': config['path-sound']
}


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+8 to toggle the breakpoint.
    print("start service")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
Trecord(PARAMS).start()
TTelegram(PARAMS).start()


