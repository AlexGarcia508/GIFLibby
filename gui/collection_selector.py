from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QHBoxLayout
)

from PySide6.QtCore import Qt


# Widget for selecting collections
class CollectionSelector(QWidget):
    def __init__(self, collections):
        super().__init__()

        # Store available collections
        self.all_collections = collections

        # Store selected collection IDs
        self.selected_ids = []

        # Store buttons
        self.buttons = []

        self.create_ui()

        # Show default collections
        self.update_collections()

    # Create collection selector UI
    def create_ui(self):
        layout = QVBoxLayout()

        # Remove default layout padding
        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        # Keep everything aligned left
        layout.setAlignment(
            Qt.AlignLeft
        )

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search collections..."
        )

        self.search_input.textChanged.connect(
            self.update_collections
        )

        # Label
        self.label = QLabel(
            "Collections:"
        )

        # Collection button layout
        self.button_layout = QHBoxLayout()

        # Remove button layout padding
        self.button_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.button_layout.setAlignment(
            Qt.AlignLeft
        )

        self.button_layout.setSpacing(5)

        layout.addWidget(
            self.label,
            alignment=Qt.AlignLeft
        )

        layout.addWidget(
            self.search_input,
            alignment=Qt.AlignLeft
        )

        layout.addLayout(
            self.button_layout
        )

        self.setLayout(layout)

    # Update visible collections
    def update_collections(self):
        # Remove old buttons
        for button in self.buttons:
            button.deleteLater()

        self.buttons.clear()

        # Get search text
        search = self.search_input.text().lower()

        # Filter collections
        collections = [
            collection
            for collection in self.all_collections
            if search in collection[1].lower()
        ]

        # Limit visible collections
        collections = collections[:10]

        # Create buttons
        for collection in collections:
            collection_id = collection[0]
            name = collection[1]

            button = QPushButton(name)

            # Show selected state
            if collection_id in self.selected_ids:
                button.setCheckable(True)
                button.setChecked(True)

            button.clicked.connect(
                lambda checked, c=collection_id: self.toggle_collection(c)
            )

            self.button_layout.addWidget(
                button
            )

            self.buttons.append(
                button
            )

    # Add or remove collection
    def toggle_collection(self, collection_id):
        if collection_id in self.selected_ids:
            self.selected_ids.remove(collection_id)
        else:
            self.selected_ids.append(collection_id)

        self.update_collections()

    # Return selected collection IDs
    def get_collections(self):
        return self.selected_ids