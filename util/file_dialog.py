import tkinter as tk
from tkinter import filedialog
def open_file_dialog(title="Select file", filetypes=None) -> str | None:

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    file_path = filedialog.askopenfilename(
        title=title,
        filetypes=filetypes
    )

    root.destroy()

    return file_path if file_path else None


def save_file_dialog(title="Save file", filetypes=None, defaultextension=None) -> str | None:
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    file_path = filedialog.asksaveasfilename(
        title=title,
        filetypes=filetypes,
        defaultextension=defaultextension
    )

    root.destroy()

    return file_path if file_path else None