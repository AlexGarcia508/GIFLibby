from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)

from gif_manager import create_gif


class AddGifDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Configure the dialog window
        self.setWindowTitle("Add GIF")
        self.setFixedSize(350, 250)

        # Build the UI elements
        self.create_ui()

    def create_ui(self):
        # Main vertical layout for stacking widgets
        layout = QVBoxLayout()

        # Input field for the GIF display name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("GIF Name")

        # Input field for the original GIF page URL (ex: Tenor page)
        self.gif_url_input = QLineEdit()
        self.gif_url_input.setPlaceholderText("GIF URL (Tenor page URL)")

        # Input field for the preview media URL (ex: MP4 preview)
        self.preview_url_input = QLineEdit()
        self.preview_url_input.setPlaceholderText("Preview URL (MP4 URL)")

        # Input field for comma-separated tags
        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("Tags (example: cute,cat)")

        # Save button that triggers GIF creation
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_gif)

        # Add labels and input fields to the layout
        layout.addWidget(QLabel("Name"))
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("GIF URL"))
        layout.addWidget(self.gif_url_input)

        layout.addWidget(QLabel("Preview URL"))
        layout.addWidget(self.preview_url_input)

        layout.addWidget(QLabel("Tags"))
        layout.addWidget(self.tags_input)

        layout.addWidget(save_button)

        # Apply the layout to the dialog window
        self.setLayout(layout)

    def save_gif(self):
        # Retrieve and clean user input
        name = self.name_input.text().strip()
        gif_url = self.gif_url_input.text().strip()
        preview_url = self.preview_url_input.text().strip()
        tags = self.tags_input.text().strip()

        # Ensure required fields are filled before saving
        if not name or not gif_url or not preview_url:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Name, GIF URL, and Preview URL are required."
            )
            return

        # Create the GIF entry in the database
        # Collections are currently empty because they are handled separately
        create_gif(
            name,
            gif_url,
            preview_url,
            [],
            tags
        )

        # Close the dialog after successful creation
        self.accept()