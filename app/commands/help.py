#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------#
#                         Print help                         #
# -----------------------------------------------------------#

from ..services import log, colors


# Command Entry Point
def run():
    log.framed_text('Bundla help')
    log.columns([
        [colors.okgreen('bundla i <bundle-key>'), 'Install Laravel bundle'],
        [colors.okgreen('bundla create bundle'), 'Create a new bundle based on a template'],
        [colors.okgreen('bundla create module'), 'Create a new module based on a template'],
        [colors.okgreen('bundle app "<shell-command>"'), 'Run the command inside the container "app"'],
        [colors.okgreen('bundla help'), 'Bundla Command List'],
        [colors.okgreen('bundla app'), 'Analogue [docker-compose exec app sh]'],
        [colors.okgreen('bundla ps'), 'Analogue [docker-compose ps]'],
        [colors.okgreen('bundla up'), 'Analogue [docker-compose up -d]'],
        [colors.okgreen('bundla down'), 'Analogue [docker-compose down]'],
        [colors.okgreen('bundla build'), 'Analogue [docker-compose build]'],
        [colors.okgreen('bundla restart'), 'Analogue [docker-compose restart]'],
        [colors.okgreen('bundla stop'), 'Analogue [docker-compose stop]'],
        [colors.okgreen('bundla start'), 'Analogue [docker-compose start]'],
    ])
    print('')
    print('GitHub Bundla: https://github.com/tgaru/bundla')
    print('')
