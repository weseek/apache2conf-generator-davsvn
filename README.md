apache2conf-generator-davsvn
=============================

A python script iterates specified directory recursively,  
scan Subversion repositories and generate Apache2 configuration for dav-svn.

Requirements
------------

* Python 3


Example
-------

sample structure of directories:

```
/var/repos                 [normal dir]
  repos1                 > [SVN repository]
  repos2                 > [SVN repository]
  notrepos                 [normal dir or file]
  prj1                     [normal dir]
    prj1-repos1          > [SVN repository]
    prj1-repos2          > [SVN repository]
  prj2                     [normal dir]
    prj2-repos           > [symlink to somewhere SVN repository]
```

### Case1:

With [`templates/noauth.tpl`](https://github.com/weseek/apache2conf-generator-davsvn/blob/master/templates/noauth.tpl):

```
<Location /svn/$relpath>
  DAV svn
  SVNPath $abspath
</Location>
```

following command:

```bash
$ python scan-and-gen.py --tpl templates/noauth.tpl /var/repos
```

will output:

```
<Location /svn/repos1>
  DAV svn
  SVNPath /var/repos/repos1
</Location>

<Location /svn/repos2>
  DAV svn
  SVNPath /var/repos/repos2
</Location>

<Location /svn/prj1/prj1-repos1>
  DAV svn
  SVNPath /var/repos/prj1/prj1-repos1
</Location>

<Location /svn/prj1/prj1-repos2>
  DAV svn
  SVNPath /var/repos/prj1/prj1-repos2
</Location>

<Location /svn/prj2/prj2-repos>
  DAV svn
  SVNPath /var/repos/prj2/prj2-repos1
</Location>
```

### Case2:

With [`templates/tplmap.json`](https://github.com/weseek/apache2conf-generator-davsvn/blob/master/templates/tplmap.json):

```
{
	"*/prj1/*": "templates/noauth.tpl",
	"*": "templates/with-htpasswd.tpl"
}
```

following command:

```bash
$ python scan-and-gen.py --tplmap templates/tplmap.json /var/repos
```

will output:

```
<Location /svn/repos1>
  DAV svn
  SVNPath /var/repos/repos1
  AuthType Basic
  AuthName "SVN Authentication"
  AuthUserFile /home/user/.htpasswd
  Require valid-user
</Location>

<Location /svn/repos2>
  DAV svn
  SVNPath /var/repos/repos2
  AuthType Basic
  AuthName "SVN Authentication"
  AuthUserFile /home/user/.htpasswd
  Require valid-user
</Location>

<Location /svn/prj1/prj1-repos1>
  DAV svn
  SVNPath /var/repos/prj1/prj1-repos1
</Location>

<Location /svn/prj1/prj1-repos2>
  DAV svn
  SVNPath /var/repos/prj1/prj1-repos2
</Location>

<Location /svn/prj2/prj2-repos>
  DAV svn
  SVNPath /var/repos/prj2/prj2-repos1
  AuthType Basic
  AuthName "SVN Authentication"
  AuthUserFile /home/user/.htpasswd
  Require valid-user
</Location>

```


Usage
-------

### scan-and-gen.py

```
$ python scan-and-gen.py -h
usage: scan-and-gen.py [-h] [--tpl TEMPLATE_FILE] [--tplmap TEMPLATE_MAP_FILE] REPOS_ROOT

This program scans REPOS_ROOT, picks up Subversion repositories, and outputs
Apache2 configurations for dav-svn to STDOUT.

positional arguments:
  REPOS_ROOT            path to the directory that contains SVN repositories

optional arguments:
  -h, --help            show this help message and exit
  --tpl TEMPLATE_FILE   path to an Apache2 configuration template file
  --tplmap TEMPLATE_MAP_FILE
                        path to a JSON file that specify template mappings
```

* You must specify only either one of `--tpl` and `--tplmap`.

### Template

Following placeholders are available in a template file.

placeholder | description
:-----------|:-----------
abspath     | absolute path to the target repository
relpath     | relative path to the target repository from REPOS_ROOT
basename    | basename of the target repository

### Template Mapping

* A JSON file specifing rules.
  * key: [fnmatch pattern](https://docs.python.org/3.4/library/fnmatch.html)
  * value: path to a template file
* The upper rules are stronger than the lower rules.

Contributing
------------

1. Fork the repository on Github
1. Write your change
1. Submit a Pull Request using Github


License and Authors
-------------------
- Author:: Yuki Takei (<yuki@weseek.co.jp>)

Copyright 2014 WESEEK, Inc.

Licensed under the Apache License, Version 2.0 (the "License");  
you may not use this file except in compliance with the License.  
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software  
distributed under the License is distributed on an "AS IS" BASIS,  
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
See the License for the specific language governing permissions and  
limitations under the License.
