from fastapi import FastAPI
from .analytics import analyze_reservoir
from .llm_engine import generate_ai_report, ask_question
from fastapi.responses import FileResponse
from .pdf_report import create_pdf
from .llm_engine import generate_ai_report
from . import models
from .models import User
from .database import SessionLocal, engine
from .models import User, ReservoirData
from .auth import hash_password, verify_password
from .schemas import RegisterSchema, LoginSchema
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from .schemas import RegisterSchema
from .auth import hash_password
from .location_engine import get_coordinates, get_weather, get_nearby_water_bodies
from .regional_planner import regional_water_plan

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
@app.post("/register")
def register(user: RegisterSchema, db: Session = Depends(get_db)):

    # check existing username
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # create new user
    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


from fastapi import HTTPException
from .schemas import LoginSchema
from .auth import verify_password

@app.post("/login")
def login(user: LoginSchema, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    return {"message": "Login successful"}



@app.get("/")
def home():
    return {"message": "Reservoir AI Backend Running"}


@app.post("/analyze")
def analyze(data: dict):
    global latest_analysis
    latest_analysis = analyze_reservoir(data)
    return latest_analysis

@app.get("/ai_report")
def ai_report():
    if latest_analysis is None:
        return {"error": "No analysis yet"}

    report = generate_ai_report(latest_analysis)
    return {"report": report}

@app.post("/ask")
def ask(data: dict):
    global latest_analysis

    if latest_analysis is None:
        return {"answer": "Please go to Dashboard mode and analyze reservoir data first."}

    try:
        question = data.get("question", "")
        answer = ask_question(question, latest_analysis)
        return {"answer": answer}

    except Exception as e:
        return {"error": str(e)}


@app.get("/download_report")
def download_report():

    global latest_analysis

    if latest_analysis is None:
        return {"error": "Analyze reservoir first"}

    # generate AI text
    ai_text = generate_ai_report(latest_analysis)

    # create pdf
    path = create_pdf(latest_analysis, ai_text)

    return FileResponse(path, filename="reservoir_report.pdf", media_type="application/pdf")


@app.get("/location_analysis")
def location_analysis(place: str):

    lat, lon = get_coordinates(place)

    if not lat:
        return {"error": "Location not found"}

    rainfall = get_weather(lat, lon)
    nearby = get_nearby_water_bodies(lat, lon)

    return {
        "latitude": lat,
        "longitude": lon,
        "predicted_rainfall_mm": rainfall,
        "nearby_water_bodies": nearby
    }
    
@app.get("/regional_plan")
def regional_plan(place: str):


    global latest_analysis

    if latest_analysis is None:
        return {"error": "Analyze reservoir first in dashboard"}

    result = regional_water_plan(place, latest_analysis)
    return result

