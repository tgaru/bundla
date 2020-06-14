#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-----------------------------------------------------------#
#               Install bundle/module Helper                #
#-----------------------------------------------------------#

import os
from ..services import app, log, files

# Bundle config validation check
def check_config(bundle_config):
    check_param(bundle_config, 'version')
    check_param(bundle_config, 'title')
    check_param(bundle_config, 'description')
    check_param(bundle_config, 'repository-url')
    check_param(bundle_config, 'repository-version')

    if str(bundle_config['version']) != '1':
        log.danger('Only version 1 of bundle.yml file is supported.')
        app.exit()

# Bundle config parameter validation check
def check_param(bundle_config, param):
    if not param in bundle_config:
        log.danger('The [' + param + '] parameter is not set for the Laravel bundle.')
        app.exit()

# Run Shell Command
def exec_shell_cmd(command, start_text, error_text):
    if start_text:
        log.info(start_text)

    if os.system(command) != 0:
        if error_text:
            log.danger(error_text)

        app.exit()

# Generated file (save)
def save_file(file_path, flag, data):
    log.info('Generated file: ' + file_path)

    if not files.save(file_path, flag, data):
        log.danger('Can not save file.')
        app.exit()

# Generated/Replacing file (copy)
def copy_file(file_from_path, file_to_path, replace = True):
    print([
        file_to_path,
        os.path.isfile(file_from_path),
        replace,
        not replace,
        not os.path.isfile(file_to_path)
    ])
    if os.path.isfile(file_from_path) and (replace or not replace and not os.path.isfile(file_to_path)):
        log.info('Copy file: ' + file_to_path)
        os.system('cp ' + file_from_path + ' ' + file_to_path)

# Launching containers, initial settings, executing commands
def first_start(bundle_config):
    composer_install = app.dict_param('composer.install', bundle_config, True)
    npm_install = app.dict_param('npm.install', bundle_config, False)

    exec_shell_cmd(
        'docker-compose up -d',
        'Containers launch...',
        'Failed to start containers.'
    )

    exec_in_app_container(
        bundle_config,
        'app-cmd-before',
        'Initial setup of Laravel bundle...',
        'Error in launching additional Laravel bundle commands.'
    )

    if composer_install:
        exec_shell_cmd(
            'docker-compose exec app sh -c "composer install --prefer-dist"',
            'Installing Composer Packages...',
            'Failed to install Composer packages.'
        )

    if npm_install:
        exec_shell_cmd(
            'docker-compose exec app sh -c "npm install"',
            'Installing NPM Packages...',
            'Failed to install NPM packages.'
        )

    exec_in_app_container(
        bundle_config,
        'app-cmd-after',
        'The final setup of the Laravel bundle...',
        'Error in launching additional Laravel bundle commands.'
    )

    exec_shell_cmd(
        'docker-compose exec app sh -c "chmod -R 777 bootstrap/ && chmod -R 777 storage/"',
        None,
        'Directory rights not set.'
    )

    if composer_install:
        exec_shell_cmd(
            'docker-compose exec app sh -c "php artisan key:generate && php artisan config:cache"',
            None,
            'Laravel key is not installed.'
        )

# Run Shell Command in "app" container
def exec_in_app_container(bundle_config, bundla_param, start_text, error_text):
    if start_text:
        log.info(start_text)

    if bundla_param in bundle_config and len(bundle_config[bundla_param]):
        exec_shell_cmd(
            'docker-compose exec app sh -c "' + ' && '.join(bundle_config[bundla_param]).replace('"', '\\"') + '"',
            start_text,
            error_text
        )