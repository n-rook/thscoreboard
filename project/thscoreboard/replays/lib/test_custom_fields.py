import unittest

from django import forms
from django.db.models import enums


from replays.lib import custom_fields


class SuitType(enums.IntegerChoices):
    CLUBS = 1, "Clubs"
    DIAMONDS = 2, "Diamonds"
    HEARTS = 3, "Hearts"
    SPADES = 4, "Spades"


class TestForm(forms.Form):
    suit = custom_fields.ChoicesEnumField(SuitType)


class ChoicesEnumFieldTest(unittest.TestCase):
    def testCoerces(self):
        form = TestForm(data={"suit": 2})
        form.is_valid()
        self.assertEqual(form.cleaned_data["suit"], SuitType.DIAMONDS)
        self.assertIsInstance(form.cleaned_data["suit"], SuitType)
