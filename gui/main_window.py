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

from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QVideoSink
from PySide6.QtCore import QUrl, Qt, QTimer
from PySide6.QtGui import QPixmap

from gif_manager import list_gifs


# Video preview widget using QVideoSink
class VideoPreview(QWidget):
    def __init__(self, path):
        super().__init__()

        self.label = QLabel()
        self.label.setFixedSize(150, 120)
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.addWidget(self.label)

        self.setLayout(layout)

        self.player = QMediaPlayer()

        self.audio = QAudioOutput()
        self.audio.setVolume(0)

        self.player.setAudioOutput(self.audio)

        self.sink = QVideoSink()

        self.sink.videoFrameChanged.connect(
            self.update_frame
        )

        self.player.setVideoOutput(self.sink)

        self.player.mediaStatusChanged.connect(
            self.loop_video
        )

        self.player.setSource(
            QUrl.fromLocalFile(path)
        )

        self.player.play()

    # Convert video frames into QLabel images
    def update_frame(self, frame):
        if not frame.isValid():
            return

        image = frame.toImage()

        if image.isNull():
            return

        pixmap = QPixmap.fromImage(image)

        self.label.setPixmap(
            pixmap.scaled(
                self.label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )

    # Restart video when finished
    def loop_video(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.player.setPosition(0)
            self.player.play()

    # Stop video when removed
    def stop(self):
        self.player.stop()


# Main application window
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowTitle("GIFLibby")
        self.resize(800, 600)

        # Keep previews alive
        self.players = []

        # Create interface
        self.create_ui()

    # Create the window layout
    def create_ui(self):
        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addLayout(self.create_banner())

        self.create_content()

        main_layout.addWidget(self.scroll_area)

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

        add_button = QPushButton("Add GIF")
        view_button = QPushButton("View GIFs")
        collection_button = QPushButton("Collections")

        settings_button = QPushButton("Settings")

        for button in [
            add_button,
            view_button,
            collection_button,
            settings_button
        ]:
            button.setFixedHeight(25)
            button.setFixedWidth(80)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search GIFs...")
        self.search_bar.setFixedHeight(20)
        self.search_bar.setFixedWidth(200)

        view_button.clicked.connect(self.show_gifs)

        banner.addWidget(add_button)
        banner.addWidget(self.create_divider())
        banner.addWidget(view_button)
        banner.addWidget(self.create_divider())
        banner.addWidget(collection_button)

        banner.addStretch()

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

        self.gif_grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.gif_grid.setSpacing(10)

        self.gif_container.setLayout(self.gif_grid)
        self.scroll_area.setWidget(self.gif_container)

    # Load GIFs into grid
    def show_gifs(self):
        while self.gif_grid.count():
            item = self.gif_grid.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        for preview in self.players:
            preview.stop()

        self.players.clear()

        gifs = list_gifs()

        if not gifs:
            self.gif_grid.addWidget(QLabel("No GIFs found."), 0, 0)
            return

        row = 0
        column = 0

        for gif in gifs:
            card, preview = self.create_gif_card(gif)

            self.players.append(preview)

            self.gif_grid.addWidget(
                card,
                row,
                column
            )

            column += 1

            if column >= 4:
                column = 0
                row += 1

    # Create individual GIF card
    def create_gif_card(self, gif):
        card = QWidget()

        layout = QVBoxLayout()
        layout.setSpacing(0)

        preview = VideoPreview(gif[3])

        layout.addWidget(preview)

        card.setLayout(layout)

        return card, preview

    # Create vertical divider
    def create_divider(self):
        divider = QFrame()

        divider.setFrameShape(QFrame.VLine)
        divider.setFrameShadow(QFrame.Sunken)

        return divider