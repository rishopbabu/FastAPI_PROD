from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import posts, users, auth, votes

models.Base.metadata.create_all(bind = engine)

app = FastAPI(
    title="Fast API",
    version="0.1.1",
    description="A simple API to learn Fast API",
    docs_url="/docs/",
    redoc_url="/redoc/",
)

# this api can acces from any domain while giving '*'
origins = ["*"]

# middleware origins like specify domain names
# origins = ["https://www.google.com"
#            "https://www.youtube.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# initial Path
@app.get("/", name="root", tags=['root'])
def home():
    return{"message": "Welcome to FASTAPI"}

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(votes.router)