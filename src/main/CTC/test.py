import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
#from test_bench_ui import Ui_MainWindow

class ClockWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create a QLabel to display the clock
        self.clock_label = QLabel(self)
        self.clock_label.setAlignment(Qt.AlignCenter | Qt.AlignRight)

        # Create a QTimer to update the clock every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 1000 milliseconds = 1 second

        # Set a larger font for the clock label
        font = QFont()
        font.setPointSize(14)  
        self.clock_label.setFont(font)

    def update_time(self):
        current_time = QTime.currentTime()
        time_str = current_time.toString(Qt.DefaultLocaleLongDate)
        self.clock_label.setText(time_str)

class TestBench(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)

class FileDialogButton(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Create a button that will open the file dialog
        self.browse_button = QPushButton("Browse CSV")
        self.browse_button.clicked.connect(self.open_file_dialog)

        layout.addWidget(self.browse_button)
        self.setLayout(layout)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)

        if filePath:
            # Handle the selected file (e.g., display its content)
            with open(filePath, "r") as file:
                csv_content = file.read()
                # You can display or process the content here

class rectangleX(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(3728, 2000)

class CustomComboBox(QComboBox):
    def __init__(self):
        super().__init__()

class MTALogo(QLabel):
    def __init__(self):
        super().__init__()
       
        image_label = QLabel(self)
        pixmap = QPixmap("MTA.png")

        # Scale the image to the desired size (e.g., 100x100 pixels)
        scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio)
        self.setPixmap(scaled_pixmap)
        self.setGeometry(30, 110, 100, 100)

class TabHeader(QWidget):
    def __init__(self, text):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel(text)

        # Set the font size and make it bold
        font = QFont()
        font.setPointSize(16)  # Adjust the font size as needed
        font.setBold(True)
        self.label.setFont(font)
       
        self.label.setAlignment(Qt.AlignCenter)
        self.line = QFrame()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setGeometry(0, 0, 300, 20)  # Adjust position and length as needed

    def paintEvent(self, event):
        # Override the paintEvent method to draw the line
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.black)
        pen.setWidth(2)

        painter.setPen(pen)
        painter.drawLine(0, self.height() - 2, self.width(), self.height() - 2)

class TabContent1(QWidget, QObject):
    def __init__(self):
        super().__init__()

        # Create a layout for TabContent1
        self.tab1_layout = QVBoxLayout(self)

        # Create a header for Tab 1
        self.tab1_header = TabHeader("Centralized Traffic Control")
        self.tab1_layout.addWidget(self.tab1_header)

        # Create a horizontal layout for the mode buttons
        mode_button_layout = QHBoxLayout()

        # Create the first button
        self.automatic = QPushButton("Automatic Mode")
        self.automatic.setFixedSize(300, 70)
        self.automatic.clicked.connect(self.automatic_clicked)
        mode_button_layout.addWidget(self.automatic)

        # Create the second button
        self.manual = QPushButton("Manual Mode")
        self.manual.setFixedSize(300, 70)
        self.manual.clicked.connect(self.manual_clicked)
        mode_button_layout.addWidget(self.manual)

        # Create the third button
        """self.maintenance = QPushButton("Maintenance Mode")
        self.maintenance.setFixedSize(300, 70)
        self.maintenance.clicked.connect(self.maintenance_clicked)
        mode_button_layout.addWidget(self.maintenance)
        mode_button_layout.setAlignment(Qt.AlignLeft)"""

        spacer = QSpacerItem(2300, 10, QSizePolicy.Fixed, QSizePolicy.Fixed)
        mode_button_layout.addItem(spacer)

 ############################## Active Trains Button ##############################################
        activeTrain = QHBoxLayout()
        """self.active_button = QPushButton("View Active Trains")
        self.active_button.setStyleSheet("background-color: lightcoral;")
        self.active_button.setFixedSize(400, 100)
        activeTrain.addWidget(self.active_button)
        activeTrain.setAlignment(Qt.AlignRight)
        mode_button_layout.addLayout(activeTrain)
        # Create a stacked widget for switching between pages
        self.active_button.clicked.connect(self.active_train)"""

        # Create a table for Active Trains
        self.table = QTableWidget()
        self.table.setColumnCount(2)  # Two columns: Block Number and Train ID
        self.table.setHorizontalHeaderLabels(["Block Number", "Train ID"])

        # Create text boxes to display information
        self.traffic_light_text = QLabel("Traffic Light: N/A")
        self.crossing_state_text = QLabel("Crossing State: N/A")
        self.switch_state_text = QLabel("Switch State: N/A")
        self.speed_text = QLabel("Speed: N/A")
        self.authority_text = QLabel("Authority: N/A")

        # Hide all UI elements initially
        self.table.hide()
        self.traffic_light_text.hide()
        self.crossing_state_text.hide()
        self.switch_state_text.hide()
        self.speed_text.hide()
        self.authority_text.hide()

        # Add the mode button layout to the main layout
        self.tab1_layout.addLayout(mode_button_layout)

        ############## Buttons for what lines can be selected ###############################
        self.lineButton_layout = QHBoxLayout()
        self.lineButton_layout.setEnabled(False)

        # Create the each button
        green = QPushButton("Green Line")
        green.clicked.connect(self.green_clicked)
        green.setFixedSize(300, 70)
        self.lineButton_layout.addWidget(green)

        blue = QPushButton("Blue Line")
        blue.clicked.connect(self.blue_clicked)
        blue.setFixedSize(300, 70)
        self.lineButton_layout.addWidget(blue)

        red = QPushButton("Red Line")
        red.clicked.connect(self.red_clicked)
        red.setFixedSize(300, 70)
        self.lineButton_layout.addWidget(red)
        self.lineButton_layout.setAlignment(Qt.AlignLeft)

        # Hide the line selection buttons initially
        for i in range(self.lineButton_layout.count()):
            widget = self.lineButton_layout.itemAt(i).widget()
            if widget:
                widget.hide()

        # Create a layout for drop-down menus
        self.dropDownLayout = QVBoxLayout()

        spacer = QSpacerItem(300, 300)
        self.dropDownLayout.addSpacerItem(spacer)

        self.dropDownLayout.setEnabled(False)

        # creating drop downs
        self.line_combobox = CustomComboBox()
        self.destination_combobox = CustomComboBox()
        self.arrival_combobox = CustomComboBox()

        # Initialize the drop-down menus
        #self.initialize_combobox(self.line_combobox, 'Select a Line', ['Green Line', 'Red Line', 'Blue Line'], 300, 70)
        self.initialize_combobox(self.line_combobox, 'Select a Line', ['Blue Line'], 300, 70)
        self.line_combobox.setFixedSize(300,100)

        spacer = QSpacerItem(100, 100)
        self.dropDownLayout.addSpacerItem(spacer)

        self.initialize_combobox(self.destination_combobox, 'Select a Departing Station', ['Station A', 'Station B', 'Station C'], 475, 70)
        self.destination_combobox.setFixedSize(475,100)

        spacer = QSpacerItem(100, 100)
        self.dropDownLayout.addSpacerItem(spacer)

        self.initialize_combobox(self.arrival_combobox, 'Select an Arrival Station', ['Station A', 'Station B', 'Station C'], 475, 70)
        self.arrival_combobox.setFixedSize(475,100)

        # Initialize flags for drop-down menus
        self.line_changed = False
        self.destination_changed = False
        self.arrival_changed = False

        # Connect drop-down menus to the update_send_train_button method
        self.line_combobox.currentIndexChanged.connect(self.update_send_train_button)
        self.destination_combobox.currentIndexChanged.connect(self.update_send_train_button)
        self.arrival_combobox.currentIndexChanged.connect(self.update_send_train_button)

        spacer = QSpacerItem(100, 100)
        self.dropDownLayout.addSpacerItem(spacer)

        # Create a button for sending the train
        self.send_train_button = QPushButton("Send Train")
        self.send_train_button.setStyleSheet("background-color: red; color: white;")
        self.send_train_button.setFixedSize(400, 100)
        self.send_train_button.setGeometry(2000,2000,100,100)
        self.send_train_button.clicked.connect(self.send_train_clicked)
        self.send_train_button.setEnabled(False)

        # Create a button for planning the train
        """self.plan_train_button = QPushButton("Plan Train")
        self.plan_train_button.setStyleSheet("background-color: red; color: white;")
        self.plan_train_button.setFixedSize(400, 100)
        self.plan_train_button.setGeometry(6000,4000,100,100)
        self.plan_train_button.clicked.connect(self.plan_train_clicked)
        self.plan_train_button.setEnabled(False)"""

        # Create a layout for the send train button and hide it initially
        self.send_train_layout = QHBoxLayout()
        self.dropDownLayout.addWidget(self.send_train_button)
        #self.dropDownLayout.addWidget(self.plan_train_button)

        # Hide the drop-down menus initially
        for i in range(self.dropDownLayout.count()):
            widget = self.dropDownLayout.itemAt(i).widget()
            if widget:
                widget.hide()

        # Add the line button layout to the main layout
        self.tab1_layout.addLayout(self.lineButton_layout)
        self.tab1_layout.addLayout(self.dropDownLayout)

        self.x_widget = rectangleX()
        self.tab1_layout.addWidget(self.x_widget)

        # Set the layout for TabContent1
        self.setLayout(self.tab1_layout)

        # Initialize the last_clicked_button attribute
        self.last_clicked_button = None
        self.manual_mode_active = False

        #self.clock_widget = ClockWidget()
        #tab1_layout.addWidget(self.clock_widget)

        # Creating a timer for the send train button
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.reset_button)

        # Create and add the "Input an arrival time" label and input field to the main layout
        self.input_label = QLabel("Input an arrival time: ")
        self.input_label.setFont(QFont("Arial", 13))
        self.input_label.setGeometry(1400,100,1000,1000)
        self.arrival_time_input = ""
        self.input_label.hide()

        self.arrival_input = QLineEdit()
        self.arrival_input.setPlaceholderText("0000 (Military Time)")
        self.arrival_input.setGeometry(1900,560,200,75)
        self.arrival_input.hide()
        self.arrival_input.returnPressed.connect(self.handle_arrival_time_input)
        self.input_layout = QHBoxLayout()

        self.input_layout.addWidget(self.input_label)
        self.input_layout.addWidget(self.arrival_input)
        self.input_layout.setAlignment(Qt.AlignBottom)
        self.tab1_layout.addLayout(self.input_layout)

    ############### CSV FILE #########################
        self.file_dialog_button = QPushButton("Browse CSV")
        self.file_dialog_button.setHidden(True)
        self.tab1_layout.addWidget(self.file_dialog_button)
        self.csv_display = QTableWidget()
        self.csv_display.hide()
        self.tab1_layout.addWidget(self.csv_display)
        self.table_visible = False
        self.setLayout(self.tab1_layout)

################# table for importing ###########################################################
        self.schedule_table = QTableWidget()
        self.schedule_table.setColumnCount(6)
        self.schedule_table.setHorizontalHeaderLabels(["Train ID", "Destination Station", "Arrival Station", "Arrival Time", "Speed (mph)", "Delays"])
        self.schedule_table.setStyleSheet("background-color: white;")  # White background
        self.schedule_table.move(400, 100)
        self.schedule_table.hide()
        self.tab1_layout.addWidget(self.schedule_table)
        
        self.table.hide()
        self.traffic_light_text.hide()
        self.crossing_state_text.hide()
        self.switch_state_text.hide()
        self.speed_text.hide()
        self.authority_text.hide()
    ################################ Updating Values ###############################
        # Create a QLabel for displaying the number of ticket sales per hour
        # Create a placeholder for the ticket sales value

    def handle_arrival_time_input(self):
        user_input = self.arrival_input.text()
        self.arrival_time_entered = user_input

    def load_csv_file(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)

        if filePath:
            with open(filePath, "r") as file:
                csv_content = file.read()

            # Split the CSV content into rows
            rows = csv_content.split('\n')

            # Determine the number of rows and columns for the table
            num_rows = len(rows)
            if num_rows > 0:
                num_columns = len(rows[0].split(','))

                # Create a QLabel for throughput and set its text
                self.throughput_label = QLabel("Throughput (Tickets Sold/): 47")
                self.tab1_layout.addWidget(self.throughput_label)  # Add the label to your layout

                # Create a QTableWidget
                self.schedule_table.setRowCount(num_rows)
                self.schedule_table.setColumnCount(num_columns)
                self.schedule_table.setFixedSize(2500, 2500)

                # Populate the QTableWidget with CSV data
                for i, row in enumerate(rows):
                    columns = row.split(',')
                    for j, value in enumerate(columns):
                        item = QTableWidgetItem(value)
                        self.schedule_table.setItem(i, j, item)

                # Set headers for columns
                column_headers = ["Train ID", "Departing Station", "Arrival Station", "Arrival Times", "Speed (mph)", "Delays"]
                self.schedule_table.setHorizontalHeaderLabels(column_headers)
                self.schedule_table.setColumnWidth(0, 400)  # Train ID
                self.schedule_table.setColumnWidth(1, 400)  # Departing Station
                self.schedule_table.setColumnWidth(2, 400)  # Arrival Station
                self.schedule_table.setColumnWidth(3, 400)  # Arrival Times
                self.schedule_table.setColumnWidth(4, 400)  # Speed (mph)
                self.schedule_table.setColumnWidth(5, 400)  # Delays

                # Remove widgets other than the header
                for i in reversed(range(self.tab1_layout.count())):
                    widget = self.tab1_layout.itemAt(i).widget()
                    if widget and widget != self.tab1_header:
                        widget.setParent(None)

                # Create a new table for the "Block Number" and "Occupied" data
                self.blockTable = QTableWidget()
                self.blockTable.setRowCount(num_rows)
                self.blockTable.setColumnCount(2)
                self.blockTable.setHorizontalHeaderLabels(["Block Number", "Occupied"])  # Set header labels
                self.blockTable.setFixedSize(700,200)
                item_block_number = QTableWidgetItem("2")
                item_occupied = QTableWidgetItem("Occupied")
                # Add the new data to the second row
                item_block_number_2 = QTableWidgetItem("3")
                item_occupied_2 = QTableWidgetItem("Occupied")
                self.blockTable.setItem(1, 0, item_block_number_2)
                self.blockTable.setItem(1, 1, item_occupied_2)
                self.blockTable.setItem(0, 0, item_block_number)
                self.blockTable.setItem(0, 1, item_occupied)
                # Add the throughput label and the table to the layout of the main widget
                self.tab1_layout.addWidget(self.throughput_label)
                self.tab1_layout.addWidget(self.blockTable)
                self.tab1_layout.addWidget(self.schedule_table)
    
    def plan_train_clicked(self):
        # Enable the "Send Train" button only when all drop-down menus have valid selections
        if (self.line_combobox.currentIndex() > 0 and 
            self.destination_combobox.currentIndex() > 0 and 
            self.arrival_combobox.currentIndex() > 0 and 
            self.arrival_time_input.text()):
            self.plan_train_clicked.setEnabled(True)      
            self.arrival_combobox.setStyleSheet("")
            self.destination_combobox.setStyleSheet("")
            self.line_combobox.setStyleSheet("")

        else:
            self.send_train_button.setEnabled(False)
            
            if self.line_combobox.currentIndex() <= 0:
                self.line_combobox.setStyleSheet("background-color: yellow;")
            else:
                self.line_combobox.setStyleSheet("")
            if self.destination_combobox.currentIndex() <= 0:
                self.destination_combobox.setStyleSheet("background-color: yellow;")
            else:
                self.destination_combobox.setStyleSheet("")
            if self.arrival_combobox.currentIndex() <= 0:
                self.arrival_combobox.setStyleSheet("background-color: yellow;")
            else:
                self.arrival_combobox.setStyleSheet("")

    def initialize_combobox(self, combobox, default_text, items, width, height):
        # function to create a drop down menu
        combobox.addItem(default_text)
        for item in items:
            combobox.addItem(item)
        combobox.setFixedSize(width, height)
        self.dropDownLayout.addWidget(combobox)

    def send_train_clicked(self):
        # Check if all required fields are selected
        if (self.line_combobox.currentIndex() <= 0 or
            self.destination_combobox.currentIndex() <= 0 or
            self.arrival_combobox.currentIndex() <= 0):
            # Some fields are not selected, do not proceed
            return
        
        # Extract the selected values from the dropdowns
        selected_line = self.line_combobox.currentText()
        departing_station = self.destination_combobox.currentText()
        arrival_station = self.arrival_combobox.currentText()
        arrival_time = self.arrival_input.text()
        if not arrival_time:
            arrival_time = QTime.currentTime()
        # update the schedule table with these values
        self.update_schedule_table(selected_line, departing_station, arrival_station, arrival_time)

        # If all required fields are selected, proceed with sending the train
        self.send_train_button.setEnabled(False)
        self.send_train_button.setStyleSheet("background-color: green; color:white;")
        self.send_train_button.setText("Train Sent")
        self.timer.start(5000)

        # resetting drop downs
        self.line_combobox.setCurrentIndex(0)
        self.destination_combobox.setCurrentIndex(0)
        self.arrival_combobox.setCurrentIndex(0)
        self.arrival_combobox.setStyleSheet("")
        self.destination_combobox.setStyleSheet("")
        self.line_combobox.setStyleSheet("")

    def update_schedule_table(self, line, departing_station, arrival_station, arrival_time):
        arrival_time = self.arrival_input.text()
        if not arrival_time:
            current_time = QTime.currentTime()
            current_time = current_time.addSecs(4 * 60)  # 4 minutes = 4 * 60 seconds
            formatted_time = current_time.toString("HHmm")                   
        else:
            formatted_time = arrival_time

        # Format the time in HHmm (24-hour time) format
        #formatted_time = arrival_time.toString("HHmm")        

        train_id = f'{formatted_time}{departing_station[0]}{departing_station[8]}{arrival_station[0]}{arrival_station[8]}'

        # Determine where to insert the new row in the schedule table
        row_position = self.schedule_table.rowCount()

        # Insert a new row in the schedule table
        self.schedule_table.insertRow(row_position)
        speed = 50
        speed_str = str(speed)
        delays = "on-time"
        # Add the train information to the table
        self.schedule_table.setItem(row_position, 0, QTableWidgetItem(train_id))  # Train ID
        self.schedule_table.setItem(row_position, 1, QTableWidgetItem(departing_station))  # Departing Station
        self.schedule_table.setItem(row_position, 2, QTableWidgetItem(arrival_station))  # Arrival Station
        self.schedule_table.setItem(row_position, 3, QTableWidgetItem(formatted_time))  # Arrival Time
        self.schedule_table.setItem(row_position, 4, QTableWidgetItem(speed_str))  # speed
        self.schedule_table.setItem(row_position, 5, QTableWidgetItem(delays))  # delays

    def enable_send_train_button(self):
        # Enable the send train button if all dropdowns have valid selections
        if (self.line_combobox.currentIndex() > 0 and
            self.destination_combobox.currentIndex() > 0 and
            self.arrival_combobox.currentIndex() > 0):
            self.send_train_button.setEnabled(True)
        else:
            self.send_train_button.setEnabled(False)

    def reset_button(self):
        self.send_train_button.setEnabled(True)
        self.send_train_button.setStyleSheet("background-color: red; color: white;")
        self.send_train_button.setText("Send Train")
        self.timer.stop()
    
    def line_combobox_changed(self):
        # Update the flag for the line drop-down menu
        self.line_changed = True
        # Call the common method to update the button state
        self.update_send_train_button()

    def destination_combobox_changed(self):
        # Update the flag for the destination drop-down menu
        self.destination_changed = True
        # Call the common method to update the button state
        self.update_send_train_button()

    def arrival_combobox_changed(self):
        # Update the flag for the arrival drop-down menu
        self.arrival_changed = True
        # Call the common method to update the button state
        self.update_send_train_button()       
       
    def update_send_train_button(self):
        # Enable the "Send Train" button only when all drop-down menus have valid selections
        if (self.line_combobox.currentIndex() > 0 and
            self.destination_combobox.currentIndex() > 0 and
            self.arrival_combobox.currentIndex() > 0):
            self.send_train_button.setEnabled(True)
            
            self.arrival_combobox.setStyleSheet("")
            self.destination_combobox.setStyleSheet("")
            self.line_combobox.setStyleSheet("")

        else:
            self.send_train_button.setEnabled(False)
            
            if self.line_combobox.currentIndex() <= 0:
                self.line_combobox.setStyleSheet("background-color: yellow;")
            else:
                self.line_combobox.setStyleSheet("")
            if self.destination_combobox.currentIndex() <= 0:
                self.destination_combobox.setStyleSheet("background-color: yellow;")
            else:
                self.destination_combobox.setStyleSheet("")
            if self.arrival_combobox.currentIndex() <= 0:
                self.arrival_combobox.setStyleSheet("background-color: yellow;")
            else:
                self.arrival_combobox.setStyleSheet("")

    def showSendTrainButton(self, show):
        # Show or hide the "Send Train" button based on the 'show' parameter
        self.send_train_layout.setEnabled(show)

    def automatic_clicked(self):
        self.x_widget.draw_x = False

        # Unhighlight the last clicked button, if any
        if self.last_clicked_button:
            self.last_clicked_button.setStyleSheet("")

        self.automatic.setStyleSheet("background-color: lightBlue;")
        self.last_clicked_button = self.automatic

        # Show the line selection buttons when Automatic Mode is clicked
        for i in range(self.lineButton_layout.count()):
            widget = self.lineButton_layout.itemAt(i).widget()
            if widget:
                widget.show()

        # Hide the drop-down menus
        for i in range(self.dropDownLayout.count()):
            widget = self.dropDownLayout.itemAt(i).widget()
            if widget:
                widget.hide()
        
        for i in range(self.input_layout.count()):
            widget = self.input_layout.itemAt(i).widget()
            if widget:
                widget.hide()

         # Show the UI elements when the "Active Trains" button is pressed
        self.table.hide()
        self.traffic_light_text.hide()
        self.crossing_state_text.hide()
        self.switch_state_text.hide()
        self.speed_text.hide()
        self.authority_text.hide()

    def manual_clicked(self):
        # Unhighlight the last clicked button, if any
        if self.last_clicked_button:
            self.last_clicked_button.setStyleSheet("")
        
        self.manual_mode_active = not self.manual_mode_active

        if self.manual_mode_active:
            self.x_widget.draw_x = False
            self.manual.setStyleSheet("background-color: lightBlue;")
            self.last_clicked_button = self.manual

            # Show the drop-down menus for manual mode
            for i in range(self.dropDownLayout.count()):
                widget = self.dropDownLayout.itemAt(i).widget()
                if widget:
                    widget.show()
            
            for i in range(self.lineButton_layout.count()):
                widget = self.lineButton_layout.itemAt(i).widget()
                if widget:
                    widget.hide()


            self.input_layout.setParent(self)
            self.input_layout.setAlignment(Qt.AlignRight)
            # Show the manual input layout for manual mode
            for i in range(self.input_layout.count()):
                widget = self.input_layout.itemAt(i).widget()
                if widget:
                    widget.show()

            # Add the clock widget to the layout
            #self.clock_widget.setParent(self)
            #self.clock_widget.setGeometry(2200, 500, 400, 100)
            #self.clock_widget.show()
            self.csv_display.hide()
            self.file_dialog_button.setHidden(True)
            self.table_visible = False
            self.blockTable.hide()
            self.throughput_label.hide()

        else:
            self.x_widget.draw_x = True
            self.manual.setStyleSheet("")
            # Hide the drop-down menus
            for i in range(self.dropDownLayout.count()):
                widget = self.dropDownLayout.itemAt(i).widget()
                if widget:
                    widget.hide()
            
            # Remove the clock widget from the layout
            #self.clock_widget.hide()
            #self.clock_widget.setParent(None)
            self.arrival_input.hide()
            self.input_label.hide()

    def maintenance_clicked(self):
        self.x_widget.draw_x = False

        # Unhighlight the last clicked button, if any
        if self.last_clicked_button:
            self.last_clicked_button.setStyleSheet("")
       
        self.maintenance.setStyleSheet("background-color: lightBlue;")
        self.last_clicked_button = self.maintenance


        # Show the line selection buttons when Maintenance Mode is clicked
        for i in range(self.lineButton_layout.count()):
            widget = self.lineButton_layout.itemAt(i).widget()
            if widget:
                widget.hide()
       
        # Hide the line selection buttons initially
        for i in range(self.dropDown.count()):
            widget = self.dropDown.itemAt(i).widget()
            if widget:
                widget.hide()

    def green_clicked(self):
        #self.x_widget.draw_x = False
        # Unhighlight the last clicked button, if any
        if self.last_clicked_button:
            self.last_clicked_button.setStyleSheet("")

        # Set the background color for the clicked button
        self.sender().setStyleSheet("background-color: lightBlue;")
        self.last_clicked_button = self.sender()

        self.file_dialog_button.setHidden(False)
        self.file_dialog_button.setGeometry(30, 400, 300, 100)
        """self.browse_button.clicked.connect(self.load_csv_file)
        self.csv_display = QTextEdit()
        self.file_input_layout = QVBoxLayout()
        self.file_input_layout.addWidget(self.browse_button)
        self.file_input_layout.addWidget(self.csv_display)
        self.file_input_layout.setEnabled(False)
        for i in range(self.file_input_layout.count()):
            widget = self.file_input_layout.itemAt(i).widget()
            if widget:
                widget.show()

        green_layout.addLayout(self.file_input_layout)"""

    def red_clicked(self):
        #self.x_widget.draw_x = False

        # Unhighlight the last clicked button, if any
        if self.last_clicked_button:
            self.last_clicked_button.setStyleSheet("")

        # Set the background color for the clicked button
        self.sender().setStyleSheet("background-color: lightBlue;")
        self.last_clicked_button = self.sender()

        # Show the line selection buttons when a line button is clicked
        for i in range(self.lineButton_layout.count()):
            widget = self.lineButton_layout.itemAt(i).widget()
            if widget:
                widget.show()    

    def blue_clicked(self):
        self.tab1_header.show()
        # Unhighlight the last clicked button, if any
        if self.last_clicked_button:
            self.last_clicked_button.setStyleSheet("")

        # Set the background color for the clicked button
        self.sender().setStyleSheet("background-color: lightBlue;")
        self.last_clicked_button = self.sender()

        # Show the line selection buttons when a line button is clicked
        for i in range(self.lineButton_layout.count()):
            widget = self.lineButton_layout.itemAt(i).widget()
            if widget:
                widget.show()

        self.file_dialog_button.setHidden(False)
        self.file_dialog_button.setGeometry(30, 400, 300, 100)
        self.file_dialog_button.clicked.connect(self.load_csv_file)

        if self.table_visible:
            self.csv_display.show()

        self.schedule_table.setParent(self)  # Set the parent to the current widget (or use the appropriate parent)
        #tab1_layout.addWidget(self.schedule_table)  # Add it to the layout
        self.schedule_table.show() 

    def active_train(self):
        print("active train")


class TabContent2(QWidget, QObject):
    def __init__(self, tab_content1):
        super().__init__()
        self.tab_content1 = tab_content1

        # Create a layout for the main window
        main_layout = QHBoxLayout(self)
################################## Inputs ######################################################################
        # Create the left rectangle for "Inputs"
        input_rectangle = QWidget()
        input_layout = QVBoxLayout(input_rectangle)
        self.first_dropdowns = []  # Create a list to store references to the first dropdowns
        self.second_dropdowns = []
        self.third_dropdowns = []  # Initialize a list to store selected block failures
        self.selected_block_failures = []  # Initialize an empty list for block failures

        # Header for "Inputs"
        input_header = QLabel("Inputs")
        input_header.setAlignment(Qt.AlignCenter)  # Center align the title
        input_header.setStyleSheet("font-size: 45px;")  # Increase the font size
        input_layout.addWidget(input_header)

        # Create green rectangles inside the "Inputs" rectangle
        for title in ["Set Ticket Sales (Per Station)", "Change Train Data", "Set Devices and Block States"]:
            green_rectangle = QWidget()
            green_rectangle.setStyleSheet("background-color: lightgreen; border: 1px solid green; margin: 5px;")
            self.green_layout = QVBoxLayout(green_rectangle)

            # Header for the green rectangle
            green_header = QLabel(title)
            green_header.setStyleSheet("font-size: 30; border: 0")  # Increase the font size
            green_header.setFixedSize(500,50)
            green_header.setAlignment(Qt.AlignCenter)  # Center align the title

            if title == "Set Ticket Sales (Per Station)":
                # Create three drop-down menus side by side
                dropdown1 = QComboBox()
                dropdown1.setStyleSheet("background-color: white;")  # White background
                dropdown1.addItem("Select a Line")
                dropdown1.addItem("Green Line")
                dropdown1.addItem("Blue Line")
                dropdown1.addItem("Red Line")
                dropdown1.setFixedSize(400,100)

                dropdown2 = QComboBox()
                dropdown2.setStyleSheet("background-color: white;")  # White background
                dropdown2.addItem("Select a Station")
                dropdown2.addItem("Station 1")
                dropdown2.addItem("Station 2")
                dropdown2.setFixedSize(400,100)

                ticketNum = QLineEdit()
                ticketNum.setStyleSheet("background-color: white;")
                ticketNum.setPlaceholderText("Enter Number of Tickets")
                ticketNum.setFixedSize(400,100)
                # Create a horizontal layout to place the drop-down menus side by side
                dropdown_layout = QHBoxLayout()
                dropdown_layout.addWidget(dropdown1)
                dropdown_layout.addWidget(dropdown2)
                dropdown_layout.addWidget(ticketNum)

                # Add the header and the horizontal layout to the green rectangle
                self.green_layout.addWidget(green_header)
                self.green_layout.addLayout(dropdown_layout)

                #update_ticket_sales_signal = pyqtSignal(int)  # Define a signal to update ticket sales

                # Add an "Update Ticket Sales" button
                self.update_ticket_sales_button = QPushButton("Update Ticket Sales")
                self.update_ticket_sales_button.setFixedSize(300,100)
                self.update_ticket_sales_button.setStyleSheet("background-color: white;")

                #self.update_ticket_sales_button.setGeometry(300,300,500,500)
                #self.update_ticket_sales_button.clicked.connect(self.update_ticket_sales)  # Connect the button to a function to handle the update

                self.green_layout.addWidget(self.update_ticket_sales_button)
                #self.update_ticket_sales_signal.connect(tab_content1.update_ticket_sales_slot)


            elif title == "Change Train Data":
                self.horizontal_layout = QHBoxLayout()
                # Create three drop-down menus stacked vertically
                select_line_dropdown = QComboBox()
                select_line_dropdown.setStyleSheet("background-color: white;")  # White background
                select_line_dropdown.addItem("Select a Line")
                select_line_dropdown.addItem("Line 1")
                select_line_dropdown.setFixedSize(400,100)

                train_id_dropdown = QComboBox()
                train_id_dropdown.setStyleSheet("background-color: white;")  # White background
                train_id_dropdown.addItem("Train ID")
                train_id_dropdown.addItem("Train A")
                train_id_dropdown.setFixedSize(400,100)

                delays_dropdown = QComboBox()
                delays_dropdown.setStyleSheet("background-color: white;")  # White background
                delays_dropdown.addItem("Delays")
                delays_dropdown.addItem("No Delays")
                delays_dropdown.setFixedSize(400,100)

                # Add the header and the drop-down menus to the green rectangle
                self.horizontal_layout.addWidget(green_header)
                self.horizontal_layout.addWidget(select_line_dropdown)
                self.horizontal_layout.addWidget(train_id_dropdown)
                self.horizontal_layout.addWidget(delays_dropdown)

                self.green_layout.addLayout(self.horizontal_layout)
            elif title == "Set Devices and Block States":

                custom_titles = [
                    "Set Switch State",
                    "Set Crossing State",
                    "Set Light State",
                    "Set Block Failure",
                    "Set Maintenance",
                    "Set Occupation"
                ]
                
                custom_first_dropdown_options = ["Select a Line", "Green", "Red", "Blue"]
                custom_second_dropdown_options = ["Select a Block", "Block 1", "Block 2", "Block 3"]
                custom_third_dropdown_options = [
                ["Select State", "Option A", "Option B", "Option C"],
                ["Select State", "Choice X", "Choice Y", "Choice Z"],
                ["Select State", "Value 1", "Value 2", "Value 3"],
                ["Select State", "Shut Down", "Reopen"],
                ["Select State", "Maintain 1", "Maintain 2", "Maintain 3"],
                ["Select State", "Occupied", "Not Occupied"]
                ]

                # Create 6 rows with the specified titles and different options for the first and second drop-downs
                for idx, custom_title in enumerate(custom_titles):
                    row_layout = QHBoxLayout()

                    # Create a title label for the first box in the row
                    title_label = QLabel(custom_title)
                    title_label.setStyleSheet("font-size: 30px; background-color: white;")  # White background for the title
                    row_layout.addWidget(title_label)

                    # Add the first drop-down menu with custom options
                    self.first_dropdown = QComboBox()
                    self.first_dropdown.setStyleSheet("background-color: white;")
                    for option in custom_first_dropdown_options:
                        self.first_dropdown.addItem(option)
                    row_layout.addWidget(self.first_dropdown)
                    self.first_dropdowns.append(self.first_dropdown)
                    
                    # Add the second drop-down menu with custom options
                    self.second_dropdown = QComboBox()
                    self.second_dropdown.setStyleSheet("background-color: white;")
                    for option in custom_second_dropdown_options:
                        self.second_dropdown.addItem(option)
                    row_layout.addWidget(self.second_dropdown)
                    self.second_dropdowns.append(self.second_dropdown)

                    # Add the third drop-down menu with different options
                    self.third_dropdown = QComboBox()
                    self.third_dropdown.setStyleSheet("background-color: white;")
                    for option in custom_third_dropdown_options[idx]:
                        self.third_dropdown.addItem(option)
                    row_layout.addWidget(self.third_dropdown)
                    self.third_dropdowns.append(self.third_dropdown)
                    self.third_dropdown.currentIndexChanged.connect(self.update_block_failures)
                    self.green_layout.addLayout(row_layout)

                # Add the header and content to the green rectangle
                self.green_layout.addWidget(green_header)
                #green_layout.addWidget(content_label)
                # Create a button to update the selections
                self.update_button = QPushButton("Update")
                self.green_layout.addWidget(self.update_button)
                self.update_button.setStyleSheet("background-color: white;")
                self.update_button.setFixedSize(300,100)
                self.update_button.clicked.connect(self.update_right_side_table_with_selected_data)

            # Add the green rectangle to the input layout
            input_layout.addWidget(green_rectangle)

############################### OUTPUTS #################################################################
        # Create the right rectangle for "Outputs"
        output_rectangle = QWidget()
        output_layout = QVBoxLayout(output_rectangle)
        # Header for "Outputs"
        output_header = QLabel("Outputs")
        output_header.setAlignment(Qt.AlignCenter)  # Center align the title
        output_header.setStyleSheet("font-size: 45px;")  # Increase the font size
        output_layout.addWidget(output_header)

        # Create a light red rectangle for "View Train Data" section
        view_train_data_rectangle = QFrame()
        view_train_data_rectangle.setStyleSheet("background-color: lightcoral; margin: 0 auto;")

        # Header for the "View Train Data" section with larger font
        view_train_data_header = QLabel("View Train Data:")
        view_train_data_header.setAlignment(Qt.AlignLeft)  # Center align the title
        view_train_data_header.setStyleSheet("font-size: 30px; color: black;")  # Larger font size and black text color

        # Create drop-down menus with white backgrounds
        self.select_line_dropdown = QComboBox()
        self.select_line_dropdown.setStyleSheet("background-color: white;")  # White background
        self.select_line_dropdown.setFixedSize(500,75)
        self.select_line_dropdown.addItem("Select a Line")
        self.select_line_dropdown.addItem("Blue Line")

        self.train_id_dropdown = QComboBox()
        self.train_id_dropdown.setStyleSheet("background-color: white;")  # White background
        self.train_id_dropdown.setFixedSize(500,75)
        self.train_id_dropdown.addItem("Train ID")
        self.train_id_dropdown.addItem("1200SBSC")
        self.train_id_dropdown.addItem("1000SCSA")

        self.data_box1 = QLabel("Commanded Speed:")
        self.data_box1.setFixedSize(500,75)
        self.data_box1.setStyleSheet("background-color: white;")  # White background
        self.data_box2 = QLabel("Authority:")
        self.data_box2.setFixedSize(500,75)
        self.data_box2.setStyleSheet("background-color: white;")  # White background

        disabled_blocks_label = QLabel("Current Shut Down Blocks:")
        disabled_blocks_label.setAlignment(Qt.AlignCenter)  # Center align the label
        disabled_blocks_label.setStyleSheet("font-size: 30px; color: black; background-color: lightgreen;")
        disabled_blocks_label.setFixedSize(500, 100)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Line", "Block Number"])
        self.table.setStyleSheet("background-color: white;")  # White background

        view_train_data_layout = QVBoxLayout(view_train_data_rectangle)
        view_train_data_layout.addWidget(view_train_data_header)
        view_train_data_layout.addWidget(self.select_line_dropdown)
        view_train_data_layout.addWidget(self.train_id_dropdown)
        view_train_data_layout.addWidget(self.data_box1)
        view_train_data_layout.addWidget(self.data_box2)

        view_train_data_layout.addWidget(disabled_blocks_label)
        view_train_data_layout.addWidget(self.table)
        self.select_line_dropdown.currentIndexChanged.connect(self.update_train_data)
        self.train_id_dropdown.currentIndexChanged.connect(self.update_train_data)

        output_layout.addWidget(view_train_data_rectangle)
        output_rectangle.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred))
        input_rectangle.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred))
        main_layout.addWidget(input_rectangle)
        main_layout.addWidget(output_rectangle)

        self.setLayout(main_layout) 

        
    def update_train_data(self):
        selected_line = self.select_line_dropdown.currentText()
        selected_train_id = self.train_id_dropdown.currentText()

        if selected_train_id == "1200SBSC":
            self.data_box1.setText("Commanded Speed: 50")
            self.data_box2.setText("Authority: 5")
        elif selected_train_id == "1000SCSA":
            self.data_box1.setText("Commanded Speed: 35")
            self.data_box2.setText("Authority: 2")

    def update_block_failures(self, index):
        # Get the selected state from the third dropdown
        selected_state = self.third_dropdown.currentText()
        print(selected_state)
        if selected_state == "Shut down":
            # Add the selected block failure to the list
            line = self.first_dropdown.currentText()
            block = self.second_dropdown.currentText()
            if line != "Select a Line" and block != "Select a Block":
                self.selected_block_failures.append((line, block))
                if (line, block) not in self.selected_block_failures:
                    self.selected_block_failures.append((line, block))
        elif selected_state == "Reopen":
            line = self.first_dropdown.currentText()
            block = self.second_dropdown.currentText()
            # Remove the selected block failure from the list if it exists
            if (line, block) in self.selected_block_failures:
                self.selected_block_failures.remove((line, block))


        # Update the right-side table with the selected block failures
        self.update_right_side_table(self.selected_block_failures)

    def update_right_side_table(self, selected_data):
        # Assuming you have a QTableWidget named 'table' on the right side
        #table = self.findChild(QTableWidget, "table")  # Use the actual name of your table

        if self.table is not None:
            # Add selected data to the table
            for line, block in selected_data:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem(line))
                self.table.setItem(row_position, 1, QTableWidgetItem(block))

    def update_right_side_table_with_selected_data(self):
        # Extract the selected data from the dropdowns
        selected_data = []

        # Loop through the dropdowns in your code to extract the selected data
        for idx in range(6):
            selected_line = self.first_dropdowns[idx].currentText()
            selected_block = self.second_dropdowns[idx].currentText()
            selected_state = self.third_dropdowns[idx].currentText()

            # Add the selected data to the list
            if selected_line != "Select a Line" and selected_block != "Select a Block":
                selected_data.append((selected_line, selected_block))

            # Handle adding/removing block failures based on the selected state
            if selected_state == "Shut down":
                if selected_line != "Select a Line" and selected_block != "Select a Block":
                    self.selected_block_failures.append((selected_line, selected_block))
            elif selected_state == "Reopen":
                try:
                    self.selected_block_failures.remove((selected_line, selected_block))
                except ValueError:
                    pass

        # Update the right-side table with the selected data
        self.update_right_side_table(selected_data)


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CTC: User Interface")
        self.setGeometry(100, 100, 2000, 1500)  # Window size

        # Create a central widget to hold the layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a vertical layout for the central widget
        layout = QVBoxLayout(central_widget)

        # Create a tab widget
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)

        # Create tabs (pages) with content
        tab_content1 = TabContent1()
        tab2 = TabContent2(tab_content1)

        # Add tabs to the tab widget
        tab_widget.addTab(tab_content1, "Wireframe")
        tab_widget.addTab(tab2, "Test Bench")

        # Create a header for Tab 1 and Tab 2
        tab1_header = TabHeader("Centralized Traffic Control")
        tab2_header = TabHeader("Centralized Traffic Control")

        tab_widget.showMaximized()

def main():
    app = QApplication(sys.argv)
    window = MyWindow()

    # Load an image from a file
    mta_logo = QPixmap("mta.png")
    # Create a QLabel and set the pixmap as its content
    image_label = QLabel()
    image_label.setPixmap(mta_logo)
    image_label.setGeometry(600, 600, 100, 100)
    
    # Display MTA Logo
    mta_logo = MTALogo()  # Create an instance of MTALogo
    mta_logo.setParent(window)
    window.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()



