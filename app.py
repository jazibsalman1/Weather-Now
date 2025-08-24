from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests
import uvicorn
import os

app = FastAPI()

# Static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates (HTML)
templates = Jinja2Templates(directory="templates")

# OpenWeather API key
API_KEY = "4e2ef117419dfaa3d936769ec870005c"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/weather", response_class=HTMLResponse)
async def get_weather(request: Request, city: str = Form(...)):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()

    if response.get("cod") != 200:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": "❌ City not found!"}
        )

    weather_data = {
        "city": response["name"],
        "temperature": response["main"]["temp"],
        "description": response["weather"][0]["description"].title(),
        "icon": response["weather"][0]["icon"],
        "humidity": response["main"]["humidity"],
        "wind_speed": response["wind"]["speed"],
    }

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "weather": weather_data}
    )


if __name__ == "__main__":
    # Render requires binding to 0.0.0.0 and the PORT env variable
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
