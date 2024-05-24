from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# DATA
data = {
    'transcript': {
        'id': 'abc111',
        'name': 'John Deacon',
        'subject_list': [
            {'id': 'math101', 'name': 'Mathematics 101', 'grade': 'A', 'credit': '4'},
            {'id': 'eng101', 'name': 'English 101', 'grade': 'B', 'credit': '3'},
            {'id': 'phy101', 'name': 'Physics 101', 'grade': 'A', 'credit': '4'},
            {'id': 'chem101', 'name': 'Chemistry 101', 'grade': 'B', 'credit': '4'},
            {'id': 'comp101', 'name': 'Computer Science 101', 'grade': 'A', 'credit': '4'},
            {'id': 'hist101', 'name': 'History 101', 'grade': 'B', 'credit': '3'},
            {'id': 'bio101', 'name': 'Biology 101', 'grade': 'A', 'credit': '4'},
            {'id': 'eco101', 'name': 'Economics 101', 'grade': 'B', 'credit': '3'},
            {'id': 'art101', 'name': 'Art 101', 'grade': 'A', 'credit': '3'},
            {'id': 'mus101', 'name': 'Music 101', 'grade': 'B', 'credit': '3'}
        ]
    },
    'gpa': '3.54',
    'signature': 'NDQyMzQ4MzAzNTg2MyA1MDYyNTE1NTQzMTQyIDc4NjI4NTk3MDgyMDMgNzg5NjIxMjIxNDk0NSA2MTg3NDQ2MTgyMTYzIDc4NjcyNzcwNjU5MTkgNDM4MDE1MzgwNzUzOSA3NTUwMjE3NDcwMTU5IDU2NTg0MjA1NjYzMjUgMTgyOTAwODE3ODUzMyA1MDA1NTgyNjc3NzkyIDc0NTMxMTI5Njc0MTAgNzcxMTg0ODg5MjcwNSAzNTE4NjY0OTYyMzg1IDQwNTEzODQ5NTUzNzYgNDU3NjIwMzU1Mzc5MSA='
}

# BUAT PDF
doc = SimpleDocTemplate('transcript.pdf', pagesize=letter)
elements = []

# HEADER
styles = getSampleStyleSheet()
header = Paragraph("Program Studi Sistem dan Teknologi Informasi<br/>Sekolah Teknik Elektro dan Informatika<br/>Institut Teknologi Bandung", styles["Heading2"])
header.keepWithNext = True  # Keep header with the next content
elements.append(header)
elements.append(Paragraph("----------------------------------------------------------", styles["BodyText"]))

# P1
elements.append(Paragraph("Transkrip Akademik", styles["Heading3"]))
name = Paragraph(f"Nama: {data['transcript']['name']}", styles["BodyText"])
nim = Paragraph(f"NIM: {data['transcript']['id']}", styles["BodyText"])
elements.append(name)
elements.append(nim)

# TABEL
table_data = [["No", "Kode Mata Kuliah", "Nama Mata Kuliah", "SKS", "Nilai"]]
for i, subject in enumerate(data['transcript']['subject_list'], start=1):
    table_data.append([
        str(i),
        subject['id'],
        subject['name'],
        subject['credit'],
        subject['grade']
    ])
table = Table(table_data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))
elements.append(table)

# P2
total_credits = sum(int(subject['credit']) for subject in data['transcript']['subject_list'])
elements.append(Paragraph(f"Total Jumlah SKS = {total_credits}", styles["BodyText"]))
elements.append(Paragraph(f"IPK = {data['gpa']}", styles["BodyText"]))

# FOOTER
elements.append(Paragraph("Ketua Program Studi", styles["BodyText"]))
signature = Paragraph(f"--Begin signature--<br/>{data['signature']}<br/>--End signature--", styles["BodyText"])
elements.append(signature)
elements.append(Paragraph("(Dr. I Gusti Bagus Baskara)", styles["BodyText"]))

# EXTRACT
doc.build(elements)