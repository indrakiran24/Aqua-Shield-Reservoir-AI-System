# 🌊 AQUA SHIELD – AI Water Reservoir Monitoring & Decision System

> An AI-powered intelligent water resource management system that monitors reservoir conditions, predicts flood and drought risks, generates AI-based operational reports, and assists authorities with regional water coordination.

---

## 📖 Project Overview

AQUA SHIELD is an intelligent reservoir management system developed to support water resource authorities in monitoring reservoir conditions and making informed operational decisions.

The system analyzes real-time reservoir parameters, predicts potential flood and drought situations, generates AI-assisted management reports, and recommends regional water-sharing strategies using location intelligence and weather forecasting.

---

## ✨ Features

### 📊 Reservoir Analysis
- Storage Percentage Calculation
- Net Water Flow Analysis
- Days of Water Supply Remaining
- Automatic Risk Classification
  - ✅ Normal
  - ⚠️ Drought Risk
  - 🚨 Flood Risk

---

### 📈 Interactive Dashboard

- Plotly Gauge Chart
- Water Flow Comparison Charts
- Reservoir Health Metrics
- Real-time Risk Alerts

---

### 🤖 AI Management Report

Generate intelligent operational reports using an LLM (Ollama + Phi-3 Mini).

The report includes:

- Current reservoir condition
- Risk assessment
- Operational recommendations
- Water management strategies
- Safety measures

---

### 💬 AI Reservoir Assistant

Chat with an AI assistant about:

- Reservoir operations
- Water conservation
- Flood management
- Drought preparedness
- Infrastructure safety
- Emergency recommendations

---

### 🌍 Regional Water Coordination

The Regional Planning module provides:

- Nearby reservoir identification
- Rainfall forecast analysis
- Water-sharing recommendations
- Regional flood mitigation planning

---

### 📄 PDF Report Generation

Generate downloadable PDF reports containing:

- Reservoir metrics
- AI-generated report
- Gauge chart
- Water flow chart

---

## 🏗️ System Architecture

```
                    User
                      │
                      ▼
              Streamlit Dashboard
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
 FastAPI Backend              Ollama LLM
        │                           │
        ▼                           ▼
 MySQL Database             AI Report Generation
        │
        ▼
 Location Services
(Open-Meteo + Overpass API)
```

---

## 🛠️ Technologies Used

### Programming Language

- Python

### Backend

- FastAPI
- SQLAlchemy
- Pydantic

### Frontend

- Streamlit

### Database

- MySQL

### AI

- Ollama
- Phi-3 Mini

### Data Visualization

- Plotly

### APIs

- Open-Meteo Weather API
- Overpass API
- OpenStreetMap (Nominatim)

### PDF Generation

- ReportLab

### Authentication

- Passlib (bcrypt)

---

## 📂 Project Structure

```
Aqua-Shield-Reservoir-AI-System
│
├── app/
│   ├── analytics.py
│   ├── auth.py
│   ├── chart_generator.py
│   ├── database.py
│   ├── llm_engine.py
│   ├── location_engine.py
│   ├── main.py
│   ├── models.py
│   ├── pdf_report.py
│   ├── regional_planner.py
│   └── schemas.py
│
├── pages/
│   ├── 0_login.py
│   └── 1_dashboard.py
│
├── requirements.txt
├── main.py
└── README.md
```

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/your-username/Aqua-Shield-Reservoir-AI-System.git
```

### Navigate

```bash
cd Aqua-Shield-Reservoir-AI-System
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configure Database

Create a MySQL database:

```sql
CREATE DATABASE reservoir_ai;
```

Update the database credentials inside:

```
app/database.py
```

---

## 🤖 Install Ollama

Download Ollama:

https://ollama.com/download

Pull the Phi-3 Mini model:

```bash
ollama pull phi3:mini
```

Start Ollama:

```bash
ollama serve
```

---

## ▶️ Run Backend

```bash
uvicorn app.main:app --reload
```

Backend:

```
http://127.0.0.1:8000
```

Swagger Documentation:

```
http://127.0.0.1:8000/docs
```

---

## ▶️ Run Frontend

```bash
streamlit run main.py
```

Frontend:

```
http://localhost:8501
```

---

## 📷 Screenshots

### Login Page

> *(Add screenshot here)*

---

### Dashboard

> *(Add screenshot here)*

---

### AI Generated Report

> *(Add screenshot here)*

---

### AI Assistant

> *(Add screenshot here)*

---

### Regional Planning

> *(Add screenshot here)*

---

## 📌 Future Enhancements

- IoT sensor integration
- Live reservoir monitoring
- Satellite rainfall data
- SMS & Email alerts
- Mobile application
- Machine Learning-based prediction models
- Multi-reservoir optimization
- Cloud deployment

---

## 👨‍💻 Author

**Indrakiran**

B.Tech Computer Science Engineering

Malla Reddy University

GitHub:

https://github.com/indrakiran24

---

## 📜 License

This project is developed for educational and research purposes as a Final Year B.Tech Project.

---

⭐ If you found this project useful, consider giving it a Star on GitHub!
