"""Announce something to Discord."""

import logging
import requests

from thscoreboard import settings


def _get_payload(message):
    """Return a dict containing the JSON payload to send a message on Discord."""
    return {
        'content': message
    }


def _get_url():
    if not settings.DISCORD_WEBHOOK_ID or not settings.DISCORD_WEBHOOK_TOKEN:
        raise AssertionError('Do not call _get_url if Discord is not configured')
    return 'https://discord.com/api/webhooks/{id}/{token}'.format(
        id=settings.DISCORD_WEBHOOK_ID,
        token=settings.DISCORD_WEBHOOK_TOKEN
    )


def announce(message: str):
    """Announce a message on Discord."""

    if (not has_discord()):
        logging.info('The discord webhook is not configured, so we cannot announce anything.')
        return

    r = requests.post(
        _get_url(),
        params={'wait': 'true'},
        json=_get_payload(message)
    )
    r.raise_for_status()


def has_discord() -> bool:
    """Returns True if a Discord webhook is configured; false otherwise."""

    return bool(settings.DISCORD_WEBHOOK_ID and settings.DISCORD_WEBHOOK_TOKEN)
