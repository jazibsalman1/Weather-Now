from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import requests

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def homepage(request: Request):
    return FileResponse('static/index.html')

apikey = '4e2ef117419dfaa3d936769ec870005c'

@app.get("/weather")
async def get_weather(city: str):
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&units=metric'
        response = requests.get(url)  
        response_data = response.json()
        
        if response_data.get("cod") != 200:
            return {"error": "City not found"}
        
        weather_data = {
            "city": response_data["name"],
            "temperature": response_data["main"]["temp"],
            "description": response_data["weather"][0]["description"],
            "icon": response_data["weather"][0]["icon"],
            "humidity": response_data["main"]["humidity"],
            "wind_speed": response_data["wind"]["speed"]
        }
        return weather_data
    
    except Exception as e:
        return {"error": "Failed to fetch weather data"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Fixed host to "0.0.0.0"