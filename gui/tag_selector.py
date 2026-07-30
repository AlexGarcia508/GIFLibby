from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QHBoxLayout
)

from PySide6.QtCore import Qt


# Widget for selecting tags with suggestions
class TagSelector(QWidget):
    def __init__(self, tags):
        super().__init__()

        # Store available tags
        self.all_tags = tags

        # Store selected tags
        self.selected_tags = []

        # Maximum selected tags
        self.max_tags = 10

        # Store widgets for cleanup
        self.selected_widgets = []
        self.suggestion_widgets = []

        self.create_ui()

        # Show default suggestions
        self.update_suggestions()

    # Create UI
    def create_ui(self):
        layout = QVBoxLayout()

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout.setAlignment(
            Qt.AlignLeft
        )

        self.selected_label = QLabel(
            "Selected Tags:"
        )

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

        self.counter_label = QLabel(
            "0 / 10 tags selected"
        )

        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "Search tags..."
        )

        self.search_input.textChanged.connect(
            self.update_suggestions
        )

        self.suggestion_label = QLabel(
            "Tag Suggestions:"
        )

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

        self.setLayout(layout)

        self.update_selected_display()

    # Create compact tag button
    def create_tag_button(self, text):
        button = QPushButton(text)

        # Remove extra button padding
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

        # Prevent expanding
        button.setMinimumWidth(0)

        button.setMaximumWidth(
            button.fontMetrics().horizontalAdvance(text) + 20
        )

        button.adjustSize()

        return button

    # Update selected tags
    def update_selected_display(self):
        for widget in self.selected_widgets:
            widget.deleteLater()

        self.selected_widgets.clear()

        if not self.selected_tags:
            label = QLabel(
                "No tags selected"
            )

            self.selected_layout.addWidget(
                label
            )

            self.selected_widgets.append(
                label
            )

        else:
            for tag in self.selected_tags:
                button = self.create_tag_button(
                    tag
                )

                button.clicked.connect(
                    lambda checked, t=tag: self.remove_tag(t)
                )

                self.selected_layout.addWidget(
                    button
                )

                self.selected_widgets.append(
                    button
                )

        self.counter_label.setText(
            f"{len(self.selected_tags)} / {self.max_tags} tags selected"
        )

    # Update suggestions
    def update_suggestions(self):
        for widget in self.suggestion_widgets:
            widget.deleteLater()

        self.suggestion_widgets.clear()

        search = self.search_input.text().strip().lower()

        if not search:
            suggestions = [
                tag
                for tag in self.all_tags
                if tag not in self.selected_tags
            ]

        else:
            suggestions = [
                tag
                for tag in self.all_tags
                if search in tag.lower()
                and tag not in self.selected_tags
            ]

            if not suggestions:
                button = self.create_tag_button(
                    f'Add "{search}" tag?'
                )

                button.clicked.connect(
                    lambda checked, t=search: self.add_new_tag(t)
                )

                self.suggestion_layout.addWidget(
                    button
                )

                self.suggestion_widgets.append(
                    button
                )

                return

        for tag in suggestions[:10]:
            button = self.create_tag_button(
                tag
            )

            button.clicked.connect(
                lambda checked, t=tag: self.add_tag(t)
            )

            self.suggestion_layout.addWidget(
                button
            )

            self.suggestion_widgets.append(
                button
            )

    # Add tag
    def add_tag(self, tag):
        if len(self.selected_tags) >= self.max_tags:
            return

        if tag not in self.selected_tags:
            self.selected_tags.append(
                tag
            )

        self.update_selected_display()
        self.update_suggestions()

    # Add new tag
    def add_new_tag(self, tag):
        if len(self.selected_tags) >= self.max_tags:
            return

        self.selected_tags.append(
            tag
        )

        if tag not in self.all_tags:
            self.all_tags.append(
                tag
            )

        self.search_input.clear()

        self.update_selected_display()
        self.update_suggestions()

    # Remove tag
    def remove_tag(self, tag):
        if tag in self.selected_tags:
            self.selected_tags.remove(
                tag
            )

        self.update_selected_display()
        self.update_suggestions()

    # Return selected tags
    def get_tags(self):
        return self.selected_tags