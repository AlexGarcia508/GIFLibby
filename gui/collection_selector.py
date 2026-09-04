from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QHBoxLayout
)

from PySide6.QtCore import Qt


# Widget for selecting collections with suggestions
class CollectionSelector(QWidget):
    def __init__(self, collections):
        super().__init__()

        # Store available collection names
        self.all_collections = [
            collection[1]
            for collection in collections
        ]

        # Store selected collection names
        self.selected_collections = []

        # Maximum selected collections
        self.max_collections = 10

        # Store widgets for cleanup
        self.selected_widgets = []
        self.suggestion_widgets = []

        self.create_ui()

        # Show default suggestions
        self.update_suggestions()

    # Create UI
    def create_ui(self):
        layout = QVBoxLayout()

        # Remove layout padding
        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        # Align left
        layout.setAlignment(
            Qt.AlignLeft
        )

        # Selected label
        self.selected_label = QLabel(
            "Selected Collections:"
        )

        # Selected collection buttons
        self.selected_layout = QHBoxLayout()

        self.selected_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.selected_layout.setAlignment(
            Qt.AlignLeft
        )

        self.selected_layout.setSpacing(
            3
        )

        # Counter
        self.counter_label = QLabel(
            "0 / 10 collections selected"
        )

        # Search bar
        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "Search collections..."
        )

        self.search_input.textChanged.connect(
            self.update_suggestions
        )

        # Suggestion label
        self.suggestion_label = QLabel(
            "Collection Suggestions:"
        )

        # Suggestion buttons
        self.suggestion_layout = QHBoxLayout()

        self.suggestion_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.suggestion_layout.setAlignment(
            Qt.AlignLeft
        )

        self.suggestion_layout.setSpacing(
            3
        )

        layout.addWidget(
            self.selected_label
        )

        layout.addLayout(
            self.selected_layout
        )

        layout.addWidget(
            self.counter_label
        )

        layout.addWidget(
            self.search_input
        )

        layout.addWidget(
            self.suggestion_label
        )

        layout.addLayout(
            self.suggestion_layout
        )

        self.setLayout(
            layout
        )

        self.update_selected_display()

    # Create compact collection button
    def create_collection_button(self, text):
        button = QPushButton(
            text
        )

        button.setStyleSheet(
            """
            QPushButton {
                font-size: 12px;
                padding-left: 5px;
                padding-right: 5px;
                padding-top: 1px;
                padding-bottom: 2px;
            }
            """
        )

        button.setMinimumWidth(
            0
        )

        button.setMaximumWidth(
            button.fontMetrics().horizontalAdvance(text) + 20
        )

        button.adjustSize()

        return button

    # Update selected collections display
    def update_selected_display(self):

        for widget in self.selected_widgets:
            widget.deleteLater()

        self.selected_widgets.clear()

        if not self.selected_collections:

            label = QLabel(
                "No collections selected"
            )

            self.selected_layout.addWidget(
                label
            )

            self.selected_widgets.append(
                label
            )

        else:

            for collection in self.selected_collections:

                button = self.create_collection_button(
                    collection
                )

                button.clicked.connect(
                    lambda checked, c=collection: self.remove_collection(c)
                )

                self.selected_layout.addWidget(
                    button
                )

                self.selected_widgets.append(
                    button
                )

        self.counter_label.setText(
            f"{len(self.selected_collections)} / {self.max_collections} collections selected"
        )

    # Update suggestions
    def update_suggestions(self):

        for widget in self.suggestion_widgets:
            widget.deleteLater()

        self.suggestion_widgets.clear()

        search = self.search_input.text().strip().lower()

        if not search:

            suggestions = [
                collection
                for collection in self.all_collections
                if collection not in self.selected_collections
            ]

        else:

            suggestions = [
                collection
                for collection in self.all_collections
                if search in collection.lower()
                and collection not in self.selected_collections
            ]

            # Add new collection option
            if not suggestions:

                button = self.create_collection_button(
                    f'Add "{search}" collection?'
                )

                button.clicked.connect(
                    lambda checked, c=search: self.add_new_collection(c)
                )

                self.suggestion_layout.addWidget(
                    button
                )

                self.suggestion_widgets.append(
                    button
                )

                return

        for collection in suggestions[:10]:

            button = self.create_collection_button(
                collection
            )

            button.clicked.connect(
                lambda checked, c=collection: self.add_collection(c)
            )

            self.suggestion_layout.addWidget(
                button
            )

            self.suggestion_widgets.append(
                button
            )

    # Add collection
    def add_collection(self, collection):

        if len(self.selected_collections) >= self.max_collections:
            return

        if collection not in self.selected_collections:

            self.selected_collections.append(
                collection
            )

        self.update_selected_display()

        self.update_suggestions()

    # Add new collection
    def add_new_collection(self, collection):

        if len(self.selected_collections) >= self.max_collections:
            return

        if collection not in self.all_collections:

            self.all_collections.append(
                collection
            )

        self.selected_collections.append(
            collection
        )

        self.search_input.clear()

        self.update_selected_display()

        self.update_suggestions()

    # Remove collection
    def remove_collection(self, collection):

        if collection in self.selected_collections:

            self.selected_collections.remove(
                collection
            )

        self.update_selected_display()

        self.update_suggestions()

    # Return selected collection names
    def get_collections(self):

        return self.selected_collections