import os
import PyPDF2
import Utils


def merge_pdfs(input_pdfs, status_label):
    if not input_pdfs:
        Utils.write_label_message(status_label, "Error: No input PDFs provided.")
        return

    first_pdf = input_pdfs[0]  # Use the first PDF in the list
    output_pdf = os.path.join(os.path.dirname(first_pdf), "merge_result.pdf")

    try:
        with open(output_pdf, 'wb') as output_file:
            pdf_writer = PyPDF2.PdfWriter()

            for pdf in input_pdfs:
                try:
                    with open(pdf, 'rb') as pdf_file:
                        pdf_reader = PyPDF2.PdfReader(pdf_file)
                        for page_num in range(len(pdf_reader.pages)):
                            page = pdf_reader.pages[page_num]
                            pdf_writer.add_page(page)
                except FileNotFoundError:
                    Utils.write_label_message(status_label, f"Warning: File not found: {pdf}")

            pdf_writer.write(output_file)
        Utils.write_label_message(status_label, f"PDFs merged successfully. Output: {output_pdf}")

    except Exception as e:
        Utils.write_label_message(status_label, f"Error: An unexpected error occurred: {e}")
