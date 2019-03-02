import pinhook.plugin as p, re
import urllib.request as http
import json
import fuzzyset
from random import choice

"""
A plugin for playing Jeopardy!
"""

# TODO: make a score-keeping system
jeopardy_tmp = {}
alex = {
        "ask": ["Here is the clue", "Here is your clue", "The answer is"],
        "correct": ["To be sure", "That is correct", "Correct", "That's right"],
        "incorrect": ["I'm sorry, that is incorrect", "That's not it", "Good guess", "Close"],
        "correction": ["I think you mean", "Actually, the correct answer is", "The correct answer is"]
        }
formquestion_rex = re.compile(r'(?:\b(who|what|where|when|why|how)\b\s+\b(is|was|are|were)\b\s+)?(?P<answer>.*)\??')
html = re.compile(r'<[^>]+>')


def compare(guess, answer):
    a = fuzzyset.FuzzySet()
    a.add(answer)
    metric = a.get(guess)
    tally = 0
    if metric:
        for item in metric:
            tally += item[0]
        average = tally / len(metric)
        if average > 0.3:
            return True

def getquestion(msg):
    api = http.urlopen("http://jservice.io/api/random").read().strip()
    data = json.loads(api)
    if data:
        jeopardy_tmp[(msg.nick, msg.channel)] = {}
        jeopardy_tmp[(msg.nick, msg.channel)]["question"] = data[0]["question"]
        jeopardy_tmp[(msg.nick, msg.channel)]["answer"] = re.sub(html, '', data[0]["answer"])
        jeopardy_tmp[(msg.nick, msg.channel)]["category"] = data[0]["category"]["title"]
        jeopardy_tmp[(msg.nick, msg.channel)]["points"] = data[0]["value"]
        return {"cat": data[0]["category"]["title"], "q": data[0]["question"]}

@p.listener('jeopardy_answer')
def jeopardyanswer(msg):
    if (msg.nick, msg.channel) in jeopardy_tmp:
        answer = jeopardy_tmp[(msg.nick, msg.channel)]["answer"]
        guess = re.search(formquestion_rex, msg.text)
        if guess:
            guess = guess.group("answer")
        else:
            guess = msg.text
        if answer and guess and (compare(guess, answer) or answer.lower() == guess.lower()):
            points = jeopardy_tmp[(msg.nick, msg.channel)]["points"]
            if points:
                msg.privmsg(msg.channel, "{}, {}. You get {} points.".format(choice(alex["correct"]), msg.nick, points))
            else:
                msg.privmsg(msg.channel, "{}, {}. It's {}.".format(choice(alex["correct"]), msg.nick, answer))
        else:
            msg.privmsg(msg.channel, "{}, {}. {}: {}.".format(choice(alex["incorrect"]), msg.nick,choice(alex["correction"]), answer))
        del jeopardy_tmp[(msg.nick, msg.channel)]


@p.register('!j', 'Ask a Jeopardy Question')
@p.register('!jeopardy', 'Ask a Jeopardy Question')
def jeopardy(msg):
    output = getquestion(msg)
    if output:
        return p.message("The Category is '{}'. {}: {}".format(output["cat"], choice(alex["ask"]), output["q"]))
    else:
        return p.message("An error occurred attempting to find a question.")
