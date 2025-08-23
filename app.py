from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests
import uvicorn

app = FastAPI()

# Static files (CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

API_KEY = "4e2ef117419dfaa3d936769ec870005c"  # OpenWeather API key

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
    uvicorn.run(app, host="0.0.0.0", port=8000)
