# thscoreboard
An open-source scoreboard for Touhou games.

## Setting up a development environment

### Black

We use Black, the Python formatting tool, to format our code automatically. As such, we strongly recommend setting up your IDE or code editor to run Black automatically when saving a file. The beauty of Black is that it can just format things for you, so take advantage of that by doing this, and it'll never bother you or stop you from pushing code.

### Generating the replay parsers

Start by installing `kaitai-struct-compiler`. Once it is installed,
run `python manage.py kaitai_struct_compile`. Or, directly run the compiler: Navigate to `project/thscoreboard/replays/kaitai_parsers` and run `kaitai-struct-compiler -t python ../../../../ref/threp-ksy/*.ksy` (note that you don't need to change the slashes to backslashes to run this on Windows).

### Database configuration

settings.py is configured to use a local instance of PostgreSQL by default. To set up local Postgres:

1. Install postgres
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

In the future, we should just mark everything as being for translation.

These translations are defined in `.po` files in the locale directory. You can
edit them by hand, but it is easier to use a special editor for them. I've
added the "django-rosetta" app to this site; it is an editor you can access by
running "runserver" and then going to /rosetta on your local page. (It is not
included in the prod release.) I have no special attachment to django-rosetta;
I would not be surprised if we found a better editor later.

To add new strings-to-be-translated to the .po files, run `python manage.py makemessages --all`. This updates the .po files to include the new strings.

The .po files must be compiled into .mo files with "python manage.py compilemessages"
in order to be used. It's probably a good idea to rerun this command whenever you
need to edit the translations.

(At some point, we should probably install a Git hook to do this, too.)

The easiest way to tell if translations are working properly is to look at the
score table; the games will be abbreviated in the style of "EoSD" if the
names are translated into English, but will be in the style of "th06" otherwise.

There isn't a hook yet to actually switch the language to Japanese.

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
