import random
import re
import pinhook.plugin as p

"""
A slap plugin
"""

slaps=[
        "a live aligator",
        "a severed limb",
        "a battle axe",
        "the rack",
        "thing",
        "a chair",
        "a stick of dynamite",
        "Granny Frump",
        "a bottle of poison"
        ]

@p.listener('slaplistener')
def slaplistener(msg):
    if "slaps " + msg.botnick in msg.text.lower():
        if random.randint(0,1) == 0:
            return p.message(''.join(["A" * random.randint(5, 20), "a" * random.randint(10, 25)]))
        else:
            return p.action("slaps {} with {}".format(msg.nick, random.choice(slaps)))

@p.register('!slap', 'Usage: !slap [nick]')
def slap(msg):
    if msg.arg != "":
        output = msg.arg
    else:
        output = msg.nick
    return p.action("slaps {} with {}".format(output, random.choice(slaps)))
