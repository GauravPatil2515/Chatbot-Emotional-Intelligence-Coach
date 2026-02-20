# EQ Coach - Emotional Intelligence Coaching Chatbot

A chatbot that analyzes user tone and facial expressions (via camera) to provide real-time social skills coaching.

## Demo

[Live Demo](https://your-app.vercel.app)

## Features

- Real-time emotional tone analysis from text input
- Camera self-awareness mirror for expression coaching
- AI-powered coaching via Groq/OpenRouter with local fallback
- Detects: happy, sad, angry, anxious, confused, neutral states
- Actionable social skills tips for each emotional state

## Deploy to Vercel

1. Push this repo to GitHub
2. Go to [vercel.com](https://vercel.com) and sign in
3. Click **Add New Project** → Import the GitHub repository
4. Under **Environment Variables**, add the keys below
5. Click **Deploy**
6. Your app is live at the provided `.vercel.app` URL

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | No | Groq API key (primary AI provider) |
| `OPENROUTER_API_KEY` | No | OpenRouter API key (fallback AI provider) |
| `HUGGINGFACE_API_KEY` | No | HuggingFace API key (reserved) |

If no API keys are set, the app uses local deterministic emotion detection and coaching.

## Local Run

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

Open http://localhost:8000

## API

**POST /solve**

Request:
```json
{"data": "I'm feeling really stressed about my presentation tomorrow"}
```

Response:
```json
{"output": "Detected tone: ANXIOUS\n\n1) Feel your feet on the floor..."}
```

## Tech Stack

- Backend: Python FastAPI
- Frontend: Single HTML file (no frameworks)
- AI: Groq / OpenRouter with local fallback
- Deployment: Vercel
