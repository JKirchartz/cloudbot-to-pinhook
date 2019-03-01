import pinhook.plugin as p
import random

"""
A plugin for monitoring a channel and finding Numberwangs.
"""

digit_count=0
wang_count=0
@p.listener('numberwang')
def numberwang(msg):
    global digit_count
    global wang_count
    if msg.channel == "#counting-anarchy" and msg.text.strip().isdigit():
        digit_count = digit_count + 2
        if digit_count > random.randint(3,20) and wang_count < 1:
            wang_count = wang_count + 1
            return p.message("CONGRATS {}! THAT'S NUMBERWANG!".format(msg.nick))
        else:
            if random.randint(0, 10) == 1:
                wang_count = 0
    else:
        digit_count = digit_count - 1

