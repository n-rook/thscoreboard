"""Provide useful form fields."""

from typing import Type

from django import forms
from django.db.models import enums


class ChoicesEnumField(forms.TypedChoiceField):
    """A field defined by a Django enum.

    Unlike a regular ChoiceField, this field coerces values to match the
    elements of the original Choices enum, rather than leaving them as
    bare strings. This is useful when the value must be programmatically
    manipulated after the fact.
    """

    def __init__(self, choices_class: Type[enums.Choices]):
        def _Coerce(v):
            for member in choices_class:
                # Internally, TypedChoiceField casts values to strings.
                if v == str(member.value):
                    return member
            raise ValueError(f"{v} cannot be coerced to a {choices_class}")

        super().__init__(choices=choices_class.choices, coerce=_Coerce)
