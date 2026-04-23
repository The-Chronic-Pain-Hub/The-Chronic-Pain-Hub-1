from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, Response
import os
import httpx
import asyncio
from functools import partial

from services.whisper_service import transcribeAudio
from services.llm_service import analyzePainDescription
from services.conversation_service import generateFollowUpQuestions
from services.neuro_symbolic_service import analyze_pain_neuro_symbolic, get_system_info
from services.pain_mapping_service import pain_mapping_service
from models.pain_mapping import PainMapData, PainReport

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

# Get parent directory (root of the project)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Mount Backend images directory
app.mount("/images", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "images")), name="images")

# Health check endpoint
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
        # Run transcription and analysis in background threads
        transcription = await asyncio.to_thread(transcribeAudio, audioBytes, None)
        analysis = await asyncio.to_thread(analyzePainDescription, transcription["text"])
        
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
        # Run LLM call in background thread to avoid blocking
        followUp = await asyncio.to_thread(generateFollowUpQuestions, request.history)
        
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
        
        # Execute neuro-symbolic pipeline in a background thread to avoid blocking
        # This allows other requests (like loading new pages) to be handled concurrently
        analysis = await asyncio.to_thread(analyze_pain_neuro_symbolic, patient_text)
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
        # Step 1: Transcribe audio (run in background thread)
        transcription_result = await asyncio.to_thread(transcribeAudio, audioBytes, None)
        original_transcription = transcription_result["text"]
        
        # Step 2: Neuro-symbolic analysis (run in background thread)
        analysis = await asyncio.to_thread(analyze_pain_neuro_symbolic, original_transcription)
        
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


# ========== Module 4: NPPES API Proxy ==========

@app.get("/api/nppes")
async def proxyNPPES(request: Request):
    """
    Proxy requests to CMS NPPES API
    
    Module 4 uses this to search for healthcare providers.
    Proxying allows CORS-free access to the NPPES registry.
    """
    try:
        # Get query parameters from request
        query_params = dict(request.query_params)
        
        # Build NPPES URL
        nppes_url = "https://npiregistry.cms.hhs.gov/api/?"
        if query_params:
            from urllib.parse import urlencode
            nppes_url += urlencode(query_params)
        
        # Forward request to NPPES
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(nppes_url)
            
            return Response(
                content=response.content,
                status_code=response.status_code,
                media_type=response.headers.get("content-type", "application/json"),
                headers={"Access-Control-Allow-Origin": "*"}
            )
    except httpx.TimeoutException:
        return {
            "status": "error",
            "message": "NPPES API request timed out"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"NPPES proxy error: {str(e)}"
        }


# ========== Module 2: Pain Mapping API Endpoints ==========

@app.post("/api/pain-mapping/save")
async def savePainMapping(pain_data: PainMapData):
    """
    Save pain mapping data
    
    Receives pain mapping data from Module 2 interface, including:
    - Drawing strokes on body canvas
    - Marked pain regions
    - Intensity and depth information
    """
    try:
        # Calculate and update statistics
        stats = pain_mapping_service.calculate_statistics(pain_data)
        pain_data.total_strokes = stats["total_strokes"]
        pain_data.sensation_breakdown = stats["sensation_breakdown"]
        pain_data.neuropathic_indicators = stats["neuropathic_indicators"]
        pain_data.overall_intensity = stats["overall_intensity"]
        
        # TODO: In production, this should be saved to database
        # Currently only returns processed data
        
        return {
            "status": "success",
            "message": "Pain mapping data saved successfully",
            "data": pain_data.model_dump(),
            "statistics": stats
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@app.post("/api/pain-mapping/generate-report")
async def generatePainReport(pain_data: PainMapData):
    """
    Generate pain mapping report
    
    Based on user's pain mapping data, generates a clinical report including:
    - Natural language summary
    - Pain region analysis
    - Neuropathic pain probability assessment
    - Recommended specialists
    """
    try:
        # Generate report in background thread to avoid blocking
        report = await asyncio.to_thread(pain_mapping_service.generate_report, pain_data)
        
        return {
            "status": "success",
            "report": report.model_dump()
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@app.get("/api/pain-mapping/pain-types")
async def getPainTypes():
    """
    Get all pain types and their clinical significance
    
    Returns pain types, color coding, clinical indicators, etc.
    For frontend usage
    """
    try:
        return {
            "status": "success",
            "pain_types": pain_mapping_service.PAIN_TYPE_CLINICAL
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# Mount static files from root directory (CSS, JS, images, etc.)
# This must be at the end, after all specific routes are defined
app.mount("/", StaticFiles(directory=parent_dir, html=True), name="static")
    
@app.on_event("startup")
async def startup_event():
    print("[Startup] Precomputing dictionary embeddings...")
    precompute_dictionary_embeddings()
    print("[Startup] System ready!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

