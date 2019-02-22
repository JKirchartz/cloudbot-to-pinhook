#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import pinhook.plugin
import re
from urllib.request import urlopen

@pinhook.plugin.listener('titler')
def titler(msg):
  try:
    url = re.search("(?P<url>https?://\S+)", msg.text).group("url")
    if url:
      print('found url:' + url)
      page = str(urlopen(url).read())
      title = re.search("<title[^>]*?>(?P<title>[^<]+)</title>", page).group("title")
      if title:
        print('found title:' + title)
        return pinhook.plugin.message(title)
  except Exception as e:
    # ignore errors
    # print(e)
    return
