#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-----------------------------------------------------------#
#                 Bundle and Module Loader                  #
#-----------------------------------------------------------#

import os, collections
from git import Repo
from semver import max_satisfying
from . import app, log, settings

# Download repo
def git(repo_url, repo_version_spec, path):
    if len(repo_url.split('/')) != 5:
        return False

    log.info('Downloading from the repo: ' + str(repo_url) + ' [' + (str(repo_version_spec) if repo_version_spec else 'master') + ']')

    try:
        r = Repo.clone_from(repo_url, path)

        versions_repo = {}
        for tag in r.tags:
            v = str(tag.name.lstrip('ver').lstrip('v'))
            versions_repo[v] = str(tag.name)
        versions_repo = collections.OrderedDict(sorted(versions_repo.items(), reverse=True))

        if len(versions_repo):
            versions_repo_keys = list(versions_repo.keys())
            find_version = versions_repo_keys[0]
            if repo_version_spec:
                find_version = max_satisfying(versions_repo_keys, repo_version_spec, loose=False)

            repo_tag = versions_repo[find_version]
            r.git.checkout(repo_tag)
    except Exception as e:
        log.danger(str(e))
        return False

    return True