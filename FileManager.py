import tkinter as tk

from OcrPdf import OcrPdf
import Utils
import ConvertDirectoryToPdf
import ConvertFileToPdf
import MergePdfs
from Utils import log_event
from tkinter import ttk, filedialog


class FileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Manager App")

        self.root.geometry("1280x800")

        self.sidebar_frame = tk.Frame(root, width=100, bg="lightgray")
        self.sidebar_frame.pack(side="left", fill="y")

        # Create buttons
        self.button_convert_directory_page = tk.Button(
            self.sidebar_frame,
            text="Convert Directory",
            command=lambda: self.notebook.select(self.convert_directory_page)
        )
        self.button_convert_directory_page.pack(side="top", pady=10, padx=5, fill="x")
        self.button_convert_file_page = tk.Button(
            self.sidebar_frame,
            text="Convert File",
            command=lambda: self.notebook.select(self.convert_file_page)
        )
        self.button_convert_file_page.pack(side="top", pady=10, padx=5, fill="x")
        self.button_merge_pdf_page = tk.Button(
            self.sidebar_frame,
            text="Merge PDFs",
            command=lambda: self.notebook.select(self.merge_pdf_page)
        )
        self.button_merge_pdf_page.pack(side="top", pady=10, padx=5, fill="x")
        self.button_ocr_pdf_page = tk.Button(
            self.sidebar_frame,
            text="OCR PDF",
            command=lambda: self.notebook.select(self.ocr_pdf_page)
        )
        self.button_ocr_pdf_page.pack(side="top", pady=10, padx=5, fill="x")

        # Create a notebook (tabbed widget) for different views
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=5, pady=5)

        # Create the pages
        self.convert_directory_page = tk.Frame(self.notebook)
        self.convert_file_page = tk.Frame(self.notebook)
        self.merge_pdf_page = tk.Frame(self.notebook)
        self.ocr_pdf_page = tk.Frame(self.notebook)
        # Add the pages to the notebook
        self.notebook.add(self.convert_directory_page, text="Convert Directory")
        self.notebook.add(self.convert_file_page, text="Convert File")
        self.notebook.add(self.merge_pdf_page, text="Merge PDFs")
        self.notebook.add(self.ocr_pdf_page, text="OCR PDF")
        # Create the widgets
        self.create_convert_directory_widgets()
        self.create_convert_file_widgets()
        self.create_merge_pdf_files_widgets()
        self.create_ocr_pdf_page()

    def create_convert_directory_widgets(self):
        self.convert_directory_var = tk.StringVar()
        self.convert_directory_combobox_width = 50
        self.convert_directory_combobox = ttk.Combobox(
            self.convert_directory_page,
            textvariable=self.convert_directory_var,
            state="readonly",
            width=self.convert_directory_combobox_width
        )
        self.convert_directory_combobox.pack(pady=10, padx=10)
        self.convert_directory_combobox.bind("<Button-1>", lambda event: self.select_directory())

        label_convert_directory = tk.Label(self.convert_directory_page, text="Please select directory.")
        label_convert_directory.pack(pady=10)

        # Create a button to trigger the convert_directory function
        self.convert_directory_button = tk.Button(
            self.convert_directory_page,
            text="Convert Directory",
            command=self.perform_directory_conversion,
            state="disabled"
        )
        self.convert_directory_button.pack(pady=10)

        separator = ttk.Separator(self.convert_directory_page, orient="horizontal")
        separator.pack(fill="x", pady=10)

        # Create a Text widget for displaying events
        self.convert_directory_events_text = tk.Text(self.convert_directory_page, height=30, width=120)
        self.convert_directory_events_text.pack(pady=10, padx=10, fill="both", expand=True)

        # Create a button to clear the text widget
        self.clear_convert_directory_widget_button = tk.Button(
            self.convert_directory_page,
            text="Clear Log",
            command=self.clear_convert_directory_widget
        )
        self.clear_convert_directory_widget_button.pack(pady=10)

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.convert_directory_var.set(directory)

            self.convert_directory_button["state"] = "normal"

            content_width = len(directory) + 10
            self.convert_directory_combobox_width = max(content_width, self.convert_directory_combobox_width)
            self.convert_directory_combobox.configure(width=self.convert_directory_combobox_width)

    def perform_directory_conversion(self):
        directory = self.convert_directory_var.get()
        if directory:
            log_event(self.convert_directory_events_text, f"Converting directory: {directory}")

            ConvertDirectoryToPdf.convert_directory(directory, self.convert_directory_events_text)

    def clear_convert_directory_widget(self):
        Utils.clear_widget(self.convert_directory_events_text)

    def create_convert_file_widgets(self):
        self.convert_file_var = tk.StringVar()
        self.convert_file_combobox_width = 50
        self.convert_file_combobox = ttk.Combobox(
            self.convert_file_page,
            textvariable=self.convert_file_var,
            state="readonly",
            width=self.convert_file_combobox_width
        )
        self.convert_file_combobox.pack(pady=10, padx=10)
        self.convert_file_combobox.bind("<Button-1>", lambda event: self.select_file())

        label_convert_file = tk.Label(
            self.convert_file_page,
            text="Please select file. Supported file types are: .txt, .img, .png, .docx"
        )
        label_convert_file.pack(pady=10)

        # Create a button to trigger the convert_file function
        self.convert_file_button = tk.Button(
            self.convert_file_page,
            text="Convert File",
            command=self.perform_file_conversion,
            state="disabled"
        )
        self.convert_file_button.pack(pady=10)

        separator = ttk.Separator(self.convert_file_page, orient="horizontal")
        separator.pack(fill="x", pady=10)

        # Create a Text widget for displaying events
        self.convert_file_events_text = tk.Text(self.convert_file_page, height=30, width=120)
        self.convert_file_events_text.pack(pady=10, padx=10, fill="both", expand=True)

        # Create a button to clear the text widget
        self.clear_convert_file_widget_button = tk.Button(
            self.convert_file_page,
            text="Clear Log",
            command=self.clear_convert_file_widget
        )
        self.clear_convert_file_widget_button.pack(pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.convert_file_var.set(file_path)

            self.convert_file_button["state"] = "normal"

            content_width = len(file_path) + 10
            self.convert_file_combobox_width = max(content_width, self.convert_file_combobox_width)
            self.convert_file_combobox.configure(width=self.convert_file_combobox_width)

    def select_ocr_pdf_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.ocr_pdf_var.set(file_path)
            self.ocr_pdf_button["state"] = "normal"

            content_width = len(file_path) + 10
            self.ocr_pdf_combobox_width = max(content_width, self.ocr_pdf_combobox_width)
            self.ocr_pdf_combobox.configure(width=self.ocr_pdf_combobox_width)

    def perform_file_conversion(self):
        file_path = self.convert_file_var.get()
        if file_path:
            ConvertFileToPdf.convert_file_to_pdf(self.convert_file_combobox.get(), self.convert_file_events_text)

    def clear_convert_file_widget(self):
        Utils.clear_widget(self.convert_file_events_text)

    def create_merge_pdf_files_widgets(self):
        # Top controls
        top_frame = tk.Frame(self.merge_pdf_page)
        top_frame.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=(10, 0))

        select_files_button = tk.Button(
            top_frame,
            text="Select Files",
            command=self.select_files,
            width=15
        )
        select_files_button.pack(side="left")

        label_convert_file = tk.Label(
            self.merge_pdf_page,
            text="Please select files. Supported file type is only .pdf. Any other file type will be ignored."
        )
        label_convert_file.grid(row=1, column=0, columnspan=3, sticky="w", padx=10, pady=(5, 10))

        # Listbox
        self.selected_files_listbox = tk.Listbox(
            self.merge_pdf_page,
            selectmode=tk.SINGLE,
            height=30,
            width=120
        )
        self.selected_files_listbox.grid(row=2, column=0, sticky="nsew", padx=(10, 0), pady=10)

        scrollbar = ttk.Scrollbar(
            self.merge_pdf_page,
            command=self.selected_files_listbox.yview
        )
        scrollbar.grid(row=2, column=1, sticky="ns", pady=10)
        self.selected_files_listbox.config(yscrollcommand=scrollbar.set)

        # Buttons frame (right side)
        buttons_frame = tk.Frame(self.merge_pdf_page)
        buttons_frame.grid(row=2, column=2, sticky="n", padx=10, pady=10)

        BUTTON_WIDTH = 15

        tk.Button(
            buttons_frame,
            text="Move Up",
            width=BUTTON_WIDTH,
            command=lambda: self.move_item_up(self.selected_files_listbox)
        ).pack(pady=4)

        tk.Button(
            buttons_frame,
            text="Move Down",
            width=BUTTON_WIDTH,
            command=lambda: self.move_item_down(self.selected_files_listbox)
        ).pack(pady=4)

        tk.Button(
            buttons_frame,
            text="Delete",
            width=BUTTON_WIDTH,
            command=lambda: self.delete_item(self.selected_files_listbox)
        ).pack(pady=4)

        tk.Button(
            buttons_frame,
            text="Merge PDFs",
            width=BUTTON_WIDTH,
            command=lambda: self.start_merger(self.merge_file_list)
        ).pack(pady=(12, 0))

        # Status label
        self.status_label = tk.Label(self.merge_pdf_page, text="")
        self.status_label.grid(row=3, column=0, columnspan=3, pady=10)

        # Grid weight for resizing
        self.merge_pdf_page.grid_columnconfigure(0, weight=1)
        self.merge_pdf_page.grid_rowconfigure(2, weight=1)

    def select_files(self):
        files = filedialog.askopenfilenames()
        self.selected_files_listbox.delete(0, tk.END)
        self.merge_file_list = []
        for file in files:
            extension = file.split(".")[-1]
            if extension == "pdf":
                self.selected_files_listbox.insert(tk.END, file)
                self.merge_file_list.append(file)
        Utils.write_label_message(self.status_label, "")

    def move_item_up(self, listbox):
        selected_index = listbox.curselection()
        if selected_index:
            selected_index = int(selected_index[0])
            if selected_index > 0:
                item = listbox.get(selected_index)
                listbox.delete(selected_index)
                listbox.insert(selected_index - 1, item)
                listbox.selection_set(selected_index - 1)

    def move_item_down(self, listbox):
        selected_index = listbox.curselection()
        if selected_index:
            selected_index = int(selected_index[0])
            if selected_index < listbox.size() - 1:
                item = listbox.get(selected_index)
                listbox.delete(selected_index)
                listbox.insert(selected_index + 1, item)
                listbox.selection_set(selected_index + 1)

    def delete_item(self, listbox):
        selected_index = listbox.curselection()
        if selected_index:
            listbox.delete(selected_index)

    def start_merger(self, merge_file_list):
        MergePdfs.merge_pdfs(merge_file_list, self.status_label)

    def create_ocr_pdf_page(self):
        self.ocr_pdf_var = tk.StringVar()
        self.ocr_pdf_combobox_width = 50
        self.ocr_pdf_combobox = ttk.Combobox(
            self.ocr_pdf_page,
            textvariable=self.ocr_pdf_var,
            state="readonly",
            width=self.ocr_pdf_combobox_width
        )
        self.ocr_pdf_combobox.pack(pady=10, padx=10)
        self.ocr_pdf_combobox.bind("<Button-1>", lambda event: self.select_ocr_pdf_file())

        label_ocr_pdf = tk.Label(
            self.ocr_pdf_page,
            text="Please select PDF file."
        )
        label_ocr_pdf.pack(pady=10)

        self.ocr_pdf_button = tk.Button(
            self.ocr_pdf_page,
            text="OCR File",
            command=self.perform_ocr,
            state="disabled"
        )
        self.ocr_pdf_button.pack(pady=10)

        separator = ttk.Separator(self.ocr_pdf_page, orient="horizontal")
        separator.pack(fill="x", pady=10)

        self.ocr_pdf_events_text = tk.Text(self.ocr_pdf_page, height=30, width=120)
        self.ocr_pdf_events_text.pack(pady=10, padx=10, fill="both", expand=True)

        self.clear_ocr_pdf_widget_button = tk.Button(
            self.ocr_pdf_page,
            text="Clear Log",
            command=self.clear_ocr_pdf_widget
        )
        self.clear_ocr_pdf_widget_button.pack(pady=10)

    def perform_ocr(self):
        file_path = self.ocr_pdf_var.get()
        if file_path:
            OcrPdf.perform_ocr(file_path, self.ocr_pdf_events_text)

    def clear_ocr_pdf_widget(self):
        Utils.clear_widget(self.ocr_pdf_events_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()
