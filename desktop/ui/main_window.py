from PySide6.QtWidgets import QMainWindow, QFileDialog, QVBoxLayout, QWidget, QToolBar, QMessageBox
from PySide6.QtGui import QAction, QIcon
from ui.pdf_viewer import PDFViewer
from ui.nav_panel import NavPanel
# from ui.pdf_lazyviewer import LazyPDFViewer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern PDF Reader")
        self.setMinimumSize(900, 700)

        # 工具栏
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)

        open_action = QAction(QIcon(), "Open", self)
        open_action.triggered.connect(self.open_file)
        self.toolbar.addAction(open_action)

        print_action = QAction(QIcon(), "Print", self)
        print_action.triggered.connect(self.print_pdf)
        self.toolbar.addAction(print_action)

        # 主体
        self.viewer = PDFViewer()
        self.nav = NavPanel(self.viewer)

        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.nav)
        layout.addWidget(self.viewer)
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setAcceptDrops(True)

    def open_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Open PDF", filter="PDF files (*.pdf)")
        if file:
            self.viewer.load_pdf(file)
            self.nav.set_pdf(self.viewer.pdf_doc)

    def print_pdf(self):
        self.viewer.print_pdf()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            if url.toLocalFile().endswith('.pdf'):
                self.viewer.load_pdf(url.toLocalFile())
                self.nav.set_pdf(self.viewer.pdf_doc)
                break
