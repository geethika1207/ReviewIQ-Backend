from fastapi import FastAPI
from .db import models
from .db.database import engine, Base
from .routers import auth, code, history, dashboard, chat
from fastapi.middleware.cors import CORSMiddleware

#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://lovable.dev", "https://*.lovable.app", "http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(code.router)
app.include_router(history.router)
app.include_router(dashboard.router)
app.include_router(chat.router)