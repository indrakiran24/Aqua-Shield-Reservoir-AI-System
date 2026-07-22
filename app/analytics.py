def analyze_reservoir(data):

    capacity = float(data["capacity"])
    level = float(data["level"])
    inflow = float(data["inflow"])
    outflow = float(data["outflow"])
    evaporation = float(data["evaporation"])
    demand = float(data["demand"])

    # 1. Storage %
    storage_percent = (level / capacity) * 100

    # 2. Net daily water change
    net_flow = inflow - outflow - evaporation

    # 3. Days of supply remaining
    if demand > 0:
        days_left = level / demand
    else:
        days_left = 0

    # 4. Risk detection
    risk = "Normal"

    if storage_percent > 90 and net_flow > 0:
        risk = "Flood Risk"
    elif storage_percent < 25:
        risk = "Drought Risk"

    return {
        "storage_percent": round(storage_percent, 2),
        "net_flow": round(net_flow, 2),
        "days_left": round(days_left, 2),
        "risk": risk
    }
