import streamlit as st
import requests
import plotly.graph_objects as go
import streamlit as st

# Sidebar logout
with st.sidebar:
    st.markdown("---")
    st.markdown("## Account")

    logout = st.button("Logout", use_container_width=True)

    if logout:
        st.session_state.logged_in = False
        st.session_state.analysis_result = None
        st.session_state.chat_history = []
        st.session_state.logged_in = False
        st.switch_page("pages/0_login.py")


if "logged_in" not in st.session_state:
    st.warning("Please login first.")
    st.stop()


st.set_page_config(page_title="AQUA SHIELD-Reservoir AI System", layout="wide")

# ---------- SESSION STATE INITIALIZATION ----------

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "show_report" not in st.session_state:
    st.session_state.show_report = False

if "mode_memory" not in st.session_state:
    st.session_state.mode_memory = "Dashboard"

# ---------- ALERT BANNER FUNCTION ----------

def show_alert_banner(risk):

    if risk == "Flood Risk":
        st.error("🚨 FLOOD WARNING: Reservoir level is critically high. Controlled water release recommended immediately.")

    elif risk == "Drought Risk":
        st.warning("⚠️ LOW STORAGE WARNING: Reservoir water level is critically low. Water conservation measures required.")

    elif risk == "Normal":
        st.success("✅ Reservoir Status Normal: Water levels are within safe operating limits.")


# -------- PAGE SWITCHER --------
mode = st.sidebar.radio(
    "Select Mode",
    ["Dashboard", "AI Assistant", "Regional Planning"]
)

# detect mode change
if mode != st.session_state.mode_memory:
    st.session_state.mode_memory = mode
    st.session_state.show_report = False


if mode == "Dashboard":
    
    # Show alert if analysis exists
    if st.session_state.analysis_result is not None:
        show_alert_banner(st.session_state.analysis_result["risk"])


    st.title("AI Water Reservoir Monitoring & Decision System")

# ---------------- INPUT SECTION ----------------

st.header("Enter Reservoir Data")

col1, col2 = st.columns(2)

with col1:
    rainfall = st.number_input("Rainfall (mm)", min_value=0.0)
    inflow = st.number_input("Inflow (MCM/day)", min_value=0.0)
    outflow = st.number_input("Outflow (MCM/day)", min_value=0.0)
    evaporation = st.number_input("Evaporation Loss (MCM/day)", min_value=0.0)

with col2:
    demand = st.number_input("Daily Water Demand (MCM/day)", min_value=0.0)
    level = st.number_input("Current Reservoir Level (MCM)", min_value=0.0)
    capacity = st.number_input("Total Reservoir Capacity (MCM)", min_value=1.0)

# ---------------- ANALYZE BUTTON ----------------

if st.button("Analyze Reservoir"):

    data = {
        "rainfall": rainfall,
        "inflow": inflow,
        "outflow": outflow,
        "evaporation": evaporation,
        "demand": demand,
        "level": level,
        "capacity": capacity
    }

    result = requests.post("http://127.0.0.1:8000/analyze", json=data).json()

    # SAVE result locally
    st.session_state.analysis_result = result

    # allow report only in dashboard
    if mode == "Dashboard":
        st.session_state.show_report = True

    # reset chatbot
    st.session_state.chat_history = []


    # ---------------- DISPLAY ANALYSIS ----------------

    st.subheader("Reservoir Analysis Summary")

    c1, c2, c3, c4 = st.columns(4)
    data = st.session_state.analysis_result
    c1.metric("Storage %", f"{data['storage_percent']}%")
    c2.metric("Net Flow", f"{data['net_flow']} MCM/day")
    c3.metric("Days Remaining", f"{data['days_left']} days")
    c4.metric("Risk Status", data['risk'])

    # ---------------- GAUGE CHART ----------------

    st.subheader("Reservoir Storage Level")

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=result["storage_percent"],
        title={'text': "Storage Percentage"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "blue"},
            'steps': [
                {'range': [0, 25], 'color': "#ff4b4b"},   # drought
                {'range': [25, 60], 'color': "#f7b500"},  # warning
                {'range': [60, 100], 'color': "#2ecc71"}  # safe
            ],
        }
    ))

    st.plotly_chart(gauge, use_container_width=True)

    # ---------------- INFLOW OUTFLOW BAR CHART ----------------

    st.subheader("Water Flow Comparison")

    flow_chart = go.Figure()

    flow_chart.add_trace(go.Bar(
        x=["Inflow", "Outflow", "Evaporation"],
        y=[inflow, outflow, evaporation],
        marker_color=["green", "red", "orange"]
    ))

    flow_chart.update_layout(
        title="Daily Water Movement",
        yaxis_title="MCM/day"
    )

    st.plotly_chart(flow_chart, use_container_width=True)

    # -------- AI REPORT (ONLY DASHBOARD) --------
if mode == "Dashboard" and st.session_state.show_report and st.session_state.analysis_result is not None:

    st.subheader("AI Generated Management Report")

    try:
        with st.spinner("AI is analyzing reservoir condition..."):
            response = requests.get("http://127.0.0.1:8000/ai_report", timeout=180)

            if response.status_code == 200:
                data = response.json()
                if "report" in data:
                    st.write(data["report"])
                else:
                    st.warning("AI report not available.")
            else:
                st.warning("Backend could not generate report.")

    except:
        st.warning("AI model still loading. Please retry.")

st.subheader("Download Report")

st.markdown(
    "[📄 Download Report](http://127.0.0.1:8000/download_report)",
    unsafe_allow_html=True
)


# -------- AI ASSISTANT MODE --------
if mode == "AI Assistant":
    
    # Show current reservoir status
    if st.session_state.analysis_result is not None:
        show_alert_banner(st.session_state.analysis_result["risk"])

    
    if st.session_state.analysis_result is None:
        st.warning("Please analyze reservoir data first in Dashboard mode.")
        st.stop()


    st.title("Reservoir AI Operator Assistant")

    # Require analysis first
    if st.session_state.analysis_result is None:
        st.warning("Please analyze reservoir data in Dashboard mode first.")
        st.stop()

    st.write("Ask operational or safety questions about the reservoir.")

    # user input
    user_question = st.text_input("Ask a question:")

    if st.button("Send") and user_question.strip() != "":

        response = requests.post(
            "http://127.0.0.1:8000/ask",
            json={"question": user_question}
        )

        data = response.json()

        if "answer" in data:
            answer = data["answer"]
        else:
            answer = "AI could not generate a response."

        # store chat
        st.session_state.chat_history.append(("You", user_question))
        st.session_state.chat_history.append(("AI", answer))

    # display conversation
    st.subheader("Conversation")

    for speaker, message in st.session_state.chat_history:
        if speaker == "You":
            st.markdown(f"**🧑 You:** {message}")
        else:
            st.markdown(f"**🤖 AI:** {message}")

# -------- REGIONAL PLANNING MODE --------

if mode == "Regional Planning":
    st.title("🌍 Regional Water Coordination System")

    if st.session_state.analysis_result is None:
        st.warning("Please analyze reservoir data first in Dashboard mode.")
        st.stop()

    st.write("Plan inter-reservoir water sharing and flood mitigation using nearby reservoirs and rainfall forecast.")

    place = st.text_input("Enter District / Dam Location")

    if st.button("Generate Regional Plan"):

        with st.spinner("Analyzing nearby reservoirs and rainfall forecast..."):

            try:
                res = requests.get(f"http://127.0.0.1:8000/regional_plan?place={place}", timeout=120)
                data = res.json()

                if "error" in data:
                    st.error(data["error"])

                else:
                    st.subheader("Rainfall Forecast")
                    st.info(f"Predicted Rainfall (3 days): {data['predicted_rainfall_mm']} mm")

                    st.subheader("Nearby Water Bodies")

                    if len(data["nearby_water_bodies"]) == 0:
                        st.warning("No mapped reservoirs found nearby.")
                    else:
                        for w in data["nearby_water_bodies"]:
                            st.write("•", w)

                    st.subheader("Recommended Actions")

                    for r in data["recommendations"]:
                        st.success(r)

            except:
                st.error("Backend not reachable. Make sure FastAPI server is running.")

