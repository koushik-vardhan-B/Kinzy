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

## Try With Prompts

Math Games

1."Create a kid-friendly math addition game for ages 6–8 with five questions and a score counter"

2."Build a multiplication tables quiz for ages 8-10 where kids practice 2x to 10x tables with 10 random questions and instant feedback"

3."Make a fun fractions comparison game where kids choose which fraction is bigger, with visual pie charts and 8 questions"

Language Arts

4."Create a spelling bee game for 7-year-olds with 10 simple words, audio pronunciation hints, and a lives system"

5."Build a word scramble game where kids unscramble 8 animal names with hints and a timer"

Science

6."Make a solar system quiz for ages 9-12 with questions about planets, moons, and the sun with fun facts after each answer"

7."Create a matching game where kids match animals to their habitats (ocean, jungle, desert, arctic) with drag and drop"

Geography

8."Build a capital cities quiz game for ages 10-14 with 10 questions about European countries and their capitals"

Logic & Patterns

9."Create a pattern completion game for ages 5-7 where kids identify what comes next in color/shape sequences"

10."Make a simple memory card matching game with 8 pairs of emoji cards for young children"
