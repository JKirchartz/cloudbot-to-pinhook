import pinhook.plugin as p
import subprocess
import sys

"""
A plugin to run commands on a remote server
"""

HOST="b"

def ssh(COMMAND):
    # Ports are handled in ~/.ssh/config since we use OpenSSH
    ssh = subprocess.Popen(" ".join(["ssh", HOST, "\"", COMMAND, "\""]),
            shell=True,
            stdout=subprocess.PIPE)
    result = ssh.stdout.read()
    if result == "":
        return "no output"
    else:
        return result.decode('utf-8')

@p.register('!addlink')
@p.ops('!addlink', 'add a link')
def addlink(msg):
    return p.message(ssh('~/addlink.sh ' + msg.arg))

@p.register('!twtxt')
@p.ops('!twtxt', 'post to twtxt')
def twtxt(msg):
    return p.message(ssh('~/twtweet.sh ' + msg.arg))
