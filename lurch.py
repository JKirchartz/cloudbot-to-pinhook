from pinhook.bot import Bot

bot = Bot(
        channels=['#aaa'],
        nickname='lurch',
        server='localhost',
        ops=['kirch']
        )
bot.start()
