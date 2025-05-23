from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel

class NavPanel(QWidget):
    def __init__(self, viewer):
        super().__init__()
        self.viewer = viewer
        self.page_label = QLabel("Page: 1")
        self.prev_btn = QPushButton("Prev")
        self.next_btn = QPushButton("Next")
        self.zoom_in_btn = QPushButton("Zoom In")
        self.zoom_out_btn = QPushButton("Zoom Out")
        self.toggle_btn = QPushButton("Continuous Mode")

        self.prev_btn.clicked.connect(self.prev_page)
        self.next_btn.clicked.connect(self.next_page)
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        self.zoom_out_btn.clicked.connect(self.zoom_out)
        self.toggle_btn.clicked.connect(self.toggle_mode)

        layout = QHBoxLayout(self)
        layout.addWidget(self.prev_btn)
        layout.addWidget(self.next_btn)
        layout.addWidget(self.page_label)
        layout.addWidget(self.zoom_in_btn)
        layout.addWidget(self.zoom_out_btn)
        layout.addWidget(self.toggle_btn)
        self.setLayout(layout)

    def set_pdf(self, pdf_doc):
        self.page_label.setText(f"Page: 1 / {pdf_doc.page_count}")

    def prev_page(self):
        self.viewer.prev_page()
        self.update_label()

    def next_page(self):
        self.viewer.next_page()
        self.update_label()

    def zoom_in(self):
        self.viewer.set_scale(self.viewer.scale + 0.1)

    def zoom_out(self):
        self.viewer.set_scale(max(0.1, self.viewer.scale - 0.1))

    def toggle_mode(self):
        self.viewer.toggle_continuous()

    def update_label(self):
        if self.viewer.pdf_doc:
            self.page_label.setText(f"Page: {self.viewer.page_index + 1} / {self.viewer.pdf_doc.page_count}")
