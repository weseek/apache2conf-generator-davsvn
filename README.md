apache2conf-generator-davsvn
=============================

A python script iterates specified directory recursively, scan Subversion repositories and generate Apache2 configuration for dav-svn.

Requirements
------------

* Python 3


Summary
-------

sample structure of directories:

```
/home/user                 [normal dir]
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

`template-examples/noauth.tpl`

```
<Location /svn/$relpath>
  DAV svn
  SVNPath $abspath
</Location>
```

```bash
$ python scan-and-gen.py --tpl template-examples/noauth.tpl /path/to/reposroot
```

will outputs:

```
<Location /svn/repos1>
  DAV svn
  SVNPath /home/user/repos/repos1
</Location>

<Location /svn/repos2>
  DAV svn
  SVNPath /home/user/repos/repos2
</Location>

<Location /svn/prj1/prj1-repos1>
  DAV svn
  SVNPath /home/user/repos/prj1/prj1-repos1
</Location>

<Location /svn/prj1/prj1-repos2>
  DAV svn
  SVNPath /home/user/repos/prj1/prj1-repos2
</Location>

<Location /svn/prj2/prj2-repos>
  DAV svn
  SVNPath /home/user/repos/prj2/prj2-repos1
</Location>
```

### Case2:

`tplmap.json`
```
{
	"*/prj1/*": "template-examples/noauth.tpl",
	"*": "template-examples/with-htpasswd.tpl"
}
```

```bash
$ python scan-and-gen.py --tplmap template-examples/multiple-templates/tplmap.json /path/to/reposroot
```

will outputs:

```
<Location /svn/repos1>
  DAV svn
  SVNPath /home/vagrant/repos/repos1
  AuthType Basic
  AuthName "SVN Authentication"
  AuthUserFile /home/user/.htpasswd
  Require valid-user
</Location>

<Location /svn/repos2>
  DAV svn
  SVNPath /home/vagrant/repos/repos2
  AuthType Basic
  AuthName "SVN Authentication"
  AuthUserFile /home/user/.htpasswd
  Require valid-user
</Location>

<Location /svn/prj1/prj1-repos1>
  DAV svn
  SVNPath /home/vagrant/repos/prj1/prj1-repos1
</Location>

<Location /svn/prj1/prj1-repos2>
  DAV svn
  SVNPath /home/vagrant/repos/prj1/prj1-repos2
</Location>

<Location /svn/prj2/prj2-repos>
  DAV svn
  SVNPath /home/vagrant/repos/prj2/prj2-repos1
  AuthType Basic
  AuthName "SVN Authentication"
  AuthUserFile /home/user/.htpasswd
  Require valid-user
</Location>

```

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
