from typing import Any


def get_responsive_value_from_width(width: int, output: tuple[Any, Any, Any, Any]):
    if width >= 1536:
        return output[3]
    if width >= 1280:
        return output[2]
    elif width >= 1024:
        return output[1]
    return output[0]
