from typing import Optional, Tuple, TypedDict, Union


class ButtonStylesDict(TypedDict):
    corner_radius: Optional[int]
    fg_color: Optional[Union[str, Tuple[str, str]]]
    hover_color: Optional[Union[str, Tuple[str, str]]]
    border_color: Optional[Union[str, Tuple[str, str]]]
    border_width: Optional[int]
    text_color: Optional[Union[str, Tuple[str, str]]]
    text_color_disabled: Optional[Union[str, Tuple[str, str]]]


BUTTON_DEFAULT_STYLES: ButtonStylesDict = {
    "corner_radius": 6,
    "border_width": 0,
    "fg_color": ("#3a7ebf", "#1f538d"),
    "hover_color": ("#325882", "#14375e"),
    "border_color": ("#3E454A", "#949A9F"),
    "text_color": ("#DCE4EE", "#DCE4EE"),
    "text_color_disabled": ("gray74", "gray60"),
}

BUTTON_YELLOW_STYLES: ButtonStylesDict = {
    "corner_radius": 6,
    "border_width": 0,
    "fg_color": ("#F8D650", "#1f538d"),
    "hover_color": ("#D9B726", "#14375e"),
    "border_color": ("#3E454A", "#949A9F"),
    "text_color": ("#000000", "#DCE4EE"),
    "text_color_disabled": ("#564300 ", "gray60"),
}

BUTTON_ORANGE_STYLES: ButtonStylesDict = {
    "corner_radius": 6,
    "border_width": 0,
    "fg_color": ("#E9983F", "#1f538d"),
    "hover_color": ("#A76A26", "#14375e"),
    "border_color": ("#3E454A", "#949A9F"),
    "text_color": ("#000000", "#DCE4EE"),
    "text_color_disabled": ("#6C3500", "gray60"),
}

BUTTON_GREEN_STYLES: ButtonStylesDict = {
    "corner_radius": 6,
    "border_width": 0,
    "fg_color": ("#49A35B", "#1f538d"),
    "hover_color": ("#488B54", "#14375e"),
    "border_color": ("#3E454A", "#949A9F"),
    "text_color": ("#000000", "#DCE4EE"),
    "text_color_disabled": ("#065420", "gray60"),
}

BUTTON_OUTLINE_STYLES: ButtonStylesDict = {
    "corner_radius": 6,
    "border_width": 2,
    "fg_color": "transparent",
    "hover_color": ("gray80", "gray28"),
    "border_color": ("#3a7ebf", "#1f538d"),
    "text_color": ("#3a7ebf", "#1f538d"),
    "text_color_disabled": ("gray74", "gray60"),
}
