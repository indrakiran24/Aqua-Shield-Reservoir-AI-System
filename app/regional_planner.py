import math
from .location_engine import get_coordinates, get_weather, get_nearby_water_bodies

def regional_water_plan(place: str, latest_analysis: dict):


    if latest_analysis is None:
        return {"error": "Run reservoir analysis first"}

    lat, lon = get_coordinates(place)

    if not lat:
        return {"error": "Location not found"}

    rainfall = get_weather(lat, lon)
    nearby = get_nearby_water_bodies(lat, lon)

    risk = latest_analysis["risk"]
    storage = latest_analysis["storage_percent"]
    days_left = latest_analysis["days_left"]

    recommendations = []

    # ----- Drought mitigation -----
    if risk == "Drought Risk" or storage < 35:
        recommendations.append(
            "Initiate water sharing request from nearby reservoirs."
        )
        recommendations.append(
            "Open irrigation feeder canals for controlled inflow transfer."
        )
        recommendations.append(
            f"Current supply lasts only {days_left} days. Immediate external support required."
        )

    # ----- Flood mitigation -----
    elif risk == "Flood Risk":
        recommendations.append(
            "Start controlled downstream water release immediately."
        )
        recommendations.append(
            "Coordinate with downstream reservoirs to receive excess water."
        )
        recommendations.append(
            "Inspect spillway gates and activate flood buffer storage zones."
        )

    # ----- Normal -----
    else:
        recommendations.append(
            "Maintain current operating policy and monitor rainfall forecast."
        )
        if rainfall > 50:
            recommendations.append(
                "Heavy rainfall predicted. Prepare pre-release plan to create buffer storage."
            )

    return {
        "location": place,
        "predicted_rainfall_mm": rainfall,
        "nearby_water_bodies": nearby,
        "recommendations": recommendations
    }

