import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import RectangleObject

def split_first_page(pdf_path, output_pdf, split_percent):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    # Get the first page
    page = reader.pages[0]
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)

    # Calculate split height based on percentage
    split_height = height * (split_percent / 100.0)

    # --- Top part ---
    top_page = page
    top_page.cropbox = RectangleObject([0, height - split_height, width, height])
    writer.add_page(top_page)

    # --- Bottom part ---
    bottom_page = page
    bottom_page.cropbox = RectangleObject([0, 0, width, height - split_height])
    writer.add_page(bottom_page)

    # --- Add the rest of the pages unchanged ---
    for i in range(1, len(reader.pages)):
        writer.add_page(reader.pages[i])

    # Save output PDF
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
                # Get percentage from entry box
                split_percent = float(percent_entry.get())
                if not (0 < split_percent < 100):
                    raise ValueError("Percentage must be between 0 and 100")

                split_first_page(pdf_path, output_path, split_percent)
                messagebox.showinfo("Success", f"Split PDF saved:\n{output_path}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

# GUI setup
root = tk.Tk()
root.title("PDF Splitter")

label = tk.Label(root, text="Enter split percentage (top part):")
label.pack(pady=10)

percent_entry = tk.Entry(root)
percent_entry.insert(0, "50")  # default value
percent_entry.pack(pady=5)

btn = tk.Button(root, text="Choose PDF", command=choose_file)
btn.pack(pady=20)

root.geometry("400x200")
root.mainloop()

