import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class FailureWindow():
    def __init__(self):
        self.failure_window = QDialog()
        self.setup_failure_popup()
        
    def setup_failure_popup(self):
        self.failure_window.setWindowTitle("Change Failures")
        self.failure_window.setGeometry(1550, 500, 250, 300)
        self.failure_window.setStyleSheet("background-color: #ff4747;")
        
        self.failure_title()
        self.change_background()
        self.add_block_selection()
        self.add_failure_selection()
        self.add_set_button()
    
    def failure_title(self):
        label = QLabel("Failure Configuration:", self.failure_window)
        label.setGeometry(10, 10, 230, 30)
        label.setStyleSheet("font-weight: bold; font-size: 18px")
        
        #Horizontal divider line
        thickness = 5
        line = QFrame(self.failure_window)
        line.setFrameShape(QFrame.HLine)
        line.setGeometry(0, 40, 250, thickness)
        line.setLineWidth(thickness)
    
    def change_background(self):
        background_widget = QWidget(self.failure_window)
        background_widget.setGeometry(0, 45, 250, 300)
        background_widget.setStyleSheet("background-color: #ffd6d6;")
        
    def add_block_selection(self):
        # Add "Select Block #:" label
        label = QLabel("Select Block #:", self.failure_window)
        label.setGeometry(10, 50, 230, 30)
        label.setStyleSheet("font-weight: bold; font-size: 18px; background-color: #ffd6d6;")
        
        # Add a dropdown selection
        self.block_dropdown = QComboBox(self.failure_window)
        self.block_dropdown.setGeometry(10, 80, 115, 30)
        self.block_dropdown.setStyleSheet("background-color: white;")
        # Add items to the dropdown as needed
        for i in range(1, 16):
            self.block_dropdown.addItem("Block " + str(i))
        
        # Connect the combo box to a function that enables/disables the button
        self.block_dropdown.currentIndexChanged.connect(self.update_exit_button_state)
    
    def add_failure_selection(self):
        # Add "Set Failure Type:" label
        label2 = QLabel("Set Failure Type:", self.failure_window)
        label2.setGeometry(10, 120, 230, 30)
        label2.setStyleSheet("font-weight: bold; font-size: 18px; background-color: #ffd6d6;")
        
        failures = [
            "Track Circuit Failure",
            "Power Failure",
            "Broken Rail"
        ]
        
        y_offset = 150
        for failure in failures:
            option = QCheckBox(failure, self.failure_window)
            option.setGeometry(10, y_offset, 230, 30)
            option.setStyleSheet("background-color: #ffd6d6;")
            y_offset += 30
    
    def update_exit_button_state(self):
        #Enable the button to "Set Failure Configuration" if a drop down item from the menu is selected
        is_block_selected = self.block_dropdown.currentIndex() != -1
        self.button.setEnabled(is_block_selected)

    def add_set_button(self):
        self.button = QPushButton("Set Failure Configuration", self.failure_window)
        self.button.setGeometry(50, 250, 150, 30)
        self.button.setStyleSheet("background-color: #39E75F;")
        self.button.clicked.connect(self.failure_window.close)
        self.button.setEnabled(False) #Button is set as disabled to begin with

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
        
        button.clicked.connect(self.show_failure_popup)
        
    def show_failure_popup(self):
        failure_popup = FailureWindow()
        failure_popup.failure_window.exec()
        
        
if __name__ == '__main__':
    selection_window = SelectionWindow()
