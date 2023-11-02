# importing libraries
import sys
import math
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import csv
from datetime import datetime, timedelta

#from .signals import CTCtoTrackController, TrackControllerToCTC

class CTCWindow(QMainWindow):
    # font variables
    textFontSize = 9
    labelFontSize = 12
    headerFontSize = 16
    titleFontSize = 22
    fontStyle = 'Product Sans'
    # color variables
    colorDarkBlue = '#085394'
    colorLightRed = '#EA9999'
    colorLightBlue = '#9FC5F8'
    colorLightGrey = '#CCCCCC'
    colorMediumGrey = '#DDDDDD'
    colorDarkGrey = '#666666'
    colorBlack = '#000000' 
    # dimensions
    w = 960
    h = 960
    moduleName = 'CTC'

    def __init__(self):
        super().__init__()
        self.mode_handler = ModeHandler(self)
        self.scheduler = Scheduler(self)
        # setting title
        self.setWindowTitle(self.moduleName)

        # setting geometry
        self.setGeometry(50, 50, self.w, self.h)

        """main window template layout"""
        # body block
        self.bodyBlock = QLabel(self)
        self.bodyBlock.setGeometry(20, 20, 920, 920)
        self.bodyBlock.setStyleSheet('background-color: white;'
                                     'border: 1px solid black')

        # header block
        self.headerBlock = QLabel(self)
        self.headerBlock.setGeometry(20, 20, 920, 70)
        self.headerBlock.setStyleSheet('background-color:' + self.colorDarkBlue + ';'
                                       'border: 1px solid black')

        # title
        self.titleLabel = QLabel('Pittsburgh Metropolitan Transportation Authority', self)
        self.titleLabel.setFont(QFont(self.fontStyle, self.titleFontSize))
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setGeometry(120,35,400,400)
        self.titleLabel.adjustSize()
        self.titleLabel.setStyleSheet('color: white')

        # logo
        self.pixmapMTALogo = QtGui.QPixmap('src/main/CTC/MTA_NYC_logo.svg.png')
        self.pixmapMTALogo = self.pixmapMTALogo.scaled(70, 70)
        self.logo = QLabel(self)
        self.logo.setPixmap(self.pixmapMTALogo)
        self.logo.move(20, 20)
        self.logo.adjustSize()

        # module
        self.moduleLabel = QLabel('Centralized Traffic Control', self)
        self.moduleLabel.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.moduleLabel.setAlignment(Qt.AlignCenter)
        self.moduleLabel.move(30, 100)
        self.moduleLabel.adjustSize()
        self.moduleLabel.setStyleSheet('color:' + self.colorDarkBlue)

        # test bench icon
        self.pixmapGear = QtGui.QPixmap('src/main/CTC/gear_icon.png')
        self.pixmapGear = self.pixmapGear.scaled(25, 25)
        self.testbenchIcon = QLabel(self)
        self.testbenchIcon.setPixmap(self.pixmapGear)
        self.testbenchIcon.setGeometry(30, 140, 32, 32)

        # test bench button
        self.testbenchButton = QPushButton('Test Bench', self)
        self.testbenchButton.setFont(QFont(self.fontStyle, self.textFontSize))
        self.testbenchButton.setGeometry(60, 140, 100, 32)
        self.testbenchButton.setStyleSheet('color:' + self.colorDarkBlue +
                                           ';border: 1px solid white')

        # system time input
        self.systemTimeInput = QLabel('00:00:00', self)
        self.systemTimeInput.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.systemTimeInput.setGeometry(820,67,150,100)
        self.systemTimeInput.setStyleSheet('color:' + self.colorDarkBlue)

        # system time label
        self.systemTimeLabel = QLabel('System Time:', self)
        self.systemTimeLabel.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.systemTimeLabel.adjustSize()
        self.systemTimeLabel.setGeometry(650, 65, 200, 100)
        self.systemTimeLabel.setStyleSheet('color:' + self.colorDarkBlue)

        # system speed label
        self.systemSpeedLabel = QLabel('System Speed:', self)
        self.systemSpeedLabel.setFont(QFont(self.fontStyle, self.textFontSize))
        self.systemSpeedLabel.setGeometry(700,140,100,100)
        self.systemSpeedLabel.adjustSize()
        self.systemSpeedLabel.setStyleSheet('color:' + self.colorDarkBlue)

        # system speed input
        self.systemSpeedInput = QLabel('x1.0', self)
        self.systemSpeedInput.setFont(QFont(self.fontStyle, self.textFontSize))
        self.systemSpeedInput.setGeometry(850,127,50,50)
        self.systemSpeedInput.setStyleSheet('color:' + self.colorDarkBlue)

        # increase system speed button
        self.pixmapFastForward = QtGui.QPixmap('src/main/CTC/fast-forward.svg')
        self.pixmapFastForward = self.pixmapFastForward.scaled(20, 20)
        self.speedUpButton = QPushButton(self)
        self.speedUpButton.setIcon(QtGui.QIcon(self.pixmapFastForward))
        self.speedUpButton.setGeometry(890, 143, 20, 20)
        self.speedUpButton.setStyleSheet('color:' + self.colorDarkBlue +
                                         ';border: 1px solid white')

        # decrease system speed button
        self.pixmapRewind = QtGui.QPixmap('src/main/CTC/rewind.svg')
        self.pixmapRewind = self.pixmapRewind.scaled(20, 20)
        self.slowDownButton = QPushButton(self)
        self.slowDownButton.setIcon(QtGui.QIcon(self.pixmapRewind))
        self.slowDownButton.setGeometry(819, 143, 20, 20)
        self.slowDownButton.setStyleSheet('color:' + self.colorDarkBlue +
                                          ';border: 1px solid white')
        
################################# MODE BUTTONS #############################################################################
        self.last_clicked_button = None
        # Add an "Automatic Mode" button
        self.automatic = QPushButton("Automatic Mode", self)
        self.automatic.setGeometry(30, 180, 130, 30)  # Set the button's position and size
        self.automatic.setFont(QFont(self.fontStyle, self.textFontSize))
        self.automatic.setStyleSheet('background-color: ' + self.colorLightGrey + '; color: ' + self.colorDarkBlue + '; border: 1px solid black')
        self.automatic.clicked.connect(self.mode_handler.automaticButtonClicked)

        # Manual Button
        self.manual = QPushButton("Manual Mode", self)
        self.manual.setGeometry(165, 180, 130, 30)  # Set the button's position and size
        self.manual.setFont(QFont(self.fontStyle, self.textFontSize))
        self.manual.setStyleSheet('background-color: white; color:' + 
                                  self.colorBlack + '; border: 1px solid black')
        self.manual.clicked.connect(self.mode_handler.manualButtonClicked) 
        
        # Maintenance Button
        self.maintenance = QPushButton("Maintenance Mode", self)
        self.maintenance.setGeometry(300, 180, 130, 30)  # Set the button's position and size
        self.maintenance.setFont(QFont(self.fontStyle, self.textFontSize))
        self.maintenance.setStyleSheet('background-color: white; color:' +
                                        self.colorBlack + '; border: 1px solid black')
        self.maintenance.clicked.connect(self.mode_handler.maintenanceButtonClicked) 

        # Select a Line
        self.selectLine = QComboBox(self)
        self.selectLine.setGeometry(30, 220, 130, 30)
        self.selectLine.addItem("Select a Line")
        self.selectLine.addItem("Blue Line")
        self.selectLine.addItem("Green Line")
        self.selectLine.addItem("Red Line")
        self.selectLine.setFont(QFont(self.fontStyle, self.textFontSize))
        self.selectLine.currentIndexChanged.connect(self.scheduler.getSelectedLine)  
        
        # CSV File Button
        self.inputSchedule = QPushButton("Import Schedule", self)
        self.inputSchedule.setGeometry(165, 220, 130, 30)  # Set the button's position and size
        self.inputSchedule.setFont(QFont(self.fontStyle, self.textFontSize))
        self.inputSchedule.setStyleSheet('background-color: white; color:' + 
                                         self.colorBlack + '; border: 1px solid black')
        self.inputSchedule.clicked.connect(self.scheduler.load_file)    

################################# Automatic ###################################################################
        # Error text
        self.error_label = QLabel("", self)
        self.error_label.setFont(QFont(self.fontStyle, self.textFontSize))
        self.error_label.setStyleSheet("color: red")
        self.error_label.setGeometry(170, 245, 125, 30)

        # Schedule Table
        self.schedule_header = QLabel("Schedule:", self)
        self.schedule_header.setFont(QFont(self.fontStyle, self.textFontSize))
        self.schedule_header.setGeometry(30,430,500,100)
        self.schedule_table = QTableWidget(self)
        self.schedule_table.setColumnCount(5)
        self.schedule_table.setHorizontalHeaderLabels(["Train ID", "Departing From","Stops", "Departure Time", "Arrival Time"])
        self.schedule_table.setStyleSheet("background-color: white;")  
        self.schedule_table.setGeometry(35,500,890,430)
        self.schedule_table.setColumnWidth(0, 150) 
        self.schedule_table.setColumnWidth(1, 150)  
        self.schedule_table.setColumnWidth(2, 250) 
        self.schedule_table.setColumnWidth(3, 130) 
        self.schedule_table.setColumnWidth(4, 130)
        self.schedule_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Occupancy Table
        self.occupancy_header = QLabel("Occupied Blocks:", self)
        self.occupancy_header.setFont(QFont(self.fontStyle, self.textFontSize))
        self.occupancy_header.setGeometry(675,159,120,100)
        self.occupancy_table = QTableWidget(self)
        self.occupancy_table.setColumnCount(2)
        self.occupancy_table.setHorizontalHeaderLabels(["Block", "Line"])
        self.occupancy_table.setStyleSheet("background-color: white;")  
        self.occupancy_table.setGeometry(675,225,252,265)

        # Throughput per line
        self.throughput_label = QLabel("Throughput: N/A", self)
        self.throughput_label.setFont(QFont(self.fontStyle, self.textFontSize))
        self.throughput_label.setGeometry(50, 275, 400, 50)

        # Commanded Speed
        self.speed_label = QLabel("Commanded Speed (mph): N/A", self)
        self.speed_label.setFont(QFont(self.fontStyle, self.textFontSize))
        self.speed_label.setGeometry(50, 300, 600, 50)

        # Authority
        self.authority_label = QLabel("Authority: N/A", self)
        self.authority_label.setFont(QFont(self.fontStyle, self.textFontSize))
        self.authority_label.setGeometry(50, 325, 600, 50)


############################################## MANUAL MODE #################################################################
        # Departing Station
        self.departingStation = QComboBox(self)
        self.departingStation.setVisible(False)
        self.departingStation.setGeometry(50, 275, 200, 55)
        self.departingStation.addItem("Select a Departing Station")
        self.selectLine.currentIndexChanged.connect(self.scheduler.updateDepartingStations)
        self.departingStation.setFont(QFont(self.fontStyle, 9)) 

        # Next Station
        """self.arrivalStation = QComboBox(self)
        self.arrivalStation.setVisible(False)
        self.arrivalStation.setGeometry(50, 350, 200, 55)
        self.arrivalStation.addItem("Select Arrival Station")
        self.selectLine.currentIndexChanged.connect(self.scheduler.updateArrivalStation)
        self.arrivalStation.setFont(QFont(self.fontStyle, 9))  """

        # Send Train Button
        self.sendTrain = QPushButton("Send Train", self)
        self.sendTrain.setVisible(False)
        self.sendTrain.setGeometry(775,563,150,50)
        self.sendTrain.setFont(QFont(self.fontStyle, self.textFontSize))
        self.sendTrain.setStyleSheet('background-color: ' + self.colorLightRed + '; color: ' + self.colorBlack + '; border: 1px solid black')
        self.sendTrain.clicked.connect(self.scheduler.sendTrainClicked) 

        # Input an arrival time
        self.arrivalTime = QLineEdit(self)
        self.arrivalTime.setVisible(False)
        self.arrivalTime.setPlaceholderText("0000 (Military Time)")
        self.arrivalHeader = QLabel("Input an Arrival Time:", self)
        self.arrivalHeader.setFont(QFont(self.fontStyle, self.textFontSize))
        self.arrivalHeader.setVisible(False)
        self.arrivalHeader.setGeometry(575,210, 200, 100)
        self.arrivalTime.setGeometry(575,275,200,50)

        # Add Stop Button
        self.addStopButton = QPushButton("Add Stop", self)
        self.addStopButton.setVisible(False)
        self.addStopButton.setFont(QFont(self.fontStyle, self.textFontSize))
        self.addStopButton.setGeometry(450, 275, 100, 50)  
        self.addStopButton.setStyleSheet('background-color: white; color: ' + self.colorDarkBlue + '; border: 1px solid black')
        self.addStopButton.clicked.connect(self.scheduler.addStopPressed)
        self.current_departing_station = None

        # Add Stop Dropdown
        self.addStopDropdown = QComboBox(self)
        self.addStopDropdown.setGeometry(275,275,165,50)
        self.addStopDropdown.hide()
        self.stops = [] 
        self.current_stop_index = 0
        self.update_timer = QTimer(self)
        
        self.selectLine.currentIndexChanged.connect(self.scheduler.updateStopDropDown)  # Connect the signal to update the dropdown
        self.max_block = None 

        # Selected Stops Table
        self.stopsQueueHeader = QLabel("Selected Stops:", self)
        self.stopsQueueHeader.setFont(QFont(self.fontStyle, self.textFontSize))
        self.stopsQueueHeader.setGeometry(277,290,120,100)
        self.stopsQueueHeader.hide()
        self.stopsTable = QTableWidget(self)
        self.stopsTable.setColumnCount(2)
        self.stopsTable.setHorizontalHeaderLabels(["Station", "Dwell Time"])
        self.stopsTable.setStyleSheet("background-color: white;")  
        self.stopsTable.setGeometry(278,350,275,200)
        self.stopsTable.hide()

        self.show()

    def show_gui(self):
        self.ui.show()

"""class SignalHandlers:
    def __init__(self):
        # Connect signals to slots in the constructor
        CTCtoTrackController.sendAuthority.connect(self.handleAuthority)
        CTCtoTrackController.sendSuggestedSpeed.connect(self.handleSuggestedSpeed)
        CTCtoTrackController.sendMaintenance.connect(self.handleMaintenance)
        TrackControllerToCTC.sendOccupancyCTC.connect(self.handleOccupancy)
        TrackControllerToCTC.sendFailureStateCTC.connect(self.handleFailureState)
        TrackControllerToCTC.sendSwitchStateCTC.connect(self.handleSwitchState)
        TrackControllerToCTC.sendLightStateCTC.connect(self.handleLightState)
        TrackControllerToCTC.sendTicketSalesCTC.connect(self.handleTicketSales)

    def handleOccupancy(self, line, block_number, state):
        # Handle the occupancy signal here
        print(f"Received Occupancy Signal: Line {line}, Block {block_number}, State {state}")

    def handleFailureState(self, line, block_number, state):
        # Handle the failure state signal here
        print(f"Received Failure State Signal: Line {line}, Block {block_number}, State {state}")

    def handleSwitchState(self, line, block_number, state):
        # Handle the switch state signal here
        print(f"Received Switch State Signal: Line {line}, Block {block_number}, State {state}")

    def handleLightState(self, line, block_number, state):
        # Handle the light state signal here
        print(f"Received Light State Signal: Line {line}, Block {block_number}, State {state}")

    def handleTicketSales(self, line, ticket_sales):
        # Handle the ticket sales signal here
        print(f"Received Ticket Sales Signal: Line {line}, Ticket Sales {ticket_sales}")

    def handleAuthority(self, line, block_number, authority):
        # Handle the authority signal here
        print(f"Received Authority Signal: Line {line}, Block {block_number}, Authority {authority}")

    def handleSuggestedSpeed(self, line, block_number, suggested_speed):
        # Handle the suggested speed signal here
        print(f"Received Suggested Speed Signal: Line {line}, Block {block_number}, Suggested Speed {suggested_speed}")

    def handleMaintenance(self, line, block_number, disabled):
        # Handle the maintenance signal here
        status = "disabled" if disabled else "enabled"
        print(f"Received Maintenance Signal: Line {line}, Block {block_number}, Status {status}")
"""
    
class ModeHandler:
    def __init__(self, main_window):
        self.main_window = main_window

    # function for if automatic button is pressed
    def automaticButtonClicked(self):   
        main_window = self.main_window
     
        # Unhighlight the last clicked button, if any
        if main_window.last_clicked_button:
            main_window.last_clicked_button.setStyleSheet("")
        
        main_window.last_clicked_button = main_window.automatic
        main_window.automatic.setStyleSheet('background-color: ' + main_window.colorLightGrey + '; color: ' + main_window.colorDarkBlue + '; border: 1px solid black')

        main_window.throughput_label.setVisible(True)
        main_window.speed_label.setVisible(True)
        main_window.authority_label.setVisible(True)
        main_window.occupancy_header.setVisible(True)
        main_window.occupancy_table.setVisible(True)
        main_window.schedule_table.setVisible(True)
        main_window.schedule_table.setGeometry(35,500,890,430)
        main_window.schedule_header.setVisible(True)
        main_window.schedule_header.setGeometry(30,430,500,100)
        main_window.selectLine.setVisible(True)
        main_window.inputSchedule.setVisible(True)
        main_window.departingStation.setVisible(False)
        #main_window.arrivalStation.setVisible(False)
        main_window.sendTrain.setVisible(False)
        main_window.arrivalHeader.setVisible(False)
        main_window.arrivalTime.setVisible(False)
        main_window.addStopButton.setVisible(False)
        main_window.addStopDropdown.setVisible(False)
        main_window.stopsQueueHeader.setVisible(False)
        main_window.stopsTable.setVisible(False)

    # function for if manual button is pressed
    def manualButtonClicked(self): 
        main_window = self.main_window

        main_window.automatic.setStyleSheet('background-color: white; color:' + main_window.colorBlack + '; border: 1px solid black')       
        # Unhighlight the last clicked button, if any
        if main_window.last_clicked_button:
            main_window.last_clicked_button.setStyleSheet("")
        
        main_window.last_clicked_button = main_window.manual
        main_window.manual.setStyleSheet('background-color: ' + main_window.colorLightGrey + '; color: ' + main_window.colorDarkBlue + '; border: 1px solid black')
        
        # Hide the elements
        main_window.throughput_label.setVisible(False)
        main_window.speed_label.setVisible(False)
        main_window.authority_label.setVisible(False)
        main_window.occupancy_header.setVisible(False)
        main_window.occupancy_table.setVisible(False)
        main_window.schedule_table.setVisible(True)
        main_window.schedule_table.setRowCount(0)
        main_window.schedule_table.setGeometry(35,625,890,300)
        main_window.schedule_header.setVisible(True)
        main_window.schedule_header.setGeometry(30,560,100,100)
        main_window.selectLine.setVisible(True)
        main_window.selectLine.setCurrentIndex(0)
        main_window.inputSchedule.setVisible(True)
        main_window.departingStation.setVisible(True)
        #main_window.arrivalStation.setVisible(True)
        main_window.sendTrain.setVisible(True)
        main_window.arrivalHeader.setVisible(True)
        main_window.arrivalTime.setVisible(True)
        main_window.addStopButton.setVisible(True)
        main_window.addStopDropdown.setVisible(True)
        main_window.stopsQueueHeader.setVisible(True)
        main_window.stopsTable.setVisible(True)

    # function for if maintenance button is pressed
    def maintenanceButtonClicked(self):   
        main_window = self.main_window

        main_window.automatic.setStyleSheet('background-color: white; color:' + main_window.colorBlack + '; border: 1px solid black')      
        # Unhighlight the last clicked button, if any
        if main_window.last_clicked_button:
            main_window.last_clicked_button.setStyleSheet("")
        
        main_window.last_clicked_button = main_window.self.maintenance
        main_window.maintenance.setStyleSheet('background-color: ' + main_window.colorLightGrey + '; color: ' + main_window.colorDarkBlue + '; border: 1px solid black')

        main_window.throughput_label.setVisible(False)
        main_window.speed_label.setVisible(False)
        main_window.authority_label.setVisible(False)
        main_window.occupancy_header.setVisible(False)
        main_window.occupancy_table.setVisible(False)
        main_window.schedule_table.setVisible(False)
        main_window.schedule_header.setVisible(False)
        main_window.selectLine.setVisible(False)
        main_window.inputSchedule.setVisible(False)
        main_window.departingStation.setVisible(False)
        #main_window.arrivalStation.setVisible(False)
        main_window.sendTrain.setVisible(False)
        main_window.arrivalHeader.setVisible(False)
        main_window.arrivalTime.setVisible(False)
        main_window.addStopButton.setVisible(False)
        main_window.addStopDropdown.setVisible(False)
        main_window.stopsQueueHeader.setVisible(False)
        main_window.stopsTable.setVisible(False)

class Scheduler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.trainList = []
        self.numTrains = 0
        self.routing = Routing('src/main/CTC/GreenLine.csv', main_window)  # Create an instance of the Routing class
        self.trainID = None

    def load_file(self):
        selected_line = self.main_window.selectLine.currentText()
        if selected_line == "Select a Line":
            # Set the error message text
            self.main_window.error_label.setText("Please select a line.")
            return
        
        self.main_window.error_label.clear()

        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self.main_window, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)

        if filePath:
            with open(filePath, "r") as file:
                csv_content = file.read()

            # Split the CSV content into rows
            rows = csv_content.split('\n')

            # Determine the number of rows and columns for the table
            num_rows = len(rows)
            if num_rows > 0:
                num_columns = len(rows[0].split(','))

                # Create a QTableWidget
                self.main_window.schedule_table.setRowCount(num_rows)
                self.main_window.schedule_table.setColumnCount(num_columns)

                # Populate the table with CSV data
                for i, row in enumerate(rows):
                    columns = row.split(',')
                    for j, value in enumerate(columns):
                        item = QTableWidgetItem(value)
                        self.main_window.schedule_table.setItem(i, j, item)
            
        # This makes the table uneditable
        for row in range(self.main_window.schedule_table.rowCount()):
            for col in range(self.main_window.schedule_table.columnCount()):
                item = self.main_window.schedule_table.item(row, col)
                if item:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
    
    def setThroughput(self, throughput_value):
        self.main_window.throughput_label.setText("Throughput: " + str(throughput_value))

    def getThroughput(self):
        throughput_text = self.main_window.throughput_label.text()
        # Extract the throughput value from the label's text
        throughput_value = throughput_text.replace("Throughput: ", "")
        # You may want to handle potential conversion errors if needed
        return float(throughput_value) if throughput_value != "N/A" else None

    def setAuthority(self, authority_value):
        self.main_window.authority_label.setText("Authority: " + str(authority_value))

    def getAuthority(self):
        authority_text = self.main_window.throughput_label.text()
        # Extract the throughput value from the label's text
        authority_value = authority_text.replace("Authority: ", "")
        # You may want to handle potential conversion errors if needed
        return float(authority_value) if authority_value != "N/A" else None

    def setCommandedSpeed(self, speed_value):
        self.main_window.speed_label.setText("Suggested Speed (mph): " + str(speed_value))

    def getCommandedSpeed(self):
        speed_text = self.main_window.speed_label.text()
        # Extract the throughput value from the label's text
        speed_value = speed_text.replace("Suggested Speed (mph): ", "")
        # You may want to handle potential conversion errors if needed
        return float(speed_value) if speed_value != "N/A" else None
    
    def updateDepartingStations(self):
        # Clear the existing items in the departingStation ComboBox
        self.main_window.departingStation.clear()
        self.main_window.departingStation.addItem("Yard")
        self.selected_line = self.main_window.selectLine.currentText()

    """def updateArrivalStation(self):
        # Clear the existing items in the arrivalStation ComboBox
        self.main_window.arrivalStation.clear()
        #self.main_window.arrivalStation.addItem("Select Arrival Station")
        self.selected_line = self.main_window.selectLine.currentText()

        # Update the available stations with stations that are not in 'stops'
        if self.selected_line == "Blue Line":
            self.available_stations = ["Station B", "Station C"]
        elif self.selected_line == "Red Line":
            self.available_stations = ["Shadyside", "Herron Ave", "Swissville", "Penn Station", "Steel Plaza", "First Ave", "Station Square", "South Hills Junction"]
        elif self.selected_line == "Green Line":
            self.available_stations = ["Pioneer", "Edgebrook", "Whited", "South Bank", "Central", "IngleWood", "OverBrook", "Glenbury", "Dormont", "Mt Lebanon", "Poplar", "Castle Shannon"]
        else:
            self.available_stations = []

        # Filter out stations that are already in 'stops'
        self.available_stations = [station for station in self.available_stations if station not in self.main_window.stops]

        # Add the updated available stations to the drop-down
        self.main_window.arrivalStation.addItems(self.available_stations)"""

    def sendTrainClicked(self):
        selected_line = self.main_window.selectLine.currentText()
        departing_station = self.main_window.departingStation.currentText()
        #arrival_station = self.main_window.arrivalStation.currentText()
        arrival_time = self.main_window.arrivalTime.text()
        print("Arrival Time: ", {arrival_time})
        current_time = QTime.currentTime()

        if selected_line == "Select a Line":
            QMessageBox.critical(self.main_window, "Invalid Selection", "Please select a line.")
        elif departing_station == "Select a Departing Station":
            QMessageBox.critical(self.main_window, "Invalid Selection", "Please select a departing station.")
        #elif arrival_station == "Select Arrival Station":
            #QMessageBox.critical(self.main_window, "Invalid Selection", "Please select an arrival station.")
        elif arrival_time and (not arrival_time.isdigit() or len(arrival_time) != 4):
            QMessageBox.critical(self.main_window, "Invalid Arrival Time", "Please enter a valid military time (HHmm).")
        elif arrival_time and int(arrival_time) > 2359:
            QMessageBox.critical(self.main_window, "Invalid Arrival Time", "Arrival time cannot exceed 2359.")
        elif arrival_time and int(arrival_time) < int(QTime.currentTime().toString("HHmm")):
            QMessageBox.critical(self.main_window, "Invalid Arrival Time", "Arrival time cannot be before the current time.")
        else:
            arrival_stations = []
            arrival_stations.extend(self.main_window.stops)
            #arrival_stations.append(arrival_station)
            station_info_list = []
            print(arrival_stations)
            for arrival_station in arrival_stations:
                if selected_line == "Red Line":
                    print("red line")
                elif selected_line == "Blue Line":
                    print("blue line")
                elif selected_line == "Green Line":
                    routing = Routing('src/main/CTC/GreenLine.csv', CTC_Window) 
                    arrival_station_to_find = arrival_station
                    station_info = routing.find_station_info(arrival_station_to_find)

                    if station_info:
                        # Add station and its information as a dictionary to the list
                        station_info_list.append({"Station": arrival_station_to_find, "Info": station_info})
                    else:
                        print(f"Station '{arrival_station_to_find}' not found.")

            if station_info_list:
                departure_station_info = routing.find_station_info(departing_station)
                if departure_station_info:
                    self.path = self.routing.find_path(departing_station, arrival_stations, station_info)
                    print("Path: ", self.path)
                    self.travel = self.routing.find_travel_path(self.path)
                    print("Travel: ", self.travel)
            
            # case if no arrival time is input, needs to be calculated
            if arrival_time == "":
                travelTime = self.routing.computeTravelTime(self.travel)
                arrivalTimeBefore = self.routing.calculateArrivalTime(travelTime, current_time)
                
                arrival_hours = arrivalTimeBefore.hour()
                arrival_minutes = arrivalTimeBefore.minute()

                # Format as "HHmm"
                arrivalTime = f"{arrival_hours:02d}{arrival_minutes:02d}"
                print("Arrival Time:", arrivalTime)

                # sug speed
                # initial authority

                train = Train(self.numTrains, selected_line, arrivalTime, current_time, self.main_window.stops)
                self.trainList.append(train)
                trainID = train.getTrainID()
                print(trainID)
                self.update_schedule_table(departing_station, current_time, arrivalTime, trainID)

            # case if an arrival time is input, error check
                #departureTime = Routing.calculateDepartureTime(self, departing_station, arrivalTime)

            # case if trainID is input

            # case if suggested speed is input

            #self.trainList.append(Train(trainID, departing_station, selected_line, arrivalTime, departureTime, main_window.stops))
            #self.update_schedule_table(selected_line, departing_station, arrival_station, arrival_time, trainID)
            
            # Clear the input fields and hide them
            self.numTrains += 1
            self.main_window.departingStation.setCurrentIndex(0)
            self.main_window.arrivalTime.clear()
            self.main_window.stops.clear()
            self.updateStopDropDown()
            self.main_window.stopsTable.setRowCount(0)

    def update_schedule_table(self, departing_station, departure_time, arrival_time, trainID):
        # Determine where to insert the new row in the schedule table
        row_position = self.main_window.schedule_table.rowCount()
        departure_time_str = departure_time.toString("HHmm")
        # Insert a new row in the schedule table
        self.main_window.schedule_table.insertRow(row_position)
        stops_str = ', '.join(self.main_window.stops)

        # Add the train information to the table
        self.main_window.schedule_table.setItem(row_position, 0, QTableWidgetItem(trainID))  # Train ID
        self.main_window.schedule_table.setItem(row_position, 1, QTableWidgetItem(departing_station))  # Departing Station
        self.main_window.schedule_table.setItem(row_position, 2, QTableWidgetItem(stops_str))  # Stops
        self.main_window.schedule_table.setItem(row_position, 3, QTableWidgetItem(departure_time_str))  # Departure Time
        self.main_window.schedule_table.setItem(row_position, 4, QTableWidgetItem(arrival_time))  # Arrival Time
        
    def AutomaticSchedule(self):
        self.main_window.schedule_table.clearContents()
        self.main_window.schedule_table.setRowCount(0)    
    
    def setBlueSchedule(self):
        # Clear the existing items in the schedule table
        self.main_window.schedule_table.clearContents()
        self.main_window.schedule_table.setRowCount(0)

        blue_line_schedule = [
            ("BlueTrain1", "Yard", "Stops","Station B", "0800", "0830"),
            ("BlueTrain2", "Yard", "Stops","Station C", "0900", "0930"),
        ]

        # Set the number of rows in the schedule table
        self.main_window.schedule_table.setRowCount(len(blue_line_schedule))

        # Populate the schedule table with the Blue Line schedule
        for row, schedule_entry in enumerate(blue_line_schedule):
            for col, value in enumerate(schedule_entry):
                item = QTableWidgetItem(value)
                self.main_window.schedule_table.setItem(row, col, item)

    def setRedSchedule(self):
        # Clear the existing items in the schedule table
        self.main_window.schedule_table.clearContents()
        self.main_window.schedule_table.setRowCount(0)

        red_line_schedule = [
            ("RedTrain1", "Yard", "Stops", "Station B", "0800", "0830"),
            ("RedTrain2", "Yard", "Stops", "Station C", "0900", "0930"),
        ]

        # Set the number of rows in the schedule table
        self.main_window.schedule_table.setRowCount(len(red_line_schedule))

        # Populate the schedule table with the Red Line schedule
        for row, schedule_entry in enumerate(red_line_schedule):
            for col, value in enumerate(schedule_entry):
                item = QTableWidgetItem(value)
                self.main_window.schedule_table.setItem(row, col, item)

    def setGreenSchedule(self):
        # Clear the existing items in the schedule table
        self.main_window.schedule_table.clearContents()
        self.main_window.schedule_table.setRowCount(0)

        green_line_schedule = [
            ("GreenTrain1", "Yard", "Stops", "Station B", "0800", "0830"),
            ("GreenTrain2", "Yard", "Stops", "Station C", "0900", "0930"),
        ]

        # Set the number of rows in the schedule table
        self.main_window.schedule_table.setRowCount(len(green_line_schedule))

        # Populate the schedule table with the Green Line schedule
        for row, schedule_entry in enumerate(green_line_schedule):
            for col, value in enumerate(schedule_entry):
                item = QTableWidgetItem(value)
                self.main_window.schedule_table.setItem(row, col, item)

    def getSelectedLine(self):
        selected_line = self.main_window.selectLine.currentText()
        return selected_line
        # Clear the existing items in the schedule table
        """self.main_window.schedule_table.clearContents()
        self.main_window.schedule_table.setRowCount(0)
        
        # No line selected, do nothing  
        if selected_line == "Select a Line":
            return  
        elif selected_line == "Blue Line":
            self.setBlueSchedule()
        elif selected_line == "Red Line":
            self.setRedSchedule()
        elif selected_line == "Green Line":
            self.setGreenSchedule()
            self.max_block = 150"""

    def updateStopDropDown(self):
        self.main_window.addStopDropdown.clear()
        selected_line = self.main_window.selectLine.currentText()
        available_stations = []

        if selected_line == "Blue Line":
            available_stations = ["Select a Station to stop at", "Station B", "Station C"]
        elif selected_line == "Red Line":
            available_stations = ["Select a Station to stop at", "Shadyside", "Herron Ave", "Swissville", "Penn Station", "Steel Plaza", "First Ave", "Station Square", "South Hills Junction"]
        elif selected_line == "Green Line":
            available_stations = ["Select a Station to stop at", "Pioneer", "Edgebrook", "Whited", "South Bank", "Central", "IngleWood", "OverBrook", "Glenbury", "Dormont", "Mt Lebanon", "Poplar", "Castle Shannon"]

        #if self.main_window.arrivalStation.currentText() == "Select an Arrival Station":
            # If arrival station is not selected, add all available stations
           # QMessageBox.warning(self, "Error", "Please select an Arrival Station first.")
       # else:
            # Filter out stations that are already in 'stops' and remove the arrival station
        available_stations = [station for station in available_stations if station not in self.main_window.stops]
        self.main_window.addStopDropdown.addItems(available_stations)

    """def addStopPressed(self):
        # Get the selected arrival station
        #arrival_station = self.main_window.arrivalStation.currentText()
        #print(arrival_station)
        #if (arrival_station == 'Select Arrival Station'):
            # Show an error message if arrival station is not selected
            #QMessageBox.warning(self.main_window, "Error", "Please select an Arrival Station first.")
        #else:
            # Get the selected station to add
        selected_station = self.main_window.addStopDropdown.currentText()

        #if selected_station == arrival_station:
            # Show an error message if the selected station is the same as the arrival station
            #QMessageBox.warning(self.main_window, "Error", "Selected station cannot be the same as the Arrival Station.")
        if selected_station != "Select a Station to stop at":
            # Add the selected station to the 'stops' array
            self.main_window.stops.append(selected_station)
            # Update the dropdown to exclude the newly added stop
            self.updateStopDropDown()
            # Reset the dropdown to index 0
            self.main_window.addStopDropdown.setCurrentIndex(0)
            print("Stops:", self.main_window.stops)"""
    
    def addStopPressed(self):
        selected_station = self.main_window.addStopDropdown.currentText()
        
        if selected_station != "Select a Station to stop at":
            # Add the selected station to the 'stops' array
            self.main_window.stops.append(selected_station)

            # add stops to stop table
            dwellTime = "1 minute"
            rowPosition = self.main_window.stopsTable.rowCount()
            self.main_window.stopsTable.insertRow(rowPosition)
            self.main_window.stopsTable.setItem(rowPosition, 0, QTableWidgetItem(selected_station))
            self.main_window.stopsTable.setItem(rowPosition, 1, QTableWidgetItem(dwellTime))

            # Update the dropdown to exclude the newly added stop
            self.updateStopDropDown()
            # Reset the dropdown to index 0
            self.main_window.addStopDropdown.setCurrentIndex(0)
            print("Stops:", self.main_window.stops)
    
    def setMaxBlock(self, selected_line):
        # Set the max_block based on the selected line
        if selected_line == "Red Line":
            self.max_block = 100
        elif selected_line == "Blue Line":
            self.max_block = 150
        elif selected_line == "Green Line":
            self.max_block = 200

    def getMaxBlock(self, selected_line):
        # Check if max_block is already set, and if not, set it
        if self.max_block is None:
            self.setMaxBlock(selected_line)
        return self.max_block
    
class Routing:
    def __init__(self, filename, main_window):
        self.filename = filename
        self.data = self.load_data()
        self.main_window = main_window

    def load_data(self):
        data = []
        with open(self.filename, 'r') as file:
            csv_reader = csv.reader(file)
            for line in csv_reader:
                data.append(line)
        return data

    def find_block_info(self):
        blockList = []  # Create a list to store block information
        header = True  # Flag to skip the header row
        for row in self.data:
            if header:
                header = False  # Skip the header row
                continue

            if len(row) >= 11:
                line = row[0]
                trackSection = row[1]
                blockNumber = int(row[2])
                blockLength = float(row[3])
                speedLimit = float(row[5])
                stationName = row[6]
                seconds_to_traverse_block = float(row[10])

                # Create a Block object for each block and append it to blockList
                block = Block(blockNumber, trackSection, blockLength, speedLimit, stationName, seconds_to_traverse_block)
                blockList.append(block)

        return blockList

    def find_station_info(self, arrival_station):
        station_info = []
        arrival_station = arrival_station.lower()  # Convert the input to lowercase for case-insensitive search

        for row in self.data:
            if len(row) >= 8:
                if arrival_station in row[6].lower():
                    Line = row[0]
                    Block_Number = int(row[2])
                    Block_Length = float(row[3])
                    Speed_Limit = float(row[5])
                    Station = row[6]
                    Station_Side = row[7]
                    self.seconds_to_traverse_block = float(row[10])

                    station_info.append({
                        "Line": Line,
                        "Block_Number": Block_Number,
                        "Block_Length": Block_Length,
                        "Speed_Limit": Speed_Limit,
                        "Station": Station,
                        "Station_Side": Station_Side,
                        "seconds_to_traverse_block": self.seconds_to_traverse_block
                    })
        
        return station_info
    
    """def find_path(self, departure_station, arrival_stations, stops):
        self.path = []
        added_stations = []
        current_station = departure_station

        # Find the station information for the departing block 
        #departure_station_info = self.find_station_info(departure_station)

        #if departure_station_info is None:
        #    return None

        # Check if the departing station has already been added
        #if departure_station not in added_stations:
         #   self.path.append((departure_station, departure_station_info[0]['Block_Number']))
         #   added_stations.append(departure_station)

        for arrival_station in arrival_stations:
            # Find the station information for the current and arrival stations
            current_station_info = self.find_station_info(current_station)
            arrival_station_info = self.find_station_info(arrival_station)

            # If either station's information is missing, we can't continue the path
            if current_station_info is None or arrival_station_info is None:
                return None

            # Check if the current station has already been added
            if current_station not in added_stations:
                self.path.append((current_station, current_station_info[0]['Block_Number']))
                added_stations.append(current_station)

            # Check if the arrival station has already been added
            if arrival_station not in added_stations:
                self.path.append((arrival_station, arrival_station_info[0]['Block_Number']))
                added_stations.append(arrival_station)

            # Update the current station for the next iteration
            current_station = arrival_station

        return self.path"""
    
    def find_path(self, departure_station, arrival_stations, stops):
        self.path = []
        added_stations = []
        current_station = departure_station

        for arrival_station in arrival_stations:
            # Find the station information for the current and arrival stations
            current_station_info = self.find_station_info(current_station)
            arrival_station_info = self.find_station_info(arrival_station)

            # If either station's information is missing, we can't continue the path
            if current_station_info is None or arrival_station_info is None:
                return None

            # Check if the arrival station has already been added
            if arrival_station not in added_stations:
                self.path.append((arrival_station, arrival_station_info[0]['Block_Number']))
                added_stations.append(arrival_station)

            # Update the current station for the next iteration
            current_station = arrival_station

        return self.path
    
    def find_travel_path(self, path):
        max_block = 0
        if self.main_window.selectLine == "Green Line":
            max_block = 150

        # Extract the block numbers and station names from the path
        block_stations = [(block, station) for station, block in path]

        self.stations_to_stop = []
        self.route_array = []

        # Determine the first stop based on the first station in block_stations
        # Determine the first stop based on the first station in block_stations
        if block_stations:
            first_block, first_station = block_stations[0]
            first_stop = f"Stop at block {first_block}: {first_station}"
            self.stations_to_stop.append((first_block, first_station))


        # Categorize other stations based on their block numbers
        first_stations = []
        second_stations = []
        third_stations = []
        stop_blocks = []

        for block, station in block_stations[1:]:  # Exclude the first station from categorization
            if 62 < block < max_block:
                first_stations.append((block, station))
                stop_blocks.append(block)
            elif 0 <= block < 58:
                second_stations.append((block, station))
                stop_blocks.append(block)
            elif block < 150:
                third_stations.append((block, station))
                stop_blocks.append(block)

        # Sort stations within each category by block number
        first_stations.sort(key=lambda x: x[0])
        second_stations.sort(key=lambda x: x[0])
        third_stations.sort(key=lambda x: x[0])

        # Combine stations in the desired order
        self.stations_to_stop.extend(first_stations)
        self.stations_to_stop.extend(second_stations)
        self.stations_to_stop.extend(third_stations)

        self.routeQ = []
        #if self.main_window.selectLine == "Green Line":
        self.routeQ = self.travelGreenBlocks()

        # Use stop_blocks to check if the train should stop at a block
        for i, block in enumerate(self.routeQ):
            if isinstance(block, int):
                for station_info in self.stations_to_stop:
                    stop_block, station_name = station_info[0], station_info[1]
                    if block == stop_block:
                        self.routeQ[i] = f"Stop at block {block}: {station_name}"

        return self.routeQ

    def travelGreenBlocks(self):
        self.routeQ = []
        # Add all blocks to a path the train will have to go through
        self.routeQ.append(0)

        # K-Q
        for blockNum in range(63, 101):
            self.routeQ.append(blockNum)

        # N
        for blockNum in range(85, 76, -1):
            self.routeQ.append(blockNum)

        # R-Z
        for blockNum in range(101, 151):
            self.routeQ.append(blockNum)

        # F-A
        for blockNum in range(28, 0, -1):
            self.routeQ.append(blockNum)

        # D-I
        for blockNum in range(13, 58):
            self.routeQ.append(blockNum)

        self.routeQ.append(0)

        return self.routeQ
    
    def closeBlock(self, blockNumber):
        self.blockList[blockNumber].setEnable(0)

    def openBlock(self, blockNumber):
        self.blockList[blockNumber].setEnable(1)

    def computeTravelTime(self, travel_path):
        total_time = 0  # Initialize total time to zero
        lastStopTime = 0

        for block in travel_path:
            if isinstance(block, str) and block.startswith("Stop at block"):
                # Add 60 seconds for each stop
                print(total_time)
                total_time += 60
                lastStopTime = total_time

            elif isinstance(block, int):
                # Find the time to traverse the block using the find_block_info function
                self.block_info_list = self.find_block_info()  # Call the function to get all block information

                block_info = next((info for info in self.block_info_list if info.blockNumber == block), None)
                if block_info:
                    seconds_to_traverse_block = block_info.seconds_to_traverse_block
                    total_time += seconds_to_traverse_block
                    #print(f"Block: {block}, Seconds: {seconds_to_traverse_block}")
                else:
                    print(f"Block {block} not found in block_list.")

        print("Last stop arrival time is ")
        print(lastStopTime)
        print("Total travel time is ")
        print(total_time)
        #print(total_time)
        return lastStopTime

    def checkPosition(self, line, blockNum, occupancy):
        print("comparing current block of" + str(blockNum) + " with destination at " + str(self.routeQ[1]))
        line = self.scheduler.getSelectedLine
        if (occupancy == True and blockNum == self.routeQ[1] and line == line):
            self.routeQ.pop(0)

            if (self.stations_to_stop[0] == self.routeQ[3]):
                suggestedSpeed = int(0.75*self.block_info_list[self.routeQ[0]-1].speedLimit)*3.60
                print(suggestedSpeed)
                #signals.sendSuggestedSpeed.emit(WaysideNum, line, self.routeQ(0), suggestedSpeed)
            elif (self.stations_to_stop[0] == self.routeQ[2]):
                suggestedSpeed = int(0.50*self.block_info_list[self.routeQ[0]-1].speedLimit)*3.60
                print(suggestedSpeed)
                #signals.sendSuggestedSpeed.emit(WaysideNum, line, self.routeQ(0), suggestedSpeed)
            elif (self.stations_to_stop[0] == self.routeQ[1]):
                suggestedSpeed = int(0.25*self.block_info_list[self.routeQ[0]-1].speedLimit)*3.60
                print(suggestedSpeed)
                #signals.sendSuggestedSpeed.emit(WaysideNum, line, self.routeQ(0), suggestedSpeed)
            elif (self.stations_to_stop[0] == self.routeQ[0]):
                suggestedSpeed = 0
                print(suggestedSpeed)
                #signals.sendSuggestedSpeed.emit(WaysideNum, line, self.routeQ(0), suggestedSpeed)
                #signals.sendAuthority.emit(WaysideNum, line, self.stations_to_stop[0], 0)
                QTimer.singleShot(60, self.leaveStop)
            else:
                suggestedSpeed = (self.block_info_list[self.routeQ[0]-1].speedLimit)*3.60
                #signals.sendSuggestedSpeed.emit(WaysideNum, line, self.routeQ[0], suggestedSpeed)
   
    def leaveStop(self):
        if self.stations_to_stop:
            departing_station = self.stations_to_stop.pop()
            # Continue with your existing code for leaving the stop
            suggestedSpeed = (self.block_info_list[self.routeQ[0]-1].speedLimit) * 3.60
            # signals.sendSuggestedSpeed.emit(WaysideNum, line, self.routeQ[0], suggestedSpeed)
            current_time = QTime.currentTime()
            self.update_schedule_table(departing_station, current_time, "Dwelling", "N/A")
        else:
            # No more stations to stop, update the schedule with "Returning to yard"
            current_time = QTime.currentTime()
            self.update_schedule_table("Returning to yard", current_time, "N/A", "N/A")

    def calculateDepartureTime(arrival_time, travelTime):
        # Calculate departure time by subtracting travel time from arrival time
        departure_time = arrival_time.addSecs(int(-travelTime))
        return departure_time

    def calculateArrivalTime(self, travelTime, current_time):
        arrival_time = current_time.addSecs(int(travelTime))
        return arrival_time
        
class Train:
    train_count = 0
    def __init__(self, trainNum, line, arrivalTime, departureTime, stops):
        Train.train_count += 1
        self.trackLine = line
        self.timeArrival = arrivalTime
        self.trainDeparture = departureTime
        self.trainStops = stops 
        self.authority = 0
        trainNum = trainNum + 1
        
        #self.signals.occupancy.connect(self.routing.checkPosition)

        if (line == "Green Line"):
            self.trainID = f'{"Green"}{trainNum}'

    def getTrainID(self):
        return self.trainID
    
    def getDestination(self):
        return self.destination
    
    def getTrackLine(self):
        return self.trackLine
    
    def getArrivalTime(self):
        return self.timeArrival
    
    def getDepartureTime(self):
        return self.trainDeparture
    
    def getStops(self):
        return self.trainStops
    
    def getSuggestedSpeed(self):
        return self.suggestedSpeed
    
    def getAuthoriy(self):
        return self.authority
    
    def setAuthority(self, trainAuthority):
        self.authority = trainAuthority

    def setArrivalTime(self, arrivalTime):
        self.timeArrival = arrivalTime

    def setSuggestedSpeed(self, trainSpeed):
        self.suggestedSpeed = trainSpeed
    
    def setTrainID(self, newID):
        self.trainID = newID
    
    #def leaveStation()    
    
class Block:
    def __init__(self, blockNumber, trackSection, blockLength, speedLimit, stationName, seconds_to_traverse_block):
        self.blockNumber = blockNumber
        self.section = trackSection
        self.length = blockLength
        self.speedLimit = speedLimit
        self.station = stationName
        self.seconds_to_traverse_block = seconds_to_traverse_block
        self.occupancy = 0
        self.enable = 1
    
    def setEnable(self, blockEnable):
        self.enable = blockEnable
    def setOccupancy(self, occupancy):
        self.occupancy = occupancy

 
# create app
#app = QApplication([])
#SignalHandlers()
#CTC_Window = CTCWindow()
#mode_handler = ModeHandler(CTC_Window)  # Initialize the ModeHandler with the MainWindow instance

# run app
#app.exec()