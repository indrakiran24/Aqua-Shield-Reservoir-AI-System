import requests
from geopy.geocoders import Nominatim

# Convert area name to coordinates
def get_coordinates(place):
    geolocator = Nominatim(user_agent="reservoir_ai")
    location = geolocator.geocode(place)

    if location:
        return location.latitude, location.longitude
    else:
        return None, None


# Get rainfall forecast
def get_weather(lat, lon):

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&hourly=precipitation&forecast_days=3"
    )

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()

        data = response.json()

        rain = data["hourly"]["precipitation"]

        return sum(rain)

    except Exception as e:
        print("Weather API Error:", e)
        return 0


# Find nearby water bodies
def get_nearby_water_bodies(lat, lon):

    overpass_url = "https://overpass-api.de/api/interpreter"

    query = f"""
    [out:json];
    (
      node(around:20000,{lat},{lon})["water"="reservoir"];
      node(around:20000,{lat},{lon})["natural"="water"];
      way(around:20000,{lat},{lon})["water"="lake"];
      way(around:20000,{lat},{lon})["waterway"="dam"];
    );
    out center;
    """

    try:
        response = requests.get(
            overpass_url,
            params={"data": query},
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

    except Exception as e:
        print("Overpass Error:", e)
        print(response.text if 'response' in locals() else "")
        return []

    places = []

    for element in data.get("elements", []):

        tags = element.get("tags", {})

        if "name" in tags:
            places.append(tags["name"])

    return list(set(places))