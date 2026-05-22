from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class Key(StrEnum):
    # Letters
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"
    F = "f"
    G = "g"
    H = "h"
    I = "i"  # noqa: E741
    J = "j"
    K = "k"
    L = "l"
    M = "m"
    N = "n"
    O = "o"  # noqa: E741
    P = "p"
    Q = "q"
    R = "r"
    S = "s"
    T = "t"
    U = "u"
    V = "v"
    W = "w"
    X = "x"
    Y = "y"
    Z = "z"

    # Digits
    DIGIT_0 = "0"
    DIGIT_1 = "1"
    DIGIT_2 = "2"
    DIGIT_3 = "3"
    DIGIT_4 = "4"
    DIGIT_5 = "5"
    DIGIT_6 = "6"
    DIGIT_7 = "7"
    DIGIT_8 = "8"
    DIGIT_9 = "9"

    # Function keys
    F1 = "f1"
    F2 = "f2"
    F3 = "f3"
    F4 = "f4"
    F5 = "f5"
    F6 = "f6"
    F7 = "f7"
    F8 = "f8"
    F9 = "f9"
    F10 = "f10"
    F11 = "f11"
    F12 = "f12"
    F13 = "f13"
    F14 = "f14"
    F15 = "f15"
    F16 = "f16"
    F17 = "f17"
    F18 = "f18"
    F19 = "f19"
    F20 = "f20"
    F21 = "f21"
    F22 = "f22"
    F23 = "f23"
    F24 = "f24"

    # Modifiers
    CTRL = "ctrl"
    LEFT_CTRL = "left_ctrl"
    RIGHT_CTRL = "right_ctrl"
    SHIFT = "shift"
    LEFT_SHIFT = "left_shift"
    RIGHT_SHIFT = "right_shift"
    ALT = "alt"
    LEFT_ALT = "left_alt"
    RIGHT_ALT = "right_alt"
    META = "meta"
    LEFT_META = "left_meta"
    RIGHT_META = "right_meta"

    # Navigation
    ARROW_UP = "arrow_up"
    ARROW_DOWN = "arrow_down"
    ARROW_LEFT = "arrow_left"
    ARROW_RIGHT = "arrow_right"
    HOME = "home"
    END = "end"
    PAGE_UP = "page_up"
    PAGE_DOWN = "page_down"

    # Editing
    ENTER = "enter"
    NUMPAD_ENTER = "numpad_enter"
    BACKSPACE = "backspace"
    DELETE = "delete"
    INSERT = "insert"
    TAB = "tab"
    ESCAPE = "escape"
    SPACE = "space"

    # Lock keys
    CAPS_LOCK = "caps_lock"
    NUM_LOCK = "num_lock"
    SCROLL_LOCK = "scroll_lock"

    # Symbols
    BACKTICK = "`"
    MINUS = "-"
    EQUALS = "="
    LEFT_BRACKET = "["
    RIGHT_BRACKET = "]"
    BACKSLASH = "\\"
    SEMICOLON = ";"
    APOSTROPHE = "'"
    COMMA = ","
    PERIOD = "."
    SLASH = "/"

    # Numpad
    NUMPAD_0 = "numpad_0"
    NUMPAD_1 = "numpad_1"
    NUMPAD_2 = "numpad_2"
    NUMPAD_3 = "numpad_3"
    NUMPAD_4 = "numpad_4"
    NUMPAD_5 = "numpad_5"
    NUMPAD_6 = "numpad_6"
    NUMPAD_7 = "numpad_7"
    NUMPAD_8 = "numpad_8"
    NUMPAD_9 = "numpad_9"
    NUMPAD_ADD = "numpad_add"
    NUMPAD_SUBTRACT = "numpad_subtract"
    NUMPAD_MULTIPLY = "numpad_multiply"
    NUMPAD_DIVIDE = "numpad_divide"
    NUMPAD_DECIMAL = "numpad_decimal"

    # Media
    MEDIA_PLAY_PAUSE = "media_play_pause"
    MEDIA_STOP = "media_stop"
    MEDIA_NEXT = "media_next"
    MEDIA_PREV = "media_prev"
    VOLUME_UP = "volume_up"
    VOLUME_DOWN = "volume_down"
    VOLUME_MUTE = "volume_mute"

    # System
    PRINT_SCREEN = "print_screen"
    PAUSE = "pause"
    CONTEXT_MENU = "context_menu"

    # Mouse
    MOUSE_LEFT = "mouse_left"
    MOUSE_RIGHT = "mouse_right"
    MOUSE_MIDDLE = "mouse_middle"
    MOUSE_X1 = "mouse_x1"
    MOUSE_X2 = "mouse_x2"
    MOUSE_WHEEL_UP = "mouse_wheel_up"
    MOUSE_WHEEL_DOWN = "mouse_wheel_down"


class CreateApplication(BaseModel):
    name: str
    color: str


class Application(CreateApplication):
    application_id: int
    model_config = ConfigDict(from_attributes=True)


class CreateShortcutCategory(BaseModel):
    name: str
    app_id: int


class ShortcutCategory(BaseModel):
    category_id: int
    name: str
    app: Application
    model_config = ConfigDict(from_attributes=True)


class CreateShortcut(BaseModel):
    name: str
    keystrokes: list[str]
    category_id: int


class UpdateShortcut(BaseModel):
    name: str | None = None
    keystrokes: list[str] | None = None


class Shortcut(BaseModel):
    shortcut_id: int
    name: str
    keystrokes: list[str]
    category: ShortcutCategory
    model_config = ConfigDict(from_attributes=True)
