import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fastapi import FastAPI
from admin.router import admin_router
from shortcuts.router import shortcuts_router


routes: dict[str, FastAPI] = {
    "admin": admin_router,
    "shortcuts": shortcuts_router,
}

app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True}

for name, route in routes.items():
    app.mount(f"/{name}", route)
