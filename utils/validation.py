from ttkbootstrap.validation import ValidationEvent, validator


@validator
def validate_positive_number(event: ValidationEvent):
    """Contents is a number."""
    if len(event.postchangetext) == 0:
        return True
    return str(event.postchangetext).isnumeric() and int(event.postchangetext) > 0
