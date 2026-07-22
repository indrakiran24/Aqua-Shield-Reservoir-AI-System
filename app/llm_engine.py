import requests

def generate_ai_report(analysis):

    prompt = f"""
You are a government dam water management officer.

Write a professional reservoir status report.

STRICT RULES:
- Do NOT give tasks, instructions, or exercises.
- Do NOT add training questions.
- Do NOT add "Instruction" sections.
- Only write a real-world report.

Reservoir Data:
Storage Percentage: {analysis['storage_percent']}%
Net Flow: {analysis['net_flow']} MCM/day
Remaining Supply Days: {analysis['days_left']}
Risk Level: {analysis['risk']}

Format the output EXACTLY like this:

Current Condition:
(Explain current water situation)

Future Outlook:
(Explain what may happen)

Recommended Action:
(What dam authorities should do)
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3:mini",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "top_p": 0.9,
                "num_predict": 350
            }
        },
        timeout=180
    )
    

    return response.json()["response"]



def ask_question(question, analysis):

    context = f"""
Reservoir Information:
Storage Percentage: {analysis['storage_percent']}%
Net Flow: {analysis['net_flow']} MCM/day
Remaining Supply Days: {analysis['days_left']}
Risk Level: {analysis['risk']}
"""

    prompt = f"""
You are a reservoir operations assistant.

Answer the user's question using ONLY the reservoir data provided.
Do not invent numbers.

{context}

User Question:
{question}

Give a clear practical answer.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3:mini",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3
            }
        },
        timeout=180
    )

    return response.json()["response"]
