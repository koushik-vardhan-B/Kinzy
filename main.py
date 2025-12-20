"""
AI-Powered Educational Game Generator
FastAPI backend that uses Gemini AI to generate self-contained HTML games.
"""
import os
import uuid
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is required")

genai.configure(api_key=GEMINI_API_KEY)

# Initialize FastAPI app
app = FastAPI(
    title="AI Game Generator",
    description="Generate educational HTML games using Gemini AI"
)

# Create games directory
GAMES_DIR = Path(__file__).parent / "games"
GAMES_DIR.mkdir(exist_ok=True)

# Static files directory
STATIC_DIR = Path(__file__).parent / "static"


# System prompt for game generation
SYSTEM_PROMPT = """You are an expert educational game developer. Your task is to create a complete, self-contained HTML game based on the user's prompt.

CRITICAL REQUIREMENTS:
1. Generate a SINGLE, complete HTML file that includes ALL code
2. Include ALL CSS inside a <style> tag in the <head>
3. Include ALL JavaScript inside a <script> tag before </body>
4. DO NOT use any external libraries, CDNs, or imports
5. The game MUST be playable immediately when opened in a browser
6. Use only vanilla HTML, CSS, and JavaScript

GAME DESIGN GUIDELINES:
1. Make the game educational and age-appropriate based on the prompt
2. Include clear instructions on how to play
3. Implement a scoring system that provides feedback
4. Add visual feedback for correct/incorrect answers (colors, animations)
5. Include a way to restart or play again
6. Make the UI clean, readable, and touch-friendly for children
7. Use bright, engaging colors appropriate for educational games
8. Ensure the game is responsive and works on different screen sizes

OUTPUT FORMAT:
- Return ONLY the HTML code, nothing else
- Do NOT include markdown code blocks or any explanation
- Start with <!DOCTYPE html> and end with </html>
- The response should be valid HTML that can be saved directly as a .html file"""


class GameRequest(BaseModel):
    """Request model for game generation."""
    prompt: str = Field(
        ...,
        min_length=10,
        max_length=1000,
        description="Description of the educational game to generate"
    )


class GameResponse(BaseModel):
    """Response model for generated game."""
    game_id: str
    message: str
    play_url: str


@app.post("/api/generate", response_model=GameResponse)
async def generate_game(request: GameRequest):
    """Generate an educational HTML game based on the user's prompt."""
    try:
        # Initialize the Gemini model
        model = genai.GenerativeModel(
            model_name="gemini-3-flash-preview",
            system_instruction=SYSTEM_PROMPT
        )
        
        # Generate the game
        response = model.generate_content(
            f"Create an educational game: {request.prompt}",
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=8192,
            )
        )
        
        # Extract the HTML content
        html_content = response.text.strip()
        
        # Clean up any markdown code blocks if present
        if html_content.startswith("```html"):
            html_content = html_content[7:]
        if html_content.startswith("```"):
            html_content = html_content[3:]
        if html_content.endswith("```"):
            html_content = html_content[:-3]
        html_content = html_content.strip()
        
        # Validate the HTML starts correctly
        if not html_content.lower().startswith("<!doctype html"):
            raise HTTPException(
                status_code=500,
                detail="Generated content is not valid HTML"
            )
        
        # Generate unique ID and save the game
        game_id = str(uuid.uuid4())
        game_path = GAMES_DIR / f"{game_id}.html"
        game_path.write_text(html_content, encoding="utf-8")
        
        return GameResponse(
            game_id=game_id,
            message="Game generated successfully!",
            play_url=f"/api/game/{game_id}"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate game: {str(e)}"
        )


@app.get("/api/game/{game_id}", response_class=HTMLResponse)
async def get_game(game_id: str):
    """Serve a generated game by its ID."""
    # Validate game_id format (UUID)
    try:
        uuid.UUID(game_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid game ID format")
    
    game_path = GAMES_DIR / f"{game_id}.html"
    
    if not game_path.exists():
        raise HTTPException(status_code=404, detail="Game not found")
    
    return HTMLResponse(content=game_path.read_text(encoding="utf-8"))


# Mount static files for the frontend
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main frontend page."""
    index_path = STATIC_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Frontend not found")
    return HTMLResponse(content=index_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
