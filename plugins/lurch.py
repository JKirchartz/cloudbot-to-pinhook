import pinhook.plugin as p
import time
from random import choice, randint

@p.listener('lurchlistener')
def lurchlistener(msg):
    quotes = [
            "You rang?",
            "You rang?",
            ''.join([
                "E" * randint(1,4),
                "e" * randint(0,4),
                "u" * randint(0,6),
                "g" * randint(0,8),
                "h" * randint(4,10),
                "-h" * randint(0,6)
                ]),
            ''.join([
                "G" * randint(0,4),
                "R" * randint(1,5),
                "r" * randint(1,8),
                "-r" * randint(0,6)
                ]),
            ''.join([
                "Y" * randint(1,4),
                "y" * randint(0,4),
                "e" * randint(4,10),
                "s" * randint(0,6),
                "-s" * randint(0,6)
                ]),
            ''.join([
                "U" * randint(1,4),
                "u" * randint(0,4),
                "h" * randint(4,10),
                "-h" * randint(0,6)
                ])
            ]
    if msg.botnick in msg.text:
        return p.message(choice(quotes))


@p.register('!ping')
@p.register('!gong')
def gong(msg):
    gongos = "o" * randint(2,8)
    msg.action(msg.channel, "*g%sng*" % gongos)
    time.sleep(randint(1,3))
    return p.message("You rang?")

