#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

''' The following function is just a demonstration of a function that
could be used within the process() function. It removes HTML tags.'''

import re

TAG_RE = re.compile(r'<[^>]+>')


def remove(text):
    return TAG_RE.sub('', text)
