#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-----------------------------------------------------------#
#                Install a specific bundle                  #
#-----------------------------------------------------------#

import os, json
from git import Repo
from os.path import join as joinpath
from ..services import app, log, files, settings, converter, downloader, configurator
from ..helpers import install

# Command Entry Point
def run(bundle_name_input):
    # Setting
    input_slit = bundle_name_input.split(':')
    bundle_key = input_slit[0]
    bundle_version_spec = input_slit[1] if len(input_slit) == 2 else None
    bundle_path = joinpath(settings.path_laravel_bundles, bundle_key)
    bundle_yml_path = joinpath(bundle_path, 'bundle.yml')
    bundle_github_url = 'https://github.com/' + bundle_key

    # Getting a bundle
    if not os.path.exists(bundle_path) and \
            not downloader.git(bundle_github_url, bundle_version_spec, bundle_path) and \
            not os.path.isfile(bundle_yml_path):
        log.danger('Laravel bundle with this name does not exist.')
        app.exit()

    # Import bundle config
    bundle_config = converter.yaml2dict(files.load(bundle_yml_path))

    # Bundle config validation check
    install.check_config(bundle_config)

    log.header('Laravel bundle [' + bundle_key + ']. ' + bundle_config['title'])

    # Check for files and folders
    if os.path.isfile('.env') or os.path.isfile('.env.example') or os.path.isfile('docker-compose.yml') or os.path.exists('src/'):
        log.warning('Application files and/or folders (.env, .env.example, docker-compose.yml, src/) already exist.')
        if not log.confirm_input('DELETE THEM AND CONTINUE INSTALLATION?'): app.exit()

        # Removing an old bundle
        os.system('docker-compose down >/dev/null 2>&1')
        if os.path.isfile('.env'): files.delete_file('.env')
        if os.path.isfile('.env.example'): files.delete_file('.env.example')
        if os.path.isfile('docker-compose.yml'): files.delete_file('docker-compose.yml')
        if os.path.exists('src/'): files.delete_folder('src/')

        log.info('Files and folders deleted successfully!')

    # Download Laravel
    if not downloader.git(bundle_config['repository-url'], bundle_config['repository-version'], 'src'):
        log.danger('The repository is not cloned.')
        app.exit()

    # Configs Generation
    configs_docker_compose = configurator.create_docker_compose_configs(bundle_config)
    config_composer = configurator.create_composer_config(bundle_config)
    config_npm = configurator.create_npm_config(bundle_config)

    # Save configs
    install.copy_file(joinpath(bundle_path, 'composer.json'), 'src/composer.json', True)
    install.copy_file(joinpath(bundle_path, 'package.json'), 'src/package.json', True)
    install.save_file('.env', 'x', converter.list2env(configs_docker_compose['docker_compose_env']))
    install.copy_file('.env', '.env.example')
    install.save_file('docker-compose.yml', 'x', converter.dict2yaml(configs_docker_compose['docker_compose_yml']))
    install.save_file('src/.env', 'x', converter.list2env(configs_docker_compose['laravel_env']))
    install.copy_file('src/.env', 'src/.env.example')
    if config_composer: install.save_file('src/composer.json', 'w', json.dumps(config_composer, indent=4))
    if config_npm: install.save_file('src/package.json', 'w', json.dumps(config_npm, indent=4))

    # First start
    install.first_start(bundle_config)

    # Final actions
    log.info('The project was successfully created and launched!')

    # Display modules data
    configurator.print_modules_output(bundle_config)