from typing import Optional, Tuple, TypedDict, Union


class ProgressStylesDict(TypedDict):
    corner_radius: Optional[int]
    border_width: Optional[int]
    fg_color: Optional[Union[str, Tuple[str, str]]]
    progress_color: Optional[Union[str, Tuple[str, str]]]
    border_color: Optional[Union[str, Tuple[str, str]]]


PROGRESS_YELLOW_STYLES: ProgressStylesDict = {
    "corner_radius": 6,
    "border_width": 0,
    "fg_color": ("#F8ECBD", "#4A4D50"),
    "progress_color": ("#F8D650", "#1f538d"),
    "border_color": ("gray", "gray"),
}

PROGRESS_ORANGE_STYLES: ProgressStylesDict = {
    "corner_radius": 6,
    "border_width": 0,
    "fg_color": ("#FDC28A", "#4A4D50"),
    "progress_color": ("#E9983F", "#1f538d"),
    "border_color": ("gray", "gray"),
}

PROGRESS_RED_STYLES: ProgressStylesDict = {
    "corner_radius": 6,
    "border_width": 0,
    "fg_color": ("#FF9184", "#4A4D50"),
    "progress_color": ("#dc2626", "#1f538d"),
    "border_color": ("gray", "gray"),
}
