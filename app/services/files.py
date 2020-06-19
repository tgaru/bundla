#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------#
#               Module for working with files                #
# -----------------------------------------------------------#

import os
import shutil


# Save text to file
def save(file, mode, text):
    try:
        f = open(file, mode)
        f.write(text)
        f.close()
        return True
    except IOError:
        return False


# Get text from file
def load(file):
    try:
        f = open(file)
        return f.read()
    except IOError:
        return False


# Delete file
def delete_file(path):
    if os.path.isfile(path):
        os.remove(path)


# Delete folder
def delete_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path)


# Replace text in file
def file_replacements(path, replace_dict):
    if os.path.isfile(path):
        text = load(path)
        for search in replace_dict:
            text = text.replace(search, replace_dict[search])
        save(path, 'w', text)
