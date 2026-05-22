import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.schema import Application, Base, Shortcut, ShortcutCategory
from database.session import _SessionLocal, engine

SEED = [
    {
        "name": "Neovim",
        "color": "#4caf50",
        "categories": [
            {
                "name": "Navigation",
                "shortcuts": [
                    {"name": "move left / down / up / right", "keystrokes": ["h", "j", "k", "l"]},
                    {"name": "jump to line start",             "keystrokes": ["0"]},
                    {"name": "jump to line end",               "keystrokes": ["$"]},
                    {"name": "go to file top",                 "keystrokes": ["gg"]},
                    {"name": "go to file bottom",              "keystrokes": ["G"]},
                    {"name": "next word",                      "keystrokes": ["w"]},
                    {"name": "previous word",                  "keystrokes": ["b"]},
                ],
            },
            {
                "name": "Editing",
                "shortcuts": [
                    {"name": "insert mode",           "keystrokes": ["i"]},
                    {"name": "insert at end of line", "keystrokes": ["A"]},
                    {"name": "new line below",        "keystrokes": ["o"]},
                    {"name": "delete char",           "keystrokes": ["x"]},
                    {"name": "delete line",           "keystrokes": ["dd"]},
                    {"name": "yank line",             "keystrokes": ["yy"]},
                    {"name": "paste below",           "keystrokes": ["p"]},
                ],
            },
            {
                "name": "Buffers & Windows",
                "shortcuts": [
                    {"name": "next buffer",       "keystrokes": ["]", "b"]},
                    {"name": "close buffer",      "keystrokes": ["leader", "bd"]},
                    {"name": "split horizontal",  "keystrokes": ["ctrl", "w", "s"]},
                    {"name": "split vertical",    "keystrokes": ["ctrl", "w", "v"]},
                    {"name": "focus next window", "keystrokes": ["ctrl", "w", "w"]},
                ],
            },
            {
                "name": "Search & Replace",
                "shortcuts": [
                    {"name": "search forward",     "keystrokes": ["/"]},
                    {"name": "search backward",    "keystrokes": ["?"]},
                    {"name": "next match",         "keystrokes": ["n"]},
                    {"name": "prev match",         "keystrokes": ["N"]},
                    {"name": "substitute in line", "keystrokes": [":s/old/new"]},
                    {"name": "substitute in file", "keystrokes": [":%s/old/new/g"]},
                ],
            },
        ],
    },
    {
        "name": "tmux",
        "color": "#2196f3",
        "categories": [
            {
                "name": "Sessions",
                "shortcuts": [
                    {"name": "new session",    "keystrokes": ["prefix", ":new"]},
                    {"name": "list sessions",  "keystrokes": ["prefix", "s"]},
                    {"name": "rename session", "keystrokes": ["prefix", "$"]},
                    {"name": "detach",         "keystrokes": ["prefix", "d"]},
                ],
            },
            {
                "name": "Windows",
                "shortcuts": [
                    {"name": "new window",    "keystrokes": ["prefix", "c"]},
                    {"name": "next window",   "keystrokes": ["prefix", "n"]},
                    {"name": "prev window",   "keystrokes": ["prefix", "p"]},
                    {"name": "rename window", "keystrokes": ["prefix", ","]},
                    {"name": "close window",  "keystrokes": ["prefix", "&"]},
                ],
            },
            {
                "name": "Panes",
                "shortcuts": [
                    {"name": "split horizontal",   "keystrokes": ["prefix", '"']},
                    {"name": "split vertical",     "keystrokes": ["prefix", "%"]},
                    {"name": "close pane",         "keystrokes": ["prefix", "x"]},
                    {"name": "move between panes", "keystrokes": ["prefix", "arrow"]},
                    {"name": "zoom pane",          "keystrokes": ["prefix", "z"]},
                ],
            },
        ],
    },
]


def main():
    Base.metadata.create_all(engine)

    with _SessionLocal() as session:
        for app_data in SEED:
            app = Application(name=app_data["name"], color=app_data["color"])
            session.add(app)
            session.flush()

            for cat_data in app_data["categories"]:
                cat = ShortcutCategory(name=cat_data["name"], app_id=app.application_id)
                session.add(cat)
                session.flush()

                for sc_data in cat_data["shortcuts"]:
                    session.add(Shortcut(
                        name=sc_data["name"],
                        keystrokes=sc_data["keystrokes"],
                        category_id=cat.category_id,
                    ))

        session.commit()
        print("Seeded Neovim and tmux data.")


if __name__ == "__main__":
    main()
