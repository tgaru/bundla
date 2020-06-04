#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-----------------------------------------------------------#
#                  Useful Features Module                   #
#-----------------------------------------------------------#

import sys
from pyparsing import *
from . import log

# Abort a program
def exit():
    log.danger('Execution aborted.')
    sys.exit()

# Get the value of a dictionary parameter
def dict_param(params, dct, default = False):
    for l in params.split('.'):
        if not l in dct:
            return default

        dct = dct[l]

    return dct

# Removing color from text
text_without_color = lambda s: Suppress(Combine(Literal('\x1b') + '[' + Optional(delimitedList(Word(nums), ';')) + oneOf(list(alphas)))).transformString(s)

# ljust for colored text
def color_text_ljust(s, width):
    needed = width - len(text_without_color(s))
    if needed > 0: return s + ' ' * needed
    else: return s