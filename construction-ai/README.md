# Multimodal Construction Intelligence Platform

An AI-powered web app that helps with construction work. The user uploads a site
photo or types a question, and the AI gives back useful answers.

## Features
- Site safety check
- Crack detection and analysis
- Real estate valuation (rough estimate)
- Construction project planning
- Daily site assistant (with weather advice)

## Tech Stack
- Frontend: React (Vite), HTML5, CSS
- Backend: Python, FastAPI
- AI: Gemini multimodal model (text + image)

## How to run

### Backend
```
cd backend
pip install -r requirements.txt
set GEMINI_API_KEY=your_key_here        (Windows)
export GEMINI_API_KEY=your_key_here     (Mac/Linux)
uvicorn main:app --reload
```
Backend runs at http://localhost:8000

### Frontend
```
cd frontend
npm install
npm run dev
```
Frontend runs at http://localhost:5173

## Deploy
- Backend: Render (start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`,
  add GEMINI_API_KEY as an environment variable)
- Frontend: Vercel (set VITE_API_URL to your Render backend link)
