# importing libraries
import sys
import math
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import csv


class MainWindow(QMainWindow):
    # font variables
    textFontSize = 9
    labelFontSize = 12
    headerFontSize = 16
    titleFontSize = 22
    fontStyle = "Product Sans"
    # color variables
    colorDarkBlue = "#085394"
    colorLightRed = "#EA9999"
    colorLightBlue = "#9FC5F8"
    colorLightGrey = "#CCCCCC"
    colorMediumGrey = "#DDDDDD"
    colorDarkGrey = "#666666"
    colorBlack = "#000000"
    # dimensions
    w = 960
    h = 960
    moduleName = "CTC"

    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle(self.moduleName)

        # setting geometry
        self.setGeometry(50, 50, self.w, self.h)

        """main window template layout"""
        # body block
        self.bodyBlock = QLabel(self)
        self.bodyBlock.setGeometry(20, 20, 920, 920)
        self.bodyBlock.setStyleSheet(
            "background-color: white;" "border: 1px solid black"
        )

        # header block
        self.headerBlock = QLabel(self)
        self.headerBlock.setGeometry(20, 20, 920, 70)
        self.headerBlock.setStyleSheet(
            "background-color:" + self.colorDarkBlue + ";" "border: 1px solid black"
        )

        # title
        self.titleLabel = QLabel(
            "Pittsburgh Metropolitan Transportation Authority", self
        )
        self.titleLabel.setFont(QFont(self.fontStyle, self.titleFontSize))
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setGeometry(120, 35, 400, 400)
        self.titleLabel.adjustSize()
        self.titleLabel.setStyleSheet("color: white")

        # logo
        self.pixmapMTALogo = QtGui.QPixmap("MTA_NYC_logo.svg.png")
        self.pixmapMTALogo = self.pixmapMTALogo.scaled(70, 70)
        self.logo = QLabel(self)
        self.logo.setPixmap(self.pixmapMTALogo)
        self.logo.move(20, 20)
        self.logo.adjustSize()

        # module
        self.moduleLabel = QLabel("Centralized Traffic Control", self)
        self.moduleLabel.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.moduleLabel.setAlignment(Qt.AlignCenter)
        self.moduleLabel.move(30, 100)
        self.moduleLabel.adjustSize()
        self.moduleLabel.setStyleSheet("color:" + self.colorDarkBlue)

        # test bench icon
        self.pixmapGear = QtGui.QPixmap("gear_icon.png")
        self.pixmapGear = self.pixmapGear.scaled(25, 25)
        self.testbenchIcon = QLabel(self)
        self.testbenchIcon.setPixmap(self.pixmapGear)
        self.testbenchIcon.setGeometry(30, 140, 32, 32)

        # test bench button
        self.testbenchButton = QPushButton("Test Bench", self)
        self.testbenchButton.setFont(QFont(self.fontStyle, self.textFontSize))
        self.testbenchButton.setGeometry(60, 140, 100, 32)
        self.testbenchButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )

        # system time input
        self.systemTimeInput = QLabel("00:00:00", self)
        self.systemTimeInput.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.systemTimeInput.setGeometry(820, 67, 150, 100)
        self.systemTimeInput.setStyleSheet("color:" + self.colorDarkBlue)

        # system time label
        self.systemTimeLabel = QLabel("System Time:", self)
        self.systemTimeLabel.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.systemTimeLabel.adjustSize()
        self.systemTimeLabel.setGeometry(650, 65, 200, 100)
        self.systemTimeLabel.setStyleSheet("color:" + self.colorDarkBlue)

        # system speed label
        self.systemSpeedLabel = QLabel("System Speed:", self)
        self.systemSpeedLabel.setFont(QFont(self.fontStyle, self.textFontSize))
        self.systemSpeedLabel.setGeometry(700, 140, 100, 100)
        self.systemSpeedLabel.adjustSize()
        self.systemSpeedLabel.setStyleSheet("color:" + self.colorDarkBlue)

        # system speed input
        self.systemSpeedInput = QLabel("x1.0", self)
        self.systemSpeedInput.setFont(QFont(self.fontStyle, self.textFontSize))
        self.systemSpeedInput.setGeometry(850, 127, 50, 50)
        self.systemSpeedInput.setStyleSheet("color:" + self.colorDarkBlue)

        # increase system speed button
        self.pixmapFastForward = QtGui.QPixmap("fast-forward.svg")
        self.pixmapFastForward = self.pixmapFastForward.scaled(20, 20)
        self.speedUpButton = QPushButton(self)
        self.speedUpButton.setIcon(QtGui.QIcon(self.pixmapFastForward))
        self.speedUpButton.setGeometry(890, 143, 20, 20)
        self.speedUpButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )

        # decrease system speed button
        self.pixmapRewind = QtGui.QPixmap("rewind.svg")
        self.pixmapRewind = self.pixmapRewind.scaled(20, 20)
        self.slowDownButton = QPushButton(self)
        self.slowDownButton.setIcon(QtGui.QIcon(self.pixmapRewind))
        self.slowDownButton.setGeometry(819, 143, 20, 20)
        self.slowDownButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )

        ################################# MODE BUTTONS #############################################################################
        self.last_clicked_button = None
        # Add an "Automatic Mode" button
        self.automatic = QPushButton("Automatic Mode", self)
        self.automatic.setGeometry(
            30, 180, 130, 30
        )  # Set the button's position and size
        self.automatic.setFont(QFont(self.fontStyle, self.textFontSize))
        self.automatic.setStyleSheet(
            "background-color: "
            + self.colorLightGrey
            + "; color: "
            + self.colorDarkBlue
            + "; border: 1px solid black"
        )
        self.automatic.clicked.connect(self.automaticButtonClicked)

        # Manual Button
        self.manual = QPushButton("Manual Mode", self)
        self.manual.setGeometry(165, 180, 130, 30)  # Set the button's position and size
        self.manual.setFont(QFont(self.fontStyle, self.textFontSize))
        self.manual.setStyleSheet(
            "background-color: white; color:"
            + self.colorBlack
            + "; border: 1px solid black"
        )
        self.manual.clicked.connect(self.manualButtonClicked)

        # Maintenance Button
        self.maintenance = QPushButton("Maintenance Mode", self)
        self.maintenance.setGeometry(
            300, 180, 130, 30
        )  # Set the button's position and size
        self.maintenance.setFont(QFont(self.fontStyle, self.textFontSize))
        self.maintenance.setStyleSheet(
            "background-color: white; color:"
            + self.colorBlack
            + "; border: 1px solid black"
        )
        self.maintenance.clicked.connect(self.maintenanceButtonClicked)

        # Select a Line
        self.selectLine = QComboBox(self)
        self.selectLine.setGeometry(30, 220, 130, 30)
        self.selectLine.addItem("Select a Line")
        self.selectLine.addItem("Blue Line")
        self.selectLine.addItem("Green Line")
        self.selectLine.addItem("Red Line")
        self.selectLine.setFont(QFont(self.fontStyle, self.textFontSize))
        self.selectLine.currentIndexChanged.connect(self.getSelectedLine)

        # CSV File Button
        self.inputSchedule = QPushButton("Import Schedule", self)
        self.inputSchedule.setGeometry(
            165, 220, 130, 30
        )  # Set the button's position and size
        self.inputSchedule.setFont(QFont(self.fontStyle, self.textFontSize))
        self.inputSchedule.setStyleSheet(
            "background-color: white; color:"
            + self.colorBlack
            + "; border: 1px solid black"
        )
        self.inputSchedule.clicked.connect(self.load_file)

        ################################# Automatic ###################################################################
        # Error text
        self.error_label = QLabel("", self)
        self.error_label.setFont(QFont(self.fontStyle, self.textFontSize))
        self.error_label.setStyleSheet("color: red")
        self.error_label.setGeometry(170, 245, 125, 30)

        # Schedule Table
        self.schedule_header = QLabel("Schedule:", self)
        self.schedule_header.setFont(QFont(self.fontStyle, self.textFontSize))
        self.schedule_header.setGeometry(30, 430, 500, 100)
        self.schedule_table = QTableWidget(self)
        self.schedule_table.setColumnCount(6)
        self.schedule_table.setHorizontalHeaderLabels(
            [
                "Train ID",
                "Departing From",
                "Stops",
                "Arrival Station",
                "Departure Time",
                "Arrival Time",
            ]
        )
        self.schedule_table.setStyleSheet("background-color: white;")
        self.schedule_table.setGeometry(35, 500, 890, 430)
        self.schedule_table.setColumnWidth(0, 150)
        self.schedule_table.setColumnWidth(1, 150)
        self.schedule_table.setColumnWidth(2, 170)
        self.schedule_table.setColumnWidth(3, 150)
        self.schedule_table.setColumnWidth(4, 150)
        self.schedule_table.setColumnWidth(5, 130)
        self.schedule_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Occupancy Table
        self.occupancy_header = QLabel("Occupied Blocks:", self)
        self.occupancy_header.setFont(QFont(self.fontStyle, self.textFontSize))
        self.occupancy_header.setGeometry(675, 159, 120, 100)
        self.occupancy_table = QTableWidget(self)
        self.occupancy_table.setColumnCount(2)
        self.occupancy_table.setHorizontalHeaderLabels(["Block", "Line"])
        self.occupancy_table.setStyleSheet("background-color: white;")
        self.occupancy_table.setGeometry(675, 225, 252, 265)

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
        self.selectLine.currentIndexChanged.connect(self.updateDepartingStations)
        self.departingStation.setFont(QFont(self.fontStyle, 9))

        # Next Station
        self.arrivalStation = QComboBox(self)
        self.arrivalStation.setVisible(False)
        self.arrivalStation.setGeometry(50, 350, 200, 55)
        self.arrivalStation.addItem("Select Arrival Station")
        self.selectLine.currentIndexChanged.connect(self.updateArrivalStation)
        self.arrivalStation.setFont(QFont(self.fontStyle, 9))

        # Send Train Button
        self.sendTrain = QPushButton("Send Train", self)
        self.sendTrain.setVisible(False)
        self.sendTrain.setGeometry(775, 537, 150, 50)
        self.sendTrain.setFont(QFont(self.fontStyle, self.textFontSize))
        self.sendTrain.setStyleSheet(
            "background-color: "
            + self.colorLightRed
            + "; color: "
            + self.colorBlack
            + "; border: 1px solid black"
        )
        self.sendTrain.clicked.connect(self.sendTrainClicked)

        # Input an arrival time
        self.arrivalTime = QLineEdit(self)
        self.arrivalTime.setVisible(False)
        self.arrivalTime.setPlaceholderText("0000 (Military Time)")
        self.arrivalHeader = QLabel("Input an Arrival Time:", self)
        self.arrivalHeader.setFont(QFont(self.fontStyle, self.textFontSize))
        self.arrivalHeader.setVisible(False)
        self.arrivalHeader.setGeometry(50, 380, 200, 100)
        self.arrivalTime.setGeometry(50, 450, 200, 50)

        # Add Stop Button
        self.addStopButton = QPushButton("Add Stop", self)
        self.addStopButton.setVisible(False)
        self.addStopButton.setFont(QFont(self.fontStyle, self.textFontSize))
        self.addStopButton.setGeometry(450, 275, 100, 50)
        self.addStopButton.setStyleSheet(
            "background-color: white; color: "
            + self.colorDarkBlue
            + "; border: 1px solid black"
        )
        self.addStopButton.clicked.connect(self.addStopPressed)
        self.current_departing_station = None

        # Add Stop Dropdown
        self.addStopDropdown = QComboBox(self)
        self.addStopDropdown.setGeometry(275, 275, 165, 50)
        self.addStopDropdown.hide()
        self.stops = []
        self.current_stop_index = 0
        self.update_timer = QTimer(self)

        self.selectLine.currentIndexChanged.connect(
            self.updateStopDropDown
        )  # Connect the signal to update the dropdown
        self.max_block = None

        self.show()

    # function for if automatic button is pressed
    def automaticButtonClicked(self):
        # Unhighlight the last clicked button, if any
        if self.last_clicked_button:
            self.last_clicked_button.setStyleSheet("")

        self.last_clicked_button = self.automatic
        self.automatic.setStyleSheet(
            "background-color: "
            + self.colorLightGrey
            + "; color: "
            + self.colorDarkBlue
            + "; border: 1px solid black"
        )

        self.throughput_label.setVisible(True)
        self.speed_label.setVisible(True)
        self.authority_label.setVisible(True)
        self.occupancy_header.setVisible(True)
        self.occupancy_table.setVisible(True)
        self.schedule_table.setVisible(True)
        self.schedule_table.setGeometry(35, 500, 890, 430)
        self.schedule_header.setVisible(True)
        self.schedule_header.setGeometry(30, 430, 500, 100)
        self.selectLine.setVisible(True)
        self.inputSchedule.setVisible(True)
        self.departingStation.setVisible(False)
        self.arrivalStation.setVisible(False)
        self.sendTrain.setVisible(False)
        self.arrivalHeader.setVisible(False)
        self.arrivalTime.setVisible(False)
        self.addStopButton.setVisible(False)
        self.addStopDropdown.setVisible(False)

    # function for if manual button is pressed
    def manualButtonClicked(self):
        self.automatic.setStyleSheet(
            "background-color: white; color:"
            + self.colorBlack
            + "; border: 1px solid black"
        )
        # Unhighlight the last clicked button, if any
        if self.last_clicked_button:
            self.last_clicked_button.setStyleSheet("")

        self.last_clicked_button = self.manual
        self.manual.setStyleSheet(
            "background-color: "
            + self.colorLightGrey
            + "; color: "
            + self.colorDarkBlue
            + "; border: 1px solid black"
        )

        # Hide the elements
        self.throughput_label.setVisible(False)
        self.speed_label.setVisible(False)
        self.authority_label.setVisible(False)
        self.occupancy_header.setVisible(False)
        self.occupancy_table.setVisible(False)
        self.schedule_table.setVisible(True)
        self.schedule_table.setGeometry(35, 600, 890, 330)
        self.schedule_header.setVisible(True)
        self.schedule_header.setGeometry(30, 528, 100, 100)
        self.selectLine.setVisible(True)
        self.inputSchedule.setVisible(True)
        self.departingStation.setVisible(True)
        self.arrivalStation.setVisible(True)
        self.sendTrain.setVisible(True)
        self.arrivalHeader.setVisible(True)
        self.arrivalTime.setVisible(True)
        self.addStopButton.setVisible(True)
        self.addStopDropdown.setVisible(True)

    # function for if maintenance button is pressed
    def maintenanceButtonClicked(self):
        self.automatic.setStyleSheet(
            "background-color: white; color:"
            + self.colorBlack
            + "; border: 1px solid black"
        )
        # Unhighlight the last clicked button, if any
        if self.last_clicked_button:
            self.last_clicked_button.setStyleSheet("")

        self.last_clicked_button = self.maintenance
        self.maintenance.setStyleSheet(
            "background-color: "
            + self.colorLightGrey
            + "; color: "
            + self.colorDarkBlue
            + "; border: 1px solid black"
        )

        self.throughput_label.setVisible(False)
        self.speed_label.setVisible(False)
        self.authority_label.setVisible(False)
        self.occupancy_header.setVisible(False)
        self.occupancy_table.setVisible(False)
        self.schedule_table.setVisible(False)
        self.schedule_header.setVisible(False)
        self.selectLine.setVisible(False)
        self.inputSchedule.setVisible(False)
        self.departingStation.setVisible(False)
        self.arrivalStation.setVisible(False)
        self.sendTrain.setVisible(False)
        self.arrivalHeader.setVisible(False)
        self.arrivalTime.setVisible(False)
        self.addStopButton.setVisible(False)
        self.addStopDropdown.setVisible(False)

    def load_file(self):
        selected_line = self.selectLine.currentText()
        if selected_line == "Select a Line":
            # Set the error message text
            self.error_label.setText("Please select a line.")
            return

        self.error_label.clear()

        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(
            self,
            "Open CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)",
            options=options,
        )

        if filePath:
            with open(filePath, "r") as file:
                csv_content = file.read()

            # Split the CSV content into rows
            rows = csv_content.split("\n")

            # Determine the number of rows and columns for the table
            num_rows = len(rows)
            if num_rows > 0:
                num_columns = len(rows[0].split(","))

                # Create a QTableWidget
                self.schedule_table.setRowCount(num_rows)
                self.schedule_table.setColumnCount(num_columns)

                # Populate the table with CSV data
                for i, row in enumerate(rows):
                    columns = row.split(",")
                    for j, value in enumerate(columns):
                        item = QTableWidgetItem(value)
                        self.schedule_table.setItem(i, j, item)

        # This makes the table uneditable
        for row in range(self.schedule_table.rowCount()):
            for col in range(self.schedule_table.columnCount()):
                item = self.schedule_table.item(row, col)
                if item:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)

    def setThroughput(self, throughput_value):
        self.throughput_label.setText("Throughput: " + str(throughput_value))

    def getThroughput(self):
        throughput_text = self.throughput_label.text()
        # Extract the throughput value from the label's text
        throughput_value = throughput_text.replace("Throughput: ", "")
        # You may want to handle potential conversion errors if needed
        return float(throughput_value) if throughput_value != "N/A" else None

    def setAuthority(self, authority_value):
        self.authority_label.setText("Authority: " + str(authority_value))

    def getAuthority(self):
        authority_text = self.throughput_label.text()
        # Extract the throughput value from the label's text
        authority_value = authority_text.replace("Authority: ", "")
        # You may want to handle potential conversion errors if needed
        return float(authority_value) if authority_value != "N/A" else None

    def setCommandedSpeed(self, speed_value):
        self.speed_label.setText("Commanded Speed (mph): " + str(speed_value))

    def getCommandedSpeed(self):
        speed_text = self.speed_label.text()
        # Extract the throughput value from the label's text
        speed_value = speed_text.replace("Commanded Speed (mph): ", "")
        # You may want to handle potential conversion errors if needed
        return float(speed_value) if speed_value != "N/A" else None

    def updateDepartingStations(self):
        # Clear the existing items in the departingStation ComboBox
        self.departingStation.clear()
        self.departingStation.addItem("Yard")
        selected_line = self.selectLine.currentText()

    def updateArrivalStation(self):
        # Clear the existing items in the arrivalStation ComboBox
        self.arrivalStation.clear()
        self.arrivalStation.addItem("Select Arrival Station")
        selected_line = self.selectLine.currentText()

        # Update the available stations with stations that are not in 'stops'
        if selected_line == "Blue Line":
            self.available_stations = ["Station B", "Station C"]
        elif selected_line == "Red Line":
            self.available_stations = [
                "Shadyside",
                "Herron Ave",
                "Swissville",
                "Penn Station",
                "Steel Plaza",
                "First Ave",
                "Station Square",
                "South Hills Junction",
            ]
        elif selected_line == "Green Line":
            self.available_stations = [
                "Pioneer",
                "Edgebrook",
                "Whited",
                "South Bank",
                "Central",
                "IngleWood",
                "OverBrook",
                "Glenbury",
                "Dormont",
                "Mt Lebanon",
                "Poplar",
                "Castle Shannon",
            ]
        else:
            self.available_stations = []

        # Filter out stations that are already in 'stops'
        self.available_stations = [
            station for station in self.available_stations if station not in self.stops
        ]

        # Add the updated available stations to the drop-down
        self.arrivalStation.addItems(self.available_stations)

    def sendTrainClicked(self):
        selected_line = self.selectLine.currentText()
        departing_station = self.departingStation.currentText()
        arrival_station = self.arrivalStation.currentText()
        arrival_time = self.arrivalTime.text()
        current_time = QTime.currentTime()

        if selected_line == "Select a Line":
            QMessageBox.critical(self, "Invalid Selection", "Please select a line.")
        elif departing_station == "Select a Departing Station":
            QMessageBox.critical(
                self, "Invalid Selection", "Please select a departing station."
            )
        elif arrival_station == "Select Arrival Station":
            QMessageBox.critical(
                self, "Invalid Selection", "Please select an arrival station."
            )
        elif arrival_time and (not arrival_time.isdigit() or len(arrival_time) != 4):
            QMessageBox.critical(
                self,
                "Invalid Arrival Time",
                "Please enter a valid military time (HHmm).",
            )
        elif arrival_time and int(arrival_time) > 2359:
            QMessageBox.critical(
                self, "Invalid Arrival Time", "Arrival time cannot exceed 2359."
            )
        elif arrival_time and int(arrival_time) < int(
            QTime.currentTime().toString("HHmm")
        ):
            QMessageBox.critical(
                self,
                "Invalid Arrival Time",
                "Arrival time cannot be before the current time.",
            )
        else:
            arrival_stations = []
            arrival_stations.extend(self.stops)
            arrival_stations.append(arrival_station)
            station_info_list = []

            for arrival_station in arrival_stations:
                if selected_line == "Red Line":
                    print("red line")
                elif selected_line == "Blue Line":
                    print("blue line")
                elif selected_line == "Green Line":
                    routing = Routing("GreenLine.csv")
                    arrival_station_to_find = arrival_station
                    station_info = routing.find_station_info(arrival_station_to_find)

                    if station_info:
                        # Add station and its information as a dictionary to the list
                        station_info_list.append(
                            {"Station": arrival_station_to_find, "Info": station_info}
                        )
                    else:
                        print(f"Station '{arrival_station_to_find}' not found.")

            # Now you have station_info_list with information for each station
            for station_info_entry in station_info_list:
                print(f"Station: {station_info_entry['Station']}")
                print("Block Information:")
                for info in station_info_entry["Info"]:
                    for key, value in info.items():
                        print(f"{key}:", value)
                    print()

            if station_info_list:
                departure_station_info = routing.find_station_info(departing_station)
                if departure_station_info:
                    path = routing.find_path(
                        departing_station, arrival_stations, station_info
                    )
                    print("Path: ", path)
                    travel = routing.find_travel_path(path)
                    print("Travel: ", travel)

            self.update_schedule_table(
                selected_line, departing_station, arrival_station, arrival_time
            )
            # Clear the input fields and hide them
            self.departingStation.setCurrentIndex(0)
            self.arrivalStation.setCurrentIndex(0)
            self.arrivalTime.clear()
            self.stops.clear()

    def update_schedule_table(
        self, selected_line, departing_station, arrival_station, arrival_time
    ):
        arrival_time = self.arrivalTime.text()
        current_time1 = QTime.currentTime()
        if not arrival_time:
            current_time2 = current_time1.addSecs(4 * 60)  # 4 minutes = 4 * 60 seconds
            departure_time = current_time1.toString("HHmm")
            formatted_time = current_time2.toString("HHmm")
        else:
            departure_time = current_time1.toString("HHmm")
            formatted_time = arrival_time

        # create a unique train ID
        train_id = f"{departure_time}{departing_station[0].upper()}{departing_station[-1].upper()}{arrival_station[0].upper()}{arrival_station[-1].upper()}"

        # Determine where to insert the new row in the schedule table
        row_position = self.schedule_table.rowCount()

        # Insert a new row in the schedule table
        self.schedule_table.insertRow(row_position)
        stops_str = ", ".join(self.stops)

        # Add the train information to the table
        self.schedule_table.setItem(
            row_position, 0, QTableWidgetItem(train_id)
        )  # Train ID
        self.schedule_table.setItem(
            row_position, 1, QTableWidgetItem(departing_station)
        )  # Departing Station
        self.schedule_table.setItem(
            row_position, 2, QTableWidgetItem(stops_str)
        )  # Stops
        self.schedule_table.setItem(
            row_position, 3, QTableWidgetItem(arrival_station)
        )  # Arrival Station
        self.schedule_table.setItem(
            row_position, 4, QTableWidgetItem(departure_time)
        )  # Departure Time
        self.schedule_table.setItem(
            row_position, 5, QTableWidgetItem(formatted_time)
        )  # Arrival Time

    def setBlueSchedule(self):
        # Clear the existing items in the schedule table
        self.schedule_table.clearContents()
        self.schedule_table.setRowCount(0)

        blue_line_schedule = [
            ("BlueTrain1", "Yard", "Stops", "Station B", "0800", "0830"),
            ("BlueTrain2", "Yard", "Stops", "Station C", "0900", "0930"),
        ]

        # Set the number of rows in the schedule table
        self.schedule_table.setRowCount(len(blue_line_schedule))

        # Populate the schedule table with the Blue Line schedule
        for row, schedule_entry in enumerate(blue_line_schedule):
            for col, value in enumerate(schedule_entry):
                item = QTableWidgetItem(value)
                self.schedule_table.setItem(row, col, item)

    def setRedSchedule(self):
        # Clear the existing items in the schedule table
        self.schedule_table.clearContents()
        self.schedule_table.setRowCount(0)

        red_line_schedule = [
            ("RedTrain1", "Yard", "Stops", "Station B", "0800", "0830"),
            ("RedTrain2", "Yard", "Stops", "Station C", "0900", "0930"),
        ]

        # Set the number of rows in the schedule table
        self.schedule_table.setRowCount(len(red_line_schedule))

        # Populate the schedule table with the Red Line schedule
        for row, schedule_entry in enumerate(red_line_schedule):
            for col, value in enumerate(schedule_entry):
                item = QTableWidgetItem(value)
                self.schedule_table.setItem(row, col, item)

    def setGreenSchedule(self):
        # Clear the existing items in the schedule table
        self.schedule_table.clearContents()
        self.schedule_table.setRowCount(0)

        green_line_schedule = [
            ("GreenTrain1", "Yard", "Stops", "Station B", "0800", "0830"),
            ("GreenTrain2", "Yard", "Stops", "Station C", "0900", "0930"),
        ]

        # Set the number of rows in the schedule table
        self.schedule_table.setRowCount(len(green_line_schedule))

        # Populate the schedule table with the Green Line schedule
        for row, schedule_entry in enumerate(green_line_schedule):
            for col, value in enumerate(schedule_entry):
                item = QTableWidgetItem(value)
                self.schedule_table.setItem(row, col, item)

    def getSelectedLine(self):
        selected_line = self.selectLine.currentText()

        # Clear the existing items in the schedule table
        self.schedule_table.clearContents()
        self.schedule_table.setRowCount(0)

        # No line selected, do nothing
        if selected_line == "Select a Line":
            return
        elif selected_line == "Blue Line":
            self.setBlueSchedule()
        elif selected_line == "Red Line":
            self.setRedSchedule()
        elif selected_line == "Green Line":
            self.setGreenSchedule()
            self.max_block = 150

    def updateStopDropDown(self):
        self.addStopDropdown.clear()
        selected_line = self.selectLine.currentText()
        available_stations = []

        if selected_line == "Blue Line":
            available_stations = [
                "Select a Station to stop at",
                "Station B",
                "Station C",
            ]
        elif selected_line == "Red Line":
            available_stations = [
                "Select a Station to stop at",
                "Shadyside",
                "Herron Ave",
                "Swissville",
                "Penn Station",
                "Steel Plaza",
                "First Ave",
                "Station Square",
                "South Hills Junction",
            ]
        elif selected_line == "Green Line":
            available_stations = [
                "Select a Station to stop at",
                "Pioneer",
                "Edgebrook",
                "Whited",
                "South Bank",
                "Central",
                "IngleWood",
                "OverBrook",
                "Glenbury",
                "Dormont",
                "Mt Lebanon",
                "Poplar",
                "Castle Shannon",
            ]

        if self.arrivalStation.currentText() == "Select an Arrival Station":
            # If arrival station is not selected, add all available stations
            QMessageBox.warning(
                self, "Error", "Please select an Arrival Station first."
            )
        else:
            # Filter out stations that are already in 'stops' and remove the arrival station
            available_stations = [
                station
                for station in available_stations
                if station not in self.stops
                and station != self.arrivalStation.currentText()
            ]
            self.addStopDropdown.addItems(available_stations)

    def addStopPressed(self):
        print(self.arrivalStation)
        if self.arrivalStation.currentText() == "Select an Arrival Station":
            # Show an error message if arrival station is not selected
            QMessageBox.warning(
                self, "Error", "Please select an Arrival Station first."
            )
        else:
            # Get the selected station
            selected_station = self.addStopDropdown.currentText()

            if selected_station != "Select a Station to stop at":
                # Add the selected station to the 'stops' array
                self.stops.append(selected_station)
                # Update the dropdown to exclude the newly added stop
                self.updateStopDropDown()
                # Reset the dropdown to index 0
                self.addStopDropdown.setCurrentIndex(0)
                print("Stops:", self.stops)

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
            self.set_max_block(selected_line)
        return self.max_block


class Routing:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        data = []
        with open(self.filename, "r") as file:
            csv_reader = csv.reader(file)
            for line in csv_reader:
                data.append(line)
        return data

    def find_block_info(self, block_number):
        for row in self.data:
            if len(row) >= 11:
                columns = row[:11]
                if columns[2] == str(block_number):
                    Line = columns[0]
                    Section = columns[1]
                    Block_Number = int(columns[2])
                    Block_Length = float(columns[3])
                    Block_Grade = float(columns[4])
                    Speed_Limit = float(columns[5])
                    Infrastructure = columns[6]
                    Station_Side = columns[7]
                    ELEVATION = float(columns[8])
                    CUMALTIVE_ELEVATION = float(columns[9])
                    seconds_to_traverse_block = float(columns[10])

                    return {
                        "Line": Line,
                        "Section": Section,
                        "Block_Number": Block_Number,
                        "Block_Length": Block_Length,
                        "Block_Grade": Block_Grade,
                        "Speed_Limit": Speed_Limit,
                        "Infrastructure": Infrastructure,
                        "Station_Side": Station_Side,
                        "ELEVATION": ELEVATION,
                        "CUMALTIVE_ELEVATION": CUMALTIVE_ELEVATION,
                        "seconds_to_traverse_block": seconds_to_traverse_block,
                    }
        return None

    def find_station_info(self, arrival_station):
        station_info = []
        arrival_station = (
            arrival_station.lower()
        )  # Convert the input to lowercase for case-insensitive search

        for row in self.data:
            if len(row) >= 8:
                if arrival_station in row[6].lower():
                    Line = row[0]
                    Block_Number = int(row[2])
                    Block_Length = float(row[3])
                    Speed_Limit = float(row[5])
                    Station = row[6]
                    Station_Side = row[7]
                    seconds_to_traverse_block = float(row[10])

                    station_info.append(
                        {
                            "Line": Line,
                            "Block_Number": Block_Number,
                            "Block_Length": Block_Length,
                            "Speed_Limit": Speed_Limit,
                            "Station": Station,
                            "Station_Side": Station_Side,
                            "seconds_to_traverse_block": seconds_to_traverse_block,
                        }
                    )
        return station_info

    def find_path(self, departure_station, arrival_stations, stops):
        self.path = []
        added_stations = []
        current_station = departure_station

        # Find the station information for the departing station
        departure_station_info = self.find_station_info(departure_station)

        if departure_station_info is None:
            return None

        # Check if the departing station has already been added
        if departure_station not in added_stations:
            self.path.append(
                (departure_station, departure_station_info[0]["Block_Number"])
            )
            added_stations.append(departure_station)

        for arrival_station in arrival_stations:
            # Find the station information for the current and arrival stations
            current_station_info = self.find_station_info(current_station)
            arrival_station_info = self.find_station_info(arrival_station)

            # If either station's information is missing, we can't continue the path
            if current_station_info is None or arrival_station_info is None:
                return None

            # Check if the current station has already been added
            if current_station not in added_stations:
                self.path.append(
                    (current_station, current_station_info[0]["Block_Number"])
                )
                added_stations.append(current_station)

            # Check if the arrival station has already been added
            if arrival_station not in added_stations:
                self.path.append(
                    (arrival_station, arrival_station_info[0]["Block_Number"])
                )
                added_stations.append(arrival_station)

            # Update the current station for the next iteration
            current_station = arrival_station

        return self.path

    def find_travel_path(self, path):
        # if line == "Green Line":
        # max_block = 150

        # Extract the block numbers and station names from the path
        block_stations = [(block, station) for station, block in path]

        # Sort the stations based on block numbers
        block_stations.sort(key=lambda x: x[0])
        travel_path = []

        # Categorize stations based on their block numbers
        first_stations = []
        second_stations = []
        third_stations = []

        for block, station in block_stations:
            if 60 < block < 150:
                first_stations.append((block, station))
            elif 0 <= block < 60:
                second_stations.append((block, station))
            elif block < 150:
                third_stations.append((block, station))

        # Sort stations within each category by block number
        first_stations.sort(key=lambda x: x[0])
        second_stations.sort(key=lambda x: x[0])
        third_stations.sort(key=lambda x: x[0])

        # Combine stations in the desired order
        travel_path.extend(first_stations)
        travel_path.extend(second_stations)
        travel_path.extend(third_stations)

        return travel_path


# create app
app = QApplication(sys.argv)
# create window instance
window = MainWindow()

# run app
app.exec()
