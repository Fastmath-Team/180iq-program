from typing import cast
from ttkbootstrap.validation import ValidationEvent, validator


@validator
def validate_positive_number(event: ValidationEvent):
    """Contents is a number."""
    postchangetext = cast(str, event.postchangetext)

    if not postchangetext:
        return True

    try:
        return int(postchangetext) > 0

    except ValueError:
        return False
