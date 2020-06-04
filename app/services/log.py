#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-----------------------------------------------------------#
#                  Console output module                    #
#-----------------------------------------------------------#

from . import app, colors, settings

# Display a message in the log.
def _echo(color, text):
    print(colors.header(settings.app_console_prefix) + color + text + colors.ENDC)

# Generate a string N length from a character.
def _gen(char, lenght):
    string = ''
    for x in range(lenght): string += str(char)
    return string

# Information message
def info(text):
    _echo(colors.OKGREEN, text)

# Warning message
def warning(text):
    _echo(colors.WARNING, text)

# Dangerous message
def danger(text):
    _echo(colors.FAIL, text)

# Neutral message
def primary(text):
    _echo(colors.OKBLUE, text)

# Header message
def header(text):
    _echo(colors.HEADER, text)

# Get text from user
def input_text(question):
    print(colors.header(settings.app_console_prefix) + colors.warning(question), end='')
    try:
        return input()
    except KeyboardInterrupt as e:
        print('')
        app.exit()

# User Confirmation
def confirm_input(question):
    print(colors.header(settings.app_console_prefix) + colors.warning(question) + ' (y/n) [n]: ', end='')

    try:
        result = str(input())
        return True if result == 'yes' or result == 'y' else False
    except KeyboardInterrupt as e:
        print('')
        return False

# Print text in a frame
def framed_text(text):
    length = 12 + len(text)
    center_text = '|      ' + colors.okgreen(text)  + '      |'
    print(
        '\n' +
        '+' + _gen('-', length) + '+' + '\n' +
        '|' + _gen(' ', length) + '|' + '\n' +
        center_text + '\n' +
        '|' + _gen(' ', length) + '|' + '\n' +
        '+' + _gen('-', length) + '+' + '\n'
    )

# Print list in a frame
def framed_list(lst):
    length_lst = len(lst)
    if not length_lst: return False
    if lst[length_lst-1] == '': del lst[length_lst-1]
    length = max(len(app.text_without_color(word)) for word in lst) + 8

    text = '+' + _gen('-', length) + '+' + '\n'
    text +='|' + _gen(' ', length) + '|' + '\n'
    text += ''.join('|    ' + app.color_text_ljust(word, length - 4) + '|\n' for word in lst)
    text += '|' + _gen(' ', length) + '|' + '\n'
    text += '+' + _gen('-', length) + '+' + '\n'

    print(text)

    return True

# Print columns
def columns(lst):
    col_width = max(len(word) for row in lst for word in row) + 2
    for row in lst:
        print(''.join(word.ljust(col_width) for word in row))