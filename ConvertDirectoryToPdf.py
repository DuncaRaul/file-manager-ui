import os
from os.path import isfile, join
from datetime import datetime
from img2pdf import convert
from Utils import log_event
from threading import Thread


def convert_directory(directory_path, text_widget):
    def process_directory():
        pdf_list = get_all_subdirectories(directory_path + "/")
        pdf_directory = directory_path + "/PDFS"
        os.makedirs(pdf_directory, exist_ok=True)
        log_file_path = directory_path + "/LOG.txt"
        output_directory = pdf_directory + "/"

        with open(log_file_path, 'w') as log_file:
            log_file.write(f"Log file created at: {datetime.now()}\n")

            if len(pdf_list) == 0:
                log_event(text_widget, f"Processing started for PDF\n")
                combine_images_no_subdirectory(directory_path, log_file)
                log_event(text_widget, f"Processing completed for PDF\n")
            else:
                pdf_file_number = 1
                for manga in pdf_list:
                    sub_directory_paths = get_all_subdirectories(manga)
                    pdf_file_name = get_pdf_file_name(directory_path, manga, sub_directory_paths)
                    log_event(text_widget, f"Processing started for {pdf_file_name}{pdf_file_number}\n")

                    combine_images_into_pdf(manga, sub_directory_paths, output_directory, pdf_file_name, log_file)

                    log_event(text_widget, f"Processing completed for {pdf_file_name}{pdf_file_number}\n")
                    pdf_file_number += 1
            log_event(text_widget, "Conversion completed.")

    Thread(target=process_directory, daemon=True).start()


def combine_images_no_subdirectory(directory_path, log_file):
    final_file_path = f"{directory_path}/PDFS/PDF.pdf"
    with open(final_file_path, 'wb') as pdf_file:
        log_file.write(f"Chapter done = {final_file_path[2:]}\n")
        pdf_file.write(convert(get_image_path_list(directory_path)))


def combine_images_into_pdf(manga, sub_directory_paths, pdf_path, pdf_file_name, log_file):
    manga_pdf_directory = f"{pdf_path}{pdf_file_name}"[:-1]
    os.makedirs(manga_pdf_directory, exist_ok=True)

    if len(sub_directory_paths) > 0:
        for sub_dir in sub_directory_paths:
            generate_pdf(manga_pdf_directory, pdf_file_name, log_file, sub_dir)
    else:
        generate_pdf(manga_pdf_directory, pdf_file_name, log_file, manga)


def generate_pdf(manga_pdf_directory, pdf_file_name, log_file, sub_directory):
    if os.path.exists(manga_pdf_directory):
        final_file_path = f"{manga_pdf_directory}/{pdf_file_name}{extract_chapter_number(sub_directory)}.pdf"
        if not os.path.exists(final_file_path):
            with open(final_file_path, 'wb') as pdf_file:
                log_file.write(f"Chapter done = {final_file_path[2:]}\n")
                pdf_file.write(convert(get_image_path_list(sub_directory)))


def get_image_path_list(directory):
    image_path_list = []
    for file in os.listdir(directory):
        file_path = join(directory, file).replace("\\", "/")
        if is_file_image(file_path.lower()):
            image_path_list.append(file_path)

    return image_path_list


def get_pdf_file_name(directory_path, manga, sub_directory_paths):
    if len(sub_directory_paths) <= 0:
        return directory_path.split("/")[-1].replace(" ", "_") + "_"

    return manga.split("/")[-1].replace(" ", "_") + "_"


def get_all_subdirectories(directory_path):
    subdirectories = []

    for entry in os.scandir(directory_path):
        if entry.is_dir() and "PDFS" not in entry.name and "Read" not in entry.name and "Not Read" not in entry.name:
            subdirectories.append(entry.path.replace("\\", "/"))

    return subdirectories


def extract_chapter_number(sub_dir_path):
    split_dir = sub_dir_path.split("/")
    split_name = split_dir[-1].split(" ")
    chapter_number = next((s for i, s in enumerate(split_name) if s.lower() == "chapter"), None)
    if chapter_number is not None and (index := split_name.index(chapter_number) + 1) < len(split_name):
        return split_name[index]
    return ""


def is_file_image(file_name):
    return file_name.lower().endswith(('.jpg', '.jpeg', '.png'))

