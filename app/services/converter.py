#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-----------------------------------------------------------#
#                  Data conversion module                   #
#-----------------------------------------------------------#

import yaml

# Convert list to ENV (string).
def list2env(list):
    env = ''

    for line in list:
        line_length = len(line)

        if line_length == 2: env += str(line[0]) + '=' + str(line[1])
        elif line_length == 1: env += str(line[0])

        env += '\n'

    return env.strip('\n')

# Convert ENV(string) to list.
def env2list(env):
    lst = []
    lines = env.split('\n')
    for line in lines:
        try:
            data = line.split('=')
            lst.append([data[0], data[1]])
        except Exception as e:
            lst.append([])
    return lst

# Convert dictionary to YAML (string).
def dict2yaml(dct):
    return yaml.dump(dct, sort_keys=False)

# Convert YAML(string) to dictionary.
def yaml2dict(yml):
    return yaml.load(yml, Loader=yaml.FullLoader)