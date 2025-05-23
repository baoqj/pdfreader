from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
import fitz

def fitz_pixmap_to_qimage(pix):
    if pix.n == 4:
        fmt = QImage.Format_RGBA8888
    elif pix.n == 3:
        fmt = QImage.Format_RGB888
    else:
        fmt = QImage.Format_Grayscale8
    qimg = QImage(pix.samples, pix.width, pix.height, pix.stride, fmt)
    return qimg.copy()

class PDFViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.pdf_doc = None
        self.page_index = 0
        self.scale = 1.0
        self.continuous = False

        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.pages_widget = QWidget()
        self.pages_layout = QVBoxLayout(self.pages_widget)
        self.pages_layout.setSpacing(16)
        self.scroll.setWidget(self.pages_widget)

        layout = QVBoxLayout(self)
        layout.addWidget(self.scroll)
        self.setLayout(layout)

        self.page_labels = []

    def load_pdf(self, path):
        self.pdf_doc = fitz.open(path)
        self.page_index = 0
        self.show_page()

    def show_page(self):
        if not self.pdf_doc:
            return
        # 清空原有label
        while self.pages_layout.count():
            child = self.pages_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.page_labels = []

        if self.continuous:
            # 连续模式：一次性渲染所有页面
            for i in range(self.pdf_doc.page_count):
                page = self.pdf_doc[i]
                pix = page.get_pixmap(matrix=fitz.Matrix(self.scale, self.scale))
                qimg = fitz_pixmap_to_qimage(pix)
                pixmap = QPixmap.fromImage(qimg)
                label = QLabel()
                label.setAlignment(Qt.AlignCenter)
                label.setPixmap(pixmap)
                label.setFixedHeight(pixmap.height())
                label.setSizePolicy(QLabel().sizePolicy())
                self.pages_layout.addWidget(label)
                self.page_labels.append(label)
        else:
            # 单页模式
            page = self.pdf_doc[self.page_index]
            pix = page.get_pixmap(matrix=fitz.Matrix(self.scale, self.scale))
            qimg = fitz_pixmap_to_qimage(pix)
            pixmap = QPixmap.fromImage(qimg)
            label = QLabel()
            label.setAlignment(Qt.AlignCenter)
            label.setPixmap(pixmap)
            label.setFixedHeight(pixmap.height())
            label.setSizePolicy(QLabel().sizePolicy())
            self.pages_layout.addWidget(label)
            self.page_labels.append(label)

    def next_page(self):
        if not self.continuous and self.pdf_doc and self.page_index + 1 < self.pdf_doc.page_count:
            self.page_index += 1
            self.show_page()

    def prev_page(self):
        if not self.continuous and self.pdf_doc and self.page_index > 0:
            self.page_index -= 1
            self.show_page()

    def set_scale(self, scale):
        self.scale = scale
        self.show_page()

    def toggle_continuous(self):
        self.continuous = not self.continuous
        self.show_page()

    def print_pdf(self):
        from PySide6.QtPrintSupport import QPrinter, QPrintDialog
        printer = QPrinter(QPrinter.HighResolution)
        dlg = QPrintDialog(printer, self)
        if dlg.exec() == QPrintDialog.Accepted:
            if self.pdf_doc:
                from PySide6.QtGui import QPainter
                painter = QPainter(printer)
                if self.continuous:
                    for i in range(self.pdf_doc.page_count):
                        page = self.pdf_doc[i]
                        pix = page.get_pixmap(matrix=fitz.Matrix(self.scale, self.scale))
                        qimg = fitz_pixmap_to_qimage(pix)
                        rect = painter.viewport()
                        size = qimg.size()
                        size.scale(rect.size(), Qt.KeepAspectRatio)
                        painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
                        painter.setWindow(qimg.rect())
                        painter.drawImage(0, 0, qimg)
                        if i != self.pdf_doc.page_count - 1:
                            printer.newPage()
                else:
                    page = self.pdf_doc[self.page_index]
                    pix = page.get_pixmap(matrix=fitz.Matrix(self.scale, self.scale))
                    qimg = fitz_pixmap_to_qimage(pix)
                    rect = painter.viewport()
                    size = qimg.size()
                    size.scale(rect.size(), Qt.KeepAspectRatio)
                    painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
                    painter.setWindow(qimg.rect())
                    painter.drawImage(0, 0, qimg)
                painter.end()
