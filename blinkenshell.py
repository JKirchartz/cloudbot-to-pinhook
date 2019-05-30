#!/usr/bin/env python3

from pinhook.bot import Bot

bot = Bot(
        channels=['#lurch'],
        nickname='lurch',
        server='irc.blinkenshell.org',
        port=6697,
        ssl_required=True,
        ops=['kirch']
        )
bot.start()
