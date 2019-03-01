import pinhook.plugin as p, re
import urllib.request as http
import json
from random import choice

"""
A plugin for playing Jeopardy!
"""

# TODO: make a score-keeping system
jeopardy_tmp = {}
alex = {
        "ask": ["Here is the clue", "Here is your clue"],
        "correct": ["To be sure", "That is correct", "Correct"],
        "incorrect": ["I'm sorry, that is incorrect"]
        }
formquestion_rex = re.compile("(?:\b(who|what|where|when|why|how)\b\s+\b(is|was|are|were)\b\s+)?(?P<answer>.*)\??")

def getquestion(msg):
    api = http.urlopen("http://jservice.io/api/random").read().strip()
    data = json.loads(api)
    if data:
        jeopardy_tmp[(msg.nick, msg.channel)] = {}
        jeopardy_tmp[(msg.nick, msg.channel)]["question"] = data[0]["question"]
        jeopardy_tmp[(msg.nick, msg.channel)]["answer"] = data[0]["answer"]
        jeopardy_tmp[(msg.nick, msg.channel)]["category"] = data[0]["category"]["title"]
        jeopardy_tmp[(msg.nick, msg.channel)]["points"] = data[0]["value"]
        print(jeopardy_tmp[(msg.nick, msg.channel)])
        return {"cat": data[0]["category"]["title"], "q": data[0]["question"]}

@p.listener('jeopardy_answer')
def jeopardyanswer(msg):
    if (msg.nick, msg.channel) in jeopardy_tmp:
        answer = jeopardy_tmp[(msg.nick, msg.channel)]["answer"]
        guess = re.search(formquestion_rex, msg.text).group("answer")
        print("Guess: {}, Answer: {}".format(guess, answer))
        if answer and guess and (answer.lower() == guess.lower() or guess.lower() in answer.lower()):
            msg.privmsg(msg.channel, "{}, {}. You get {} points.".format(choice(alex["correct"]), msg.nick, jeopardy_tmp[(msg.nick, msg.channel)]["points"]))
        else:
            msg.privmsg(msg.channel, "{}, {}.".format(choice(alex["incorrect"]), msg.nick))
            msg.privmsg(msg.channel, "the correct answer is {}.".format(answer))
        del jeopardy_tmp[(msg.nick, msg.channel)]


@p.register('!jeopardy', 'Ask a Jeopardy Question')
def jeopardy(msg):
    output = getquestion(msg)
    if output:
        return p.message("The Category is '{}'. {}: {}".format(output["cat"], choice(alex["ask"]), output["q"]))
    else:
        return p.message("An error occurred attempting to find a question.")
