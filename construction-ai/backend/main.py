import os
import base64
import requests
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Construction Intelligence Platform")

# Allow the React app to call this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

# Each feature is just a different instruction (prompt) for the AI.
PROMPTS = {
    "safety": (
        "You are a construction site safety officer. Look at the input and list "
        "safety problems (missing helmets, open edges, bad scaffolding, etc.). "
        "Give each problem a risk level (Low/Medium/High) and one fix."
    ),
    "cracks": (
        "You are a structural inspector. Check the image or text for cracks or "
        "damage. Say where the cracks are, how serious they look, and what "
        "should be done next. Reply in simple points."
    ),
    "valuation": (
        "You are a real estate expert. Based on the input, give a rough "
        "estimate of the property or construction condition and value factors "
        "(location, build quality, condition). Say clearly that this is only an estimate."
    ),
    "planning": (
        "You are a construction project planner. Create a simple step-by-step "
        "plan with tasks, rough time for each, and materials needed."
    ),
    "assistant": (
        "You are a daily site assistant. Answer the question about the "
        "construction site clearly. If weather is mentioned, include weather "
        "advice for work (rain, heat, wind)."
    ),
}


@app.get("/")
def home():
    return {"message": "Construction Intelligence API is running"}


# Note: this is a normal "def" (not "async def") so FastAPI runs it in a
# separate thread. That way a slow AI call does not freeze the whole server.
@app.post("/analyze")
def analyze(
    feature: str = Form(...),
    text: str = Form(""),
    image: UploadFile = File(None),
):
    if not API_KEY:
        return {"error": "GEMINI_API_KEY is not set. Set it and restart the server."}

    instruction = PROMPTS.get(feature, PROMPTS["assistant"])

    # Build the message for the AI: instruction + user text + optional image
    parts = [{"text": f"{instruction}\n\nUser input: {text or 'See the image.'}"}]

    if image is not None:
        image_bytes = image.file.read()
        parts.append(
            {
                "inline_data": {
                    "mime_type": image.content_type or "image/jpeg",
                    "data": base64.b64encode(image_bytes).decode("utf-8"),
                }
            }
        )

    # "low" thinking makes the AI answer faster (default is "medium")
    body = {
        "contents": [{"parts": parts}],
        "generationConfig": {"thinkingConfig": {"thinkingLevel": "low"}},
    }

    try:
        response = requests.post(
            URL, params={"key": API_KEY}, json=body, timeout=90
        )
    except requests.exceptions.Timeout:
        return {"error": "The AI took too long to answer. Please try again."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Could not reach the AI service: {e}"}

    if response.status_code != 200:
        return {"error": f"AI error ({response.status_code}): {response.text}"}

    data = response.json()
    try:
        answer = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        return {"error": f"AI did not return an answer: {data}"}

    return {"feature": feature, "result": answer}