# SIN

## Local Development Setup

1. `git clone <repo>`
2. `cd <app dir>`
3. `pip install --install-option="--user" virtualenvwrapper`
4. `export WORKON_HOME=$HOME/.virtualenvs`
5. `source /usr/local/bin/virtualenvwrapper.sh`
6. `mkvirtualenv SINvenv`
7. `pip install -r requirements.txt`
8. `bower install jquery bootstrap`
9. Create a new settings file: `cp webapps2/example_settings.py webapps2/settings.py`
10. Generate new secret key and place into settings file

### Setup PostgreSQL
1. `pg_ctl start -D /usr/local/var/postgres`
2. `createuser -d webapps`
3. `createdb webapps2`
4. `psql -d webapps2 webapps`

### Running locally
  * Ensure PostgreSQL is running
  * `cd <project dir>` and activate the virtualenv
  * `python manage.py collectstatic`; this collects static files from the static folders and the webapps_assets and bower_components directories (as per webapps/settings.py)
  * `python manage.py runserver`; runs the server using localhost at port 8000

### If there are migrations to make:
  * `python manage.py makemigrations <app name>`
  * `python manage.py migrate`
  * `python manage.py syncdb`

## Deploying

SSH into `sin.reed.edu` as the `sin` user, and run the `/home/sin/deploy.sh` script.
