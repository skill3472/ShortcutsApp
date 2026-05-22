import sys
from contextlib import asynccontextmanager
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fastapi import FastAPI
from admin.router import admin_router
from database.schema import Base
from database.session import engine
from shortcuts.router import shortcuts_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(admin_router)
app.include_router(shortcuts_router)


@app.get("/health")
def health():
    return {"ok": True}
