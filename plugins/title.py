#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import pinhook.plugin
import re
from pyquery import PyQuery

@pinhook.plugin.listener('title')
def title(msg):
  try:
    url = re.search("(?P<url>https?://[^\s]+)", msg.text).group("url")
    if url:
      page = PyQuery(url)
      return pinhook.plugin.message(page("title").text())
  except:
    # ignore errors
    return
