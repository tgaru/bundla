#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------#
#                        Entry point                         #
# -----------------------------------------------------------#

import sys, os
from app.services import app, log
from app.helpers import commands

# Console Options List
command_list = [
    ['help', {
        'len': 1,
        'def': commands.help_command
    }],
    ['h', {
        'len': 1,
        'def': commands.help_command
    }],
    ['install', {
        'len': 2,
        'def': commands.install_command
    }],
    ['i', {
        'len': 2,
        'def': commands.install_command
    }],
    ['create', {
        'len': 2,
        'def': commands.create_command
    }],
    ['clear', {
        'len': 1,
        'def': commands.clear_vendor_command
    }],
    ['app', {
        'len': 2,
        'def': commands.run_app_command
    }],
    ['app', {
        'len': 1,
        'def': commands.run_shell_command,
        'data': 'docker-compose exec app sh'
    }],
    ['ps', {
        'len': 1,
        'def': commands.run_shell_command,
        'data': 'docker-compose ps'
    }],
    ['up', {
        'len': 1,
        'def': commands.run_shell_command,
        'data': 'docker-compose up -d'
    }],
    ['down', {
        'len': 1,
        'def': commands.run_shell_command,
        'data': 'docker-compose down'
    }],
    ['build', {
        'len': 1,
        'def': commands.run_shell_command,
        'data': 'docker-compose build'
    }],
    ['restart', {
        'len': 0,
        'def': commands.run_shell_command,
        'data': 'docker-compose restart'
    }],
    ['stop', {
        'len': 0,
        'def': commands.run_shell_command,
        'data': 'docker-compose stop'
    }],
    ['start', {
        'len': 0,
        'def': commands.run_shell_command,
        'data': 'docker-compose start'
    }],
]

input_params = sys.argv
params_len = len(input_params) - 1
first_param = input_params[1] if params_len >= 1 else None

try:
    for command in command_list:
        command_name = command[0]
        command_params = command[1]

        if command_name != first_param: continue
        if command_params['len'] and command_params['len'] != params_len: continue

        try:
            command_data = command_params['data']
        except KeyError:
            command_data = None

        commands.dispatch(command_params['def'], input_params, command_data)
        sys.exit()

    log.info('Welcome to Bundla! Enter the "bundla help" to see a list of commands.')
except KeyboardInterrupt as e:
    log.danger(str(e))
    app.ex()
