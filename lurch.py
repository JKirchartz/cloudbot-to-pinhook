#!/usr/bin/env python3

from pinhook.bot import Bot

bot = Bot(
        channels=['#aaa', '#counting', '#counting-meta', '#counting-anarchy', '#bots'],
        nickname='lurch',
        server='localhost',
        ops=['kirch']
        )
bot.start()
