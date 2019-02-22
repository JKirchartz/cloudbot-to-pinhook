import random
import re
import pinhook.plugin as p

"""
A plugin to throw a pizza party
"""


def generate():
    big = random.randint(5, 20)
    small = random.randint(5, 20)
    return ''.join(["🍕" * big, "🎉" * small]);

@p.listener('pizza')
def pizza(msg):
    if re.search('pizza party', msg.text, re.I | re.M):
        return p.message(generate())

@p.register('!pp')
@p.register('!party')
@p.register('!pizzaparty')
def party(msg):
    if msg.arg:
        random.seed(msg)
    return p.message(generate())
