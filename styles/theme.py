from __future__ import annotations

import json
from dataclasses import dataclass
from typing import List, cast

from dacite import Config, DaciteError, from_dict

from utils.file import get_file

_THEME_FILE_PATH = get_file("styles/theme.json")


@dataclass
class Theme:
    CTk: CtkOrCtkToplevel
    CTkToplevel: CtkOrCtkToplevel
    CTkFrame: CtkFrame
    CTkButton: CtkButton
    CTkLabel: CtkLabel
    CTkEntry: CtkEntry
    CTkCheckBox: CtkCheckBox
    CTkSwitch: CtkSwitch
    CTkRadioButton: CtkRadioButton
    CTkProgressBar: CtkProgressBar
    CTkSlider: CtkSlider
    CTkOptionMenu: CtkOptionMenu
    CTkComboBox: CtkComboBox
    CTkScrollbar: CtkScrollbar
    CTkSegmentedButton: CtkSegmentedButton
    CTkTextbox: CtkTextbox
    CTkScrollableFrame: CtkScrollableFrame
    DropdownMenu: DropdownMenu
    CTkFont: CtkFont


@dataclass
class CtkOrCtkToplevel:
    fg_color: List[str]


@dataclass
class CtkFrame:
    corner_radius: int
    border_width: int
    fg_color: List[str]
    top_fg_color: List[str]
    border_color: List[str]


@dataclass
class CtkLabel:
    corner_radius: int
    fg_color: str
    text_color: List[str]


@dataclass
class CtkEntry:
    corner_radius: int
    border_width: int
    fg_color: List[str]
    border_color: List[str]
    text_color: List[str]
    placeholder_text_color: List[str]


@dataclass
class CtkButton:
    corner_radius: int
    border_width: int
    fg_color: List[str]
    hover_color: List[str]
    border_color: List[str]
    text_color: List[str]
    text_color_disabled: List[str]


@dataclass
class CtkCheckBox:
    corner_radius: int
    border_width: int
    fg_color: List[str]
    hover_color: List[str]
    border_color: List[str]
    text_color: List[str]
    text_color_disabled: List[str]
    checkmark_color: List[str]


@dataclass
class CtkSwitch:
    corner_radius: int
    border_width: int
    button_length: int
    fg_color: List[str]
    progress_color: List[str]
    button_color: List[str]
    button_hover_color: List[str]
    text_color: List[str]
    text_color_disabled: List[str]


@dataclass
class CtkRadioButton:
    corner_radius: int
    border_width_checked: int
    border_width_unchecked: int
    fg_color: List[str]
    border_color: List[str]
    hover_color: List[str]
    text_color: List[str]
    text_color_disabled: List[str]


@dataclass
class CtkProgressBar:
    corner_radius: int
    border_width: int
    fg_color: List[str]
    progress_color: List[str]
    border_color: List[str]


@dataclass
class CtkSlider:
    corner_radius: int
    button_corner_radius: int
    border_width: int
    button_length: int
    fg_color: List[str]
    progress_color: List[str]
    button_color: List[str]
    button_hover_color: List[str]


@dataclass
class CtkOptionMenu:
    corner_radius: int
    fg_color: List[str]
    button_color: List[str]
    button_hover_color: List[str]
    text_color: List[str]
    text_color_disabled: List[str]


@dataclass
class CtkComboBox:
    corner_radius: int
    border_width: int
    fg_color: List[str]
    border_color: List[str]
    button_color: List[str]
    button_hover_color: List[str]
    text_color: List[str]
    text_color_disabled: List[str]


@dataclass
class CtkScrollbar:
    corner_radius: int
    border_spacing: int
    fg_color: str
    button_color: List[str]
    button_hover_color: List[str]


@dataclass
class CtkSegmentedButton:
    corner_radius: int
    border_width: int
    fg_color: List[str]
    selected_color: List[str]
    selected_hover_color: List[str]
    unselected_color: List[str]
    unselected_hover_color: List[str]
    text_color: List[str]
    text_color_disabled: List[str]


@dataclass
class CtkTextbox:
    corner_radius: int
    border_width: int
    fg_color: List[str]
    border_color: List[str]
    text_color: List[str]
    scrollbar_button_color: List[str]
    scrollbar_button_hover_color: List[str]


@dataclass
class CtkScrollableFrame:
    label_fg_color: List[str]


@dataclass
class DropdownMenu:
    fg_color: List[str]
    hover_color: List[str]
    text_color: List[str]


@dataclass
class CtkFont:
    macOS: FontConfig
    Windows: FontConfig
    Linux: FontConfig


@dataclass
class FontConfig:
    family: str
    size: int
    weight: str


def load_theme():
    try:
        with open(_THEME_FILE_PATH, "r", encoding="utf-8") as f:
            raw_config_data = json.load(f)

        return from_dict(
            data_class=Theme, data=raw_config_data, config=Config(check_types=True)
        )

    except FileNotFoundError:
        print(f"Error: The configuration file '{_THEME_FILE_PATH}' was not found.")
    except json.JSONDecodeError:
        print(
            f"Error: Could not decode JSON from '{_THEME_FILE_PATH}'. Check if the file content is valid JSON."
        )
    except DaciteError as e:
        # Dacite will raise a DaciteError if there's a type mismatch or a required field is missing
        print(
            f"Error converting config: {e}. Check your JSON structure against dataclass definitions."
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


THEME = cast(Theme, load_theme())
