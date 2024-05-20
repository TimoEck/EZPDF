import PyPDF2  # Importing the PyPDF2 library for PDF operations

from tkinter import Tk  # Importing Tk from tkinter for creating file dialogs
from tkinter.filedialog import askopenfilename  # Importing askopenfilename for file selection dialogs
import os  # Importing os for operating system dependent functionality

class EZPDF:

    def __init__(self, option="M") -> None:
        # Initialize the class with a menu option and an empty list for filenames
        self.menu_option = option
        self.filenames = []

    def select_option(self):
        # Display the menu and prompt the user to choose an option
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
                # Check if the selection is valid
                if selection in ["M", "R", "E"]:
                    self.option = selection
                    return self.option
                else:
                    # Prompt for a valid option if the input is not recognized
                    print("Enter a valid option.")
            except ValueError:
                # Catch any value errors and prompt for a valid option
                print("Enter a valid option.")

    def get_files(self):
        # Open a file dialog to select multiple PDF files
        Tk().withdraw()
        self.filenames = askopenfilename(multiple=True, title="Select PDFs to merge", filetypes=[("PDF", "*.pdf")])
        return self.filenames

    def get_file(self):
        # Open a file dialog to select a single PDF file
        Tk().withdraw()
        self.filenames = askopenfilename(multiple=False, title="Select PDF", filetypes=[("PDF", "*.pdf")])
        return self.filenames

    def merge_file(self):
        # Create a PDF merger object
        merger = PyPDF2.PdfMerger()
        desktop = os.path.expanduser("~/Desktop/")
        output_dir = os.path.join(desktop, "EZPDF_PDFs")

        # Check if the output directory exists, create it if necessary
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Append all selected PDF files to the merger
        for pdf in self.filenames:
            try:
                merger.append(pdf)
            except Exception as e:
                print(f"Error appending file {pdf}: {e}")

        try:
            # Prompt for the filename for the merged PDF
            output = str(input("""
╔══════════════════════════════════════════════════╗
║ Enter filename:                                  ║
╚══════════════════════════════════════════════════╝
"""))
            if not output.lower().endswith('.pdf'):
                output += '.pdf'
            output_filename = os.path.join(output_dir, output)
        except Exception as e:
            print(f"Error generating output filename: {e}")

        try:
            # Save the merged PDF file
            merger.write(output_filename)
            merger.close()
            print(f"Merged PDF saved as {output_filename}")
        except Exception as e:
            print(f"Error saving merged PDF: {e}")

    def reverse_pages(self):
        # Check if files were selected
        if not self.filenames:
            print("No file selected.")
            return

        # Read the selected PDF file
        reader = PyPDF2.PdfReader(self.filenames)
        writer = PyPDF2.PdfWriter()

        # Add pages in reverse order to the writer
        for page in reversed(reader.pages):
            writer.add_page(page)

        desktop = os.path.expanduser("~/Desktop/")
        output_dir = os.path.join(desktop, "EZPDF_PDFs")

        # Check if the output directory exists, create it if necessary
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Prompt for the filename for the reversed PDF
        output = input("""
╔══════════════════════════════════════════════════╗
║ Enter filename for reversed PDF (without .pdf):  ║
╚══════════════════════════════════════════════════╝
""")
        if not output.lower().endswith('.pdf'):
            output += '.pdf'
        output_filename = os.path.join(output_dir, output)

        try:
            # Save the reversed PDF file
            with open(output_filename, 'wb') as output_f:
                writer.write(output_f)
            print(f"Reversed PDF saved as {output_filename}")
        except Exception as e:
            print(f"Error saving reversed PDF: {e}")

if __name__ == "__main__":
    while True:
        # Create an instance of the EZPDF class and display the menu
        pdfCaptain = EZPDF()
        option = pdfCaptain.select_option()

        # Execute the corresponding function based on the user option
        if option == "M":
            pdfCaptain.get_files()
            pdfCaptain.merge_file()
        elif option == "R":
            pdfCaptain.get_file()
            pdfCaptain.reverse_pages()

        # Ask the user if they want to edit more PDF files
        another = input("Edit PDFs anymore? (y/n): ").upper()
        if another != 'Y':
            break
