""" GUI Implementation for the project using Qt5 Python bindings """

from PIL.ImageQt import ImageQt
from PyQt5.QtCore import pyqtSignal, Qt, QTimer, QUrl
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QLayout, QStackedWidget, QCheckBox, QLabel, QComboBox, QHBoxLayout, QVBoxLayout, QPushButton, QFrame, QGridLayout, QAction, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap, QFont, QImage, QFontDatabase
from PyQt5.QtMultimedia import QSound, QSoundEffect

from enum import Enum
import sys
import time

import draw

IMAGE_SIZE = 800

class HexagonGridWidget(QWidget):
    def __init__(self, parent, sim):
        """ Widget for visualizing he """
        super(HexagonGridWidget, self).__init__(parent)

        self.sim = sim

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(IMAGE_SIZE, IMAGE_SIZE)

        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.startRendering()

    def renderGrid(self):
        """ Render the hexagonal grid """
        q_image = draw.draw_grid(self.sim.current_grid, IMAGE_SIZE)
        pixmap = QPixmap.fromImage(q_image)
        pixmap = pixmap.scaled(IMAGE_SIZE, IMAGE_SIZE)
        self.image_label.setPixmap(pixmap)
        self.image_label.update()

    def startRendering(self):
        self.renderGrid()
        # Set up rendering loop using a QTimer
        self.frame_time_sum = 0
        self.fps_update_freq = 100
        self.frame_counter = 0
        self.last_frame = None

        self.render_timer = QTimer(self)
        self.current_frame_time = 16
        self.sorting_speed_mult = 1
        self.render_timer.setInterval(self.current_frame_time) #~60 FPS

        self.render_timer.timeout.connect(self.renderTimeout)
        self.render_timer.start()

        # Render one frame
        self.running_sim = True

    def renderTimeout(self):
        """ Run a step of sorting algorithms and then render them to their images """
        if self.running_sim:
            self.sim.update()
            print(f"Iteration: {self.sim.iteration_count}")

        if self.last_frame == None:
            self.last_frame = time.time()

        self.renderGrid()

        # Calculate FPS and print it
        end = time.time()
        self.frame_time_sum += end - self.last_frame
        self.last_frame = end
        self.frame_counter += 1
        if self.frame_counter % self.fps_update_freq == 0:
            print(f'FPS: {self.fps_update_freq/self.frame_time_sum} ({1000*self.frame_time_sum/self.fps_update_freq}ms)')
            self.frame_time_sum = 0
    
    def keyPressEvent(self, event):
        # Play/pause key
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Space:
            self.running_sim = not self.running_sim
        if event.key() == Qt.Key_Right:
            self.modifySpeed(0.5)
        if event.key() == Qt.Key_Left:
            self.modifySpeed(2)

    def modifySpeed(self, scale):
        """ Increases the speed of the sorting visualization """
        if self.current_frame_time >= 16:
            self.current_frame_time = max(16, scale*self.current_frame_time)
            
        self.render_timer.setInterval(self.current_frame_time)

class MainWindow(QMainWindow):
    def __init__(self, sim):
        super().__init__()

        self.setWindowTitle('Snowflake Simulation')
        self.setStyleSheet("background-color: #181818; color: white")

        self.grid_widget = HexagonGridWidget(self, sim)
        self.setCentralWidget(self.grid_widget)

        self.grid_widget.setFocus()
        self.grid_widget.renderGrid()

class MainApplication(QApplication):
    def __init__(self, grid):
        super().__init__([])

        window = MainWindow(grid)
        window.show()

        sys.exit(self.exec_())