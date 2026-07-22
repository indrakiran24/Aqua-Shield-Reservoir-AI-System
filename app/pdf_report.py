from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os
from reportlab.platypus import Image
from .chart_generator import generate_charts


def create_pdf(analysis, ai_text):

    filename = "reservoir_report.pdf"
    filepath = os.path.join("data", filename)

    doc = SimpleDocTemplate(filepath, pagesize=A4)

    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("Reservoir Monitoring Report", styles["Title"]))
    story.append(Spacer(1, 20))

    # Date
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    story.append(Paragraph(f"<b>Generated On:</b> {now}", styles["Normal"]))
    story.append(Spacer(1, 20))

    # Analysis Section
    story.append(Paragraph("<b>Reservoir Analysis</b>", styles["Heading2"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph(f"Storage Percentage: {analysis['storage_percent']}%", styles["Normal"]))
    story.append(Paragraph(f"Net Flow: {analysis['net_flow']} MCM/day", styles["Normal"]))
    story.append(Paragraph(f"Remaining Supply Days: {analysis['days_left']}", styles["Normal"]))
    story.append(Paragraph(f"Risk Status: {analysis['risk']}", styles["Normal"]))

    story.append(Spacer(1, 20))

        # -------- ADD CHARTS --------
    gauge_path, flow_path = generate_charts(analysis)

    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>Reservoir Charts</b>", styles["Heading2"]))
    story.append(Spacer(1, 15))

    story.append(Image(gauge_path, width=400, height=260))
    story.append(Spacer(1, 20))
    story.append(Image(flow_path, width=400, height=260))
    story.append(Spacer(1, 20))

    # AI Report Section
    story.append(Paragraph("<b>AI Generated Operational Report</b>", styles["Heading2"]))
    story.append(Spacer(1, 10))

    # Split long text into paragraphs
    for line in ai_text.split("\n"):
        story.append(Paragraph(line, styles["Normal"]))
        story.append(Spacer(1, 8))

    doc.build(story)

    return filepath
