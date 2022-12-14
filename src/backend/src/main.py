# This is to write the backend
from fastapi import FastAPI
import sys
import os
from pathlib import Path
sys.path.insert(0,os.path.join(Path(__file__).parents[0],"router"))
from user import router as user_router
from post import router as post_router
from authentication import router as authentication_router

app = FastAPI()
app.include_router(router= user_router)
app.include_router(router= post_router)
app.include_router(router= authentication_router)
