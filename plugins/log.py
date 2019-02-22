#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import pinhook.plugin

output =[]
keeplines = 10

characters = [];

def char(nick):
  global characters
  for char in characters:
    if char.nick == nick:
      break
    else:
      characters.push(dict(nick=nick, img=randomCharacter()))


@pinhook.plugin.listener('ears')
def ears(msg):
  global output
  global keeplines
  output.append(dict(nick=msg.nick, text=msg.text))
  # only keep last X lines
  if len(output) >= keeplines:
    output.pop(0)

@pinhook.plugin.register('!log', 'check ' + str(keeplines) + ' lines of backlog')
def log(msg):
  global output
  comic = list()
  for line in output:
    comic.push(dict(
      nick=line.nick,
      text=line.text,
      char=char(line.nick)
    ))
  return pinhook.plugin.message(' | '.join(output))
