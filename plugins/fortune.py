import pinhook.plugin as p
import subprocess

"""
A plugin to get a fortune cookie
"""

@p.register('!fortune', 'Get a fortune cookie')
def fortune(msg):
    fortune = subprocess.Popen(["fortune", "%s" % msg.arg],
            shell=False,
            stdout=subprocess.PIPE)
    return p.message(fortune.stdout.read().decode('utf-8'))
