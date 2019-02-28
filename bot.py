#!/usr/bin/env python3

from pinhook.bot import Bot

ph = Bot(
    channels=['#discord', '#fnord'],
    nickname='lurch',
    server='irc.maddshark.net',
    ops=['derkirche']
)
ph.start()
