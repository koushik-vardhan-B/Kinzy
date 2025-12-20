# AI Game Generator

An AI-powered educational game generator built with FastAPI and Google Gemini AI.

🚀 **Live Demo:** [https://kinzy-3.onrender.com/](https://kinzy-3.onrender.com/)

## Setup

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your API key from [Google AI Studio](https://aistudio.google.com/apikey).

## Running the Project

```bash
uvicorn main:app --reload
```

The server starts at `http://localhost:8000`

## How to Generate and Play a Game

1. Open `http://localhost:8000` in your browser
2. Enter a game prompt describing the educational game you want
3. Click **"Generate Game"**
4. Wait for the AI to generate the game
5. Click **"Play Game"** to open it in a new tab

### Example Prompt

> "Create a kid-friendly math addition game for ages 6–8 with five questions and a score counter"

## Project Structure

```
├── main.py              # FastAPI backend
├── requirements.txt     # Python dependencies
├── .env                 # API key (create this)
├── static/
│   └── index.html       # Frontend UI
└── games/               # Generated games (auto-created)
```
