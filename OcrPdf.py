import os
import threading
import traceback
import ocrmypdf
from datetime import datetime


class OcrPdf:
    @staticmethod
    def perform_ocr(pdf_path: str, events_text_widget):
        def log(msg: str):
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            def _append():
                events_text_widget.insert("end", f"[{ts}] {msg}\n")
                events_text_widget.see("end")
                events_text_widget.update_idletasks()
            try:
                events_text_widget.after(0, _append)
            except Exception:
                pass

        def worker():
            try:
                if not pdf_path or not os.path.isfile(pdf_path):
                    log(f"ERROR: File not found: {pdf_path}")
                    return

                if not pdf_path.lower().endswith(".pdf"):
                    log("ERROR: Selected file is not a PDF.")
                    return

                base, ext = os.path.splitext(pdf_path)
                out_path = f"{base}_ocr.pdf"

                log(f"Starting OCR for: {pdf_path}")
                log(f"Output will be: {out_path}")

                try:
                    log("Using ocrmypdf (preferred).")
                    ocrmypdf.ocr(
                        pdf_path,
                        out_path,
                        force_ocr=True,
                        deskew=True,
                        optimize=1,
                        progress_bar=False,
                    )

                    log("OCR complete (ocrmypdf).")
                    log(f"Saved: {out_path}")
                    return

                except ImportError:
                    log("ocrmypdf not installed. Falling back to pdf2image + pytesseract.")
                except Exception as e:
                    log(f"ocrmypdf failed, falling back. Reason: {e}")

                try:
                    from pdf2image import convert_from_path
                except ImportError:
                    log("ERROR: pdf2image not installed. Install: pip install pdf2image")
                    return

                try:
                    import pytesseract
                except ImportError:
                    log("ERROR: pytesseract not installed. Install: pip install pytesseract")
                    return

                try:
                    from PyPDF2 import PdfMerger
                except ImportError:
                    log("ERROR: PyPDF2 not installed. Install: pip install PyPDF2")
                    return

                log("Converting PDF pages to images (this can take a while)...")
                try:
                    pages = convert_from_path(pdf_path, dpi=300)
                except Exception as e:
                    log("ERROR converting PDF to images.")
                    log("If you're on Windows/macOS, you likely need Poppler installed and on PATH.")
                    log(f"Details: {e}")
                    return

                log(f"Converted {len(pages)} page(s). Running OCR per page...")

                tmp_page_pdfs = []
                try:
                    for i, img in enumerate(pages, start=1):
                        log(f"OCR page {i}/{len(pages)}...")
                        pdf_bytes = pytesseract.image_to_pdf_or_hocr(img, extension="pdf")
                        tmp_pdf_path = f"{base}__ocr_tmp_page_{i}.pdf"
                        with open(tmp_pdf_path, "wb") as f:
                            f.write(pdf_bytes)

                        tmp_page_pdfs.append(tmp_pdf_path)

                    log("Merging OCR pages into final PDF...")
                    merger = PdfMerger()
                    for p in tmp_page_pdfs:
                        merger.append(p)
                    with open(out_path, "wb") as f_out:
                        merger.write(f_out)
                    merger.close()

                    log("OCR complete (fallback).")
                    log(f"Saved: {out_path}")

                finally:
                    for p in tmp_page_pdfs:
                        try:
                            os.remove(p)
                        except Exception:
                            pass

            except Exception:
                log("ERROR: Unexpected failure during OCR.")
                log(traceback.format_exc())

        threading.Thread(target=worker, daemon=True).start()
