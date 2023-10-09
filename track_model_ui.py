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
        title_label.setGeometry(title_position, 10, label_width, 30)  # Position and size of the title label
        title_label.setAlignment(Qt.AlignCenter)  # Center-align the text
        title_font = QFont("Arial", 20, QFont.Bold)  # Customize the font
        title_label.setFont(title_font)
        
        
if __name__ == '__main__':
    selectionWindow = SelectionWindow()
