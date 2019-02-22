import random
import re
import pinhook.plugin as p

"""
A plugin to Wilhelm Scream
"""


wilhelmrexer = re.compile('(FLASH\!|a{3,}?)', re.I | re.M)

def generate():
    big = random.randint(5, 20)
    small = random.randint(10, 25)
    return ''.join(["A" * big, "a" * small]);

@p.listener('wilhelmlistener')
def wilhelmlistener(msg):
    random.seed(msg)
    if wilhelmrexer.search(msg.text.strip()) is not None:
        return p.message(generate())

@p.register('!wilhelm')
def wilhelm(msg):
    if msg.arg:
        random.seed(msg)
    return p.message(generate())
