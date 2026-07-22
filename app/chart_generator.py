import plotly.graph_objects as go
import os

def generate_charts(analysis):

    if not os.path.exists("data"):
        os.makedirs("data")

    # ---------- GAUGE CHART ----------
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=analysis["storage_percent"],
        title={'text': "Reservoir Storage Percentage"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "blue"},
            'steps': [
                {'range': [0, 25], 'color': "red"},
                {'range': [25, 60], 'color': "yellow"},
                {'range': [60, 100], 'color': "green"}
            ],
        }
    ))

    gauge_path = "data/gauge_chart.png"
    gauge.write_image(gauge_path, width=600, height=400)

    # ---------- FLOW BAR CHART ----------
    flow = go.Figure(data=[
        go.Bar(
            x=["Net Flow"],
            y=[analysis["net_flow"]]
        )
    ])

    flow.update_layout(
        title="Daily Net Water Flow",
        yaxis_title="MCM/day"
    )

    flow_path = "data/flow_chart.png"
    flow.write_image(flow_path, width=600, height=400)

    return gauge_path, flow_path
