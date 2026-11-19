import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import RectangleObject

def split_first_page(pdf_path, output_pdf):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    # Get the first page
    page = reader.pages[0]
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)

    # --- Top half ---
    top_page = page
    top_page.cropbox = RectangleObject([0, height/2, width, height])
    writer.add_page(top_page)

    # --- Bottom half ---
    bottom_page = page
    bottom_page.cropbox = RectangleObject([0, 0, width, height/2])
    writer.add_page(bottom_page)

    # Save both halves into one PDF
    with open(output_pdf, "wb") as f_out:
        writer.write(f_out)

def choose_file():
    pdf_path = filedialog.askopenfilename(
        title="Select PDF",
        filetypes=[("PDF files", "*.pdf")]
    )
    if pdf_path:
        output_path = filedialog.asksaveasfilename(
            title="Save Output PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        if output_path:
            try:
                split_first_page(pdf_path, output_path)
                messagebox.showinfo("Success", f"Split PDF saved:\n{output_path}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

# GUI setup
root = tk.Tk()
root.title("PDF Splitter")

label = tk.Label(root, text="Split first page of PDF into two halves")
label.pack(pady=10)

btn = tk.Button(root, text="Choose PDF", command=choose_file)
btn.pack(pady=20)

root.geometry("400x200")
root.mainloop()


