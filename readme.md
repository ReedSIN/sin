##SIN Webapps2 Documentation

####Local Development Setup
`git clone <repo>`
`cd <app dir>`
`pip install --install-option="--user" virtualenvwrapper`
`export WORKON_HOME=$HOME/.virtualenvs`
`source /usr/local/bin/virtualenvwrapper.sh`
`mkvirtualenv SINvenv`
`pip install -r requirements.txt`
`bower install jquery bootstrap`
Create a new settings file: `cp webapps2/example_settings.py webapps2/settings.py`
Generate new secret key and place into settings file.

####Start postgres database & server
`pg_ctl start -D /usr/local/var/postgres`
`createuser -d webapps`
`createdb webapps2`
`psql -d webapps2 webapps`

####Running locally:
  * start postgres database should be something like `pg_ctl start -D /usr/local/var/postgres`, where `/usr/local/var/postgres` is the location of the database. 
  * In another tab/window `cd <webapps-dir>` and start the virtual environment
  * `python manage.py collectstatic` this collects static files from the static folders and the webapps_assets and bower_components directories (as per webapps/settings.py).
  * `python manage.py runserver` runs the server using localhost at port 8000.  

##### If there are migrations to make:
  * `python manage.py makemigrations <app_name>`
  * `python manage.py migrate`
  * `python manage.py syncdb`

  
####To Do:
* Make the static resources more obvious
* Hide the keys & database stuff in settings.py

####Note On the URLs in the sidebar template:
The urls, as they are defined in webapps2/urls.py will allow a url such as: 'http://localhost:8000/organization-manager/' but not 'http://localhost:8000/webapps2/organization-manager/'. The current sidebar include uses links that have the latter form. 



###

`ssh <username>@sin.reed.edu`
`cd var/django/webapps2`
`source env/bin/activate` or `. env/bin/activate`
`cd webapps2`