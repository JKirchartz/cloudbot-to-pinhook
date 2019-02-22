import pinhook.plugin
from random import choice, randint


quotes = [
        "You rang?"
        ''.join([choice(["E", "U"]) * randInt(1,4), choice(["h", "g", "-"]) * randint(4,10)])
        ]


@pinhook.plugin.listener('lurchlistener')
def lurchlistener(msg):
    if msg.botnick in msg.text:
        return pinhook.plugin.message(choice(quotes))
