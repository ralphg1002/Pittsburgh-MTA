import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class SelectionWindow():
    def __init__(self):
        self.setup_selection_window()
      
    def setup_selection_window(self):
        app = QApplication(sys.argv)
        mainWindow = QWidget()
        mainWindow.setGeometry(350,200,1200,750)
        mainWindow.setWindowTitle("Track Model")
        
        self.add_vline(mainWindow)
        self.add_hline(mainWindow)
        self.add_title(mainWindow)
        self.add_input_section(mainWindow)
        self.add_block_info_label(mainWindow)
        self.add_change_failures_button(mainWindow)
        
        mainWindow.show()
        sys.exit(app.exec_())
        
    def add_vline(self, parent_window):
        thickness = 5
        
        line = QFrame(parent_window)
        line.setFrameShape(QFrame.VLine)
        line.setGeometry(950, 50, thickness, 700)
        line.setLineWidth(thickness)
        
    def add_hline(self, parent_window):
        thickness = 5
        
        line = QFrame(parent_window)
        line.setFrameShape(QFrame.HLine)
        line.setGeometry(0, 50, 1200, thickness)
        line.setLineWidth(thickness)
        
    def add_title(self, parent_window):
        window_width = parent_window.width()
        label_width = 300
        title_position = int((window_width - label_width) / 2)
        
        title_label = QLabel("Track Model", parent_window)
        title_label.setGeometry(title_position, 10, label_width, 30)
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont("Arial", 20, QFont.Bold)
        title_label.setFont(title_font)
        
    def add_input_section(self, parent_window):
        label = QLabel("Enter Block #:", parent_window)
        label.setGeometry(970, 70, 150, 30)
        label.setStyleSheet("font-weight: bold; font-size: 18px")
        
        entry_field = QLineEdit(parent_window)
        entry_field.setGeometry(970, 110, 100, 30)
        entry_field.setPlaceholderText("Enter block number")
        
        button = QPushButton("Go", parent_window)
        button.setGeometry(1080, 110, 60, 30)
        button.setStyleSheet("background-color: blue; color: white")
        
    def add_block_info_label(self, parent_window):
        label = QLabel("Block Information:", parent_window)
        label.setGeometry(970, 160, 200, 30)
        label.setStyleSheet("font-weight: bold; font-size: 18px")
        
        block_info = [
            "Block Length", "Speed Limit", "Elevation", "Cumulative Elevation",
            "Block Grade", "Allowed Directions of Travel", "Track Heater",
            "Failures", "Beacon"
        ]
        y_offset = 190
        for info in block_info:
            checkbox = QCheckBox(info, parent_window)
            checkbox.setGeometry(980, y_offset, 200, 30)
            y_offset += 30
        
        track_info = [
            "Show Occupied Blocks", "Show Switches", 
            "Show Light Signals", "Show Railway Crossings"
        ]
        y_offset += 20
        for info in track_info:
            checkbox = QCheckBox(info, parent_window)
            checkbox.setGeometry(970, y_offset, 200, 30)
            y_offset += 30
    
    def add_change_failures_button(self, parent_window):
        button = QPushButton("Change Failures ->", parent_window)
        button.setStyleSheet("background-color: red; color: white")
        button_width = 200
        button_height = 30
        button_x = int(950 + (parent_window.width() - 950 - button_width) / 2)
        button_y = parent_window.height() - 50
        button.setGeometry(button_x, button_y, button_width, button_height)
        
        
if __name__ == '__main__':
    selectionWindow = SelectionWindow()
