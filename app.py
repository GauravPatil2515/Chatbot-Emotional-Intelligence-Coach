from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from pathlib import Path
import httpx, os

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

HERE = Path(__file__).parent

PROMPT = "You are an Emotional Intelligence Coach. Analyze the user's emotional tone and feelings from their message. Identify specific emotions, provide empathetic validation, then give 3-4 concrete actionable social skills coaching tips. Be warm but direct. Keep response under 150 words."

KEYWORDS = {
    "happy": "happy joy excited great wonderful amazing love glad awesome fantastic good proud grateful thankful",
    "sad": "sad depressed unhappy miserable lonely crying hurt pain sorry disappointed down hopeless empty",
    "angry": "angry mad furious annoyed frustrated hate rage irritated upset disgusted bitter resentful",
    "anxious": "anxious worried nervous stressed overwhelmed panic afraid scared fear dread uneasy tense",
    "confused": "confused lost uncertain unsure puzzled bewildered stuck torn conflicted indecisive"
}

TIPS = {
    "happy": "Detected tone: HAPPY\n\nYour positive energy is wonderful! Here's how to maximize it:\n\n1) Share this feeling with someone - positivity is contagious and deepens bonds\n2) Note exactly what triggered this joy so you can recreate it\n3) Use this confident mood to have a conversation you've been putting off\n4) Practice expressing gratitude to someone who contributed to your happiness",
    "sad": "Detected tone: SAD\n\nI hear the heaviness in your words. Here's your coaching plan:\n\n1) Name the exact feeling - is it grief, disappointment, or loneliness? Precision helps processing\n2) Allow yourself to feel it without judgment - suppression backfires\n3) Reach out to one trusted person today - vulnerability builds authentic connection\n4) Try 5-4-3-2-1 grounding: name 5 things you see, 4 you hear, 3 you touch, 2 you smell, 1 you taste",
    "angry": "Detected tone: ANGRY\n\nI sense strong frustration. Let's work through it constructively:\n\n1) Pause - take 3 slow deep breaths before responding to anyone\n2) Identify the boundary that was crossed - anger often signals unmet needs\n3) Express yourself using 'I feel... when... because...' format instead of accusations\n4) Channel the energy physically - even a 5-minute walk resets your nervous system",
    "anxious": "Detected tone: ANXIOUS\n\nI notice worry in your words. Let's ground you:\n\n1) Feel your feet on the floor right now - anchor to the present\n2) Challenge the thought: what's the actual probability of your worst fear?\n3) Focus only on what you can control in the next hour, nothing more\n4) Box breathing: inhale 4 seconds, hold 4, exhale 4, hold 4 - repeat 4 times",
    "confused": "Detected tone: CONFUSED\n\nUncertainty is uncomfortable but completely normal. Try this:\n\n1) Separate what you DO know from what you DON'T - write it down\n2) Ask one specific clarifying question to the right person\n3) Accept that not everything needs an immediate answer - sit with ambiguity\n4) Trust your track record - you've navigated uncertainty before successfully",
    "neutral": "Detected tone: BALANCED\n\nGreat emotional baseline! Perfect time to build EQ skills:\n\n1) In your next conversation, practice active listening - paraphrase what you hear\n2) Try mirroring someone's body language subtly - it builds rapport\n3) Ask one open-ended question today to deepen a relationship\n4) Reflect on your last social interaction - what went well and what would you change?"
}

class Req(BaseModel):
    data: str = ""

def detect(text):
    t = text.lower()
    best, score = "neutral", 0
    for emo, words in KEYWORDS.items():
        s = sum(1 for w in words.split() if w in t)
        if s > score:
            best, score = emo, s
    return best

def fallback(text):
    if not text.strip():
        return "Welcome to your EQ Coach! Share how you're feeling or describe a social situation, and I'll provide personalized emotional intelligence coaching."
    return TIPS[detect(text)]

async def ai_call(text):
    for key_name, url, model in [
        ("GROQ_API_KEY", "https://api.groq.com/openai/v1/chat/completions", "llama-3.3-70b-versatile"),
        ("OPENROUTER_API_KEY", "https://openrouter.ai/api/v1/chat/completions", "meta-llama/llama-3.3-70b-instruct:free"),
    ]:
        key = os.environ.get(key_name)
        if not key:
            continue
        try:
            async with httpx.AsyncClient(timeout=8) as c:
                r = await c.post(url, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}, json={"model": model, "messages": [{"role": "system", "content": PROMPT}, {"role": "user", "content": text}], "max_tokens": 300})
                if r.status_code == 200:
                    return r.json()["choices"][0]["message"]["content"]
        except Exception:
            continue
    return None

@app.get("/")
async def home():
    return HTMLResponse((HERE / "index.html").read_text())

@app.post("/solve")
async def solve(req: Req):
    text = req.data or ""
    result = await ai_call(text) if text.strip() else None
    return {"output": result or fallback(text)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
