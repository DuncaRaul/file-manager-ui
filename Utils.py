import tkinter as tk


def log_event(text_widget, message):
    text_widget.configure(state="normal")
    text_widget.insert(tk.END, f"{message}\n")
    text_widget.configure(state="disabled")
    text_widget.see(tk.END)


def clear_widget(text_widget):
    text_widget.configure(state="normal")
    text_widget.delete("1.0", tk.END)
    text_widget.configure(state="disabled")


def write_label_message(text_label, message):
    text_label.config(text=message)
