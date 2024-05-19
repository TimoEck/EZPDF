import PyPDF2

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import os
# Merger = PdfMerger

class EZPDF:

    def __init__(self, option = "M") -> None:
        self.menu_option = option
        self.filenames = []

    def select_option(self):
        selection = input("""
╔══════════════════════════════════════════════════╗
║ Choose an option:                                ║
║                                                  ║
║ [M] Merge pdf pages                              ║
║ [R] Reverse pdf pages                            ║
║ [E] Close Application                            ║
║                                                  ║
║                                made by Timo Eck  ║
╚══════════════════════════════════════════════════╝
""").upper()

        while True:
      
            try:
                if selection in ["M", "S", "R", "E"]:
                    self.option = selection
                    return self.option
                else:
                    print("Enter a valid option.")
            except ValueError:
                print("Enter a valid option.")
                
        

    def get_files(self):
        Tk().withdraw()
        self.filenames = askopenfilename(multiple=True,title="Select PDF's to merge",filetypes=[("PDF","*.pdf")])
        return self.filenames

    def get_file(self):
        Tk().withdraw()
        self.filenames = askopenfilename(multiple=False,title="Select PDF's to merge",filetypes=[("PDF","*.pdf")])
        return self.filenames


    def merge_file(self):
        # Create a PDF merger
        
        merger = PyPDF2.PdfMerger()
        desktop = os.path.expanduser("~/Desktop/")
        output_dir = os.path.join(desktop, "EZPDF_PDFs")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        
        page_count = 0  # Initialize page_count

        for pdf in self.filenames:

            try:
                merger.append(pdf)
            except Exception as e:
                print(f"Error appending file {pdf}: {e}")
        
        try:
            output = str(input("""
╔══════════════════════════════════════════════════╗
║ Enter filename:                                  ║
╚══════════════════════════════════════════════════╝
"""))
            if not output.lower().endswith('.pdf'):
                output += '.pdf'
            output_filename = os.path.join(output_dir, output)
        except Exception as e:
            print(f"Error saving merged PDF: {e}")
        try:
            merger.write(output_filename)       
            merger.close()
            print(f"Merged PDF saved as {output_filename}")
        except Exception as e:
            print(f"Error saving merged PDF: {e}")

    #Sort Files                
    def reverse_pages(self):
        if not self.filenames:
            print("No file selected.")
            return

        reader = PyPDF2.PdfReader(self.filenames)
        writer = PyPDF2.PdfWriter()

        for page in reversed(reader.pages):
            writer.add_page(page)
            desktop = os.path.expanduser("~/Desktop/")
        output_dir = os.path.join(desktop, "EZPDF_PDFs")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output = input("""
╔══════════════════════════════════════════════════╗
║ Enter filename for reversed PDF (without .pdf):  ║
╚══════════════════════════════════════════════════╝
""")
        if not output.lower().endswith('.pdf'):
            output += '.pdf'
        output_filename = os.path.join(output_dir, output)

        try:
            with open(output_filename, 'wb') as output_f:
                writer.write(output_f)
            print(f"Reversed PDF saved as {output_filename}")
        except Exception as e:
            print(f"Error saving reversed PDF: {e}")


    
if __name__ == "__main__":
    while True:
        pdfCaptain = EZPDF()
        option = pdfCaptain.select_option()
        if option == "M":      
            pdfCaptain.get_files()
            pdfCaptain.merge_file()
        elif option == "R":
            pdfCaptain.get_file()
            pdfCaptain.reverse_pages()
        another = input("Edit PDFs anymore? (y/n): ").upper()
        if another != 'Y':
            break