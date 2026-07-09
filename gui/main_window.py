from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFrame,
    QLineEdit,
    QLabel
)
from gif_manager import list_gifs

# Main application window
class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowTitle("GIFLibby")
        self.resize(800, 600)

        # Create interface
        self.create_ui()

    # Create the window layout
    def create_ui(self):

        # Main vertical layout
        main_layout = QVBoxLayout()

        # Remove default padding around the layout
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Remove extra spacing
        main_layout.setSpacing(0)

        # Create top banner
        banner = self.create_banner()

        # Add banner to window
        main_layout.addLayout(banner)

        # Create content area
        self.create_content()

        # Add content below banner
        main_layout.addWidget(
            self.content_area
        )

        # Load GIFs when app starts
        self.show_gifs()

        # Apply layout
        self.setLayout(main_layout)

    # Create the top button banner
    def create_banner(self):

        banner = QHBoxLayout()

        # Remove padding around banner
        banner.setContentsMargins(5, 0, 5, 5)

        # Keep items close together
        banner.setSpacing(3)

        # Left side buttons
        add_button = QPushButton("Add GIF")
        view_button = QPushButton("View GIFs")
        collection_button = QPushButton("Collections")

        # Right side buttons
        settings_button = QPushButton("Settings")

        # Make buttons smaller
        for button in [
            add_button,
            view_button,
            collection_button,
            settings_button
        ]:
            button.setFixedHeight(25)
            button.setFixedWidth(80)

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText(
            "Search GIFs..."
        )
        self.search_bar.setFixedHeight(20)
        self.search_bar.setFixedWidth(200)

        # View GIFs button loads GIFs
        view_button.clicked.connect(
            self.show_gifs
        )

        # Add left buttons
        banner.addWidget(add_button)
        banner.addWidget(
            self.create_divider()
        )

        banner.addWidget(view_button)
        banner.addWidget(
            self.create_divider()
        )

        banner.addWidget(collection_button)

        # Push right-side items to the right
        banner.addStretch()

        # Add search and settings
        banner.addWidget(
            self.search_bar
        )

        banner.addWidget(
            self.create_divider()
        )

        banner.addWidget(settings_button)

        return banner

    # Create main content area
    def create_content(self):

        self.content_area = QLabel()

        self.content_area.setText(
            "GIFs will appear here"
        )

    # Display GIF list
    def show_gifs(self):

        gifs = list_gifs()

        if not gifs:
            self.content_area.setText(
                "No GIFs found."
            )
            return

        text = ""

        for gif in gifs:
            text += (
                f"ID: {gif[0]}\n"
                f"Name: {gif[1]}\n"
                f"Path: {gif[2]}\n"
                f"----------------\n"
            )

        self.content_area.setText(text)

    # Create vertical divider line
    def create_divider(self):

        divider = QFrame()

        divider.setFrameShape(
            QFrame.VLine
        )

        divider.setFrameShadow(
            QFrame.Sunken
        )

        return divider