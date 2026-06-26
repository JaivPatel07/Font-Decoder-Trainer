import fitz
import json
import os


OUTPUT_FOLDER = "outputs"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def extract_pdf(pdf_path):

    doc = fitz.open(pdf_path)

    pages = []

    fonts = {}

    for page_number, page in enumerate(doc, start=1):

        raw = page.get_text("dict")

        page_data = {
            "page": page_number,
            "width": page.rect.width,
            "height": page.rect.height,
            "blocks": []
        }

        for block in raw["blocks"]:

            # Ignore images
            if block["type"] != 0:
                continue

            block_data = {
                "bbox": block["bbox"],
                "lines": []
            }

            for line in block["lines"]:

                line_data = {
                    "bbox": line["bbox"],
                    "spans": []
                }

                for span in line["spans"]:

                    font = span["font"]

                    fonts[font] = fonts.get(font, 0) + 1

                    span_data = {
                        "text": span["text"],
                        "font": span["font"],
                        "size": span["size"],
                        "flags": span["flags"],
                        "color": span["color"],
                        "bbox": span["bbox"]
                    }

                    line_data["spans"].append(span_data)

                block_data["lines"].append(line_data)

            page_data["blocks"].append(block_data)

        pages.append(page_data)

    output = {
        "file": os.path.basename(pdf_path),
        "total_pages": len(doc),
        "fonts": fonts,
        "pages": pages
    }

    json_path = os.path.join(
        OUTPUT_FOLDER,
        os.path.basename(pdf_path).replace(".pdf", ".json")
    )

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print("=" * 80)
    print("PDF ANALYSIS COMPLETE")
    print("=" * 80)
    print("Pages :", len(doc))
    print("Fonts :", fonts)
    print("Saved :", json_path)

    return output