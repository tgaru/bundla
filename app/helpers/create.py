#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------#
#                 Create bundle/module Helper                #
# -----------------------------------------------------------#

import shutil
from os.path import join as joinpath
from ..services import files, settings


# Copy template
def _copy_template(from_path, to_path):
    try:
        shutil.copytree(from_path, to_path)
    except FileExistsError:
        return False

    return True


# Create bundle
def bundle(params):
    from_path = joinpath(settings.path_configs, 'templates/bundle/')
    to_path = joinpath(settings.path_laravel_bundles, params['username'], params['project_key'])
    result = _universal_method(from_path, to_path, params)
    if not result: return False

    files.file_replacements(joinpath(to_path, 'bundle.yml'), {
        '<bundle-title>': '"' + params['project_key'] + '"'
    })

    return True


# Create module
def module(params):
    from_path = joinpath(settings.path_configs, 'templates/module/')
    to_path = joinpath(settings.path_docker_compose_modules, params['username'], params['project_key'])

    return _universal_method(from_path, to_path, params)


# Create module/bundle universal method
def _universal_method(from_path, to_path, params):
    copy_result = _copy_template(from_path, to_path)

    if not copy_result:
        return False

    files.file_replacements(joinpath(to_path, 'README.md'), {
        '{{name}}': params['project_name'],
        '{{key}}': params['username'] + '/' + params['project_key']
    })

    return True
