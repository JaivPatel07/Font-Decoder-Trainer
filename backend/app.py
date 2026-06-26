from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from backend.services.ocr import OCRService
from backend.services.aligner import FontAligner
import os

from backend.services.extractor import extract_pdf

app = FastAPI(
    title="Font Decoder Trainer",
    version="1.0.0"
)


UPLOAD_FOLDER = "datasets"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "Font Decoder Trainer Running"
    }


@app.post("/extract")
async def extract(file: UploadFile = File(...)):

    pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    result = extract_pdf(pdf_path)

    return JSONResponse(result)

ocr = OCRService()
@app.post("/ocr")
async def run_ocr(file: UploadFile = File(...)):

    pdf_path = os.path.join(
        "datasets",
        file.filename
    )

    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    result = ocr.extract(pdf_path)

    return result