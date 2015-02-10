#SIN Webapps2 Documentation

##Local Development Setup
`git clone <repo>`
`cd <app dir>`
`pip install --install-option="--user" virtualenvwrapper`
`export WORKON_HOME=$HOME/.virtualenvs`
`source /usr/local/bin/virtualenvwrapper.sh`
`mkvirtualenv SINvenv`
`pip install -r requirements.txt`

##Start postgres database & server
`pg_ctl start -D /usr/local/var/postgres`
`createuser -d webapps`
`createdb webapps2`
`psql -d webapps2 webapps` 

##Set up a local LDAP server for 'authentication'
--> i think this works now

##Make the static resources more obvious
##Find all the styles etc
##fix urls


