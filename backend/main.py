from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.core.seed import seed_database
from app.countdown.models import Countdown
from app.countdown.routes import router as countdown_router
from app.declarations.models import Declaration
from app.declarations.routes import router as declarations_router
from app.errors import register_error_handlers
from app.romance.models import RomanceQuote
from app.romance.routes import router as romance_router
from app.routine.models import Task
from app.routine.routes import router as routine_router
from app.users.models import User
from app.users.routes import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_database()
    yield


app = FastAPI(
    title="Routine Organizer API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_error_handlers(app)

app.include_router(users_router)
app.include_router(routine_router)
app.include_router(countdown_router)
app.include_router(declarations_router)
app.include_router(romance_router)


@app.get("/")
def health_check():
    return {"status": "ok", "service": "Routine Organizer API"}