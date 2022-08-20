# thscoreboard
An open-source scoreboard for Touhou games.

## Setting up a development environment

### Database configuration

settings.py is configured to use a local instance of PostgreSQL by default. To set up local Postgres:

1. Install postgres
1. Create a database on your local postgres, called "thscoreboard".
1. Create a login user that the server will use, also called "thscoreboard". You can pick whatever password you want. Give this user rights to access and change the "thscoreboard" database. In general, it is best not to use a superuser account to connect to a database like this, since superusers can do all sorts of messed up stuff by accident.
1. Create a local "connection service" file, or update yours if one already exists. See https://www.postgresql.org/docs/current/libpq-pgservice.html for details. Define a service naemd "local_thscoreboard".
1. Add a ".dev_pgpass" file in the project directory (that is, ./project/thscoreboard). Its only contents should be a line saying `localhost:5432:thscoreboard:thscoreboard:YOUR_PASSWORD`.
1. Run "python manage.py runserver" and see if it successfully connects. If so, run "python manage.py migrate" to set up the initial database contents.
1. Run "python manage.py setup_constant_tables" to set up constant tables, like the Game and Shot tables.

