from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFrame,
    QLineEdit,
    QScrollArea,
    QGridLayout,
    QLabel,
    QCheckBox,
    QMenu,
    QMessageBox
)

from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QVideoSink
from PySide6.QtCore import QUrl, Qt, QTimer, Signal
from PySide6.QtGui import QPixmap

from gif_manager import list_gifs, send_gif_by_id, remove_gif
from gui.add_gif_dialog import AddGifDialog


# Clickable GIF card
class GifCard(QWidget):
    clicked = Signal()
    delete_requested = Signal()

    def __init__(self):
        super().__init__()

        self.delete_mode = False
        self.selected = False
        self.checkbox = None

    # Enable or disable delete mode
    def set_delete_mode(self, enabled):
        self.delete_mode = enabled
        self.selected = False

        if self.checkbox:
            self.checkbox.setVisible(enabled)
            self.checkbox.setChecked(False)

    # Select or deselect card
    def set_selected(self, selected):
        self.selected = selected

        if self.checkbox:
            self.checkbox.setChecked(selected)

    # Handle left click
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.delete_mode:
                self.set_selected(not self.selected)
            else:
                self.clicked.emit()

        super().mousePressEvent(event)

    # Show right-click menu
    def contextMenuEvent(self, event):
        menu = QMenu(self)

        delete_action = menu.addAction("Delete")

        action = menu.exec(
            self.mapToGlobal(event.pos())
        )

        if action == delete_action:
            self.delete_requested.emit()


# Video preview widget using QVideoSink
class VideoPreview(QWidget):
    def __init__(self, preview_url):
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

        if preview_url.startswith("http"):
            source = QUrl(preview_url)
        else:
            source = QUrl.fromLocalFile(preview_url)

        self.player.setSource(source)
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
        self.player.setSource(QUrl())
        self.player.setVideoOutput(None)
        self.deleteLater()


# Main application window
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowTitle("GIFLibby")
        self.resize(800, 600)

        # Keep previews alive
        self.players = []

        # Keep track of the currently displayed GIFs
        self.displayed_gifs = []

        # Delete mode
        self.delete_mode = False

        # Create interface
        self.create_ui()

    # Open add GIF dialog
    def open_add_dialog(self):
        dialog = AddGifDialog(self)

        if dialog.exec():
            self.show_gifs(force=True)

    # Send GIF to Discord
    def send_gif(self, gif_id):
        send_gif_by_id(gif_id)

    # Enter or execute delete mode
    def toggle_delete_mode(self):
        if self.delete_mode:
            self.delete_selected_gifs()
        else:
            self.start_delete_mode()

    # Start delete selection mode
    def start_delete_mode(self):
        if not self.displayed_gifs:
            return

        self.delete_mode = True

        self.delete_button.setText("Delete Selected")
        self.cancel_delete_button.setVisible(True)

        for index in range(self.gif_grid.count()):
            item = self.gif_grid.itemAt(index)
            card = item.widget()

            if isinstance(card, GifCard):
                card.set_delete_mode(True)

    # Cancel delete selection mode
    def cancel_delete_mode(self):
        self.delete_mode = False

        self.delete_button.setText("Delete")
        self.cancel_delete_button.setVisible(False)

        for index in range(self.gif_grid.count()):
            item = self.gif_grid.itemAt(index)
            card = item.widget()

            if isinstance(card, GifCard):
                card.set_delete_mode(False)

    # Delete selected GIFs
    def delete_selected_gifs(self):
        selected_ids = []

        for index in range(self.gif_grid.count()):
            item = self.gif_grid.itemAt(index)
            card = item.widget()

            if isinstance(card, GifCard) and card.selected:
                selected_ids.append(card.gif_id)

        if not selected_ids:
            QMessageBox.information(
                self,
                "Delete GIFs",
                "No GIFs selected."
            )
            return

        count = len(selected_ids)

        message = (
            f"Are you sure you want to delete {count} GIF"
            f"{'s' if count != 1 else ''}?\n\n"
            "This cannot be undone."
        )

        result = QMessageBox.question(
            self,
            "Delete GIFs",
            message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if result != QMessageBox.Yes:
            return

        for gif_id in selected_ids:
            remove_gif(gif_id)

        self.cancel_delete_mode()
        self.show_gifs(force=True)

    # Delete one GIF
    def delete_single_gif(self, gif_id):
        gif = next(
            (item for item in self.displayed_gifs if item[0] == gif_id),
            None
        )

        if gif is None:
            return

        result = QMessageBox.question(
            self,
            "Delete GIF",
            f'Are you sure you want to delete "{gif[1]}"?\n\n'
            "This cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if result != QMessageBox.Yes:
            return

        remove_gif(gif_id)

        self.show_gifs(force=True)

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
        add_button.clicked.connect(self.open_add_dialog)

        view_button = QPushButton("View GIFs")
        view_button.clicked.connect(self.show_gifs)

        collection_button = QPushButton("Collections")

        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(
            self.toggle_delete_mode
        )

        self.cancel_delete_button = QPushButton("Cancel")
        self.cancel_delete_button.clicked.connect(
            self.cancel_delete_mode
        )
        self.cancel_delete_button.setVisible(False)

        settings_button = QPushButton("Settings")

        for button in [
            add_button,
            view_button,
            collection_button,
            self.delete_button,
            self.cancel_delete_button,
            settings_button
        ]:
            button.setFixedHeight(25)
            button.setFixedWidth(80)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search GIFs...")
        self.search_bar.setFixedHeight(20)
        self.search_bar.setFixedWidth(200)

        banner.addWidget(add_button)
        banner.addWidget(self.create_divider())
        banner.addWidget(view_button)
        banner.addWidget(self.create_divider())
        banner.addWidget(collection_button)
        banner.addWidget(self.create_divider())
        banner.addWidget(self.delete_button)
        banner.addWidget(self.cancel_delete_button)

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

        self.gif_grid.setAlignment(
            Qt.AlignTop | Qt.AlignLeft
        )

        self.gif_grid.setSpacing(10)

        self.gif_container.setLayout(
            self.gif_grid
        )

        self.scroll_area.setWidget(
            self.gif_container
        )

    # Load GIFs into grid
    def show_gifs(self, force=False):
        gifs = list_gifs()

        # Do nothing if the displayed GIF list has not changed
        if not force and gifs == self.displayed_gifs:
            return

        # Exit delete mode
        self.delete_mode = False
        self.delete_button.setText("Delete")
        self.cancel_delete_button.setVisible(False)

        # Remove existing cards
        while self.gif_grid.count():
            item = self.gif_grid.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        # Stop existing previews
        for preview in self.players:
            preview.stop()

        self.players.clear()

        # Store the new displayed GIF list
        self.displayed_gifs = gifs

        if not gifs:
            self.gif_grid.addWidget(
                QLabel("No GIFs found."),
                0,
                0
            )
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
        card = GifCard()

        card.gif_id = gif[0]

        layout = QVBoxLayout()
        layout.setSpacing(0)

        # Selection checkbox
        checkbox = QCheckBox()
        checkbox.setVisible(False)
        checkbox.setFixedHeight(20)

        # Update card selection directly
        checkbox.clicked.connect(
            lambda checked, c=card: setattr(
                c,
                "selected",
                checked
            )
        )

        card.checkbox = checkbox

        layout.addWidget(checkbox)

        # gif[3] is preview_url
        preview = VideoPreview(gif[3])

        layout.addWidget(preview)

        card.setLayout(layout)

        card.clicked.connect(
            lambda gif_id=gif[0]: self.send_gif(gif_id)
        )

        card.delete_requested.connect(
            lambda gif_id=gif[0]: self.delete_single_gif(gif_id)
        )

        return card, preview

    # Create vertical divider
    def create_divider(self):
        divider = QFrame()

        divider.setFrameShape(
            QFrame.VLine
        )

        divider.setFrameShadow(
            QFrame.Sunken
        )

        return divider