# thscoreboard
An open-source scoreboard for Touhou games.

## Setting up a development environment

### Generating the replay parsers

Start by installing `kaitai-struct-compiler`. Then, navigate to `project/thscoreboard/scores/kaitai_parsers` and run `kaitai-struct-compiler -t python ../../../../ref/threp-ksy/*.ksy` (note that you don't need to change the slashes to backslashes to run this on Windows)

### Database configuration

settings.py is configured to use a local instance of PostgreSQL by default. To set up local Postgres:

1. Install postgres
1. Create a database on your local postgres, called "thscoreboard".
1. Create a login user that the server will use, also called "thscoreboard". You can pick whatever password you want. Give this user rights to access and change the "thscoreboard" database. In general, it is best not to use a superuser account to connect to a database like this, since superusers can do all sorts of messed up stuff by accident.
1. Give "thscoreboard" rights to create databases. This is not necessary for running the server locally, but you need it to run tests.
1. Create a .env file in ./project/thscoreboard. This file will contain environment variables loaded when running locally. An environment variable named `LOCAL_DATABASE_PASSWORD` is required; set it to your password. .env is gitignored by default, so you do not need to worry about committing it by accident.
1. Run "python manage.py runserver" and see if it successfully connects. If so, run "python manage.py migrate" to set up the initial database contents.
1. Run "python manage.py setup_constant_tables" to set up constant tables, like the Game and Shot tables.

### Email configuration

This project rarely needs to send email. For example, it sends
email if the user forgot their password and needs to reset it.

By default, in a development provider, we use the "Console" email backend.
This backend "sends" emails by logging them to the console. Obviously this
is not super realistic, but it should be good enough for most purposes.

