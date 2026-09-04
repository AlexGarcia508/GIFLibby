from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)
from PySide6.QtCore import Qt

from gif_manager import (
    create_gif,
    list_collections,
    get_tags
)

from gui.tag_selector import TagSelector
from gui.collection_selector import CollectionSelector
from utils.browser_extractor import extract_mp4


# Window used for adding new GIFs
class AddGifDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(
            "Add GIF"
        )

        self.setFixedSize(
            450,
            550
        )

        self.create_ui()

    # Create dialog layout
    def create_ui(self):
        layout = QVBoxLayout()

        # Keep all widgets left aligned
        layout.setAlignment(
            Qt.AlignTop
        )

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(
            "GIF Name"
        )

        self.gif_url_input = QLineEdit()
        self.gif_url_input.setPlaceholderText(
            "GIF URL"
        )

        self.preview_url_input = QLineEdit()
        self.preview_url_input.setPlaceholderText(
            "Preview MP4 URL"
        )

        # Load existing data
        collections = list_collections()
        tags = get_tags()

        self.collection_selector = CollectionSelector(
            collections
        )

        self.tag_selector = TagSelector(
            tags
        )

        save_button = QPushButton(
            "Save"
        )

        save_button.clicked.connect(
            self.save_gif
        )

        layout.addWidget(
            QLabel("Name")
        )

        layout.addWidget(
            self.name_input
        )

        layout.addWidget(
            QLabel("GIF URL")
        )

        layout.addWidget(
            self.gif_url_input
        )

        layout.addWidget(
            QLabel("Preview URL")
        )

        layout.addWidget(
            self.preview_url_input
        )

        layout.addWidget(
            self.collection_selector
        )

        layout.addWidget(
            self.tag_selector
        )

        layout.addWidget(
            save_button
        )

        self.setLayout(
            layout
        )

    # Save GIF
    def save_gif(self):
        name = self.name_input.text().strip()
        gif_url = self.gif_url_input.text().strip()
        preview_url = self.preview_url_input.text().strip()

        if not name or not gif_url:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Name and GIF URL are required."
            )
            return

        # Automatically extract preview if user did not provide one
        if not preview_url:
            preview_url = extract_mp4(gif_url)

        if not preview_url:
            QMessageBox.warning(
                self,
                "Preview Error",
                "Could not find MP4 preview."
            )
            return

        collections = self.collection_selector.get_collections()
        tags = self.tag_selector.get_tags()

        create_gif(
            name,
            gif_url,
            preview_url,
            collections,
            ",".join(tags)
        )

        self.accept()