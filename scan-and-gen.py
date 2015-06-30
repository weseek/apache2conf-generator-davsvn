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

import argparse
import os
import sys
from string import Template


def main():
    # parse arguments
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('reposroot_path', metavar='REPOS_ROOT',
                        help='path to the directory ' +
                             'that contains SVN repositories')

    args = parser.parse_args()

    reposroot_path = args.reposroot_path

    # verify whethere directory or not
    if (not os.path.exists(reposroot_path)):
        sys.exit("directory not exists: " + reposroot_path)
    elif (not os.path.isdir(reposroot_path)):
        sys.exit("'{path}' is not a directory".format(path=reposroot_path))

    # detect
    detected_dict = detect_repos(reposroot_path)

    # print
    print_conf(detected_dict)


def detect_repos(reposroot_path):
    '''
    return a list of dictionary
        that have several informations of the SVN repositories

        abspath:    absolute path of repository
        relpath:    relative path from reposroot_path
        basename:   basename of repository
    '''

    detected_list = []

    # judge root
    reposroot_abs_path = os.path.abspath(reposroot_path)
    if (judge_svn_repos(reposroot_abs_path)):
        detected_list.append(reposroot_abs_path)
        return detected_list

    # process recursively
    exclude_dirs = set([...])
    for dirpath, dirnames, filenames in os.walk(reposroot_path,
                                                followlinks=True):

        # skip exlude_dirs contains
        if (dirpath in exclude_dirs):
            dirnames.clear()
            continue

        for dirname in dirnames:
            abspath = os.path.join(dirpath, dirname)

            # evaluate
            isSvnRepos = judge_svn_repos(abspath)

            if (isSvnRepos):
                relpath = os.path.relpath(abspath, start=reposroot_path)
                detected_list.append({
                    'abspath': abspath,
                    'relpath': relpath,
                    'basename': dirname
                })
                # modify dirnames (in order not to os.walk subdirectories)
                exclude_dirs.add(abspath)

    return detected_list


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


def print_conf(detected_list):
    '''
    print Apache2 Configuration to stdout
    '''

    for repos_info in detected_list:
        print(generate_conf_unit(repos_info))


def generate_conf_unit(repos_info):
    tpl = open("template-examples/with-htpasswd.tpl")
    t = Template(tpl.read())
    tpl.close()

    return t.safe_substitute(repos_info)


if __name__ == "__main__":
    main()
