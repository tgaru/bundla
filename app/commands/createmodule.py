#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------#
#                    Create a new module                     #
# -----------------------------------------------------------#

from os.path import join as joinpath
from ..services import app, log, settings, colors
from ..helpers import create


# Command Entry Point
def run():
    log.header('Create a new module.')

    username = log.input_text('Enter your GitHub username: ')
    project_key = log.input_text('Enter the key name of the module (repository name): ')
    project_name = log.input_text('Enter the name of the module: ')

    result_copy = create.module({
        'username': username,
        'project_key': project_key,
        'project_name': project_name
    })

    if not result_copy:
        log.danger('This module already exists!')
        app.ex()

    to_path = joinpath(settings.path_docker_compose_modules, username, project_key)

    log.framed_list([
        colors.okgreen('Template-based module successfully created!'),
        '',
        colors.okgreen('Module name: ') + project_name,
        colors.okgreen('Module-Key: ') + username + '/' + project_key,
        colors.okgreen('Local path: ') + to_path
    ])
