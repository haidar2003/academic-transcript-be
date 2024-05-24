from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from models import *
from academic_transcript import *
import uvicorn
import json
import os
from pydantic import BaseModel
from cryptography import *

origins = [
    "http://localhost:80",
    "http://localhost:5173",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/transcript")
async def add_transcript(transcript: Transcript):
    return create_transcript(transcript)

@app.get("/transcript", response_model=TranscriptList)
async def get_transcript():
    return read_transcript()

@app.get("/transcript/encrypted", response_model=TranscriptList)
async def get_transcript_encrypted():
    return read_transcript_encrpted()

@app.get("/transcript/encrypted/all", response_model=TranscriptList)
async def get_transcript_encrypted_all():
    return read_transcript_encrpted_all()

@app.get("/key/generate")
async def generate_key():
    return generate_rsa_key()

@app.get("/key", response_model=Key)
async def get_key():
    return get_rsa_key()

@app.post("/signature", response_model=SignatureResponse)
async def validate(signature_data: SignatureValidation):
    return validate_signature(signature_data)

@app.post("/pdf/encrypted")
async def download_encrypted_pdf(request : PDFRequest):
    
    return send_encrypted_pdf(request.nim)

@app.post("/pdf/decrypted")
async def download_decrypted_pdf(request : UploadFile):
    return await send_decrypted_pdf(request)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=80)





