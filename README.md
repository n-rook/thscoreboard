# thscoreboard
An open-source scoreboard for Touhou games.

## Setting up a development environment

### Black

We use Black, the Python formatting tool, to format our code automatically. As such, we strongly recommend setting up your IDE or code editor to run Black automatically when saving a file. The beauty of Black is that it can just format things for you, so take advantage of that by doing this, and it'll never bother you or stop you from pushing code.

### Generating the replay parsers

Start by installing `kaitai-struct-compiler`. Then, navigate to `project/thscoreboard/replays/kaitai_parsers` and run `kaitai-struct-compiler -t python ../../../../ref/threp-ksy/*.ksy` (note that you don't need to change the slashes to backslashes to run this on Windows).

### Database configuration

settings.py is configured to use a local instance of PostgreSQL by default. To set up local Postgres:

1. Install PostgreSQL 14 or later.
1. Create a database on your local postgres, called "thscoreboard".
1. Create a login user that the server will use, also called "thscoreboard". You can pick whatever password you want. Give this user rights to access and change the "thscoreboard" database. In general, it is best not to use a superuser account to connect to a database like this, since superusers can do all sorts of messed up stuff by accident.
1. Give "thscoreboard" rights to create databases. This is not necessary for running the server locally, but you need it to run tests.
1. Create a .env file in ./project/thscoreboard. This file will contain environment variables loaded when running locally. An environment variable named `LOCAL_DATABASE_PASSWORD` is required; set it to your password. .env is gitignored by default, so you do not need to worry about committing it by accident.
1. Run "python manage.py runserver" and see if it successfully connects. If so, run "python manage.py migrate" to set up the initial database contents.
1. Run "python manage.py setup_constant_tables" to set up constant tables, like the Game and Shot tables.
1. Install jest, for example with `npm install jest --global`, and run `jest` to run js tests.

### Email configuration

This project rarely needs to send email. For example, it sends
email if the user forgot their password and needs to reset it.

By default, in a development provider, we use the "Console" email backend.
This backend "sends" emails by logging them to the console. Obviously this
is not super realistic, but it should be good enough for most purposes.

### Translation and localization

Silent Selene supports two languages: English and Japanese. In order to deal with
language files, you must install "gettext". This package is available here for Windows:

https://mlocati.github.io/articles/gettext-iconv-windows.html

For details on Django translations, see this page:

https://docs.djangoproject.com/en/4.1/topics/i18n/translation/

The basics, though, are as follows. To mark a string as being translated in
code, use a function from "django.utils.translation." Usually this is as follows:

```
from django.utils.translation import gettext as _

...
return _('something to be translated')
```

But there are advanced features, too.

You can also mark strings as being for translation in templates, too:

https://docs.djangoproject.com/en/4.1/topics/i18n/translation/#internationalization-in-template-code

Every piece of text that is displayed on the site should be marked using these
translation libraries.

These translations are defined in `.po` files in the locale directory. You can
edit them by hand, but it is easier to use a special editor for them. I've
added the "django-rosetta" app to this site; it is an editor you can access by
running "runserver" and then going to /rosetta on your local page. (It is not
included in the prod release.)

To add new strings-to-be-translated to the .po files, run
`python manage.py makemessages --all --no-wrap`. This updates the .po files to include the new strings.

The .po files must be compiled into .mo files with "python manage.py compilemessages"
in order to be used. This is done automatically on the server, so you do not
need to include .mo files in your pull requests.

As a general rule, **do not include new .po files as part of your PRs.** This
is to avoid merge conflicts; if two different PRs both regenerate the .po
files, they can be difficult to reconcile.

### Adding support for new games

- add kaitai parser
- add replay_parsing.py function
- add table fields into game_fields.py (modify all if new fields are added)
- add game_ids
- if needed, update ReplayStage model and generate migrations
- set up constant tables
- add tests
- add front end translations for added string literals

## The production environment

The production server uses venv:

https://docs.python.org/3/library/venv.html

It was a fun surprise to see the version of pip installed by default in Debian
Bookworm only supports venv by default!

venv is essentially a way of isolating Python environments from each other, so
that (for example) different servers can use different versions of the same
module.

The virtual environment is installed to .venv in each server directory (that is,
for example, `/home/silentselene/silentselene-staging/.venv)`. To enter the
venv, run  `. .venv/bin/activate`. Once you're in the venv, Python and related
tools are referenced from the venv; for example, python is
`/home/silentselene/silentselene-staging/.venv/bin/python`. Commands like
`pip install` will install to the venv.

Note that the venvs were created by running `python -m venv .venv` in these
directories. As always, manage these as `silentselene`, not root, or else
root will wind up owning files.

### Deploying updates

Updates are run by the `silentselene-deploy` account, separately from the
`silentselene` account that serves the Web application. The update script is
[`ref/deploy/update.py`](ref/deploy/update.py), and the one-shot systemd unit
definitions are:

- `ref/server/systemd/silentselene-deploy.service`
- `ref/server/systemd/silentselene-staging-deploy.service`

Install the unit files in `/etc/systemd/system/`, then explicitly start the
appropriate unit for each deployment:

```sh
sudo systemctl start silentselene-deploy.service
sudo systemctl start silentselene-staging-deploy.service
```

Staging automatically checks the remote `main` branch once a minute. Install
and enable the accompanying poll timer to activate this behavior:

```sh
sudo systemctl enable --now silentselene-staging-poll.timer
```

The timer starts `silentselene-staging-deploy.service` only when `main` has a
new revision, so unchanged checks do not run migrations or rebuild assets.

The units execute `update.py` as `silentselene-deploy`. The account needs write
access to the corresponding checkout, including its `.git` directory, and read
access to the credential used for the Git remote. The Web-service account does
not need either Git write access or Discord credentials.

The updater permits only fast-forward Git updates. Every invocation then runs
`migrate`, `setup_constant_tables`, `compilescss`, `compilemessages`, and
`collectstatic --noinput`. It sends a Discord message and reloads the
corresponding uWSGI service only after those commands all succeed. These steps
run even if the checkout was already at the latest revision.

uWSGI reload is fully defined by the systemd units: the Web units reload their
uWSGI master with `SIGHUP`, and the deploy units use a fixed `ExecStartPost=`
command to request that reload. The updater itself has no `sudo` dependency or
privilege to control services.

Each deployment logs its start, Git revision, every Django command, Discord
notification, completion, and any exception to the systemd journal. Inspect a
deployment with:

```sh
sudo journalctl -u silentselene-deploy.service
sudo journalctl -u silentselene-staging-deploy.service
```

The Discord credential belongs only in root-owned mode-`0600` environment files
on the server, not in this repository:

```text
/etc/silentselene/deploy.env
/etc/silentselene/staging-deploy.env
```

Each environment file must contain either `DISCORD_WEBHOOK_URL`, or both
`DISCORD_WEBHOOK_ID` and `DISCORD_WEBHOOK_TOKEN`.
