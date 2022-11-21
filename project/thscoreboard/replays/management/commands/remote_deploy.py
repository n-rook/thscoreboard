import logging
import os

from django.core.management import base
import requests
from requests import auth


class Command(base.BaseCommand):

    help = 'Deploy to a remote server.'

    def add_arguments(self, parser: base.CommandParser) -> None:
        super().add_arguments(parser)

        parser.add_argument('target', help='The host (and port) of the server which should fetch a new version from HEAD.')
        parser.add_argument('username', help='The username of the superuser with deployment rights.')
        parser.add_argument('password', nargs='?', help='The password of the superuser with deployment rights.')

    def handle(self, *args, **options):
        """Deploy to a remote server."""
        target = options['target']
        username = options['username']
        if options['password']:
            password = options['password']
        elif 'DEPLOY_PASSWORD' in os.environ:
            password = os.environ['DEPLOY_PASSWORD']
        else:
            raise ValueError('No password specified')

        RequestDeploy(target, username, password)


def RequestDeploy(hostport: str, username: str, password: str):
    if 'localhost' in hostport:
        # Use basic HTTP if just connecting to localhost.
        scheme = 'http'
    else:
        scheme = 'https'

    basic_auth = auth.HTTPBasicAuth(username, password)
    address = f'{scheme}://{hostport}/deploy'
    logging.info('Sending deployment request to %s', address)
    r = requests.post(address, auth=basic_auth)
    logging.info('Response:\n%s', r.content)
    r.raise_for_status()
