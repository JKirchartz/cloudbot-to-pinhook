import pinhook.plugin as p

"""
An ejector seat for your channel
"""

@p.register('!eject', "The Ejector Seat. Usage: !eject [nick]")
def eject(msg):
    if msg.arg != "":
        output = msg.arg
    else:
        output = msg.nick
    return p.action("pulls the lever on %s's ejector seat" % output);
