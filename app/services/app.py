#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------#
#                   Useful Features Module                   #
# -----------------------------------------------------------#

import sys
from pyparsing import *
from . import log


# Abort a program
def ex():
    log.danger('Execution aborted.')
    sys.exit()


# Get the value of a dictionary parameter
def dict_param(params, dct, default=False):
    for param in params.split('.'):
        if param not in dct:
            return default

        dct = dct[param]

    return dct


# Removing color from text
def text_without_color(text):
    return Suppress(
        Combine(
            Literal('\x1b') + '[' + Optional(delimitedList(Word(nums), ';')) + oneOf(list(alphas))
        )
    ).transformString(text)


# ljust for colored text
def color_text_ljust(s, width):
    needed = width - len(text_without_color(s))
    if needed > 0:
        return s + ' ' * needed
    else:
        return s
