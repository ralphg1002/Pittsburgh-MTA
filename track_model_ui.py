import sys
import load_track
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
        title = QLabel("Failure Configuration:", self.failure_window)
        title.setGeometry(10, 10, 230, 30)
        title.setStyleSheet("font-weight: bold; font-size: 18px")
        
        #Horizontal divider line
        thickness = 5
        hline = QFrame(self.failure_window)
        hline.setFrameShape(QFrame.HLine)
        hline.setGeometry(0, 40, 250, thickness)
        hline.setLineWidth(thickness)
    
    def change_background(self):
        background = QWidget(self.failure_window)
        background.setGeometry(0, 45, 250, 300)
        background.setStyleSheet("background-color: #ffd6d6;")
        
    def add_block_selection(self):
        select_block = QLabel("Select Block #:", self.failure_window)
        select_block.setGeometry(10, 50, 230, 30)
        select_block.setStyleSheet("font-weight: bold; font-size: 18px; background-color: #ffd6d6;")
        
        # Add a dropdown selection
        self.block_dropdown = QComboBox(self.failure_window)
        self.block_dropdown.setGeometry(10, 80, 115, 30)
        self.block_dropdown.setStyleSheet("background-color: white;")
        for i in range(1, 16):
            self.block_dropdown.addItem("Block " + str(i))
        
        self.block_dropdown.currentIndexChanged.connect(self.update_exit_button_state)
    
    def add_failure_selection(self):
        set_failure = QLabel("Set Failure Type:", self.failure_window)
        set_failure.setGeometry(10, 120, 230, 30)
        set_failure.setStyleSheet("font-weight: bold; font-size: 18px; background-color: #ffd6d6;")
    
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
        self.simulation_speed = 1.0
        self.selected_line = None
        self.temperature = 65
        self.setup_selection_window()
      
    def setup_selection_window(self):
        app = QApplication(sys.argv)
        mainWindow = QWidget()
        mainWindow.setGeometry(350,200,1200,750)
        mainWindow.setWindowTitle("Track Model")
        app.setWindowIcon(QIcon("pngs/mta_logo.png"))
        
        #General layout
        self.add_mta_logo(mainWindow)
        self.set_clock(mainWindow)
        self.set_simulation_speed_controls(mainWindow)
        self.add_vline(mainWindow)
        self.add_hline(mainWindow)
        self.add_title(mainWindow)
        
        #Map
        self.add_line_panel(mainWindow)
        self.control_temperature(mainWindow)
        self.add_import_button(mainWindow)
        #The following are hidden initially and are shown upon an excel file import
        self.display_file_path(mainWindow)
        self.add_track_map(mainWindow)
        self.add_map_zoom(mainWindow)
        
        #Block Info Selection
        self.add_input_section(mainWindow)
        self.add_selectable_block_info(mainWindow)
        self.add_change_failures_button(mainWindow)
        
        mainWindow.show()
        sys.exit(app.exec_())
        
    def add_mta_logo(self, parent_window):
        mta_png = QPixmap("pngs/mta_logo.png")
        mta_png = mta_png.scaledToWidth(90)
        mta_logo = QLabel(parent_window)
        mta_logo.setPixmap(mta_png)
        mta_logo.setGeometry(0, 0, mta_png.width(), mta_png.height())
              
    def set_clock(self, parent_window):
        self.clock = QLabel("System Clock: 00:00:00", parent_window)
        self.clock.setGeometry(980, 10, 220, 30)
        self.clock.setStyleSheet("font-weight: bold; font-size: 18px")
        self.update_clock()

        #Update clock in real time while window is open
        timer = QTimer(parent_window)
        timer.timeout.connect(self.update_clock)
        #Update every 1 second
        timer.start(1000)

    def update_clock(self):
        current_datetime = QDateTime.currentDateTime()
        formatted_time = current_datetime.toString("HH:mm:ss")
        self.clock.setText("System Clock: " + formatted_time)
    
    def set_simulation_speed_controls(self, parent_window):
        simulation_speed_text = QLabel("Simulation Speed:", parent_window)
        simulation_speed_text.setGeometry(900, 50, 170, 30)
        simulation_speed_text.setStyleSheet("font-weight: bold; font-size: 18px")

        self.speed_text = QLabel("1.0x", parent_window)
        self.speed_text.setGeometry(1110, 50, 40, 30)
        self.speed_text.setAlignment(Qt.AlignCenter)
        self.speed_text.setStyleSheet("font-weight: bold; font-size: 18px")
        
        decrease_speed = QPushButton("<<", parent_window)
        decrease_speed.setGeometry(1070, 55, 30, 20)
        decrease_speed.clicked.connect(self.decrease_simulation_speed)

        increase_speed = QPushButton(">>", parent_window)
        increase_speed.setGeometry(1160, 55, 30, 20)
        increase_speed.clicked.connect(self.increase_simulation_speed)

    def decrease_simulation_speed(self):
        #Speed cannot go below 0.5
        if self.simulation_speed > 0.5:
            self.simulation_speed -= 0.5
            self.speed_text.setText(f"{self.simulation_speed}x")

    def increase_simulation_speed(self):
        if self.simulation_speed < 5.0:
            self.simulation_speed += 0.5
            self.speed_text.setText(f"{self.simulation_speed}x")
        
    def add_vline(self, parent_window):
        thickness = 5
        
        line = QFrame(parent_window)
        line.setFrameShape(QFrame.VLine)
        line.setGeometry(950, 100, thickness, 700)
        line.setLineWidth(thickness)
        
    def add_hline(self, parent_window):
        thickness = 5
        
        line = QFrame(parent_window)
        line.setFrameShape(QFrame.HLine)
        line.setGeometry(0, 100, 1200, thickness)
        line.setLineWidth(thickness)
   
    def add_title(self, parent_window):        
        window_width = parent_window.width()
        label_width = 300
        title_position = int((window_width - label_width) / 2)
        
        title_label = QLabel("Track Model", parent_window)
        title_label.setGeometry(title_position, 35, label_width, 30)
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont("Arial", 20, QFont.Bold)
        title_label.setFont(title_font)

    def add_line_panel(self, parent_window):
        select_line = QLabel("Select Line:", parent_window)
        select_line.setGeometry(90, 130, 110, 30)
        select_line.setStyleSheet("font-weight: bold; font-size: 18px")

        self.blue_panel = QLabel("Blue Line", parent_window)
        self.green_panel = QLabel("Green Line", parent_window)
        self.red_panel = QLabel("Red Line", parent_window)

        self.blue_panel.setGeometry(20, 160, 80, 30)
        self.green_panel.setGeometry(100, 160, 80, 30)
        self.red_panel.setGeometry(180, 160, 80, 30)
        
        #Initially greyed out as none are selected
        unselected = "background-color: grey; color: white; border: 1px solid black; border-radius: 5px; padding: 5px;"
        self.blue_panel.setStyleSheet(unselected)
        self.green_panel.setStyleSheet(unselected)
        self.red_panel.setStyleSheet(unselected)

        #Handlers that call the select_line method
        self.blue_panel.mousePressEvent = lambda event, line="Blue Line": self.select_line(line)
        self.green_panel.mousePressEvent = lambda event, line="Green Line": self.select_line(line)
        self.red_panel.mousePressEvent = lambda event, line="Red Line": self.select_line(line)

    def select_line(self, selected_line):
        unselected = "background-color: grey; color: white; border: 1px solid black; border-radius: 5px; padding: 5px;"
        if selected_line != self.selected_line:
            if selected_line == "Blue Line":
                self.blue_panel.setStyleSheet("background-color: blue; color: white; border: 1px solid black; border-radius: 5px; padding: 5px;")
                self.green_panel.setStyleSheet(unselected)
                self.red_panel.setStyleSheet(unselected)
            elif selected_line == "Green Line":
                self.blue_panel.setStyleSheet(unselected)
                self.green_panel.setStyleSheet("background-color: green; color: white; border: 1px solid black; border-radius: 5px; padding: 5px;")
                self.red_panel.setStyleSheet(unselected)
            elif selected_line == "Red Line":
                self.blue_panel.setStyleSheet(unselected)
                self.green_panel.setStyleSheet(unselected)
                self.red_panel.setStyleSheet("background-color: red; color: white; border: 1px solid black; border-radius: 5px; padding: 5px;")
                
            self.selected_line = selected_line
            
    def control_temperature(self, parent_window):
        set_temperature = QLabel("Set Temperature:", parent_window)
        set_temperature.setGeometry(420, 130, 160, 30)
        set_temperature.setStyleSheet("font-weight: bold; font-size: 18px")

        self.temperature_input = QLineEdit(parent_window)
        self.temperature_input.setGeometry(440, 160, 40, 30)
        self.temperature_input.setAlignment(Qt.AlignCenter)
        self.temperature_input.setPlaceholderText("65")

        fahrenheit_unit = QLabel("°F", parent_window)
        fahrenheit_unit.setGeometry(480, 160, 30, 30)
        fahrenheit_unit.setStyleSheet("font-weight: bold; font-size: 14px")

        set_temperature_button = QPushButton("Set", parent_window)
        set_temperature_button.setGeometry(500, 160, 60, 30)
        set_temperature_button.setStyleSheet("background-color: blue; color: white")
        set_temperature_button.clicked.connect(self.set_temperature)

    def set_temperature(self):
        if self.temperature_input.text() != "":
            self.temperature = self.temperature_input.text()
        self.temperature_input.setPlaceholderText(str(self.temperature))
        print(self.temperature)

    def add_track_map(self, parent_window):
        self.map_png = QPixmap("pngs/blue_line.png")
        self.og_width, self.og_height = 950, 550
        self.map_width, self.map_height = self.og_width, self.og_height
        self.map_png = self.map_png.scaled(self.map_width, self.map_height)

        self.track_map = QLabel(parent_window)
        self.track_map.setPixmap(self.map_png)
        self.track_map.setGeometry(0, 200, self.map_width, self.map_height)
        self.track_map.hide()

    def add_map_zoom(self, parent_window):
        self.zoom_in_button = QPushButton("+", parent_window)
        self.zoom_in_button.setGeometry(910, 210, 30, 30)
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_in_button.hide()

        self.zoom_out_button = QPushButton("-", parent_window)
        self.zoom_out_button.setGeometry(910, 240, 30, 30)
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.zoom_out_button.hide()

    def zoom_in(self):
        self.map_width += 50
        self.map_height += 50
        self.map_png = self.map_png.scaled(self.map_width, self.map_height)
        self.track_map.setPixmap(self.map_png)

    def zoom_out(self):
        self.map_width -= 50
        self.map_height -= 50
        #Cannot zoom out past original size map
        self.map_width = max(self.map_width, self.og_width)
        self.map_height = max(self.map_height, self.og_height)
        self.map_png = self.map_png.scaled(self.map_width, self.map_height)
        self.track_map.setPixmap(self.map_png)    

    def display_file_path(self, parent_window):
        #Originally, nothing is shown
        self.file_path = QLabel("", parent_window)
        self.file_path.setGeometry(740, 130, 200, 30)
        self.file_path.setAlignment(Qt.AlignRight)
        self.file_path.setStyleSheet("color: #008000; font-size: 9px;")
        
    def update_file_path(self, file_path):
        #When file is selected, its path is shown
        self.file_path.setText("Selected File:\n" + file_path)
    
    def add_import_button(self, parent_window):
        import_button = QPushButton("Import Track Data", parent_window)
        import_button.setGeometry(820, 160, 120, 30)
        import_button.setStyleSheet("background-color: #39E75F;")
        #Need to call lambda as parent_window is not accessible otherwise
        import_button.clicked.connect(lambda: self.import_track_data(parent_window))

    def update_gui(self, file_path):
        self.update_file_path(file_path)
        self.select_line("Blue Line") #Sets label to blue as that is the only line
        self.track_map.show()
        self.zoom_in_button.show()
        self.zoom_out_button.show()
        self.change_failures_button.setEnabled(True)
        
    def import_track_data(self, parent_window):
        options = QFileDialog.Options() | QFileDialog.ReadOnly
        #Opens file explorer in new customized window
        file_path, file_type = QFileDialog.getOpenFileName(parent_window, "Import Track Data", "", "Excel Files (*.xlsx *.xls)", options= options)
        
        if file_path:
            #Update Gui
            self.update_gui(file_path)
            
            self.track_data = load_track.read_track_data(file_path)
            print(self.track_data)
        
    def add_input_section(self, parent_window):
        label = QLabel("Enter Block #:", parent_window)
        label.setGeometry(970, 120, 150, 30)
        label.setStyleSheet("font-weight: bold; font-size: 18px")
        
        entry_field = QLineEdit(parent_window)
        entry_field.setGeometry(970, 160, 100, 30)
        entry_field.setPlaceholderText("Enter block #")
        
        button = QPushButton("Go", parent_window)
        button.setGeometry(1080, 160, 60, 30)
        button.setStyleSheet("background-color: blue; color: white")
        
    def add_selectable_block_info(self, parent_window):
        label = QLabel("Block Information:", parent_window)
        label.setGeometry(970, 210, 200, 30)
        label.setStyleSheet("font-weight: bold; font-size: 18px")
        
        block_info = [
            "Block Length", "Speed Limit", "Elevation", "Cumulative Elevation",
            "Block Grade", "Allowed Directions of Travel", "Track Heater",
            "Failures", "Beacon"
        ]
        y_offset = 240
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
        self.change_failures_button = QPushButton("Change Failures ->", parent_window)
        self.change_failures_button.setStyleSheet("background-color: red; color: white")
        button_width = 200
        button_height = 30
        button_x = int(950 + (parent_window.width() - 950 - button_width) / 2)
        button_y = parent_window.height() - 50
        self.change_failures_button.setGeometry(button_x, button_y, button_width, button_height)
        self.change_failures_button.setEnabled(False)
        
        self.change_failures_button.clicked.connect(self.show_failure_popup)
        
    def show_failure_popup(self):
        failure_popup = FailureWindow()
        failure_popup.failure_window.exec()
        
        
if __name__ == '__main__':
    selection_window = SelectionWindow()
