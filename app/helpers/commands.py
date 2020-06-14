#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-----------------------------------------------------------#
#                    Entry Point Helper                     #
#-----------------------------------------------------------#

import os
from ..services import log, settings, files
from ..commands import install, help, createbundle, createmodule

# Execute method
def dispatch(value, input, data):
    return value(input, data)

# Run command: bundla help/h
def help_command(input, data):
    help.run()

# Run command: bundla install/i
def install_command(input, data):
    install.run(input[2])

# Run command: bundla create module/bundle
def create_command(input, data):
    if input[2] == 'bundle' or input[2] == 'b': createbundle.run()
    elif input[2]  == 'module' or input[2]  == 'm': createmodule.run()
    else: log.danger('Allowed values: "bundle" and "module"')

# Run shell command
def run_shell_command(input, data):
    os.system(data)

# Run the command in the container "app"
def run_app_command(input, data):
    run_shell_command(input, 'docker-compose exec app sh -c "' + input[2].replace('"', '\\"') + '"')

# Clear Bundla vendor
def clear_vendor_command(input, data):
    files.delete_folder(settings.path_vendor)
    log.info('Delete the folder ' + settings.path_vendor)
