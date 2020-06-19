#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------#
#                 Application configuration                  #
# -----------------------------------------------------------#

import sys
from os.path import join as joinpath, expanduser

app_console_prefix = '[Bundla] '

path_global = joinpath(expanduser("~"), '.bundla/')
# path_global = sys.path[0] # DEBUG
path_vendor = joinpath(path_global, 'vendor/')
path_configs = joinpath(path_global, 'configs/')
path_laravel_bundles = joinpath(path_vendor, 'bundles/')
path_docker_compose_modules = joinpath(path_vendor, 'modules/docker-compose/')
