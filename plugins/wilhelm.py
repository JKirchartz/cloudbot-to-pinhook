import random
import re
import pinhook.plugin as p

"""
A plugin to Wilhelm Scream
"""

def wilhelmgen():
    big = random.randint(5, 20)
    small = random.randint(10, 25)
    return ''.join(["A" * big, "a" * small]);

@p.listener('wilhelmlistener')
def wilhelmlistener(msg):
    if "FLASH!" in msg.text or "aaa" in msg.text.lower():
        return p.message(wilhelmgen())

@p.register('!wilhelm')
def wilhelm(msg):
    return p.message(wilhelmgen())
