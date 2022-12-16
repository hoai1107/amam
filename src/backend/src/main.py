# This is to write the backend
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .router.user import router as user_router
from .router.post import router as post_router
from .router.authentication import router as authentication_router

app = FastAPI()
app.include_router(router=user_router)
app.include_router(router=post_router)
app.include_router(router=authentication_router)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
