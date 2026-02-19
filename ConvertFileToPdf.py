from pathlib import Path
from threading import Thread
from fpdf import FPDF
from docx2pdf import convert
from PIL import Image
from Utils import log_event


def convert_file_to_pdf(file_path, text_widget):
    def process_file():
        if file_path:
            log_event(text_widget, f"Converting file: {file_path}")
            generate_pdf(file_path, text_widget)
            log_event(text_widget, f"Conversion finished for file: {file_path}")

    Thread(target=process_file, daemon=True).start()


def generate_pdf(file_path, text_widget):
    extension = file_path.lower().split(".")[-1]
    try:
        if extension == "txt":
            convert_text_to_pdf(file_path)
        elif extension == "docx":
            convert_word_to_pdf(file_path)
        elif extension in ("jpg", "png"):
            convert_image_to_pdf(file_path)
        else:
            log_event(text_widget, "Unsupported file type\n")
    except Exception as e:
        log_event(text_widget, f"Error during conversion: {str(e)}\n")


def convert_text_to_pdf(input_file):
    output_pdf = input_file.replace(".txt", ".pdf")

    with open(input_file, 'r') as text_file:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for line in text_file:
            pdf.cell(200, 10, txt=line, ln=True)

        pdf.output(output_pdf)


def convert_word_to_pdf(input_file):
    output_pdf = input_file.replace(".docx", ".pdf")
    convert(input_file, output_pdf)


def convert_image_to_pdf(input_file: str) -> Path:
    input_path = Path(input_file)
    output_path = input_path.with_suffix(".pdf")

    with Image.open(input_path) as img:
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(output_path, "PDF")

    return output_path
