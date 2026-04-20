from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os

from services.whisper_service import transcribeAudio
from services.llm_service import analyzePainDescription
from services.conversation_service import generateFollowUpQuestions
from services.neuro_symbolic_service import analyze_pain_neuro_symbolic, get_system_info

# Smart embedding service selection
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "biolord")  # Options: "biolord", "openai"

if EMBEDDING_MODEL == "biolord":
    print(f"[Main] Using BioLORD-2023-M embeddings (medical specialist)")
    from services.semantic_distance_service_biolord import precompute_dictionary_embeddings
else:
    print(f"[Main] Using OpenAI embeddings (general purpose)")
    from services.semantic_distance_service_v2 import precompute_dictionary_embeddings

from pydantic import BaseModel
from typing import List, Dict


class ConversationRequest(BaseModel):
    history: List[Dict]
    
    
app = FastAPI(
    title = "Pain Report Platform",
    version = "0.2.0"  # Updated to v0.2.0 with BioLORD support
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/images", StaticFiles(directory="images"), name="images")

# Serve frontend HTML
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the frontend demo page."""
    try:
        html_path = os.path.join(os.path.dirname(__file__), "../Frontend/demo.html")
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>Frontend not found</h1><p>API is running at /api/*</p>",
            status_code=404
        )
    
@app.get("/health")
async def healthCheck():
    return {
        "status": "healthy",
        "message": "The API is healthy and running",
        "version": "0.1.3"
    }
    
    
@app.post("/api/analyze-audio")
async def analyze_audio(file: UploadFile = File(...)):
    #check file
    if not file.content_type.startswith("audio/"):
        return {"error": "Invalid file type.", 
                "message": "Please upload an audio file."}
    
    #read file
    audioBytes = await file.read()
    
    try:
        transcription = transcribeAudio(audioBytes, language=None)
        
        analysis = analyzePainDescription(transcription["text"])
        
        return {
            "status": "success",
            "message": "Audio file received",
            "size": len(audioBytes),
            "filename": file.filename,
            "trancription": transcription["text"],
            "language": transcription["language"],
            "analysis": analysis
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    
    
@app.post("/api/follow-up")
async def getFollowUpQuestion(request: ConversationRequest):
    try:
        followUp = generateFollowUpQuestions(request.history)
        
        return {
            "status": "success",
            "followup": followUp
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@app.post("/api/analyze-text-neuro-symbolic")
async def analyzeTextNeuroSymbolic(request: dict):
    """
    Analyze text pain description using neuro-symbolic architecture.
    
    This is the new upgraded analysis endpoint that uses:
    - LLM for narrow-scope entity extraction only
    - Ontology mapping for multilingual medical terminology
    - Rule-based engine for deterministic clinical recommendations
    
    Returns structured pain data with complete explainability and reasoning chain.
    """
    try:
        patient_text = request.get("text", "")
        if not patient_text:
            return {
                "status": "error",
                "message": "No text provided"
            }
        
        # Execute neuro-symbolic pipeline
        analysis = analyze_pain_neuro_symbolic(patient_text)
        return analysis
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@app.post("/api/analyze-audio-neuro-symbolic")
async def analyzeAudioNeuroSymbolic(file: UploadFile = File(...)):
    """
    Analyze audio pain description using neuro-symbolic architecture.
    
    Combines:
    1. Whisper transcription (audio → text)
    2. Neuro-symbolic analysis (text → structured clinical data)
    
    Returns complete explainable report with reasoning chain.
    """
    if not file.content_type.startswith("audio/"):
        return {
            "error": "Invalid file type.", 
            "message": "Please upload an audio file."
        }
    
    audioBytes = await file.read()
    
    try:
        # Step 1: Transcribe audio
        transcription_result = transcribeAudio(audioBytes, language=None)
        original_transcription = transcription_result["text"]
        
        # Step 2: Neuro-symbolic analysis (includes normalization + ontology mapping)
        analysis = analyze_pain_neuro_symbolic(original_transcription)
        
        # Merge transcription info with analysis results
        # The analysis already contains transcription normalization in analysis["transcription"]
        return {
            "status": "success",
            "message": "Audio analyzed successfully using neuro-symbolic architecture",
            "size": len(audioBytes),
            "filename": file.filename,
            "whisper_language": transcription_result["language"],
            **analysis  # Spread analysis results (includes transcription, structured_data, etc.)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@app.get("/api/system-info")
async def getSystemInfo():
    """
    Get information about the neuro-symbolic pain assessment system.
    
    Returns system configuration, capabilities, and limitations.
    Useful for documentation and debugging.
    """
    try:
        info = get_system_info()
        return {
            "status": "success",
            "system_info": info
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    
@app.on_event("startup")
async def startup_event():
    print("[Startup] Precomputing dictionary embeddings...")
    precompute_dictionary_embeddings()
    print("[Startup] System ready!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

