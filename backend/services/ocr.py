import easyocr
import fitz
import cv2
import numpy as np


class OCRService:

    def __init__(self):

        self.reader = easyocr.Reader(
            ['en', 'hi'],
            gpu=False
        )

    def pdf_to_images(self, pdf_path):

        doc = fitz.open(pdf_path)

        images = []

        for page in doc:

            pix = page.get_pixmap(dpi=300)

            img = np.frombuffer(
                pix.samples,
                dtype=np.uint8
            ).reshape(
                pix.height,
                pix.width,
                pix.n
            )

            if pix.n == 4:
                img = cv2.cvtColor(
                    img,
                    cv2.COLOR_RGBA2RGB
                )

            images.append(img)

        return images

    def extract(self, pdf_path):

        pages = self.pdf_to_images(pdf_path)

        output = []

        for page_no, image in enumerate(pages, start=1):

            result = self.reader.readtext(
                image,
                detail=1,
                paragraph=False
            )

            lines = []

            for item in result:

                bbox, text, confidence = item

                lines.append({
                    "text": text,
                    "confidence": float(confidence),
                    "bbox": bbox
                })

            output.append({
                "page": page_no,
                "lines": lines
            })

        return output