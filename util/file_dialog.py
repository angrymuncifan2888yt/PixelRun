def open_file_dialog(title="Select file", filetypes=None) -> str | None:
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    file_path = filedialog.askopenfilename(
        title=title,
        filetypes=filetypes
    )

    root.destroy()

    return file_path if file_path else None
