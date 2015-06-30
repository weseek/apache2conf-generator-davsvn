#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2014. WESEEK, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import json
import fnmatch
from argparse import ArgumentParser
from string import Template
from collections import OrderedDict


def create_argument_parser():
    desc = """This program scans REPOS_ROOT, picks up Subversion repositories,
           and outputs Apache2 configurations for dav-svn to STDOUT."""

    # parse arguments
    parser = ArgumentParser(description=desc)
    parser.add_argument('reposroot_path', metavar='REPOS_ROOT',
                        help='path to the directory ' +
                             'that contains SVN repositories')
    parser.add_argument('--tpl', metavar='TEMPLATE_FILE',
                        help='path to an Apache2 configuration template file')
    parser.add_argument('--tplmap', metavar='TEMPLATE_MAP_FILE',
                        help='path to a JSON file ' +
                             'that specify template mappings')

    return parser


def verify_arguments(args):
    """
    verify arguments

    @param parser: dict of arguments
    """

    # verify option
    if ((args.tpl and args.tplmap) or
            (not args.tpl and not args.tplmap)):
        sys.exit("you must specify only either one of --tpl and --tplmap")

    # verify template file
    if (args.tpl and not os.path.exists(args.tpl)):
        sys.exit("'{0}' is not exists".format(args.tpl))
    if (args.tpl and not os.path.isfile(args.tpl)):
        sys.exit("'{0}' is not a file".format(args.tpl))

    # verify template file
    if (args.tplmap and not os.path.exists(args.tplmap)):
        sys.exit("'{0}' is not exists".format(args.tpl))
    if (args.tplmap and not os.path.isfile(args.tplmap)):
        sys.exit("'{0}' is not a file".format(args.tpl))

    # verify reposroot_path
    reposroot_path = args.reposroot_path
    if (not os.path.exists(reposroot_path)):
        sys.exit("'{0}' is not exists".format(reposroot_path))
    elif (not os.path.isdir(reposroot_path)):
        sys.exit("'{0}' is not a directory".format(reposroot_path))


def main():
    # parse arguments
    parser = create_argument_parser()

    args = parser.parse_args()

    # verify
    # if there is invalid args, sys.exit will be called.
    verify_arguments(args)

    # create default template mappings
    tplmap = {"*": args.tpl}
    # custom template mappings from JSON (using OrderedDict)
    if (args.tplmap):
        with open(args.tplmap) as f:
            tplmap = json.loads(f.read(), encoding="utf-8",
                                object_pairs_hook=OrderedDict)

    # detect
    repos_info_list = detect_repos(args.reposroot_path)

    # print
    print_conf(repos_info_list, tplmap)


def detect_repos(reposroot_path):
    '''
    return a list of ReposInfo instances
    '''

    repos_info_list = []

    # judge root
    reposroot_abs_path = os.path.abspath(reposroot_path)
    if (judge_svn_repos(reposroot_abs_path)):
        repos_info_list.append(reposroot_abs_path)
        return repos_info_list

    # process recursively
    exclude_dirs = set()
    for dirpath, dirnames, filenames in (
            os.walk(reposroot_path, followlinks=True)):

        # skip exlude_dirs contains
        if (dirpath in exclude_dirs):
            dirnames.clear()
            continue

        for dirname in dirnames:
            abspath = os.path.join(dirpath, dirname)

            # evaluate
            isSvnRepos = judge_svn_repos(abspath)

            if (isSvnRepos):
                info = ReposInfo()
                info.abspath = abspath
                info.relpath = os.path.relpath(abspath, start=reposroot_path)
                info.basename = dirname

                repos_info_list.append(info)
                # modify dirnames (in order not to os.walk subdirectories)
                exclude_dirs.add(abspath)

    return repos_info_list


def judge_svn_repos(path):
    '''
    return True if 'path' is a SVN repository
    '''

    path_conf = path + os.sep + 'conf'
    path_db = path + os.sep + 'db'
    path_hooks = path + os.sep + 'hooks'
    path_locks = path + os.sep + 'locks'

    return (os.path.isdir(path_conf) and
            os.path.isdir(path_db) and
            os.path.isdir(path_hooks) and
            os.path.isdir(path_locks))


def print_conf(repos_info_list, tplmap):
    """
    print Apache2 Configuration to stdout

    @param repos_info_list: list of ReposInfo instances
    @param tplmap: template map
            key: glob expression
            value: template path
    @type tplmap: dict
    """

    for repos_info in repos_info_list:
        # pattern matching
        for pattern, tpl_path in tplmap.items():
            if fnmatch.fnmatch(repos_info.abspath, pattern):
                print(generate_conf_unit(tpl_path, repos_info))
                break


def generate_conf_unit(tplpath, repos_info):
    """
    @param tplpath: template path
    @param repos_info: ReposInfo
    """

    # open template
    with open(tplpath) as tpl:
        t = Template(tpl.read())
        # substitute
        return t.safe_substitute(repos_info.__dict__)


class ReposInfo:
    abspath = None
    """absolute path of repository"""

    relpath = None
    """elative path from reposroot_path"""

    basename = None
    """basename of repository"""


if __name__ == "__main__":
    main()
