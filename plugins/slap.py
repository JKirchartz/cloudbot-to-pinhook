import random
import re
import pinhook.plugin as p

"""
A slap plugin
"""

@p.listener('slaplistener')
def slaplistener(msg):
    if "slaps " + msg.botnick in msg.text.lower():
        print("I've been slapped!")
        if random.randint(0,1) == 0:
            print("so I screamed.")
            return p.message(''.join(["A" * random.randint(5, 20), "a" * random.randint(10, 25)]))
        else:
            print("so I slapped back.")
            return p.action("slaps %s with a rather large trout" % msg.nick)

@p.register('!slap', 'Usage: !slap [nick]')
def slap(msg):
    if msg.arg != "":
        output = msg.arg
    else:
        output = msg.nick
    return p.action("slaps %s with a rather large trout" % output);
