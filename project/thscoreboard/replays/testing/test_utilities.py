from django import test


def OverrideTranslations():
    """Returns a context manager that disables translations.

    Technically, this instead overrides the settings to use a language
    for which we don't support translations. However, regardless, it's still
    necessary to get consistent results if we want to test functions that
    return translated strings.

    Note that there is probably something wrong with the way we're
    running translations in CI, and there's probably a better way to do this.
    See https://github.com/n-rook/thscoreboard/issues/58
    """
    # https://github.com/n-rook/thscoreboard/issues/58
    # gettext doesn't work right on the GitHub bot, so we intentionally
    # override it with a language for which we don't have translations.
    return test.override_settings(LANGUAGE_CODE='pt-br')
