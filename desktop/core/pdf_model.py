import fitz  # PyMuPDF

class PDFModel:
    def __init__(self, path):
        self.doc = fitz.open(path)
        self.path = path

    def page_count(self):
        return self.doc.page_count

    def get_page(self, index):
        return self.doc[index]
