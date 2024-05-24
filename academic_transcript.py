import base64
import hashlib
import json
from fastapi import HTTPException
from models import *
from cryptography import *

RC4_KEY = '18221134_18221152'
AES_KEY = 'MADE_BY_RAFI_HAIDAR_RADITYA_AZKA'

# HELPER FUNCTIONS
def load_json(filename):
    with open(f"{filename}.json","r") as f:
        data = json.load(f)[filename]
    return data

def save_json(filename, data):
    with open(f"{filename}.json", "w") as f:
        json.dump({filename: data}, f, indent=4)

def genereate_gpa(transcript: Transcript) -> str:
    total_credit = 0
    total_grade = 0

    for subject in transcript.subject_list:
        if subject.id:
            if subject.grade == 'A':
                total_grade += 4 * int(subject.credit)
            elif subject.grade == 'B':
                total_grade += 3 * int(subject.credit)
            elif subject.grade == 'C':
                total_grade += 2 * int(subject.credit)
            elif subject.grade == 'D':
                total_grade += 1 * int(subject.credit)
            
            total_credit += int(subject.credit)

    return str(round(total_grade/total_credit, 2))

def genereate_signature(transcript: Transcript, exponent_pri, modulus, gpa) -> str:
    transcript_str = ''.join([
        transcript.id,
        transcript.name,
        gpa,
        ''.join([
            subject.id + subject.name + subject.grade + subject.credit
            for subject in transcript.subject_list
        ]),
    ])

    hashed_transcript = hashlib.sha3_256(transcript_str.encode()).hexdigest()

    signature = rsa.custom_generate_signature(hashed_transcript, exponent_pri, modulus, 4)

    b64_signature = base64.b64encode(bytes(signature, 'latin1')).decode('latin1')

    return b64_signature

# KEY
def generate_rsa_key():
    key_data = load_json('key')

    print(key_data)

    next_id = 1

    if len(key_data) > 0:
        if key_data:
            next_id = key_data[-1]['id'] + 1

    pub, pri = rsa.generate_key(10, 10000000) 

    pub = json.loads(pub)
    pri = json.loads(pri)

    new_key = Key(
        id=next_id,
        exponent_pri = pri['exponent'],
        exponent_pub = pub['exponent'],
        modulus = pri['modulus']
    )

    key_data.append(new_key.model_dump())
    save_json('key', key_data)

def get_rsa_key() -> Key:
    key_data = load_json('key')

    if not key_data:
        return None

    latest_key_dict = key_data[-1]
    latest_key = Key(**latest_key_dict)

    return latest_key

# CREATE TRANSCRIPT
def create_transcript(transcript: Transcript):
    transcript_data = load_json('transcript')
    key_data = load_json('key')

    existing_id = set(rc4.custom_rc4(False, transcript['transcript']['id'], RC4_KEY) for transcript in transcript_data)
    if transcript.id in existing_id:
        raise HTTPException(status_code=400, detail=f"Student {transcript.id} already exists")

    exponent_pri = key_data[-1]['exponent_pri']
    modulus = key_data[-1]['modulus']

    gpa = genereate_gpa(transcript)
    signature = genereate_signature(transcript, exponent_pri, modulus, gpa)
    key_id = str(key_data[-1]['id'])

    new_transcript = TranscriptDB(
        transcript=transcript,
        gpa=gpa,
        signature=signature,
        keyID=key_id,
    )

    # ENCRYPT
    new_transcript.transcript.id = rc4.custom_rc4(True, new_transcript.transcript.id, RC4_KEY)
    new_transcript.transcript.name = rc4.custom_rc4(True, new_transcript.transcript.name, RC4_KEY)

    for subject in new_transcript.transcript.subject_list:
        subject.id = rc4.custom_rc4(True, subject.id, RC4_KEY)
        subject.name = rc4.custom_rc4(True, subject.name, RC4_KEY)
        subject.grade = rc4.custom_rc4(True, subject.grade, RC4_KEY)
        subject.credit = rc4.custom_rc4(True, subject.credit, RC4_KEY)

    new_transcript.gpa = rc4.custom_rc4(True, new_transcript.gpa, RC4_KEY)
    new_transcript.signature = rc4.custom_rc4(True, new_transcript.signature, RC4_KEY)
    new_transcript.keyID = rc4.custom_rc4(True, new_transcript.keyID, RC4_KEY)

    transcript_data.append(new_transcript.model_dump())
    save_json('transcript', transcript_data)

# GET TRANSCRIPT
def read_transcript() -> TranscriptList:
  transcript_data = load_json('transcript')

  view_transcripts = []

  for transcript in transcript_data:
    view_transcript = TranscriptView(
        transcript=Transcript(**transcript['transcript']),  
        gpa=transcript['gpa'],
        signature=transcript['signature'],
    )

    # DECRYPT
    view_transcript.transcript.id = rc4.custom_rc4(False, view_transcript.transcript.id, RC4_KEY)
    view_transcript.transcript.name = rc4.custom_rc4(False, view_transcript.transcript.name, RC4_KEY)

    for subject in view_transcript.transcript.subject_list:
        subject.id = rc4.custom_rc4(False, subject.id, RC4_KEY)
        subject.name = rc4.custom_rc4(False, subject.name, RC4_KEY)
        subject.grade = rc4.custom_rc4(False, subject.grade, RC4_KEY)
        subject.credit = rc4.custom_rc4(False, subject.credit, RC4_KEY)

    view_transcript.gpa = rc4.custom_rc4(False, view_transcript.gpa, RC4_KEY)
    view_transcript.signature = rc4.custom_rc4(False, view_transcript.signature, RC4_KEY)


    view_transcripts.append(view_transcript)

  return TranscriptList(transcript_list=view_transcripts)

def read_transcript_encrpted() -> TranscriptList:
  transcript_data = load_json('transcript')

  view_transcripts = []

  for transcript in transcript_data:
    view_transcript = TranscriptView(
        transcript=Transcript(**transcript['transcript']),  
        gpa=transcript['gpa'],
        signature=transcript['signature'],
    )

    # DECRYPT
    view_transcript.signature = rc4.custom_rc4(False, view_transcript.signature, RC4_KEY)


    view_transcripts.append(view_transcript)
    
  return TranscriptList(transcript_list=view_transcripts)

def read_transcript_encrpted_all() -> TranscriptList:
  transcript_data = load_json('transcript')

  view_transcripts = []

  for transcript in transcript_data:
    view_transcript = TranscriptView(
        transcript=Transcript(**transcript['transcript']),  
        gpa=transcript['gpa'],
        signature=transcript['signature'],
    )

    view_transcripts.append(view_transcript)
    
  return TranscriptList(transcript_list=view_transcripts)

# SIGNATURE VALIDATION
# TOLONG TAMBAH TRY-CATCH BAUT B64 GAK VALID
def validate_signature(signature_data: SignatureValidation) -> SignatureResponse:
    transcript_data = next((transcript for transcript in load_json('transcript') if rc4.custom_rc4(False, transcript['transcript']['id'], RC4_KEY) == signature_data.id), None)

    if transcript_data is None:
        return SignatureResponse(result=f'Tidak ada mahasiswa dengan NIM {signature_data.id}')
    
    keyID = rc4.custom_rc4(False, transcript_data['keyID'], RC4_KEY)

    key_data = next((key for key in load_json('key') if str(key['id']) == keyID), None)
    
    signature = signature_data.signature

    # DECRYPT
    if signature_data.signature_type == 'encrypted':
        signature = rc4.custom_rc4(False, signature, RC4_KEY)

    # DECRYPT
    transcript_data['transcript']['id'] = rc4.custom_rc4(False, transcript_data['transcript']['id'], RC4_KEY)
    transcript_data['transcript']['name'] = rc4.custom_rc4(False, transcript_data['transcript']['name'], RC4_KEY)

    for subject in transcript_data['transcript']['subject_list']:
        subject['id'] = rc4.custom_rc4(False, subject['id'], RC4_KEY)
        subject['name'] = rc4.custom_rc4(False, subject['name'], RC4_KEY)
        subject['grade'] = rc4.custom_rc4(False, subject['grade'], RC4_KEY)
        subject['credit'] = rc4.custom_rc4(False, subject['credit'], RC4_KEY)

    transcript_data['gpa'] = rc4.custom_rc4(False, transcript_data['gpa'], RC4_KEY)
    transcript_data['signature'] = rc4.custom_rc4(False, transcript_data['signature'], RC4_KEY)

    # HASH
    transcript_str = ''.join([
        transcript_data['transcript']['id'],
        transcript_data['transcript']['name'],
        transcript_data['gpa'],
        ''.join([
            subject['id'] + subject['name'] + subject['grade'] + subject['credit']
            for subject in transcript_data['transcript']['subject_list']
        ])
    ])

    hashed_transcript = hashlib.sha3_256(transcript_str.encode()).hexdigest()

    # b64 -> str
    signature = base64.b64decode(signature).decode("latin1")

    # VALIDATE
    hashed_transcript_received = rsa.custom_validate_signature(signature, key_data['exponent_pub'], key_data['modulus'], 4)

    if hashed_transcript_received == hashed_transcript:
        return SignatureResponse(result=f'Hasil hash cocok, tanda tangan VALID')
    else:
        return SignatureResponse(result=f'Hasil hash tidak cocok, tanda tangan TIDAK VALID')

# TRANSCRIPT PDF


# TESTING
if __name__ == "__main__":
    dummy_transcript_data = Transcript(
    id="abc222",
    name="Preston Garvey",
    subject_list=[
        Subject(id="math101", name="Mathematics 101", grade="A", credit="4"),
        Subject(id="eng101", name="English 101", grade="A", credit="3"),
        Subject(id="phy101", name="Physics 101", grade="A", credit="4"),
        Subject(id="chem101", name="Chemistry 101", grade="A", credit="4"),
        Subject(id="comp101", name="Computer Science 101", grade="A", credit="4"),
        Subject(id="hist101", name="History 101", grade="A", credit="3"),
        Subject(id="bio101", name="Biology 101", grade="A", credit="4"),
        Subject(id="eco101", name="Economics 101", grade="B", credit="3"),
        Subject(id="art101", name="Art 101", grade="A", credit="3"),
        Subject(id="mus101", name="Music 101", grade="C", credit="3"),
    ]
)

    create_transcript(dummy_transcript_data)
    # print(get_transcript().model_dump())



    # print(get_transcript_encrpted())
    # print(get_transcript_encrpted_all())

    test = SignatureValidation(signature_type='encrypted', signature='P+TIJuxKWoYCUbvB03KVWYmUZqCyFz8bc9JALg8we4gccimjU8xHdBeFJbU8LDl8VNwfg3ICTxvzxZFJq0z1d5o1BNaEdcOyrGxNfZ25x+TMvhfUcAhY4neP7UVwJLk3QoxFkb1g7boIkTs/44HsKcilP3JAp7OE5ajz50MFZGSbU8qQVsIKm6TuAT+0pln5uYCUI2DEHJTm9rOJS6jBNHBSU2WmiF2FKI91WyCb2sUkni6/cg043JfFey3o13dGB1l7m8k9cS9v4eeapYyYoyKEOgP9fRlJQyJv5IuTtz6ca/GdVlBrTCKAkRt4WYiBq6wo7bh1mvAFV2asN681RjEFocsjOIuD0GWjk+q4QvuRmIUt+67JFbC7H0EinBwsRZfl5BfKtkcrTMrp', id='abc111')
    print(validate_signature(test))

    # print(load_json('transcript'))
