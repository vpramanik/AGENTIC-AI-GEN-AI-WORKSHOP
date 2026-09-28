import requests

# ======= ORIGINAL CODE (open-meteo.com - blocked on college network) =======
# def get_weather(latitude, longitude):
#     weather_url = "https://api.open-meteo.com/v1/forecast"
#     weather_params = {
#         "latitude": latitude,
#         "longitude": longitude,
#         "current_weather": "true",
#     }
#
#     weather_response = requests.get(weather_url, params=weather_params)
#     weather_response.raise_for_status()
#
#     result = weather_response.json()["current_weather"]
#     # print("result=", result)
#     return result
#
#
# functions = {"get_weather": get_weather}
#
# tools = [
#     {
#         "type": "function",
#         "function": {
#             "name": "get_weather",
#             "description": "Get current weather for a location. Infer the latitude and longitude yourself from the place name.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {"latitude": {"type": "number"}, "longitude": {"type": "number"}},
#                 "required": ["latitude", "longitude"],
#             },
#         },
#     }
# ]
# ======= END ORIGINAL CODE =======


# ======= NEW CODE (wttr.in - works on college network) =======
def get_weather(city):
    url = f"https://wttr.in/{city}?format=j1"
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "curl"})
        response.raise_for_status()
        data = response.json()
        current = data["current_condition"][0]
        result = {
            "temperature_C": current["temp_C"],
            "temperature_F": current["temp_F"],
            "feels_like_C": current["FeelsLikeC"],
            "humidity": current["humidity"] + "%",
            "weather": current["weatherDesc"][0]["value"],
            "wind_speed_kmph": current["windspeedKmph"],
            "wind_direction": current["winddir16Point"],
        }
        return result
    except requests.exceptions.ConnectionError:
        return "Error: Cannot connect to weather API. Check your internet connection."
    except requests.exceptions.Timeout:
        return "Error: Weather API request timed out."
    except Exception as e:
        return f"Error fetching weather: {e}"


functions = {"get_weather": get_weather}

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city or location by name.",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string", "description": "City name, e.g. 'Delhi', 'Mumbai', 'New York'"}},
                "required": ["city"],
            },
        },
    }
]
# ======= END NEW CODE =======
