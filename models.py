from typing import List
from pydantic import BaseModel, Field

class Key(BaseModel):
    id: int
    exponent_pri: int
    exponent_pub: int
    modulus: int

class Subject(BaseModel):
    id: str
    name: str
    grade: str
    credit: str

class Transcript(BaseModel):
    id: str
    name: str
    subject_list: List[Subject]

class TranscriptDB(BaseModel):
    transcript: Transcript
    gpa: str
    signature: str
    keyID: str

class TranscriptView(BaseModel):
    transcript: Transcript
    gpa: str
    signature: str

class TranscriptList(BaseModel):
    transcript_list: List[TranscriptView]

class SignatureValidation(BaseModel):
    signature_type: str
    signature: str
    id: str

class SignatureResponse(BaseModel):
    result: str

class PDFRequest(BaseModel):
    nim: str