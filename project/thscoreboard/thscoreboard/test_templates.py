"""A test that checks all templates for simple mistakes."""

import pathlib

from django import test
from django import template as django_template


def ListTemplateFiles() -> list[str]:
    template_directories = []
    for engine in django_template.loader.engines.all():
        template_directories.extend([pathlib.Path(d) for d in engine.template_dirs])

    template_directories = [
        d
        for d in template_directories
        # Exclude templates from libraries.
        if "site-packages" not in d.parts
    ]
    template_files = []
    for d in template_directories:
        for filepath in d.glob("**/*.html"):
            template_files.append(filepath)
    return template_files


def ListTemplates():
    return [
        (filepath, filepath.read_text(encoding="utf-8"))
        for filepath in ListTemplateFiles()
    ]


class TemplatesTestCase(test.TestCase):
    def testDidNotForgetI18N(self):
        for path, contents in ListTemplates():
            with self.subTest(path):
                if not (
                    "{% translate" in contents or "{% blocktranslate %}" in contents
                ):
                    continue

                self.assertIn(
                    "{% load i18n %}",
                    contents,
                    msg="You forgot to {% load i18n %} in your template!",
                )
