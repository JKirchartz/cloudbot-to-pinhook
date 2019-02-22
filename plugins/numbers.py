import pinhook.plugin as p
import urllib.request as http

"""
A plugin for monitoring a counting channel and posting updates to counting-meta
Can also find arbitrary & random numbers
"""


def get_number(num):
    trivia = http.urlopen("http://numbersapi.com/" + str(num) + "/trivia?default=false").read().strip()
    math = http.urlopen("http://numbersapi.com/" + str(num) + "/math?default=false").read().strip()
    if trivia !=  "false":
        return trivia.decode("utf-8")
    if math != "false":
        return math.decode("utf-8")

#@p.listener('numbers')
#def numbers(msg):
#    if msg.channel == "#counting" and msg.text.strip().isdigit():
#        output = get_number(msg.text.strip())
#        if output and output != "false":
#            msg.privmsg('#counting-meta', "Interesting Number Detected: " + str(output))

@p.register('!num', 'Get interesting facts about a number. Usage: !num [int|random]')
def num(msg):
    output = get_number(msg.arg.strip())
    if output and output != "false":
        return p.message(str(output))
    else:
        return p.message("Sorry, I can't find anything interesting about " + msg.arg.strip() + ".")
