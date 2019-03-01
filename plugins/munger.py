#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 jkirchartz <me@jkirchartz.com>
#
# Distributed under terms of the NPL (Necessary Public License) license.

import pinhook.plugin
from datetime import datetime
import json
import random
import re

mcache = dict()
buffer_size = 1
usage = "!m[unge] [ubbi|circle|flip|vaporwave|mock|chef|russian] -- munges previous line, or provided text"

# spongemock.py
# author: Noah Krim
# email: nkrim62@gmail.com

def mock(text, diversity_bias=0.5, random_seed=None):
	# Error handling
	if diversity_bias < 0 or diversity_bias > 1:
		raise ValueError('diversity_bias must be between the inclusive range [0,1]')
	# Seed the random number generator
	random.seed(random_seed)
	# Mock the text
	out = ''
	last_was_upper = True
	swap_chance = 0.5
	for c in text:
		if c.isalpha():
			if random.random() < swap_chance:
				last_was_upper = not last_was_upper
				swap_chance = 0.5
			c = c.upper() if last_was_upper else c.lower()
			swap_chance += (1-swap_chance)*diversity_bias
		out += c
	return out

# end spongemock

def chefalize(phrase):
    """convert HTML to Swedish Chef-speak
    Cribbed from Mark Pilgrim's "Dive Into Python" - http://www.diveintopython.net/html_processing/index.html -
    code at http://www.siafoo.net/snippet/133
   which was based on the classic chef.x, copyright (c) 1992, 1993 John Hagerman
   """
    subs = ((r'a([nu])', r'u\1'),
        (r'A([nu])', r'U\1'),
        (r'a\B', r'e'),
        (r'A\B', r'E'),
        (r'en\b', r'ee'),
        (r'\Bew', r'oo'),
        (r'\Be\b', r'e-a'),
        (r'\be', r'i'),
        (r'\bE', r'I'),
        (r'\Bf', r'ff'),
        (r'\Bir', r'ur'),
        (r'(\w*?)i(\w*?)$', r'\1ee\2'),
        (r'\bow', r'oo'),
        (r'\bo', r'oo'),
        (r'\bO', r'Oo'),
        (r'the', r'zee'),
        (r'The', r'Zee'),
        (r'th\b', r't'),
        (r'\Btion', r'shun'),
        (r'\Bu', r'oo'),
        (r'\BU', r'Oo'),
        (r'v', r'f'),
        (r'V', r'F'),
        (r'w', r'w'),
        (r'W', r'W'),
        (r'([a-z])[.]', r'\1.  Bork Bork Bork!'))


    for fromPattern, toPattern in subs:
        phrase = re.sub(fromPattern, toPattern, phrase)

    return phrase


def vaporwave(text):
    output = ""
    for c in list(text):
        a = ord(c)
        if a >= 33 and a <= 126:
            output += chr( (a - 33) + 65281 )
        else:
            output += c
    return output


unicode_offsets = {
        "cursive": {"upper": 119951, "lower": 119945},
        "circle": {"upper": 9333, "lower": 9327}
        }

def unicode_offset(text, fun):
    output = ""
    for c in list(text):
        a = ord(c)
        if a > 64 and a < 91:
            output += chr( a + unicode_offsets[fun]["upper"] )
        elif a > 96 and a < 123:
            output += chr( a + unicode_offsets[fun]["lower"] )
        else:
            output += c
    return output

json_mungers = {}

json_mungers['russian'] = {
	"A": ["Д"],
	"B": ["Б", "Ъ", "Ь"],
	"C": ["Ҫ"],
	"E": ["Ԑ", "Є", "Э"],
	"F": ["Ӻ", "Ғ"],
	"H": ["Њ", "Ҥ", "Ӊ", "Ң"],
	"I": ["Ї"],
	"K": ["Қ", "Ҡ", "Ҝ", "Ԟ"],
	"M": ["Ԡ"],
	"N": ["И", "Ѝ", "Й"],
	"O": ["Ф"],
	"R": ["Я"],
	"T": ["Г", "Ґ", "Ҭ"],
	"U": ["Ц","Џ"],
	"W": ["Ш", "Щ"],
	"X": ["Ӿ", "Ҳ", "Ӽ", "Ж"],
	"Y": ["Ч", "Ұ"]
}

json_mungers['tiny'] = {
  "a":"ᵃ",
  "b":"ᵇ",
  "c":"ᶜ",
  "d":"ᵈ",
  "e":"ᵉ",
  "f":"ᶠ",
  "g":"ᵍ",
  "h":"ʰ",
  "i":"ᶦ",
  "j":"ʲ",
  "k":"ᵏ",
  "l":"ᶫ",
  "m":"ᵐ",
  "n":"ᶰ",
  "o":"ᵒ",
  "p":"ᵖ",
  "q":"ᑫ",
  "r":"ʳ",
  "s":"ˢ",
  "t":"ᵗ",
  "u":"ᵘ",
  "v":"ᵛ",
  "w":"ʷ",
  "x":"ˣ",
  "y":"ʸ",
  "z":"ᶻ",
  "A":"ᴬ",
  "B":"ᴮ",
  "C":"ᶜ",
  "D":"ᴰ",
  "E":"ᴱ",
  "F":"ᶠ",
  "G":"ᴳ",
  "H":"ᴴ",
  "I":"ᴵ",
  "J":"ᴶ",
  "K":"ᴷ",
  "L":"ᴸ",
  "M":"ᴹ",
  "N":"ᴺ",
  "O":"ᴼ",
  "P":"ᴾ",
  "Q":"ᑫ",
  "R":"ᴿ",
  "S":"ˢ",
  "T":"ᵀ",
  "U":"ᵁ",
  "V":"ⱽ",
  "W":"ᵂ",
  "X":"ˣ",
  "Y":"ʸ",
  "Z":"ᶻ",
  "`":"`",
  "~":"~",
  "!":"﹗",
  "@":"@",
  "#":"#",
  "$":"﹩",
  "%":"﹪",
  "^":"^",
  "&":"﹠",
  "*":"﹡",
  "(":"⁽",
  ")":"⁾",
  "_":"⁻",
  "-":"⁻",
  "=":"⁼",
  "+":"+",
  "{":"{",
  "[":"[",
  "}":"}",
  "]":"]",
  ":":"﹕",
  ";":"﹔",
  "?":"﹖",
}

json_mungers['upsidedown'] = {
  'A':'∀',
  'B':'𐐒',
  'C':'Ɔ',
  'E':'Ǝ',
  'F':'Ⅎ',
  'G':'פ',
  'H':'H',
  'I':'I',
  'J':'ſ',

  'L':'˥',
  'M':'W',
  'N':'N',

  'P':'Ԁ',

  'R':'ᴚ',

  'T':'⊥',
  'U':'∩',
  'V':'Λ',


  'Y':'⅄',

  'a':'ɐ',
  'b':'q',
  'c':'ɔ',
  'd':'p',
  'e':'ǝ',
  'f':'ɟ',
  'g':'ƃ',
  'h':'ɥ',
  'i':'ᴉ',
  'j':'ɾ',
  'k':'ʞ',

  'm':'ɯ',
  'n':'u',

  'p':'d',
  'q':'b',
  'r':'ɹ',

  't':'ʇ',
  'u':'n',
  'v':'ʌ',
  'w':'ʍ',



  '1':'Ɩ',
  '2':'ᄅ',
  '3':'Ɛ',
  '4':'ㄣ',
  '5':'ϛ',
  '6':'9',
  '7':'ㄥ',
  '8':'8',
  '9':'6',
  '0':'0',
  '.':'˙',
  ',':'\'',
  '\'':',',
  '"':',,',
  '`':',',
  '<':'>',
'>':'<',
'∴':'∵',
'&':'⅋',
'_':'‾',
'?':'¿',
'!':'¡',
'[':']',
']':'[',
'(':')',
')':'(',
'{':'}',
'}':'{'
}

def munger(text, json_type='russian'):
  output = ""
  json_munger = json_mungers[json_type]
  if json_type == 'russian':
      text = text.upper()
  for c in text:
      if c in json_munger:
          output += random.choice(json_munger[c])
      else:
          output += c
  return output

def munge(text, function='mock'):
  fun = function.lower()
  if fun == 'flip':
      fun = 'upsidedown'
      text = text[::-1]
  if fun == 'chef' or fun == 'swedish':
      return chefalize(text)
  if fun == 'aesthetic' or fun == 'vaporwave':
      return vaporwave(text)
  elif fun == 'ubbi':
      return re.sub(r"([aeiou]+)", r"ub\1", text);
  elif fun == 'mock':
      return mock(text)
  if fun == 'circled':
      return unicode_offset(text, "circle");
  elif fun in unicode_offsets:
      return unicode_offset(text, fun)
  elif fun in json_mungers:
      return munger(text, fun)
  elif fun == "help":
      return usage
  else:
      return " ".join(["no munger named", fun])

@pinhook.plugin.listener('track')
def track(msg):
  if not str(msg.text).startswith(('!', '.', ';', ':')):
      mcache[msg.channel] = str(msg.text)


@pinhook.plugin.register("!m", usage)
@pinhook.plugin.register("!munge", usage)
def munge_command(msg):
  output = ""
  text = msg.arg
  if len(text.split()) >= 2:
        text = text.split()
        output = munge(" ".join(text[1:]), text[0])
  else:
        try:
            if len(text):
                output = munge(mcache[msg.channel], text)
            else:
                output = munge(mcache[msg.channel])
        except KeyError:
            output = "Invalid Munger or Not Enough Messages. Usage: " + usage

  return pinhook.plugin.message(output)

