<Location /svn/$relpath>
  DAV svn
  SVNPath $abspath
  AuthType Basic
  AuthName "SVN Authentication"
  AuthUserFile /home/user/.htpasswd
  Require valid-user
</Location>
