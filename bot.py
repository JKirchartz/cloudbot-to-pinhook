#!/usr/bin/env python

from pinhook.bot import Bot

ph = Bot(
    channels=['#fnord'],
    nickname='DocVuDu',
    server='irc.maddshark.net',
    ops=['derkirche']
)
ph.start()
