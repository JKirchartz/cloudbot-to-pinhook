import random
import pinhook.plugin as p

"""
A plugin to shake a magic 8 ball vigorously
"""

@p.register('!8ball', 'Ask the magic 8 Ball a question!')
def eightball(msg):
    random.seed(msg)
    answers = [
            "Signs point to yes.",
            "Yes.",
            "Reply hazy, try again.",
            "Without a doubt.",
            "My sources say no.",
            "As I see it, yes.",
            "You may rely on it.",
            "Concentrate and ask again.",
            "Outlook not so good.",
            "It is decidedly so.",
            "Better not tell you now.",
            "Very doubtful.",
            "Yes - definitely.",
            "It is certain.",
            "Cannot predict now.",
            "Most likely.",
            "Ask again later.",
            "My reply is no.",
            "Outlook good.",
            "Don\'t count on it."
            ];
    return p.message(random.choice(answers))
