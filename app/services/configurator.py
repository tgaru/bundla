#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------#
#                  Config generation module                  #
# -----------------------------------------------------------#

import os
import json
from os.path import join as joinpath
from . import app, log, files, settings, converter, downloader, colors


# Creating configs for Laravel and Docker Сompose based on the bundle config.
def create_docker_compose_configs(bundle_config):
    configs = {
        'laravel_env': converter.env2list(
            files.load(joinpath(settings.path_configs, 'laravel.default.env'))
        ),  # src/.env
        'docker_compose_env': [],  # .env
        'docker_compose_yml': {  # docker-compose.yml
            'version': '3',
            'services': {},
            'volumes': {}
        }
    }

    log.info('Generation of configuration files...')

    # Processing each Docker Compose module.
    for module_key in bundle_config['docker-compose']['modules']:
        module_version_spec = bundle_config['docker-compose']['modules'][module_key]
        module_path = joinpath(settings.path_docker_compose_modules, module_key)

        log.primary('Adding module: [' + module_key + ' ' + module_version_spec + ']')

        if not os.path.exists(module_path) and \
                not downloader.git(
                    'https://github.com/' + module_key,
                    module_version_spec,
                    joinpath(settings.path_docker_compose_modules, module_key)
                ):
            log.danger('Failed to load remote module.')
            app.ex()

        module_config = get_module_config(module_key)

        # Generating .env configurations for Laravel
        result = gen_laravel_config(module_config, module_key)
        if result:
            if len(configs['laravel_env']): configs['laravel_env'].append([])
            configs['laravel_env'] += result

        # Generating .env configurations for Docker Compose
        result = gen_docker_compose_config(module_config, module_key)
        if result:
            if len(configs['docker_compose_env']): configs['docker_compose_env'].append([])
            configs['docker_compose_env'] += result

        # Docker-compose.yml services generation for Docker Compose
        result = gen_docker_compose_services_config(module_config)
        if result:
            configs['docker_compose_yml']['services'] = {**configs['docker_compose_yml']['services'], **result}

        # Docker-compose.yml volumes generation for Docker Compose
        result = gen_docker_compose_volumes_config(module_config)
        if result:
            configs['docker_compose_yml']['volumes'] = {**configs['docker_compose_yml']['volumes'], **result}

    return configs


# Creating a config for Composer based on the bundle config.
def create_composer_config(bundle_config):
    composer = json.loads(files.load('src/composer.json'))
    if 'composer' not in bundle_config:
        return False

    if not app.dict_param('composer.expansion', bundle_config, True):
        composer['require'] = {}
        composer['require-dev'] = {}

    if 'require' not in composer:
        composer['require'] = {}
    if 'require-dev' not in composer:
        composer['require-dev'] = {}

    # Generate the "require" section
    composer_require = app.dict_param('composer.require', bundle_config, {})
    if len(composer_require):
        composer['require'] = {**composer['require'], **composer_require}

    # Generate the "require-dev" section
    composer_require_dev = app.dict_param('composer.require-dev', bundle_config, {})
    if len(composer_require_dev):
        composer['require-dev'] = {**composer['require-dev'], **composer_require_dev}

    return composer


# Creating a config for NPM based on the bundle config.
def create_npm_config(bundle_config):
    npm = json.loads(files.load('src/package.json'))
    if 'npm' not in bundle_config:
        return False

    if not app.dict_param('npm.expansion', bundle_config, True):
        npm['dependencies'] = {}
        npm['devDependencies'] = {}

    if 'dependencies' not in npm:
        npm['dependencies'] = {}
    if 'devDependencies' not in npm:
        npm['devDependencies'] = {}

    # Generate the "dependencies" section
    npm_dependencies = app.dict_param('npm.dependencies', bundle_config, {})
    if len(npm_dependencies):
        npm['dependencies'] = {**npm['dependencies'], **npm_dependencies}

    # Generate the "devDependencies" section
    npm_dev_dependencies = app.dict_param('npm.devDependencies', bundle_config, {})
    if len(npm_dev_dependencies):
        npm['devDependencies'] = {**npm['devDependencies'], **npm_dev_dependencies}

    return npm


# Get the module config
def get_module_config(module_key):
    module_file = joinpath(settings.path_docker_compose_modules, module_key, 'module.yml')

    if not os.path.isfile(module_file):
        log.danger('Error. Docker Compose module with this name does not exist.')
        app.ex()

    return converter.yaml2dict(files.load(module_file))


# Display modules data
def print_modules_output(bundle_config):
    texts = []
    modules = app.dict_param('docker-compose.modules', bundle_config)

    # Processing each Docker Compose module.
    for module_key in modules:
        module_config = get_module_config(module_key)
        module_print = app.dict_param('print', module_config)

        if not module_print:
            continue

        texts.append(colors.header('[' + module_key + ']'))
        for text in module_print:
            texts.append(colors.okgreen(text))
        texts.append('')

    log.framed_list(texts)


# Generating .env configurations for Laravel
def gen_laravel_config(module_config, module_key):
    env_laravel = app.dict_param('env.laravel', module_config, {})

    if not len(env_laravel):
        return False

    result = [
        ['# ' + module_key]
    ]

    for p in env_laravel:
        result.append([p, env_laravel[p]])

    return result


# Generating .env configurations for Docker Compose
def gen_docker_compose_config(module_config, module_key):
    env_docker_compose = app.dict_param('env.docker-compose', module_config, {})

    if not len(env_docker_compose):
        return False

    result = [
        ['# For the service [' + module_key + ']']
    ]

    for p in env_docker_compose:
        result.append([p, env_docker_compose[p]])

    return result


# Docker-compose.yml services generation for Docker Compose
def gen_docker_compose_services_config(module_config):
    if 'service' in module_config:
        return module_config['service']

    return {}


# Docker-compose.yml volumes generation for Docker Compose
def gen_docker_compose_volumes_config(module_config):
    if 'volume' in module_config:
        return module_config['volume']

    return {}
