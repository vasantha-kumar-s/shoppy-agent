"""
AgentCart — Voice API Endpoints (STT & TTS).
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Response
from pydantic import BaseModel
from app.voice.stt_service import STTService
from app.voice.tts_service import TTSService

router = APIRouter(prefix="/api/voice", tags=["Voice"])


class SpeakRequest(BaseModel):
    text: str


@router.post("/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    """Transcribe uploaded audio file (microphone recording) to text using faster-whisper."""
    try:
        contents = await audio.read()
        if not contents:
            raise HTTPException(status_code=400, detail="Empty audio recording.")

        transcript = await STTService.transcribe(contents, filename=audio.filename or "audio.webm")
        return {"transcript": transcript}
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Speech transcription failed: {str(e)}. Ensure faster-whisper service is running.",
        )


@router.post("/speak")
async def synthesize_speech(body: SpeakRequest):
    """Synthesize text into speech audio bytes using Kokoro TTS."""
    try:
        audio_bytes = await TTSService.synthesize(body.text)
        return Response(content=audio_bytes, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Text-to-speech failed: {str(e)}. Ensure Kokoro TTS container is running.",
        )
