#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-----------------------------------------------------------#
#                   Create a new bundle                     #
#-----------------------------------------------------------#

from os.path import join as joinpath
from ..services import app, log, settings, colors
from ..helpers import create

# Command Entry Point
def run():
    log.header('Create a new bundle.')

    username = log.input_text('Enter your GitHub username: ')
    project_key = log.input_text('Enter the name of the bundle (repository name): ')
    project_name = log.input_text('Enter the bundle title: ')

    result_copy = create.bundle({
        'username': username,
        'project_key': project_key,
        'project_name': project_name
    })

    if not result_copy:
        log.danger('This bundle already exists!')
        app.exit()

    to_path = joinpath(settings.path_laravel_bundles, username, project_key)

    log.framed_list([
        colors.okgreen('Template-based bundle successfully created!'),
        '',
        colors.okgreen('Bundle name: ') + project_name,
        colors.okgreen('Bundle-Key: ') + username + '/' + project_key,
        colors.okgreen('Local path: ') + to_path
    ])