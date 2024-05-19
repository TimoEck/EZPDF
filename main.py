import PyPDF2

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import os
# Merger = PdfMerger

class EZPDF:

    def __init__(self, option = "M") -> None:
        self.option = option
        self.filenames = []

    def select_option(self):
        selection = input("""
╔══════════════════════════════════════════════════╗
║ Choose an option:                                ║
║                                                  ║
║ [M] Merge pdf pages                              ║
║ [E] Close Application                            ║
║                                                  ║
║                                made by Timo Eck  ║
╚══════════════════════════════════════════════════╝
""").upper()

        while True:
            try:
                if selection == "M":
                    self.option = selection
                    return self.option
                elif selection == "E":
                    exit()
                else:
                    print("Enter a valid option.")
                

            except ValueError:
                print("Enter a valid option.")
                continue
        

    def get_file(self):
        Tk().withdraw()
        self.filenames = askopenfilename(multiple=True,title="Select PDF's to merge",filetypes=[("PDF","*.pdf")])
        return self.filenames



    def merge_file(self):
        # Create a PDF merger
        merger = PyPDF2.PdfMerger()
        desktop = os.path.expanduser("~/Desktop/")
        output_dir = os.path.join(desktop, "EZPDF_PDFs")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        
        for pdf in self.filenames:

            try:
                merger.append(pdf)
            except Exception as e:
                print(f"Error appending file {pdf}: {e}")

        output_filename = os.path.join(output_dir, 'Complete.pdf')

        try:
            merger.write(output_filename)       
            merger.close()
            print(f"Merged PDF saved as {output_filename}")
        except Exception as e:
            print(f"Error saving merged PDF: {e}")
                    

if __name__ == "__main__":
    while True:
        pdfCaptain = EZPDF()
        option = pdfCaptain.select_option()
        if option == "M":      
            pdfCaptain.get_file()
            pdfCaptain.merge_file()
        another = input("Merge PDFs anymore? (y/n): ").upper()
        if another != 'Y':
            break