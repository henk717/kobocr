### The windows portion of this example relies on https://mendelson.org/pdftoprinter.html

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import pathlib
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

pdfmetrics.registerFont(TTFont('input_font', 'font.ttf'))
input_folder = "output"

class NewFileHandler(FileSystemEventHandler):
     def on_created(self, event):
          with open(event.src_path, "r", encoding="utf-8") as file_to_print:
               print_text = file_to_print.read().replace('\n', '')
               # Create a PDF
               filename = "output.pdf"
               doc = SimpleDocTemplate(filename, pagesize=A4)
               styles = getSampleStyleSheet()
               style = styles["Normal"]
               style.fontName = "input_font"
               style.fontSize = 20
               paragraph = Paragraph(print_text, style)
               doc.build([paragraph])

               # Print command (varies slightly by platform)
               if os.name == 'nt':  # Windows
                    os.system(f"PDFtoPrinter {filename}")
               else:  # macOS or Linux
                    os.system(f"lp {filename}")


if __name__ == "__main__":
    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=input_folder, recursive=False)
    observer.start()

    try:
        print(f"Watching for new print jobs in: {input_folder}")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()