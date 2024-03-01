from pypdf import PdfReader, PdfWriter

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename


input_filename = ""
output_filename = ""


def select_input_file():
    filepath = askopenfilename(
        filetypes=[("Portable Document", "*.pdf"), ("All Files", "*.*")]
    )
    if not filepath:
        return

    global input_filename
    input_filename = filepath

    lbl_input_file["text"] = f"Input file: {input_filename}"


def select_output_file():
    filepath = asksaveasfilename(
        filetypes=[("Portable Document", "*.pdf"), ("All Files", "*.*")]
    )
    if not filepath:
        return

    global output_filename
    output_filename = filepath

    lbl_output_file["text"] = f"Output file: {output_filename}"


def reorder(n):
    pages_order = []
    i = 0
    while i < n:
        pages_order.append(2 * n - i)
        pages_order.append(i + 1)
        pages_order.append(i + 2)
        pages_order.append(2 * n - i - 1)
        i += 2

    return [pages_order.index(i + 1) for i in range(2 * n)]


def main():
    global input_filename, output_filename

    reverse = False

    reader = PdfReader(input_filename)
    writer = PdfWriter()

    pages = reader.pages
    if reverse:
        pages = reader.pages[::-1]

    if len(reader.pages) % 2 != 0:
        raise Exception("Number of pages not even - Ensure you scan both sides of each side")

    indices = reorder(len(reader.pages))

    for index in indices:
        if index % 2 == 0:
            page = pages[int(index / 2)]

            page.mediabox.right /= 2
            writer.add_page(page)
            page.mediabox.right *= 2
        else:
            page = pages[int((index - 1) / 2)]
            page.mediabox.left = page.mediabox.right / 2
            writer.add_page(page)
            page.mediabox.left = 0

    with open(output_filename, "wb") as fp:
        writer.write(fp)

    input_filename = ""
    output_filename = ""


if __name__ == '__main__':
    window = tk.Tk()

    lbl_input_file = tk.Label(text="Input file: ")
    lbl_input_file.pack()

    lbl_output_file = tk.Label(text="Output file: ")
    lbl_output_file.pack()

    btn_input = ttk.Button(text="Select Input File", command=select_input_file)
    btn_save = ttk.Button(text="Save As...", command=select_output_file)

    btn_input.pack()
    btn_save.pack()

    btn_run = ttk.Button(text="Convert", command=main)
    btn_run.pack()

    window.mainloop()
