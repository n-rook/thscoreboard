"""Provides access to uWSGI.

If uwsgi is not installed, the methods in this module just do nothing.

See https://uwsgi-docs.readthedocs.io/en/latest/PythonModule.html
"""

try:
    import uwsgi
except ImportError:
    uwsgi = None


def reload():
    """Reload the uWSGI app."""
    if uwsgi:
        uwsgi.reload()
