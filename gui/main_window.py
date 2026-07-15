from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFrame,
    QLineEdit,
    QScrollArea,
    QGridLayout,
    QLabel
)

from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl, Qt, QTimer

from gif_manager import list_gifs


# Main application window
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowTitle("GIFLibby")
        self.resize(800, 600)

        # Keep players alive
        self.players = []

        # Create interface
        self.create_ui()

    # Create the window layout
    def create_ui(self):
        main_layout = QVBoxLayout()

        # Remove default padding and spacing
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create top banner
        main_layout.addLayout(self.create_banner())

        # Create GIF area
        self.create_content()

        # Add GIF area below banner
        main_layout.addWidget(self.scroll_area)

        # Load GIFs after the window finishes rendering
        QTimer.singleShot(
            100,
            self.show_gifs
        )

        self.setLayout(main_layout)

    # Create the top button banner
    def create_banner(self):
        banner = QHBoxLayout()

        banner.setContentsMargins(5, 0, 5, 5)
        banner.setSpacing(3)

        # Left buttons
        add_button = QPushButton("Add GIF")
        view_button = QPushButton("View GIFs")
        collection_button = QPushButton("Collections")

        # Right button
        settings_button = QPushButton("Settings")

        # Button size
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
        self.search_bar.setPlaceholderText("Search GIFs...")
        self.search_bar.setFixedHeight(20)
        self.search_bar.setFixedWidth(200)

        # Reload GIFs
        view_button.clicked.connect(self.show_gifs)

        # Left side
        banner.addWidget(add_button)
        banner.addWidget(self.create_divider())
        banner.addWidget(view_button)
        banner.addWidget(self.create_divider())
        banner.addWidget(collection_button)

        # Push right side
        banner.addStretch()

        # Right side
        banner.addWidget(self.search_bar)
        banner.addWidget(self.create_divider())
        banner.addWidget(settings_button)

        return banner

    # Create scrollable GIF grid
    def create_content(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.gif_container = QWidget()

        self.gif_grid = QGridLayout()

        # Keep GIFs at the top-left
        self.gif_grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # Space between GIF previews
        self.gif_grid.setSpacing(10)

        self.gif_container.setLayout(self.gif_grid)
        self.scroll_area.setWidget(self.gif_container)

    # Load GIFs into grid
    def show_gifs(self):
        # Clear old cards
        while self.gif_grid.count():
            item = self.gif_grid.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        self.players.clear()

        gifs = list_gifs()

        if not gifs:
            self.gif_grid.addWidget(QLabel("No GIFs found."), 0, 0)
            return

        row = 0
        column = 0

        # Create GIF cards
        for gif in gifs:
            card = self.create_gif_card(gif)
            self.gif_grid.addWidget(card, row, column)

            column += 1

            # Four GIFs per row
            if column >= 4:
                column = 0
                row += 1

    # Create individual GIF card
    def create_gif_card(self, gif):
        card = QWidget()

        layout = QVBoxLayout()
        layout.setSpacing(0)

        # Video display
        video = QVideoWidget()
        video.setFixedSize(150, 120)

        # Video player
        player = QMediaPlayer()
        audio = QAudioOutput()

        # Mute preview
        audio.setVolume(0)

        player.setAudioOutput(audio)
        player.setVideoOutput(video)

        # Load MP4 preview
        player.setSource(QUrl.fromLocalFile(gif[3]))

        # Loop video
        player.mediaStatusChanged.connect(
            lambda status: self.loop_video(player, status)
        )

        player.play()

        # Prevent player cleanup
        self.players.append(player)

        layout.addWidget(video)
        card.setLayout(layout)

        return card

    # Restart video when finished
    def loop_video(self, player, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            player.setPosition(0)
            player.play()

    # Create vertical divider
    def create_divider(self):
        divider = QFrame()

        divider.setFrameShape(QFrame.VLine)
        divider.setFrameShadow(QFrame.Sunken)

        return divider