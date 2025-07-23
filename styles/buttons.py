from typing import Optional, Tuple, TypedDict, Union

from styles.theme import THEME


class ButtonStylesDict(TypedDict):
    corner_radius: Optional[int]
    fg_color: Optional[Union[str, Tuple[str, str]]]
    hover_color: Optional[Union[str, Tuple[str, str]]]
    border_color: Optional[Union[str, Tuple[str, str]]]
    border_width: Optional[int]
    text_color: Optional[Union[str, Tuple[str, str]]]
    text_color_disabled: Optional[Union[str, Tuple[str, str]]]


BUTTON_DEFAULT_STYLES: ButtonStylesDict = {
    "corner_radius": THEME.CTkButton.corner_radius,
    "border_width": THEME.CTkButton.border_width,
    "fg_color": (THEME.CTkButton.fg_color[0], THEME.CTkButton.fg_color[1]),
    "hover_color": (THEME.CTkButton.hover_color[0], THEME.CTkButton.hover_color[1]),
    "border_color": (THEME.CTkButton.border_color[0], THEME.CTkButton.border_color[1]),
    "text_color": (THEME.CTkButton.text_color[0], THEME.CTkButton.text_color[1]),
    "text_color_disabled": (
        THEME.CTkButton.text_color_disabled[0],
        THEME.CTkButton.text_color_disabled[1],
    ),
}

BUTTON_YELLOW_STYLES: ButtonStylesDict = {
    "corner_radius": 6,
    "border_width": 2,
    "fg_color": THEME.CTkFrame.fg_color[0],
    "hover_color": THEME.CTkFrame.top_fg_color[0],
    "border_color": ("#F8D650", "#1f538d"),
    "text_color": ("#C1A10D", "#1f538d"),
    "text_color_disabled": ("gray74", "gray60"),
}

BUTTON_ORANGE_STYLES: ButtonStylesDict = {
    "corner_radius": 6,
    "border_width": 2,
    "fg_color": THEME.CTkFrame.fg_color[0],
    "hover_color": THEME.CTkFrame.top_fg_color[0],
    "border_color": ("#E9983F", "#1f538d"),
    "text_color": ("#E9983F", "#1f538d"),
    "text_color_disabled": ("gray74", "gray60"),
}

BUTTON_GREEN_STYLES: ButtonStylesDict = {
    "corner_radius": 6,
    "border_width": 2,
    "fg_color": THEME.CTkFrame.fg_color[0],
    "hover_color": THEME.CTkFrame.top_fg_color[0],
    "border_color": ("#49A35B", "#1f538d"),
    "text_color": ("#49A35B", "#1f538d"),
    "text_color_disabled": ("gray74", "gray60"),
}

BUTTON_FILLED_STYLES: ButtonStylesDict = {
    "corner_radius": 6,
    "border_width": 0,
    "fg_color": ("#3670B1", "#1f538d"),
    "hover_color": ("#1A4677", "#14375e"),
    "border_color": ("#3E454A", "#949A9F"),
    "text_color": ("#F5FCFF", "#DCE4EE"),
    "text_color_disabled": ("gray74", "gray60"),
}
