from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from signals import trainModelToTrackModel, trackControllerToTrackModel

class TestbenchWindow:
    def __init__(self):
        self.testbench = QDialog()
        self.setup_testbench()

    def setup_testbench(self):
        self.testbench.setWindowTitle("Change Failures")
        self.testbench.setGeometry(450, 300, 960, 600)

        # General layout
        self.add_mta_logo()
        self.add_title()
        self.add_hline()

        # Inputs
        self.setup_inputs()
        # self.setup_failure_inputs()

        # New
        self.add_occupancy_test()
        self.add_passenger_test()
        self.add_lightstate_test()
        self.add_crossingstate_test()
        self.add_switchstate_test()

    def add_mta_logo(self):
        mtaLogo = QLabel(self.testbench)
        mtaLogo.setGeometry(0, 0, 80, 80)
        mtaLogo.setPixmap(
            QPixmap("src/main/TrackModel/pngs/MTA_logo.png").scaled(80, 80)
        )

    def add_title(self):
        windowWidth = self.testbench.width()
        labelWidth = 350
        titlePosition = int((windowWidth - labelWidth) / 2)

        titleLabel = QLabel("Track Model- Testbench", self.testbench)
        titleLabel.setGeometry(titlePosition, 25, labelWidth, 40)
        titleLabel.setAlignment(Qt.AlignCenter)
        titleFont = QFont("Arial", 18, QFont.Bold)
        titleLabel.setFont(titleFont)

    def add_hline(self):
        thickness = 5
        line = QFrame(self.testbench)
        line.setFrameShape(QFrame.HLine)
        line.setGeometry(0, 80, 960, thickness)
        line.setLineWidth(thickness)

    def setup_inputs(self):
        blueBackground = QWidget(self.testbench)
        blueBackground.setGeometry(10, 120, 400, 450)
        blueBackground.setStyleSheet("background-color: #A9D0F5;")

        whiteBackground = "background-color: white"

        inputsLabel = QLabel("Change Inputs:", blueBackground)
        inputsLabel.setGeometry(0, 0, 400, 30)
        inputsLabel.setStyleSheet(
            "background-color: blue; color: white; font-weight: bold"
        )
        inputsLabel.setAlignment(Qt.AlignCenter)

        selectBlock = QLabel("Select Block #:", blueBackground)
        selectBlock.setGeometry(10, 50, 150, 30)
        self.blockInput = QSpinBox(blueBackground)
        self.blockInput.setGeometry(120, 50, 50, 30)
        self.blockInput.setStyleSheet(whiteBackground)
        self.blockInput.setMinimum(1)
        self.blockInput.setMaximum(15)
        self.blockInput.setValue(1)
        goButton = QPushButton("Go", blueBackground)
        goButton.setGeometry(220, 50, 150, 30)
        goButton.setStyleSheet("background-color: blue; color: white")
        # Connect the button to the update_block_info_display method
        goButton.clicked.connect(self.update_display)

        speedLabel = QLabel("Set Commanded Speed (mph):", blueBackground)
        speedLabel.setGeometry(10, 90, 200, 30)
        self.speedInput = QLineEdit(blueBackground)
        self.speedInput.setGeometry(220, 90, 150, 30)
        self.speedInput.setStyleSheet(whiteBackground)
        self.speedInput.setEnabled(False)

        authorityLabel = QLabel("Set Authority (blocks):", blueBackground)
        authorityLabel.setGeometry(10, 130, 200, 30)
        self.authorityInput = QLineEdit(blueBackground)
        self.authorityInput.setGeometry(220, 130, 150, 30)
        self.authorityInput.setStyleSheet(whiteBackground)
        self.authorityInput.setEnabled(False)

        railwayLabel = QLabel("Set Railway Crossing (0/1):", blueBackground)
        railwayLabel.setGeometry(10, 170, 200, 30)
        self.railwayInput = QSpinBox(blueBackground)
        self.railwayInput.setGeometry(220, 170, 150, 30)
        self.railwayInput.setStyleSheet(whiteBackground)
        self.railwayInput.setMinimum(0)
        self.railwayInput.setMaximum(1)
        self.railwayInput.setValue(0)
        self.railwayInput.setEnabled(False)

        switchLabel = QLabel("Set Switch Position (0/1):", blueBackground)
        switchLabel.setGeometry(10, 210, 200, 30)
        self.switchInput = QSpinBox(blueBackground)
        self.switchInput.setGeometry(220, 210, 150, 30)
        self.switchInput.setStyleSheet(whiteBackground)
        self.switchInput.setMinimum(0)
        self.switchInput.setMaximum(1)
        self.switchInput.setValue(0)
        self.switchInput.setEnabled(False)

        heaterLabel = QLabel("Set Track Heater (0/1):", blueBackground)
        heaterLabel.setGeometry(10, 250, 200, 30)
        self.heaterInput = QSpinBox(blueBackground)
        self.heaterInput.setGeometry(220, 250, 150, 30)
        self.heaterInput.setStyleSheet(whiteBackground)
        self.heaterInput.setMinimum(0)
        self.heaterInput.setMaximum(1)
        self.heaterInput.setValue(0)
        self.heaterInput.setEnabled(False)

        trackStateLabel = QLabel("Set Track State:", blueBackground)
        trackStateLabel.setGeometry(10, 290, 200, 30)
        self.trackOpen = QRadioButton("Open", blueBackground)
        self.trackOpen.setGeometry(120, 290, 60, 30)
        self.trackOpen.setEnabled(False)
        self.trackOccupied = QRadioButton("Occupied", blueBackground)
        self.trackOccupied.setGeometry(190, 290, 80, 30)
        self.trackOccupied.setEnabled(False)
        self.trackMaintenance = QRadioButton("Maintenance", blueBackground)
        self.trackMaintenance.setGeometry(280, 290, 100, 30)
        self.trackMaintenance.setEnabled(False)
        self.trackStateButtons = QButtonGroup()
        self.trackStateButtons.addButton(self.trackOpen)
        self.trackStateButtons.addButton(self.trackOccupied)
        self.trackStateButtons.addButton(self.trackMaintenance)

        ticketSalesLabel = QLabel("Set Ticket Sales/Hr:", blueBackground)
        ticketSalesLabel.setGeometry(10, 330, 200, 30)
        self.ticketSalesInput = QLineEdit(blueBackground)
        self.ticketSalesInput.setGeometry(220, 330, 150, 30)
        self.ticketSalesInput.setStyleSheet(whiteBackground)
        self.ticketSalesInput.setEnabled(False)

        waitingLabel = QLabel("Set Waiting @ Station:", blueBackground)
        waitingLabel.setGeometry(10, 370, 200, 30)
        self.waitingInput = QLineEdit(blueBackground)
        self.waitingInput.setGeometry(220, 370, 150, 30)
        self.waitingInput.setStyleSheet(whiteBackground)
        self.waitingInput.setEnabled(False)

        lightLabel = QLabel("Set Light Color:", blueBackground)
        lightLabel.setGeometry(10, 410, 150, 30)
        self.greenRadio = QRadioButton("Green", blueBackground)
        self.greenRadio.setGeometry(170, 410, 70, 30)
        self.greenRadio.setEnabled(False)
        self.yellowRadio = QRadioButton("Yellow", blueBackground)
        self.yellowRadio.setGeometry(250, 410, 70, 30)
        self.yellowRadio.setEnabled(False)
        self.redRadio = QRadioButton("Red", blueBackground)
        self.redRadio.setGeometry(330, 410, 70, 30)
        self.redRadio.setEnabled(False)
        self.lightStateButtons = QButtonGroup()
        self.lightStateButtons.addButton(self.greenRadio)
        self.lightStateButtons.addButton(self.yellowRadio)
        self.lightStateButtons.addButton(self.redRadio)

    # def setup_failure_inputs(self):
    #     redBackground = QWidget(self.testbench)
    #     redBackground.setGeometry(500, 120, 350, 80)
    #     redBackground.setStyleSheet("background-color: #ffd6d6;")

    #     failureLabel = QLabel("Set Failure Input:", redBackground)
    #     failureLabel.setGeometry(0, 0, 350, 30)
    #     failureLabel.setStyleSheet(
    #         "background-color: red; color: white; font-weight: bold"
    #     )
    #     failureLabel.setAlignment(Qt.AlignCenter)

    #     self.failureCheckboxes = []
    #     failures = ["Track Circuit Failure", "Power Failure", "Broken Rail"]
    #     xOffset = 0
    #     for failure in failures:
    #         option = QCheckBox(failure, redBackground)
    #         option.setGeometry(xOffset, 40, 150, 30)
    #         if failure == "Broken Rail":
    #             option.setGeometry(xOffset - 40, 40, 150, 30)
    #         option.setStyleSheet("background-color: #ffd6d6")
    #         self.failureCheckboxes.append(option)
    #         xOffset += 150

    def update_display(self):
        self.selectedBlock = self.blockInput.value()
        # Disable all input fields and buttons at the beginning
        self.speedInput.setEnabled(False)
        self.authorityInput.setEnabled(False)
        self.railwayInput.setEnabled(False)
        self.switchInput.setEnabled(False)
        self.heaterInput.setEnabled(False)
        self.ticketSalesInput.setEnabled(False)
        self.waitingInput.setEnabled(False)

        # Reset the radio button state
        self.trackOpen.setEnabled(False)
        self.trackOccupied.setEnabled(False)
        self.trackMaintenance.setEnabled(False)

        # Reset the radio button state
        self.greenRadio.setEnabled(False)
        self.yellowRadio.setEnabled(False)
        self.redRadio.setEnabled(False)
        # Enable the relevant input fields and buttons based on the selected block
        if self.selectedBlock == 5:
            self.switchInput.setEnabled(True)
        if self.selectedBlock == 10 or self.selectedBlock == 15:
            self.ticketSalesInput.setEnabled(True)
            self.waitingInput.setEnabled(True)

        self.heaterInput.setEnabled(True)
        self.speedInput.setEnabled(True)
        self.authorityInput.setEnabled(True)
        # Enable the radio buttons for track state and light state
        self.trackOpen.setEnabled(True)
        self.trackOccupied.setEnabled(True)
        self.trackMaintenance.setEnabled(True)
        self.greenRadio.setEnabled(True)
        self.yellowRadio.setEnabled(True)
        self.redRadio.setEnabled(True)

    def add_occupancy_test(self):
        selectLineLabel = QLabel("Select Line:", self.testbench)
        selectLineLabel.setGeometry(490, 100, 75, 30)
        selectLineLabel.setStyleSheet("font-weight: bold")
        self.occupancyLineInput = QLineEdit(self.testbench)
        self.occupancyLineInput.setGeometry(570, 100, 50, 30)
        self.occupancyLineInput.setStyleSheet("background-color: white")

        currentBlockLabel = QLabel("Current Block:", self.testbench)
        currentBlockLabel.setGeometry(625, 100, 100, 30)
        currentBlockLabel.setStyleSheet("font-weight: bold")
        self.occupancyCurrentBlock = QLineEdit(self.testbench)
        self.occupancyCurrentBlock.setGeometry(720, 100, 50, 30)
        self.occupancyCurrentBlock.setStyleSheet("background-color: white")

        prevBlockLabel = QLabel("Prev Block:", self.testbench)
        prevBlockLabel.setGeometry(780, 100, 100, 30)
        prevBlockLabel.setStyleSheet("font-weight: bold")
        self.occupancyPrevBlock = QLineEdit(self.testbench)
        self.occupancyPrevBlock.setGeometry(860, 100, 50, 30)
        self.occupancyPrevBlock.setStyleSheet("background-color: white")

        # self.lineInput.addItem("Green")
        # self.lineInput.addItem("Red")
        # self.lineInput.currentIndexChanged.connect(self.send_occupancy_signal)

        signalTest = QPushButton("Occupancy Test", self.testbench)
        signalTest.setGeometry(615, 140, 150, 30)
        signalTest.setStyleSheet(
            "background-color: green; color: white; font-weight: bold"
        )
        signalTest.clicked.connect(self.send_occupancy_signal)

    def send_occupancy_signal(self):
        line = self.occupancyLineInput.text()
        if self.occupancyCurrentBlock.text() != "":
            cur = int(self.occupancyCurrentBlock.text())
        else:
            cur = ""
        prev = int(self.occupancyPrevBlock.text())
        trainModelToTrackModel.sendPolarity.emit(line, cur, prev)

    def add_passenger_test(self):
        selectLineLabel = QLabel("Select Line:", self.testbench)
        selectLineLabel.setGeometry(490, 190, 75, 30)
        selectLineLabel.setStyleSheet("font-weight: bold")
        self.passengerLineInput = QLineEdit(self.testbench)
        self.passengerLineInput.setGeometry(570, 190, 50, 30)
        self.passengerLineInput.setStyleSheet("background-color: white")

        stationNameLabel = QLabel("Station Name:", self.testbench)
        stationNameLabel.setGeometry(625, 190, 100, 30)
        stationNameLabel.setStyleSheet("font-weight: bold")
        self.passengerStationName = QLineEdit(self.testbench)
        self.passengerStationName.setGeometry(720, 190, 50, 30)
        self.passengerStationName.setStyleSheet("background-color: white")

        passengers = QLabel("Passengers:", self.testbench)
        passengers.setGeometry(780, 190, 100, 30)
        passengers.setStyleSheet("font-weight: bold")
        self.trainPassengers = QLineEdit(self.testbench)
        self.trainPassengers.setGeometry(860, 190, 50, 30)
        self.trainPassengers.setStyleSheet("background-color: white")

        signalTest = QPushButton("Passenger Test", self.testbench)
        signalTest.setGeometry(615, 230, 150, 30)
        signalTest.setStyleSheet(
            "background-color: green; color: white; font-weight: bold"
        )
        signalTest.clicked.connect(self.send_passenger_signal)

    def send_passenger_signal(self):
        line = self.passengerLineInput.text()
        station = self.passengerStationName.text()
        passengersOnBoard = int(self.trainPassengers.text())
        trainModelToTrackModel.sendCurrentPassengers.emit(
            line, station, passengersOnBoard
        )
    
    def add_lightstate_test(self):
        selectLineLabel = QLabel("Line Number:", self.testbench)
        selectLineLabel.setGeometry(490, 280, 85, 30)
        selectLineLabel.setStyleSheet("font-weight: bold")
        self.lightLineInput = QLineEdit(self.testbench)
        self.lightLineInput.setGeometry(580, 280, 50, 30)
        self.lightLineInput.setStyleSheet("background-color: white")

        blockLabel = QLabel("Select Block:", self.testbench)
        blockLabel.setGeometry(635, 280, 100, 30)
        blockLabel.setStyleSheet("font-weight: bold")
        self.lightBlock = QLineEdit(self.testbench)
        self.lightBlock.setGeometry(720, 280, 50, 30)
        self.lightBlock.setStyleSheet("background-color: white")

        lightColorLabel = QLabel("Light State:", self.testbench)
        lightColorLabel.setGeometry(780, 280, 100, 30)
        lightColorLabel.setStyleSheet("font-weight: bold")
        self.lightColor = QLineEdit(self.testbench)
        self.lightColor.setGeometry(860, 280, 50, 30)
        self.lightColor.setStyleSheet("background-color: white")

        lightTest = QPushButton("Light State Test", self.testbench)
        lightTest.setGeometry(615, 320, 150, 30)
        lightTest.setStyleSheet(
            "background-color: green; color: white; font-weight: bold"
        )
        lightTest.clicked.connect(self.send_light_signal)

    def send_light_signal(self):
        line = int(self.lightLineInput.text())
        blockNum = int(self.lightBlock.text())
        color = self.lightColor.text()
        trackControllerToTrackModel.lightState.emit(line, 1, blockNum, color)

    def add_crossingstate_test(self):
        selectLineLabel = QLabel("Line Number:", self.testbench)
        selectLineLabel.setGeometry(530, 370, 85, 30)
        selectLineLabel.setStyleSheet("font-weight: bold")
        self.crossingLineInput = QLineEdit(self.testbench)
        self.crossingLineInput.setGeometry(620, 370, 50, 30)
        self.crossingLineInput.setStyleSheet("background-color: white")

        stateLabel = QLabel("Crossing State:", self.testbench)
        stateLabel.setGeometry(680, 370, 100, 30)
        stateLabel.setStyleSheet("font-weight: bold")
        self.crossingState = QLineEdit(self.testbench)
        self.crossingState.setGeometry(780, 370, 50, 30)
        self.crossingState.setStyleSheet("background-color: white")

        crossingTest = QPushButton("Crossing State Test", self.testbench)
        crossingTest.setGeometry(615, 410, 150, 30)
        crossingTest.setStyleSheet(
            "background-color: green; color: white; font-weight: bold"
        )
        crossingTest.clicked.connect(self.send_crossing_signal)

    def send_crossing_signal(self):
        line = int(self.crossingLineInput.text())
        state = True
        if self.crossingState.text() == '0':
            state = False
        trackControllerToTrackModel.crossingState.emit(line, None, None, state)

    def add_switchstate_test(self):
        selectLineLabel = QLabel("Line Number:", self.testbench)
        selectLineLabel.setGeometry(490, 460, 85, 30)
        selectLineLabel.setStyleSheet("font-weight: bold")
        self.switchLineInput = QLineEdit(self.testbench)
        self.switchLineInput.setGeometry(580, 460, 50, 30)
        self.switchLineInput.setStyleSheet("background-color: white")

        blockLabel = QLabel("Select Block:", self.testbench)
        blockLabel.setGeometry(635, 460, 100, 30)
        blockLabel.setStyleSheet("font-weight: bold")
        self.switchBlock = QLineEdit(self.testbench)
        self.switchBlock.setGeometry(720, 460, 50, 30)
        self.switchBlock.setStyleSheet("background-color: white")

        switchStateLabel = QLabel("Switch State:", self.testbench)
        switchStateLabel.setGeometry(780, 460, 100, 30)
        switchStateLabel.setStyleSheet("font-weight: bold")
        self.switchState = QLineEdit(self.testbench)
        self.switchState.setGeometry(860, 460, 50, 30)
        self.switchState.setStyleSheet("background-color: white")

        switchTest = QPushButton("Switch State Test", self.testbench)
        switchTest.setGeometry(615, 510, 150, 30)
        switchTest.setStyleSheet(
            "background-color: green; color: white; font-weight: bold"
        )
        switchTest.clicked.connect(self.send_switch_signal)

    def send_switch_signal(self):
        line = int(self.switchLineInput.text())
        blockNum = int(self.switchBlock.text())
        state = True
        if self.switchState.text() == '0':
            state = False
        trackControllerToTrackModel.switchState.emit(line, None, blockNum, state)