#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------#
#                     Entry Point Helper                     #
# -----------------------------------------------------------#

import os
from ..services import log, settings, files
from ..commands import install, help, createbundle, createmodule


# Execute method
def dispatch(value, input_params, data):
    return value(input_params, data)


# Run command: bundla help/h
def help_command(input_params, data):
    help.run()


# Run command: bundla install/i
def install_command(input_params, data):
    install.run(input_params[2])


# Run command: bundla create module/bundle
def create_command(input_params, data):
    if input_params[2] == 'bundle' or input_params[2] == 'b':
        createbundle.run()
    elif input_params[2] == 'module' or input_params[2] == 'm':
        createmodule.run()
    else:
        log.danger('Allowed values: "bundle" and "module"')


# Run shell command
def run_shell_command(input_params, data):
    os.system(data + ' '.join([''] + input_params[2:]))


# Run the command in the container "app"
def run_app_command(input_params, data):
    run_shell_command(input_params, 'docker-compose exec app sh -c "' + input_params[2].replace('"', '\\"') + '"')


# Clear Bundla vendor
def clear_vendor_command(input_params, data):
    files.delete_folder(settings.path_vendor)
    log.info('Delete the folder ' + settings.path_vendor)
