import datetime as dt
import requests
from flask import Flask, render_template
from src.api_call import get_coordinates, get_current_weather, get_historical_weather

app = Flask(__name__)

OWM_ICON = "https://openweathermap.org/img/wn/{code}@2x.png"

@app.route("/")
def index():
    city_name = "Stockholm"                   
    lat, lon = get_coordinates(city_name)     

    now = get_current_weather(lat, lon)
    now_w = now["weather"][0]

    page_data = {
        "temperature_c": int(now["main"]["temp"]),
        "weather": now_w["description"].capitalize(),
        "time": dt.datetime.now().strftime("%B, %d - %Y"),
        "icon": OWM_ICON.format(code=now_w.get("icon", "01d")),
        "city": city_name,                
    }

    last_year_data = None
    try:
        target = (
            dt.datetime.now(dt.timezone.utc)
            .replace(hour=12, minute=0, second=0, microsecond=0)
            - dt.timedelta(days=365)
        )

        hist = get_historical_weather(lat, lon, target)

        payload = hist.get("current")
        if payload is None and "data" in hist and hist["data"]:
            payload = hist["data"][0]

        if payload:
            hw = payload["weather"][0]
            last_year_data = {
                "temperature_c": int(payload["temp"]),
                "weather": hw["description"].capitalize(),
                "date": target.strftime("%B, %d - %Y"),
                "icon": OWM_ICON.format(code=hw.get("icon", "01d")),
                "city": city_name,              
            }

    except requests.HTTPError as e:
        print("History API failed:", e)
    except Exception as e:
        print("History API error:", e)

    return render_template("index.html", page_data=page_data, last_year_data=last_year_data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
