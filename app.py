from fastapi import FastAPI
from pyowm import OWM
from pyowm.utils.config import get_default_config
from pyowm.utils import timestamps
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import setuptools
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import requests

app = FastAPI()
try:
    owm = OWM('YOUR_OWM_API_KEY')  # Replace with your OWM API key
except Exception as e:
    print(f"Error initializing OWM: {e}")
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/")
async def read_index(request: Request):
    return FileResponse('static/index.html')

