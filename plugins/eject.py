import pinhook.plugin as p

"""
A plugin to Wilhelm Scream
"""

@p.register('!eject', "The Ejector Seat. Usage: !eject [nick]")
def eject(msg):
    if msg.arg != "":
        output = msg.arg
    else:
        output = msg.nick
    return p.message("pulls the lever on %s's ejector seat" % output);
