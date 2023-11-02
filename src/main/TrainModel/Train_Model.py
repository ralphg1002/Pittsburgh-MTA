import sys
from PyQt5 import QtGui
from PyQt5.QtCore import (
    QCoreApplication,
    QRect,
    QSize,
    Qt,
    QTimer,
    QTime
)
from PyQt5.QtGui import (
    QCursor,
    QFont,
    QPixmap
)
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout, 
    QComboBox,
    QCheckBox
)
from qtwidgets import AnimatedToggle
# from Signals import TrackModelSignals, TrainControllerSignals


class TrainModel(QMainWindow):
    # Font variables
    textFontSize = 10
    labelFontSize = 12
    headerFontSize = 16
    titleFontSize = 22
    fontStyle = 'Product Sans'

    # Color variables
    colorDarkBlue = '#085394'
    colorLightRed = '#EA9999'
    colorLightBlue = '#9FC5F8'
    colorLightGrey = '#CCCCCC'
    colorMediumGrey = '#DDDDDD'
    colorDarkGrey = '#666666'
    colorBlack = '#000000'

    # Dimensions
    w = 960
    h = 960
    moduleName = 'Train Model'

    def __init__(self):
        super().__init__()

        # QTimer for system clock
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.setSystemTime)
        self.timer.start(500)

        ''' Header Template '''

        # Setting title
        self.setWindowTitle(self.moduleName)

        # Setting geometry
        self.setGeometry(50, 50, self.w, self.h)

        # Body block
        self.bodyBlock = QLabel(self)
        self.bodyBlock.setGeometry(20, 20, 920, 920)
        self.bodyBlock.setStyleSheet('background-color: white;'
                                     'border: 1px solid black')

        # Header block
        self.headerBlock = QLabel(self)
        self.headerBlock.setGeometry(20, 20, 920, 70)
        self.headerBlock.setStyleSheet('background-color:' + self.colorDarkBlue + ';'
                                                                                  'border: 1px solid black')

        # Title
        self.titleLabel = QLabel('Train Model', self)
        self.titleLabel.setFont(QFont(self.fontStyle, self.titleFontSize))
        self.titleLabel.setAlignment(Qt.AlignCenter)
        title_width = 400
        title_height = 50
        title_x = (self.width() - title_width) // 2
        title_y = 35
        self.titleLabel.setGeometry(title_x, title_y, title_width, title_height)
        self.titleLabel.setStyleSheet('color: white')

        # MTA Logo
        self.pixmapMTALogo = QtGui.QPixmap('src/main/TrainModel/MTA_Logo.png')
        self.pixmapMTALogo = self.pixmapMTALogo.scaled(70, 70)
        self.logo = QLabel(self)
        self.logo.setPixmap(self.pixmapMTALogo)
        self.logo.move(20, 20)
        self.logo.adjustSize()

        # Module
        self.moduleLabel = QLabel('Train Model', self)
        self.moduleLabel.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.moduleLabel.setAlignment(Qt.AlignCenter)
        self.moduleLabel.move(30, 100)
        self.moduleLabel.adjustSize()
        self.moduleLabel.setStyleSheet('color:' + self.colorDarkBlue)

        # Test bench icon
        self.pixmapGear = QtGui.QPixmap('src/main/TrainModel/gear_icon.png')
        self.pixmapGear = self.pixmapGear.scaled(25, 25)
        self.testbenchIcon = QLabel(self)
        self.testbenchIcon.setPixmap(self.pixmapGear)
        self.testbenchIcon.setGeometry(30, 140, 32, 32)

        # Test bench button
        self.testbenchButton = QPushButton('Test Bench', self)
        self.testbenchButton.setFont(QFont(self.fontStyle, self.textFontSize))
        self.testbenchButton.setGeometry(60, 140, 100, 32)
        self.testbenchButton.setStyleSheet('color:' + self.colorDarkBlue +
                                           ';border: 1px solid white')

        # System time input
        self.systemTimeInput = QLabel('00:00:00', self)
        self.systemTimeInput.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.systemTimeInput.setGeometry(820, 67, 150, 100)
        self.systemTimeInput.setStyleSheet('color:' + self.colorDarkBlue)

        # System time label
        self.systemTimeLabel = QLabel('System Time:', self)
        self.systemTimeLabel.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.systemTimeLabel.adjustSize()
        self.systemTimeLabel.setGeometry(650, 65, 200, 100)
        self.systemTimeLabel.setStyleSheet('color:' + self.colorDarkBlue)

        # System speed label
        self.systemSpeedLabel = QLabel('System Speed:', self)
        self.systemSpeedLabel.setFont(QFont(self.fontStyle, self.textFontSize))
        self.systemSpeedLabel.setGeometry(689, 140, 200, 100)
        self.systemSpeedLabel.adjustSize()
        self.systemSpeedLabel.setStyleSheet('color:' + self.colorDarkBlue)

        # System speed input
        self.systemSpeedInput = QLabel('x1.0', self)
        self.systemSpeedInput.setFont(QFont(self.fontStyle, self.textFontSize))
        self.systemSpeedInput.setGeometry(850, 127, 50, 50)
        self.systemSpeedInput.setStyleSheet('color:' + self.colorDarkBlue)

        ''' Drop-down Menu '''

        # Calculate the position of the QComboBox
        drop_down_width = 500
        drop_down_height = 40
        drop_down_x = int((self.w - drop_down_width) // 2)
        drop_down_y = int((self.h / 2) + (self.h / 4) - (drop_down_height / 2))

        # Create the QComboBox
        self.comboBox = QComboBox(self.bodyBlock)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(drop_down_x, drop_down_y, drop_down_width, drop_down_height))
        font1 = QFont(self.fontStyle)
        font1.setPointSize(18)
        font1.setKerning(True)
        self.comboBox.setFont(font1)

        # Populate the QComboBox with items
        self.comboBox.addItem("Train 1")
        self.comboBox.addItem("Train 2")
        self.comboBox.addItem("Train 3")
        self.comboBox.addItem("Train 4")
        self.comboBox.addItem("Train 5")

        # Create a search icon for new window
        self.search_button = QtGui.QPixmap('src/main/TrainModel/search_icon.png')
        self.search_button = self.search_button.scaled(40, 40)
        self.icon = QLabel(self)
        self.icon.setPixmap(self.search_button)
        self.icon.setGeometry(QRect(750, 720, 40, 40))
        self.icon.adjustSize()

        # Connect the search icon to the vehicle class
        self.icon.mousePressEvent = self.open_results_window

        # Insert Train Image to main window
        image_path = 'src/main/TrainModel/Train_Image.jpg'
        pixmap_train = QPixmap(image_path)
        image_width = 500
        image_height = 400
        image_y = drop_down_y - image_height - 20 
        pixmap_train = pixmap_train.scaled(image_width, image_height)
        train_image_label = QLabel(self.bodyBlock)
        train_image_label.setPixmap(pixmap_train)
        train_image_label.setGeometry(drop_down_x, image_y, image_width, image_height)

        self.retranslate_Ui()

        self.results_window = None

    def retranslate_Ui(self):
        self.setWindowTitle(QCoreApplication.translate("TrainModel", u"MainWindow", None))
        self.titleLabel.setText(QCoreApplication.translate("TrainModel", u"Train Model", None))
        self.logo.setText("")

    def open_results_window(self, event):
        # This function is called when the search icon is clicked
        selected_item = self.comboBox.currentText()
        self.results_window = ResultsWindow(selected_item)
        self.results_window.show()

    def setSystemTime(self):
        time = QTime.currentTime()
        time_text = time.toString('hh:mm:ss')
        self.systemTimeInput.setText(time_text)

    def show_gui(self):
        self.show()


class ResultsWindow(QMainWindow):
    # Font variables
    textFontSize = 10
    labelFontSize = 12
    headerFontSize = 16
    titleFontSize = 22
    fontStyle = 'Product Sans'

    # Color variables
    colorDarkBlue = '#085394'
    colorLightRed = '#EA9999'
    colorLightBlue = '#9FC5F8'
    colorLightGrey = '#CCCCCC'
    colorMediumGrey = '#DDDDDD'
    colorDarkGrey = '#666666'
    colorBlack = '#000000'

    # Dimensions
    w = 960
    h = 960
    
    moduleName = 'Results Window'

    def __init__(self, selected_text):
        super().__init__()
        self.trains = SharedData()

        # QTimer for system clock
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.setSystemTime)
        self.timer.start(500)

        ''' Header Template '''

        # Setting title
        self.setWindowTitle(self.moduleName)

        # Setting geometry
        self.setGeometry(50, 50, self.w, self.h)

        # Body block
        self.bodyBlock = QLabel(self)
        self.bodyBlock.setGeometry(20, 20, 920, 920)
        self.bodyBlock.setStyleSheet('background-color: white;'
                                     'border: 1px solid black')

        # Header block
        self.headerBlock = QLabel(self)
        self.headerBlock.setGeometry(20, 20, 920, 70)
        self.headerBlock.setStyleSheet('background-color:' + self.colorDarkBlue + ';'
                                                                                  'border: 1px solid black')

        # Title
        self.titleLabel = QLabel('Train Model', self)
        self.titleLabel.setFont(QFont(self.fontStyle, self.titleFontSize))
        self.titleLabel.setAlignment(Qt.AlignCenter)
        title_width = 400
        title_height = 50
        title_x = (self.width() - title_width) // 2
        title_y = 35
        self.titleLabel.setGeometry(title_x, title_y, title_width, title_height)
        self.titleLabel.setStyleSheet('color: white')

        # MTA Logo
        self.pixmapMTALogo = QtGui.QPixmap('src/main/TrainModel/MTA_Logo.png')
        self.pixmapMTALogo = self.pixmapMTALogo.scaled(70, 70)
        self.logo = QLabel(self)
        self.logo.setPixmap(self.pixmapMTALogo)
        self.logo.move(20, 20)
        self.logo.adjustSize()

        # Module
        self.moduleLabel = QLabel('Train Model', self)
        self.moduleLabel.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.moduleLabel.setAlignment(Qt.AlignCenter)
        self.moduleLabel.move(30, 100)
        self.moduleLabel.adjustSize()
        self.moduleLabel.setStyleSheet('color:' + self.colorDarkBlue)

        # Test bench icon
        self.pixmapGear = QtGui.QPixmap('src/main/TrainModel/gear_icon.png')
        self.pixmapGear = self.pixmapGear.scaled(25, 25)
        self.testbenchIcon = QLabel(self)
        self.testbenchIcon.setPixmap(self.pixmapGear)
        self.testbenchIcon.setGeometry(30, 140, 32, 32)

        # Test bench button
        self.testbenchButton = QPushButton('Test Bench', self)
        self.testbenchButton.setFont(QFont(self.fontStyle, self.textFontSize))
        self.testbenchButton.setGeometry(60, 140, 100, 32)
        self.testbenchButton.setStyleSheet('color:' + self.colorDarkBlue +
                                           ';border: 1px solid white')

        # System time input
        self.systemTimeInput = QLabel('00:00:00', self)
        self.systemTimeInput.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.systemTimeInput.setGeometry(820, 67, 150, 100)
        self.systemTimeInput.setStyleSheet('color:' + self.colorDarkBlue)

        # System time label
        self.systemTimeLabel = QLabel('System Time:', self)
        self.systemTimeLabel.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.systemTimeLabel.adjustSize()
        self.systemTimeLabel.setGeometry(650, 65, 200, 100)
        self.systemTimeLabel.setStyleSheet('color:' + self.colorDarkBlue)

        # System speed label
        self.systemSpeedLabel = QLabel('System Speed:', self)
        self.systemSpeedLabel.setFont(QFont(self.fontStyle, self.textFontSize))
        self.systemSpeedLabel.setGeometry(689, 140, 100, 100)
        self.systemSpeedLabel.adjustSize()
        self.systemSpeedLabel.setStyleSheet('color:' + self.colorDarkBlue)

        # System speed input
        self.systemSpeedInput = QLabel('x1.0', self)
        self.systemSpeedInput.setFont(QFont(self.fontStyle, self.textFontSize))
        self.systemSpeedInput.setGeometry(850, 127, 50, 50)
        self.systemSpeedInput.setStyleSheet('color:' + self.colorDarkBlue)

        # Create a QLabel to display the drop-down text
        current_train = QLabel(self)
        current_train.setText(f"Selected Train: {selected_text}")
        current_train.setFont(QFont(self.fontStyle, 16))
        current_train.setGeometry(QRect(275, 100, 400, 50))
        current_train.setAlignment(Qt.AlignCenter)

        # Extract the selected train name from the QLabel's text
        selected_train_name = current_train.text().split(":")[-1].strip()

        ''' Vehicle Status '''

        # Create a QLabel for the vehicle status window
        self.vehicle_label = QLabel(self.bodyBlock)
        self.vehicle_label.setGeometry(QRect(75, 170, 350, 300))
        self.vehicle_label.setStyleSheet("margin: 10px; padding: 0px; border: none;")

        # Create a container widget for the blue and white backgrounds for vehicle status
        self.vehicle_background_widget = QWidget(self.vehicle_label)
        self.vehicle_background_widget.setGeometry(QRect(0, 0, 350, 50))
        self.vehicle_background_widget.setStyleSheet(
            "background-color: #007BFF; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the blue and white backgrounds for vehicle status
        self.vehicle_background_layout = QVBoxLayout(self.vehicle_background_widget)
        self.vehicle_background_layout.setContentsMargins(0, 0, 0, 0)
        self.vehicle_background_layout.setSpacing(0)

        # Create a QLabel for the white background below the blue for vehicle status
        self.vehicle_white_background_label = QLabel(self.bodyBlock)
        self.vehicle_white_background_label.setGeometry(QRect(75, 200, 350, 300))
        self.vehicle_white_background_label.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the blue header for vehicle status
        self.vehicle_white_background_layout = QVBoxLayout(self.vehicle_white_background_label)
        self.vehicle_white_background_layout.setContentsMargins(5, 5, 5, 5)
        self.vehicle_white_background_layout.setSpacing(10)

        # Create QLabel widgets for the list of words
        vehicle_word_list = ["Speed Limit: {} mph", "Current Speed: {} mph",
                             "Setpoint Speed: {}", "Commanded Speed: {}",
                             "Acceleration: {}", "Deceleration: {}", "Brakes: {}",
                             "Power: {}", "Power Limit: {}"]

        vehicle_status = {}

        # Check if the selected train exists in the trains dictionary
        if selected_train_name in self.trains.trains:
            train_data = self.trains.trains[selected_train_name]
            vehicle_status = train_data.get("vehicle_status", {})

            # Create and add QLabel widgets for each word the layout in vehicle status
            for word_placeholders in vehicle_word_list:
                word_key = word_placeholders.split(':')[0].strip().lower().replace(' ', '_')
                word_value = vehicle_status.get(word_key, "N/A")

                # Create the QLabel widget
                if "{}" in word_placeholders and "{}" in word_placeholders[word_placeholders.find("{}")+2:]:  # Check if there are two placeholders in the string
                    word = word_placeholders.format(selected_train_name, word_value)
                else:
                    word = word_placeholders.format(word_value)

                # Create the QLabel widget
                self.word_label = QLabel(word, self.vehicle_white_background_label)
                self.word_label.setStyleSheet("color: #000000; background-color: transparent; border: none;")
                self.word_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.word_label.setContentsMargins(5, 5, 5, 5)
                self.word_label.setFont(QFont("Arial", 9))

                self.vehicle_white_background_layout.addWidget(self.word_label, alignment=Qt.AlignTop)

        self.vehicle_white_background_layout.addStretch(1)

        # Create the title label for vehicle status
        self.vehicle_title_label = QLabel("Vehicle Status:", self.vehicle_label)
        self.font = QFont()
        self.font.setPointSize(14)
        self.font.setBold(True)
        self.vehicle_title_label.setFont(self.font)
        self.vehicle_title_label.setStyleSheet("color: #FFFFFF; background-color: transparent; border: none;")
        self.vehicle_title_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.vehicle_title_label.setGeometry(QRect(0, 0, self.vehicle_background_widget.width(),
                                                   self.vehicle_background_widget.height()))

        ''' Failure Status '''

        # Create a QLabel for the failure rectangle
        self.failure_label = QLabel(self.bodyBlock)
        self.failure_label.setGeometry(QRect(500, 170, 350, 300))
        self.failure_label.setStyleSheet("margin: 10px; padding: 0px; border: none;")

        # Create a container widget for the red and white backgrounds for failure window
        self.failure_background_widget = QWidget(self.failure_label)
        self.failure_background_widget.setGeometry(QRect(0, 0, 350, 50))
        self.failure_background_widget.setStyleSheet(
            "background-color: #FF0000; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the red and white background widget for failure window
        self.failure_white_background_layout = QVBoxLayout(self.failure_background_widget)
        self.failure_white_background_layout.setContentsMargins(0, 0, 0, 0)
        self.failure_white_background_layout.setSpacing(0)

        # Create a QLabel for the white background below the red for failure window
        self.failure_white_background_label = QLabel(self.bodyBlock)
        self.failure_white_background_label.setGeometry(QRect(500, 200, 350, 300))
        self.failure_white_background_label.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the red header for failure window
        self.failure_white_background_layout = QVBoxLayout(self.failure_white_background_label)
        self.failure_white_background_layout.setContentsMargins(5, 5, 5, 5)
        self.failure_white_background_layout.setSpacing(10)

        # Create QLabel widgets for the list of words
        failure_word_list = ["Engine Failure: {}", "Signal Pickup Failure: {}", 
                             "Brake Failure: {}", "Emergency Brake: {}"]

        failure_status = {}
        
        # Check if the selected train exists in the trains dictionary
        if selected_train_name in self.trains.trains:
            train_data = self.trains.trains[selected_train_name]
            failure_status = train_data.get("failure_status", {})

            # Create and add QLabel widgets for each word the layout in failure status
            for word_placeholders in failure_word_list:
                word_key = word_placeholders.split(':')[0].strip().lower().replace(' ', '_')
                word_value = failure_status.get(word_key, "N/A")

                # Create the QLabel widget
                if "{}" in word_placeholders and "{}" in word_placeholders[word_placeholders.find("{}")+2:]:
                    word = word_placeholders.format(selected_train_name, word_value)
                else:
                    word = word_placeholders.format(word_value)
            
                self.word_label = QLabel(word, self.failure_white_background_label)
                self.word_label.setStyleSheet("color: #000000; background-color: transparent; border: none;")
                self.word_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.word_label.setContentsMargins(0, 0, 0, 0)
                self.word_label.setFont(QFont("Arial", 9))

                check = QCheckBox()                
                if check.isChecked():
                    self.trains.set_value(selected_train_name, "failure_status", word_key, True)
                else:
                    self.trains.set_value(selected_train_name, "failure_status", word_key, False)

                self.failure_white_background_layout.addWidget(self.word_label, alignment=Qt.AlignTop)

        self.failure_white_background_layout.addStretch(1)

        # Create the title label
        self.failure_title_label = QLabel("Failures:", self.failure_label)
        self.font = QFont()
        self.font.setPointSize(14)
        self.font.setBold(True)
        self.failure_title_label.setFont(self.font)
        self.failure_title_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        self.failure_title_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.failure_title_label.setGeometry(QRect(0, 0, self.failure_background_widget.width(), self.failure_background_widget.height()))

        ''' Passenger Status '''

        # Create a QLabel for the Passenger Status
        self.passenger_label = QLabel(self.bodyBlock)
        self.passenger_label.setGeometry(QRect(75, 550, 350, 300))
        self.passenger_label.setStyleSheet("margin: 10px; padding: 0px; border: none;")

        # Create a container widget for the blue and white backgrounds for passenger status
        self.passenger_background_widget = QWidget(self.passenger_label)
        self.passenger_background_widget.setGeometry(QRect(0, 0, 350, 50))
        self.passenger_background_widget.setStyleSheet(
            "background-color: #007BFF; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the blue and white background widget for passenger status
        self.passenger_background_layout = QVBoxLayout(self.passenger_background_widget)
        self.passenger_background_layout.setContentsMargins(0, 0, 0, 0)
        self.passenger_background_layout.setSpacing(0)

        # Create a QLabel for the white background below the blue
        self.passenger_white_background_label = QLabel(self.bodyBlock)
        self.passenger_white_background_label.setGeometry(QRect(75, 580, 350, 300))
        self.passenger_white_background_label.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the blue header for vehicle status
        self.passenger_white_background_layout = QVBoxLayout(self.passenger_white_background_label)
        self.passenger_white_background_layout.setContentsMargins(5, 5, 5, 5)
        self.passenger_white_background_layout.setSpacing(10)

        # Create QLabel widgets for the list of words
        passenger_word_list = ["Passengers: {}", "Passenger Limit: {}",
                               "Left Door: {}", "Right Door: {}", "Lights Status: {}",
                               "Announcements: {}", "Temperature: {}",
                               "Air Conditioning: {}", "Advertisements: {}"]

        passenger_status = {}

        # Check if the selected train exists in the trains dictionary
        if selected_train_name in self.trains.trains:
            train_data = self.trains.trains[selected_train_name]
            passenger_status = train_data.get("passenger_status", {})

            # Create and add QLabel widgets for each word in the layout in passenger status
            for word_placeholders in passenger_word_list:
                word_key = word_placeholders.split(':')[0].strip().lower().replace(' ', '_')
                word_value = passenger_status.get(word_key, "N/A")

                # Create the QLabel widget
                if "{}" in word_placeholders and "{}" in word_placeholders[word_placeholders.find("{}")+2:]:
                    word = word_placeholders.format(selected_train_name, word_value)
                else:
                    word = word_placeholders.format(word_value)

                self.word_label = QLabel(word, self.passenger_white_background_label)
                self.word_label.setStyleSheet("color: #000000; background-color: transparent; border: none;")
                self.word_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.word_label.setContentsMargins(5, 5, 5, 5)
                self.word_label.setFont(QFont("Arial", 9))

                self.passenger_white_background_layout.addWidget(self.word_label, alignment=Qt.AlignTop)    

        self.passenger_white_background_layout.addStretch(1)

        # Create the title label
        self.passenger_title_label = QLabel("Passenger Status:", self.passenger_label)
        self.font = QFont()
        self.font.setPointSize(14)
        self.font.setBold(True)
        self.passenger_title_label.setFont(self.font)
        self.passenger_title_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        self.passenger_title_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.passenger_title_label.setGeometry(QRect(0, 0, self.passenger_background_widget.width(),
                                                     self.passenger_background_widget.height()))

        ''' Navigation Status '''

        # Create a QLabel for the Navigation status
        self.navigation_label = QLabel(self.bodyBlock)
        self.navigation_label.setGeometry(QRect(500, 550, 350, 300))
        self.navigation_label.setStyleSheet("margin: 10px; padding: 0px; border: none;")

        # Create a container widget for the blue and white backgrounds for navigation status
        self.navigation_background_widget = QWidget(self.navigation_label)
        self.navigation_background_widget.setGeometry(QRect(0, 0, 350, 50))
        self.navigation_background_widget.setStyleSheet(
            "background-color: #007BFF; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the blue and white background widget for navigation status
        self.navigation_background_layout = QVBoxLayout(self.navigation_background_widget)
        self.navigation_background_layout.setContentsMargins(0, 0, 0, 0)
        self.navigation_background_layout.setSpacing(0)

        # Create a QLabel for the white background below the blue for navigation status
        self.navigation_white_background_label = QLabel(self.bodyBlock)
        self.navigation_white_background_label.setGeometry(QRect(500, 580, 350, 300))
        self.navigation_white_background_label.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the blue header for navigation status
        self.navigation_white_background_layout = QVBoxLayout(self.navigation_white_background_label)
        self.navigation_white_background_layout.setContentsMargins(5, 5, 5, 5)
        self.navigation_white_background_layout.setSpacing(10)

        # Create QLabel widgets for the list of words
        navigation_word_list = ["Authority: {}", "Beacon: {}", "Block Length: {}", "Block Grade: {}", 
                                "Next Station: {}", "Previous Station: {}", "Headlights: {}", 
                                "Passenger Emergency Brake: {}"]
        
        navigation_status = {}

        # Check if the selected train exists in the trains dictionary
        if selected_train_name in self.trains.trains:
            train_data = self.trains.trains[selected_train_name]
            navigation_status = train_data.get("navigation_status", {})

            # Create and add QLabel widgets for each word the layout in navigation status
            for word_placeholders in navigation_word_list:
                word_key = word_placeholders.split(':')[0].strip().lower().replace(' ', '_')
                word_value = navigation_status.get(word_key, "N/A")

                # Create the QLabel widget
                if "{}" in word_placeholders and "{}" in word_placeholders[word_placeholders.find("{}")+2:]:
                    word = word_placeholders.format(selected_train_name, word_value)
                else:
                    word = word_placeholders.format(word_value)
                
                self.word_label = QLabel(word, self.navigation_white_background_label)
                self.word_label.setStyleSheet("color: #000000; background-color: transparent; border: none;")
                self.word_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.word_label.setContentsMargins(5, 5, 5, 5)
                self.word_label.setFont(QFont("Arial", 9))

                self.navigation_white_background_layout.addWidget(self.word_label, alignment=Qt.AlignTop)

        self.navigation_white_background_layout.addStretch(1)

        # Create the title label
        self.navigation_title_label = QLabel("Navigation Status:", self.navigation_label)
        self.font = QFont()
        self.font.setPointSize(14)
        self.font.setBold(True)
        self.navigation_title_label.setFont(self.font)
        self.navigation_title_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        self.navigation_title_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.navigation_title_label.setGeometry(QRect(0, 0, self.navigation_background_widget.width(),
                                                     self.navigation_background_widget.height()))

    def setSystemTime(self):
        time = QTime.currentTime()
        time_text = time.toString('hh:mm:ss')
        self.systemTimeInput.setText(time_text)


class SharedData:
    def __init__(self):
        self.trains = {
            "Train 1": {
                "vehicle_status": {
                    "speed_limit": 35,
                    "current_speed": 45,
                    "setpoint_speed": 55,
                    "commanded_speed": 40,
                    "acceleration": 3.5,
                    "deceleration": 2.0,
                    "brakes": True,
                    "power": 75.0,
                    "power_limit": 100.0
                },
                "failure_status": {
                    "engine_failure": False,
                    "signal_pickup_failure": False, 
                    "brake_failure": False,
                    "emergency_brake": False
                },
                "passenger_status": {
                    "passengers": 42,
                    "passenger_limit": 50,
                    "left_door": False,
                    "right_door": True,
                    "lights_status": True,
                    "announcements": True,
                    "temperature": 72,
                    "air_conditioning": False,
                    "advertisements": "Buy Drinks"
                },
                "navigation_status": {
                    "authority": 5,
                    "beacon": 6,
                    "block_length": 2,
                    "block_grade": 15,
                    "next_station": 9,
                    "prev_station": 5,
                    "headlights": True,
                    "passenger_emergency_brake": False
                }
            },
            "Train 2": {
                "vehicle_status": {
                    "speed_limit": 45,
                    "current_speed": 45,
                    "setpoint_speed": 55,
                    "commanded_speed": 40,
                    "acceleration": 3.5,
                    "deceleration": 2.0,
                    "brakes": True,
                    "power": 75.0,
                    "power_limit": 100.0
                },
                "failure_status": {
                    "engine_failure": False,
                    "signal_pickup_failure": False,
                    "brake_failure": False,
                    "emergency_brake": False
                },
                "passenger_status": {
                    "passengers": 42,
                    "passenger_limit": 50,
                    "left_door": False,
                    "right_door": True,
                    "lights_status": True,
                    "announcements": True,
                    "temperature": 72,
                    "air_conditioning": False,
                    "advertisements": "Buy Drinks"
                },
                "navigation_status": {
                    "authority": 5,
                    "beacon": 6,
                    "block_length": 2,
                    "block_grade": 15,
                    "next_station": 9,
                    "prev_station": 5,
                    "headlights": True,
                    "passenger_emergency_brake": False
                }
            },
            "Train 3": {
                "vehicle_status": {
                    "speed_limit": 35,
                    "current_speed": 45,
                    "setpoint_speed": 55,
                    "commanded_speed": 40,
                    "acceleration": 3.5,
                    "deceleration": 2.0,
                    "brakes": True,
                    "power": 75.0,
                    "power_limit": 100.0
                },
                "failure_status": {
                    "engine_failure": False,
                    "signal_pickup_failure": False,
                    "brake_failure": False,
                    "emergency_brake": False
                },
                "passenger_status": {
                    "passengers": 42,
                    "passenger_limit": 50,
                    "left_door": False,
                    "right_door": True,
                    "lights_status": True,
                    "announcements": True,
                    "temperature": 72,
                    "air_conditioning": False,
                    "advertisements": "Buy Drinks"
                },
                "navigation_status": {
                    "authority": 5,
                    "beacon": 6,
                    "block_length": 2,
                    "block_grade": 15,
                    "next_station": 9,
                    "prev_station": 5,
                    "headlights": True,
                    "passenger_emergency_brake": False
                }
            },
            "Train 4": {
                "vehicle_status": {
                    "speed_limit": 35,
                    "current_speed": 45,
                    "setpoint_speed": 55,
                    "commanded_speed": 40,
                    "acceleration": 3.5,
                    "deceleration": 2.0,
                    "brakes": True,
                    "power": 75.0,
                    "power_limit": 100.0
                },
                "failure_status": {
                    "engine_failure": False,
                    "signal_pickup_failure": False,
                    "brake_failure": False,
                    "emergency_brake": False
                },
                "passenger_status": {
                    "passengers": 42,
                    "passenger_limit": 50,
                    "left_door": False,
                    "right_door": True,
                    "lights_status": True,
                    "announcements": True,
                    "temperature": 72,
                    "air_conditioning": False,
                    "advertisements": "Buy Drinks"
                },
                "navigation_status": {
                    "authority": 5,
                    "beacon": 6,
                    "block_length": 2,
                    "block_grade": 15,
                    "next_station": 9,
                    "prev_station": 5,
                    "headlights": True,
                    "passenger_emergency_brake": False
                }
            },
            "Train 5": {
                "vehicle_status": {
                    "speed_limit": 35,
                    "current_speed": 45,
                    "setpoint_speed": 55,
                    "commanded_speed": 40,
                    "acceleration": 3.5,
                    "deceleration": 2.0,
                    "brakes": True,
                    "power": 75.0,
                    "power_limit": 100.0
                },
                "failure_status": {
                    "engine_failure": False,
                    "signal_pickup_failure": False,
                    "brake_failure": False,
                    "emergency_brake": False
                },
                "passenger_status": {
                    "passengers": 42,
                    "passenger_limit": 50,
                    "left_door": False,
                    "right_door": True,
                    "lights_status": True,
                    "announcements": True,
                    "temperature": 72,
                    "air_conditioning": False,
                    "advertisements": "Buy Drinks"
                },
                "navigation_status": {
                    "authority": 5,
                    "beacon": 6,
                    "block_length": 2,
                    "block_grade": 15,
                    "next_station": 9,
                    "prev_station": 5,
                    "headlights": True,
                    "passenger_emergency_brake": False
                }
            }
        }

    def get_value(self, train_name, category, key):
        return self.trains.get(train_name, {}).get(category, {}).get(key)

    def set_value(self, train_name, category, key, value):
        if train_name in self.trains:
            if category in self.trains[train_name]:
                self.trains[train_name][category][key] = value


class TrainTest(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Train Model")
        self.setFixedSize(1280, 720)
        self.central_widget = QWidget(self)
        self.central_widget.setObjectName(u"central_widget")

        # Title Left Line
        self.LeftLine = QFrame(self.central_widget)
        self.LeftLine.setObjectName(u"TitleLeftLine")
        self.LeftLine.setGeometry(QRect(0, 138, self.width() // 2, 3))
        self.LeftLine.setMaximumSize(QSize(720, 1280))
        self.LeftLine.setFrameShape(QFrame.HLine)
        self.LeftLine.setFrameShadow(QFrame.Sunken)

        # Title Right Line
        self.RightLine = QFrame(self.central_widget)
        self.RightLine.setObjectName(u"TitleRightLine")
        self.RightLine.setGeometry(QRect(self.width() // 2, 138, self.width() // 2, 3))
        self.RightLine.setMaximumSize(QSize(720, 1280))
        self.RightLine.setFrameShape(QFrame.HLine)
        self.RightLine.setFrameShadow(QFrame.Sunken)

        # Title
        self.Title = QLabel("Train Model Test", self.central_widget)
        self.Title.setObjectName(u"Title")
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(32)
        self.Title.setFont(font)
        self.Title.setText(QCoreApplication.translate("TrainTest", u"Train Model Test", None))
        title_width = self.Title.sizeHint().width()
        title_height = self.Title.sizeHint().height()
        title_x = self.width() // 2 - title_width // 2
        title_y = (138 + 0) // 2 - title_height // 2
        self.Title.setGeometry(QRect(title_x, title_y, title_width, title_height))

        # MTA Logo
        self.mtaLogo = QLabel(self.central_widget)
        self.mtaLogo.setObjectName(u"mtaLogo")
        self.mtaLogo.setGeometry(QRect(0, 0, 128, 128))
        self.mtaLogo.setMaximumSize(QSize(1280, 720))
        self.mtaLogo.setPixmap(QPixmap(u"src/main/TrainModel/MTA_Logo.png"))
        self.mtaLogo.setScaledContents(True)

        # Train Image
        train_image_label = QLabel(self.central_widget)
        train_image_label.setObjectName(u"TrainImage")
        train_image_pixmap = QPixmap("src/main/TrainModel/Train_Image.jpg")
        max_image_height = 400  # You can change this to your desired height
        new_width = int((train_image_pixmap.width() * max_image_height) / train_image_pixmap.height())
        train_image_pixmap = train_image_pixmap.scaled(new_width, max_image_height, Qt.KeepAspectRatio)
        image_width = train_image_pixmap.width()
        image_height = train_image_pixmap.height()
        image_x = (self.width() - image_width) // 2
        image_y = 138 + 20
        train_image_label.setGeometry(QRect(image_x, image_y, image_width, image_height))
        train_image_label.setPixmap(train_image_pixmap)
        train_image_label.setScaledContents(True)

        # Calculate the position for the Train Image
        image_width = train_image_pixmap.width()
        image_height = train_image_pixmap.height()
        image_x = (self.width() - image_width) // 2
        image_y = (138 + 0) + 20

        train_image_label.setGeometry(QRect(image_x, image_y, image_width, image_height))

        # Search Bar
        search_bar_width = 500
        search_bar_height = 40
        search_bar_x = (self.width() - search_bar_width) // 2
        search_bar_y = image_y + image_height + 30  # Adjust the spacing as needed

        self.lineEdit = QLineEdit(self.central_widget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(search_bar_x, search_bar_y, search_bar_width, search_bar_height))
        font1 = QFont()
        font1.setPointSize(18)
        font1.setKerning(True)
        self.lineEdit.setFont(font1)

        # Push Buttons
        button_width = 150
        button_height = 50
        button_spacing = 30
        button_x = (self.width() - (3 * button_width + 2 * button_spacing)) // 2

        # First button
        self.pushButton = QPushButton(self.central_widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(button_x, search_bar_y + search_bar_height + 10, button_width, button_height))
        self.pushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton.setAutoRepeatInterval(105)

        # Second button
        self.pushButton_2 = QPushButton(self.central_widget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(
            QRect(button_x + button_width + button_spacing, search_bar_y + search_bar_height + 10,
                  button_width, button_height))
        self.pushButton_2.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_2.setAutoRepeatInterval(105)

        # Third button
        self.pushButton_3 = QPushButton(self.central_widget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_3.setGeometry(
            QRect(button_x + 2 * (button_width + button_spacing), search_bar_y + search_bar_height + 10,
                  button_width, button_height))
        self.pushButton_3.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_3.setAutoRepeatInterval(105)

        self.setCentralWidget(self.central_widget)

        # Status Bar
        self.statusbar = self.statusBar()
        self.statusbar.setObjectName("statusbar")

        # Menu Bar
        self.menubar = self.menuBar()
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 720, 22))

        self.retranslateUi()

        # Track Model Test button press
        self.pushButton.setText(QCoreApplication.translate("TrainTest", u"Track Model Test", None))
        self.pushButton.clicked.connect(self.show_track_model_test)

        # Train Controller Test button press
        self.pushButton_2.setText(QCoreApplication.translate("TrainTest", u"Train Controller Test", None))
        self.pushButton_2.clicked.connect(self.show_train_controller_test)

        # Murphy button press
        self.pushButton_3.setText(QCoreApplication.translate("TrainTest", u"Murphy Test", None))
        self.pushButton_3.clicked.connect(self.show_murphy_test)

        # Create a "Main" button
        self.main_menu = QPushButton("Main", self.central_widget)
        self.main_menu.setObjectName(u"Main Menu")
        main_menu_width = 150
        main_menu_height = 65
        main_menu_x = self.width() - main_menu_width - 10
        main_menu_y = self.height() - main_menu_height - 30
        self.main_menu.setGeometry(QRect(main_menu_x, main_menu_y, main_menu_width, main_menu_height))
        self.main_menu.setCursor(QCursor(Qt.PointingHandCursor))
        self.main_menu.setFont(QFont("Arial", 10))

        # Main button press
        self.main_menu.setText(QCoreApplication.translate("TrainTest", u"Main Menu", None))
        self.main_menu.clicked.connect(self.show_main_window)

    def update_clock_label(self):
        time_text = self.clock.elapsed_time.toString("HH:mm:ss")
        self.clock_label.setText(time_text)

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("TrainTest", u"MainWindow", None))
        self.Title.setText(QCoreApplication.translate("TrainTest", u"Train Model Test", None))
        self.mtaLogo.setText("")
        self.lineEdit.setText("")
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("TrainTest", u"Train 1, 2, 3, 4", None))
        self.pushButton.setText(QCoreApplication.translate("TrainTest", u"Track Model Test", None))
        self.pushButton_2.setText(QCoreApplication.translate("TrainTest", u"Train Controller Test", None))
        self.pushButton_3.setText(QCoreApplication.translate("TrainTest", u"Murphy Test", None))

    def show_track_model_test(self):
        self.track_model_test = TrackModelTestWindow(self.clock)
        self.track_model_test.show()

    def show_train_controller_test(self):
        self.train_controller_test = TrainControllerTestWindow(self.clock)
        self.train_controller_test.show()

    def show_murphy_test(self):
        self.murphy_test = MurphyTestWindow(self.clock)
        self.murphy_test.show()

    def show_main_window(self):
        self.main_window = TrainModel()
        self.main_window.show()
        self.close()


class TrackModelTestWindow(QMainWindow):
    def __init__(self, clock):
        super().__init__()
        self.setWindowTitle("Track Model Test")
        self.setFixedSize(1280, 720)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.clock = clock

        # Create a label for the clock in the main window
        self.font = QFont()
        self.font.setPointSize(20)
        self.clock_label = QLabel(self.central_widget)
        self.clock_label.setObjectName(u"clock_label")
        self.clock_label.setFont(self.font)
        self.clock_label.setAlignment(Qt.AlignRight | Qt.AlignTop)

        # Connect the clock's timeUpdated signal to the update_clock_label method
        self.clock.timeUpdated.connect(self.update_clock_label)

        # Start a timer to update the clock label periodically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock_label)
        self.timer.start(100)

        # Add the clock label to the central widget
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.clock_label)
        self.layout.addStretch()

        # Title Left Line
        self.LeftLine = QFrame(self.central_widget)
        self.LeftLine.setObjectName(u"TitleLeftLine")
        self.LeftLine.setGeometry(QRect(0, 138, self.width() // 2, 3))
        self.LeftLine.setMaximumSize(QSize(720, 1280))
        self.LeftLine.setFrameShape(QFrame.HLine)
        self.LeftLine.setFrameShadow(QFrame.Sunken)

        # Title Right Line
        self.RightLine = QFrame(self.central_widget)
        self.RightLine.setObjectName(u"TitleRightLine")
        self.RightLine.setGeometry(QRect(self.width() // 2, 138, self.width() // 2, 3))
        self.RightLine.setMaximumSize(QSize(720, 1280))
        self.RightLine.setFrameShape(QFrame.HLine)
        self.RightLine.setFrameShadow(QFrame.Sunken)

        # Title
        self.Title = QLabel("Track Model Test", self.central_widget)
        self.Title.setObjectName(u"Title")
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(32)
        self.Title.setFont(font)
        self.Title.setText(QCoreApplication.translate("TrainTest", u"Track Model Test", None))
        title_width = self.Title.sizeHint().width()
        title_height = self.Title.sizeHint().height()
        title_x = self.width() // 2 - title_width // 2
        title_y = (138 + 0) // 2 - title_height // 2
        self.Title.setGeometry(QRect(title_x, title_y, title_width, title_height))

        # MTA Logo
        self.mtaLogo = QLabel(self.central_widget)
        self.mtaLogo.setObjectName(u"mtaLogo")
        self.mtaLogo.setGeometry(QRect(0, 0, 128, 128))
        self.mtaLogo.setMaximumSize(QSize(1280, 720))
        self.mtaLogo.setPixmap(QPixmap(u"src/main/TrainModel/MTA_Logo.png"))
        self.mtaLogo.setScaledContents(True)

        # Create a QLabel for the first rectangle
        self.rectangle_label = QLabel(self.central_widget)
        self.rectangle_label.setGeometry(QRect(50, 170, 590, 500))
        self.rectangle_label.setStyleSheet("margin: 10px; padding: 0px;")

        # Create a container widget for the blue and white backgrounds
        self.background_widget = QWidget(self.rectangle_label)
        self.background_widget.setGeometry(QRect(0, 0, 590, 50))
        self.background_widget.setStyleSheet(
            "background-color: #007BFF; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the blue and white background widget
        self.background_layout = QVBoxLayout(self.background_widget)
        self.background_layout.setContentsMargins(0, 0, 0, 0)
        self.background_layout.setSpacing(0)

        # Create a QLabel for the white background below the blue
        self.white_background_label = QLabel(self.central_widget)
        self.white_background_label.setGeometry(QRect(50, 210, 590, 430))
        self.white_background_label.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the blue header
        self.white_background_layout = QVBoxLayout(self.white_background_label)
        self.white_background_layout.setContentsMargins(0, 0, 0, 0)
        self.white_background_layout.setSpacing(10)

        # Create QLabel widgets for the list of words
        word_list_1 = ["Speed Limit:", "Authority:", "Beacon:", "Passengers Entering:", "Acceleration Limit:",
                       "Deceleration Limit:", "Brakes:", "Block Length:", "Direction of Travel:", "Block Elevation:"]

        # Create and add QLineEdit widgets for the first word list
        self.value_inputs = {}
        for word_placeholder in word_list_1:
            word_label = QLabel(word_placeholder, self.white_background_label)
            word_label.setStyleSheet("color: #000000; background-color: transparent; border: none;")
            word_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            word_label.setContentsMargins(10, 5, 10, 5)
            word_label.setFont(QFont("Arial", 10))

            value_input = QLineEdit(self.white_background_label)
            value_input.setStyleSheet("background-color: #FFFFFF; border: 0.5px solid #000000;")
            value_input.setContentsMargins(15, 15, 15, 15)

            word_layout = QHBoxLayout()
            word_layout.addWidget(word_label, alignment=Qt.AlignLeft)
            word_layout.addWidget(value_input, alignment=Qt.AlignLeft)

            self.white_background_layout.addLayout(word_layout)

            self.value_inputs[word_placeholder] = value_input

        self.white_background_layout.addStretch(1)

        # Create Apply and Reset buttons
        self.apply_button = QPushButton("Apply", self.central_widget)
        self.apply_button.setGeometry(1100, 640, 80, 30)
        self.apply_button.clicked.connect(self.apply_values)
        self.apply_button.setEnabled(True)

        self.reset_button = QPushButton("Reset", self.central_widget)
        self.reset_button.setGeometry(1190, 640, 80, 30)
        self.reset_button.clicked.connect(self.reset_values)
        self.reset_button.setEnabled(True)

        # Create the title label
        self.title_label = QLabel("Inputs:", self.rectangle_label)
        self.font = QFont()
        self.font.setPointSize(16)
        self.font.setBold(True)
        self.title_label.setFont(self.font)
        self.title_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        self.title_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.title_label.setGeometry(QRect(0, 0, self.background_widget.width(), self.background_widget.height()))

        # Create the line separator
        self.line_separator = QFrame(self.rectangle_label)
        self.line_separator.setGeometry(QRect(10, 40, 570, 2))
        self.line_separator.setFrameShape(QFrame.HLine)
        self.line_separator.setFrameShadow(QFrame.Sunken)
        self.line_separator.setStyleSheet("background-color: #000000")

        # Create a QLabel for the second rectangle
        self.rectangle_label_2 = QLabel(self.central_widget)
        self.rectangle_label_2.setGeometry(QRect(640, 170, 590, 500))
        self.rectangle_label_2.setStyleSheet("margin: 10px; padding: 0px;")

        # Create a container widget for the red and white backgrounds
        self.background_widget_2 = QWidget(self.rectangle_label_2)
        self.background_widget_2.setGeometry(QRect(0, 0, 590, 50))
        self.background_widget_2.setStyleSheet(
            "background-color: #FF0000; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the red and white background widget
        self.white_background_layout_2 = QVBoxLayout(self.background_widget_2)
        self.white_background_layout_2.setContentsMargins(0, 0, 0, 0)
        self.white_background_layout_2.setSpacing(0)

        # Create a QLabel for the white background below the red
        self.white_background_label_2 = QLabel(self.central_widget)
        self.white_background_label_2.setGeometry(QRect(640, 210, 590, 430))
        self.white_background_label_2.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the red header
        self.white_background_layout_2 = QVBoxLayout(self.white_background_label_2)
        self.white_background_layout_2.setContentsMargins(0, 0, 0, 0)
        self.white_background_layout_2.setSpacing(5)

        # Create QLabel widgets for the list of words
        self.word_list_2 = ["Speed Limit:", "Authority:", "Commanded Speed:", "Current Speed:", "Temperature:",
                            "Passengers Currently:", "Max Passengers:", "Next Station:", "Previous Station:",
                            "Engine Failure:", "Signal Pickup Failure:", "Brake Failure:", "Power:",
                            "Passenger Emergency Brake:"]

        # Defines a dictionary with actual values for second set of words
        self.values_2 = {
            "Speed Limit:": "40 mph",
            "Authority:": "6 Blocks",
            "Commanded Speed:": "37 mph",
            "Current Speed:": "35 mph",
            "Temperature:": "78 ℉",
            "Passengers Currently:": "58",
            "Max Passengers:": "72",
            "Next Station:": "Block 7",
            "Previous Station:": "Block 3",
            "Engine Failure:": True,
            "Signal Pickup Failure:": False,
            "Brake Failure:": True,
            "Power:": "83 kW",
            "Passenger Emergency Brake:": "On"
        }

        # Initialize the list at the beginning of my method
        self.word_labels = []

        for word_placeholder in self.word_list_2:
            value = self.values_2.get(word_placeholder, '')
            label_text = f"{word_placeholder} {value}"
            word_label = QLabel(label_text, self.white_background_label_2)
            word_label.setStyleSheet("color: #000000; background-color: transparent; border: none;")
            word_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            word_label.setContentsMargins(10, 5, 10, 5)
            word_label.setFont(QFont("Arial", 10))
            self.white_background_layout_2.addWidget(word_label, alignment=Qt.AlignTop)
            self.word_labels.append(word_label)

        # Create the title label
        self.title_label_2 = QLabel("Outputs:", self.rectangle_label_2)
        self.font = QFont()
        self.font.setPointSize(16)
        self.font.setBold(True)
        self.title_label_2.setFont(self.font)
        self.title_label_2.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        self.title_label_2.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.title_label_2.setGeometry(QRect(0, 0, self.background_widget.width(), self.background_widget.height()))

        # Create the line separator
        self.line_separator_2 = QFrame(self.rectangle_label_2)
        self.line_separator_2 = QFrame(self.rectangle_label_2)
        self.line_separator_2.setGeometry(QRect(10, 40, 570, 2))
        self.line_separator_2.setFrameShape(QFrame.HLine)
        self.line_separator_2.setFrameShadow(QFrame.Sunken)
        self.line_separator_2.setStyleSheet("background-color: #000000")

    def apply_values(self):
        values_wordlist_1 = {}

        # Iterate through the input text boxes and update values_wordlist_1
        for word_placeholder, value_input in self.value_inputs.items():
            input_value = value_input.text()
            if input_value:
                try:
                    # Try to convert the input to an integer
                    input_value = int(input_value)
                except ValueError:
                    pass  # If it's not a valid integer, keep it as a string
                values_wordlist_1[word_placeholder] = input_value

        # Update the corresponding output values based on the mappings
        for word_placeholder, output_key in self.mapping.items():
            if word_placeholder in values_wordlist_1:
                self.values_2[output_key] = values_wordlist_1[word_placeholder]
                # Update the corresponding text box in the second set
                self.update_wordlist2_textbox(output_key, values_wordlist_1[word_placeholder])

        return values_wordlist_1

    def reset_values(self):
        default_values_wordlist_2 = {
            "Speed Limit": "45 mph",
            "Authority": "5 Blocks",
            "Commanded Speed": "35 mph",
            "Current Speed": "32 mph",
            "Temperature": "75 ℉",
            "Passengers Currently": "60",
            "Max Passengers": "74",
            "Next Station": "Block 9",
            "Previous Station": "Block 5",
            "Engine Failure": False,
            "Signal Pickup Failure": True,
            "Brake Failure": False,
            "Power": "80 kW",
            "Passenger Emergency Brake": "Off"
        }

        for i, (word_placeholder, value) in enumerate(zip(self.word_list_2, default_values_wordlist_2.values())):
            label_text = f"{word_placeholder} {value}" if word_placeholder else value
            self.word_labels[i].setText(label_text)

    def update_wordlist2_values(self):
        values_wordlist_1 = self.apply_values()

        for i, word_placeholder in enumerate(self.word_list_2):
            if word_placeholder in self.values_2:
                label = self.values_2[word_placeholder]

                # Check if there is a corresponding label in word list 1
                corresponding_label = self.get_corresponding_label(word_placeholder)

                if corresponding_label:
                    # Get the value from word list 1 and format the label
                    value = values_wordlist_1.get(corresponding_label, "")
                    label = f"{word_placeholder} {value}"

                self.word_labels[i].setText(label)

    def get_corresponding_label(self, label_wordlist2):
        # Define a mapping between word list 2 labels and their corresponding word list 1 labels
        label_mapping = {
            "Speed Limit:": "Speed Limit:",
            "Authority:": "Authority:",
        }

        # Get the corresponding label from the mapping
        return label_mapping.get(label_wordlist2, "")

    def update_clock_label(self):
        time_text = self.clock.elapsed_time.toString("HH:mm:ss")
        self.clock_label.setText(time_text)


class TrainControllerTestWindow(QMainWindow):
    def __init__(self, clock):
        super().__init__()
        self.setWindowTitle("Train Controller Test")
        self.setFixedSize(1280, 720)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.clock = clock

        # Create a label for the clock in the main window
        self.font = QFont()
        self.font.setPointSize(20)
        self.clock_label = QLabel(self.central_widget)
        self.clock_label.setObjectName(u"clock_label")
        self.clock_label.setFont(self.font)
        self.clock_label.setAlignment(Qt.AlignRight | Qt.AlignTop)

        # Connect the clock's timeUpdated signal to the update_clock_label method
        self.clock.timeUpdated.connect(self.update_clock_label)

        # Start a timer to update the clock label periodically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock_label)
        self.timer.start(100)

        # Add the clock label to the central widget
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.clock_label)
        self.layout.addStretch()

        # Title Left Line
        self.LeftLine = QFrame(self.central_widget)
        self.LeftLine.setObjectName(u"TitleLeftLine")
        self.LeftLine.setGeometry(QRect(0, 138, self.width() // 2, 3))
        self.LeftLine.setMaximumSize(QSize(720, 1280))
        self.LeftLine.setFrameShape(QFrame.HLine)
        self.LeftLine.setFrameShadow(QFrame.Sunken)

        # Title Right Line
        self.RightLine = QFrame(self.central_widget)
        self.RightLine.setObjectName(u"TitleRightLine")
        self.RightLine.setGeometry(QRect(self.width() // 2, 138, self.width() // 2, 3))
        self.RightLine.setMaximumSize(QSize(720, 1280))
        self.RightLine.setFrameShape(QFrame.HLine)
        self.RightLine.setFrameShadow(QFrame.Sunken)

        # Title
        self.Title = QLabel("Train Controller Test", self.central_widget)
        self.Title.setObjectName(u"Title")
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(32)
        self.Title.setFont(font)
        self.Title.setText(QCoreApplication.translate("TrainTest", u"Train Controller Test", None))
        title_width = self.Title.sizeHint().width()
        title_height = self.Title.sizeHint().height()
        title_x = self.width() // 2 - title_width // 2
        title_y = (138 + 0) // 2 - title_height // 2
        self.Title.setGeometry(QRect(title_x, title_y, title_width, title_height))

        # MTA Logo
        self.mtaLogo = QLabel(self.central_widget)
        self.mtaLogo.setObjectName(u"mtaLogo")
        self.mtaLogo.setGeometry(QRect(0, 0, 128, 128))
        self.mtaLogo.setMaximumSize(QSize(1280, 720))
        self.mtaLogo.setPixmap(QPixmap(u"src/main/TrainModel/MTA_Logo.png"))
        self.mtaLogo.setScaledContents(True)

        # Create a QLabel for the first rectangle
        self.rectangle_label = QLabel(self.central_widget)
        self.rectangle_label.setGeometry(QRect(50, 170, 590, 500))
        self.rectangle_label.setStyleSheet("margin: 10px; padding: 0px;")

        # Create a container widget for the blue and white backgrounds
        self.background_widget = QWidget(self.rectangle_label)
        self.background_widget.setGeometry(QRect(0, 0, 590, 50))
        self.background_widget.setStyleSheet(
            "background-color: #007BFF; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the blue and white background widget
        self.background_layout = QVBoxLayout(self.background_widget)
        self.background_layout.setContentsMargins(0, 0, 0, 0)
        self.background_layout.setSpacing(0)

        # Create a QLabel for the white background below the blue
        self.white_background_label = QLabel(self.central_widget)
        self.white_background_label.setGeometry(QRect(50, 210, 590, 430))
        self.white_background_label.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the blue header
        self.white_background_layout = QVBoxLayout(self.white_background_label)
        self.white_background_layout.setContentsMargins(0, 0, 0, 0)
        self.white_background_layout.setSpacing(10)

        # Create QLabel widgets for the list of words
        word_list_1 = ["Passenger Emergency Brake:", "Temperature:", "Power:", "Commanded Speed:", "Setpoint Command:",
                       "Announcements:", "Internal Lights:", "Headlights:", "Left Door:", "Right Door:",
                       "Advertisements:"]

        # Create and add QLineEdit widgets for the first word list
        self.value_inputs = {}
        for word_placeholder in word_list_1:
            word_label = QLabel(word_placeholder, self.white_background_label)
            word_label.setStyleSheet("color: #000000; background-color: transparent; border: none;")
            word_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            word_label.setContentsMargins(10, 5, 10, 5)
            word_label.setFont(QFont("Arial", 10))

            value_input = QLineEdit(self.white_background_label)
            value_input.setStyleSheet("background-color: #FFFFFF; border: 0.5px solid #000000;")
            value_input.setContentsMargins(15, 15, 15, 15)

            word_layout = QHBoxLayout()
            word_layout.addWidget(word_label, alignment=Qt.AlignLeft)
            word_layout.addWidget(value_input, alignment=Qt.AlignLeft)

            self.white_background_layout.addLayout(word_layout)

            self.value_inputs[word_placeholder] = value_input

        self.white_background_layout.addStretch(1)

        # Create Apply and Reset buttons
        self.apply_button = QPushButton("Apply", self.central_widget)
        self.apply_button.setGeometry(1100, 640, 80, 30)
        self.apply_button.clicked.connect(self.apply_values)
        self.apply_button.setEnabled(True)

        self.reset_button = QPushButton("Reset", self.central_widget)
        self.reset_button.setGeometry(1190, 640, 80, 30)
        self.reset_button.clicked.connect(self.reset_values)
        self.reset_button.setEnabled(True)

        # Create the title label
        self.title_label = QLabel("Inputs:", self.rectangle_label)
        self.font = QFont()
        self.font.setPointSize(16)
        self.font.setBold(True)
        self.title_label.setFont(self.font)
        self.title_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        self.title_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.title_label.setGeometry(QRect(0, 0, self.background_widget.width(), self.background_widget.height()))

        # Create the line separator
        self.line_separator = QFrame(self.rectangle_label)
        self.line_separator.setGeometry(QRect(10, 40, 570, 2))
        self.line_separator.setFrameShape(QFrame.HLine)
        self.line_separator.setFrameShadow(QFrame.Sunken)
        self.line_separator.setStyleSheet("background-color: #000000")

        # Create a QLabel for the second rectangle
        self.rectangle_label_2 = QLabel(self.central_widget)
        self.rectangle_label_2.setGeometry(QRect(640, 170, 590, 500))
        self.rectangle_label_2.setStyleSheet("margin: 10px; padding: 0px;")

        # Create a container widget for the red and white backgrounds
        self.background_widget_2 = QWidget(self.rectangle_label_2)
        self.background_widget_2.setGeometry(QRect(0, 0, 590, 50))
        self.background_widget_2.setStyleSheet(
            "background-color: #FF0000; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the red and white background widget
        self.white_background_layout_2 = QVBoxLayout(self.background_widget_2)
        self.white_background_layout_2.setContentsMargins(0, 0, 0, 0)
        self.white_background_layout_2.setSpacing(0)

        # Create a QLabel for the white background below the red
        self.white_background_label_2 = QLabel(self.central_widget)
        self.white_background_label_2.setGeometry(QRect(640, 210, 590, 430))
        self.white_background_label_2.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the red header
        self.white_background_layout_2 = QVBoxLayout(self.white_background_label_2)
        self.white_background_layout_2.setContentsMargins(0, 0, 0, 0)
        self.white_background_layout_2.setSpacing(5)

        # Create QLabel widgets for the list of words
        self.word_list_2 = ["Speed Limit:", "Authority:", "Commanded Speed:", "Current Speed:", "Temperature:",
                            "Passengers Currently:", "Max Passengers:", "Next Station:", "Previous Station:",
                            "Engine Failure:", "Signal Pickup Failure:", "Brake Failure:", "Power:",
                            "Passenger Emergency Brake:"]

        # Defines a dictionary with actual values for second set of words
        self.values_2 = {
            "Speed Limit:": "40 mph",
            "Authority:": "6 Blocks",
            "Commanded Speed:": "37 mph",
            "Current Speed:": "35 mph",
            "Temperature:": "78 ℉",
            "Passengers Currently:": "58",
            "Max Passengers:": "72",
            "Next Station:": "Block 7",
            "Previous Station:": "Block 3",
            "Engine Failure:": True,
            "Signal Pickup Failure:": False,
            "Brake Failure:": True,
            "Power:": "83 kW",
            "Passenger Emergency Brake:": "On"
        }

        # Initialize the list at the beginning of my method
        self.word_labels = []

        for word_placeholder in self.word_list_2:
            value = self.values_2.get(word_placeholder, '')
            label_text = f"{word_placeholder} {value}"
            word_label = QLabel(label_text, self.white_background_label_2)
            word_label.setStyleSheet("color: #000000; background-color: transparent; border: none;")
            word_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            word_label.setContentsMargins(10, 5, 10, 5)
            word_label.setFont(QFont("Arial", 10))
            self.white_background_layout_2.addWidget(word_label, alignment=Qt.AlignTop)
            self.word_labels.append(word_label)

        # Create the title label
        self.title_label_2 = QLabel("Outputs:", self.rectangle_label_2)
        self.font = QFont()
        self.font.setPointSize(16)
        self.font.setBold(True)
        self.title_label_2.setFont(self.font)
        self.title_label_2.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        self.title_label_2.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.title_label_2.setGeometry(QRect(0, 0, self.background_widget.width(), self.background_widget.height()))

        # Create the line separator
        self.line_separator_2 = QFrame(self.rectangle_label_2)
        self.line_separator_2 = QFrame(self.rectangle_label_2)
        self.line_separator_2.setGeometry(QRect(10, 40, 570, 2))
        self.line_separator_2.setFrameShape(QFrame.HLine)
        self.line_separator_2.setFrameShadow(QFrame.Sunken)
        self.line_separator_2.setStyleSheet("background-color: #000000")

    def apply_values(self):
        values_wordlist_1 = {}

        # Iterate through the input text boxes and update values_wordlist_1
        for word_placeholder, value_input in self.value_inputs.items():
            input_value = value_input.text()
            if input_value:
                try:
                    # Try to convert the input to an integer
                    input_value = int(input_value)
                except ValueError:
                    pass  # If it's not a valid integer, keep it as a string
                values_wordlist_1[word_placeholder] = input_value

        # Update the corresponding output values based on the mappings
        for word_placeholder, output_key in self.mapping.items():
            if word_placeholder in values_wordlist_1:
                self.values_2[output_key] = values_wordlist_1[word_placeholder]
                # Update the corresponding text box in the second set
                self.update_wordlist2_textbox(output_key, values_wordlist_1[word_placeholder])

        return values_wordlist_1

    def reset_values(self):
        default_values_wordlist_2 = {
            "Speed Limit": "45 mph",
            "Authority": "5 Blocks",
            "Commanded Speed": "35 mph",
            "Current Speed": "32 mph",
            "Temperature": "75 ℉",
            "Passengers Currently": "60",
            "Max Passengers": "74",
            "Next Station": "Block 9",
            "Previous Station": "Block 5",
            "Engine Failure": False,
            "Signal Pickup Failure": True,
            "Brake Failure": False,
            "Power": "80 kW",
            "Passenger Emergency Brake": "Off"
        }

        for i, (word_placeholder, value) in enumerate(zip(self.word_list_2, default_values_wordlist_2.values())):
            label_text = f"{word_placeholder} {value}" if word_placeholder else value
            self.word_labels[i].setText(label_text)

    def update_wordlist2_values(self):
        values_wordlist_1 = self.apply_values()

        for i, word_placeholder in enumerate(self.word_list_2):
            if word_placeholder in self.values_2:
                label = self.values_2[word_placeholder]

                # Check if there is a corresponding label in word list 1
                corresponding_label = self.get_corresponding_label(word_placeholder)

                if corresponding_label:
                    # Get the value from word list 1 and format the label
                    value = values_wordlist_1.get(corresponding_label, "")
                    label = f"{word_placeholder} {value}"

                self.word_labels[i].setText(label)

    def get_corresponding_label(self, label_wordlist2):
        # Define a mapping between word list 2 labels and their corresponding word list 1 labels
        label_mapping = {
            "Passenger Emergency Brake:": "Passenger Emergency Brake"
        }

        # Get the corresponding label from the mapping
        return label_mapping.get(label_wordlist2, "")

    def update_clock_label(self):
        time_text = self.clock.elapsed_time.toString("HH:mm:ss")
        self.clock_label.setText(time_text)

    def update_current_speed(self):
        if "Commanded Speed:" in self.values_2:
            commanded_speed = self.values_2["Commanded Speed:", 0]
            if self.current_speed < commanded_speed:
                acceleration = 0.5
                change = acceleration / 10
                self.current_speed = min(commanded_speed, self.current_speed + change)
            elif self.current_speed > commanded_speed:
                change = 0.1
                self.current_speed = max(commanded_speed, self.current_speed - change)

            # Update the current speed label
            self.current_speed_label.setText(f"Current Speed: {self.current_speed}")


class MurphyTestWindow(QMainWindow):
    def __init__(self, clock):
        super().__init__()
        self.setWindowTitle("Murphy Test")
        self.setFixedSize(1280, 720)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.clock = clock

        # Create a label for the clock in the main window
        self.font = QFont()
        self.font.setPointSize(20)
        self.clock_label = QLabel(self.central_widget)
        self.clock_label.setObjectName(u"clock_label")
        self.clock_label.setFont(self.font)
        self.clock_label.setAlignment(Qt.AlignRight | Qt.AlignTop)

        # Connect the clock's timeUpdated signal to the update_clock_label method
        self.clock.timeUpdated.connect(self.update_clock_label)

        # Start a timer to update the clock label periodically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock_label)
        self.timer.start(100)

        # Add the clock label to the central widget
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.clock_label)
        self.layout.addStretch()

        # Title Left Line
        self.LeftLine = QFrame(self.central_widget)
        self.LeftLine.setObjectName(u"TitleLeftLine")
        self.LeftLine.setGeometry(QRect(0, 138, self.width() // 2, 3))
        self.LeftLine.setMaximumSize(QSize(720, 1280))
        self.LeftLine.setFrameShape(QFrame.HLine)
        self.LeftLine.setFrameShadow(QFrame.Sunken)

        # Title Right Line
        self.RightLine = QFrame(self.central_widget)
        self.RightLine.setObjectName(u"TitleRightLine")
        self.RightLine.setGeometry(QRect(self.width() // 2, 138, self.width() // 2, 3))
        self.RightLine.setMaximumSize(QSize(720, 1280))
        self.RightLine.setFrameShape(QFrame.HLine)
        self.RightLine.setFrameShadow(QFrame.Sunken)

        # Title
        self.Title = QLabel("Murphy Test", self.central_widget)
        self.Title.setObjectName(u"Title")
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(32)
        self.Title.setFont(font)
        self.Title.setText(QCoreApplication.translate("TrainTest", u"Murphy Test", None))
        title_width = self.Title.sizeHint().width()
        title_height = self.Title.sizeHint().height()
        title_x = self.width() // 2 - title_width // 2
        title_y = (138 + 0) // 2 - title_height // 2
        self.Title.setGeometry(QRect(title_x, title_y, title_width, title_height))

        # MTA Logo
        self.mtaLogo = QLabel(self.central_widget)
        self.mtaLogo.setObjectName(u"mtaLogo")
        self.mtaLogo.setGeometry(QRect(0, 0, 128, 128))
        self.mtaLogo.setMaximumSize(QSize(1280, 720))
        self.mtaLogo.setPixmap(QPixmap(u"src/main/TrainModel/MTA_Logo.png"))
        self.mtaLogo.setScaledContents(True)

        # Create a QLabel for the first rectangle
        self.rectangle_label = QLabel(self.central_widget)
        self.rectangle_label.setGeometry(QRect(50, 170, 590, 500))
        self.rectangle_label.setStyleSheet("margin: 10px; padding: 0px;")

        # Create a container widget for the blue and white backgrounds
        self.background_widget = QWidget(self.rectangle_label)
        self.background_widget.setGeometry(QRect(0, 0, 590, 50))
        self.background_widget.setStyleSheet(
            "background-color: #007BFF; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the blue and white background widget
        self.background_layout = QVBoxLayout(self.background_widget)
        self.background_layout.setContentsMargins(0, 0, 0, 0)
        self.background_layout.setSpacing(0)

        # Create a QLabel for the white background below the blue
        self.white_background_label = QLabel(self.central_widget)
        self.white_background_label.setGeometry(QRect(50, 210, 590, 430))
        self.white_background_label.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the blue header
        self.white_background_layout = QVBoxLayout(self.white_background_label)
        self.white_background_layout.setContentsMargins(0, 0, 0, 0)
        self.white_background_layout.setSpacing(10)

        # Create QLabel widgets for the list of words
        word_list_1 = ["Engine Failure:", "Signal Pickup Failure:", "Brake Failure:"]

        values_1 = {
            "engine_failure": True,
            "signal_pickup_failure": False,
            "brake_failure": True
        }

        # Create a vertical layout to place each pair of label and toggle switch
        vertical_layout = QVBoxLayout()

        for word_placeholder in word_list_1:
            # Create a widget that will hold the label and toggle switch vertically
            widget = QWidget()
            widget.setStyleSheet("background-color: transparent; border: none;")
            status_label = QLabel(word_placeholder, widget)
            status_label.setStyleSheet("background: transparent; border: none;")  # Remove background and border
            status_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            status_label.setFont(QFont("Arial", 10))

            # Check if the word_placeholder is in the values_2 dictionary and is a boolean value
            if word_placeholder.lower().replace(":", "").replace(" ", "_") in values_1 and isinstance(
                    values_1[word_placeholder.lower().replace(":", "").replace(" ", "_")], bool):
                # Create a custom toggle switch for the value
                toggle_switch = AnimatedToggle(checked_color="red")  # You can also use 'Toggle' for a non-animated version
                toggle_switch.setChecked(values_1[word_placeholder.lower().replace(":", "").replace(" ", "_")])
                toggle_switch.setStyleSheet("background: transparent; border: none;")  # Remove background and border
                toggle_switch.setFixedSize(60, 30)  # Adjust the size as needed
                toggle_switch.setContentsMargins(5, 0, 5, 0)  # Adjust margins to remove spacing

                # Set the layout for the widget
                layout = QHBoxLayout()
                layout.addWidget(status_label)
                layout.addWidget(toggle_switch)
                layout.setAlignment(Qt.AlignLeft)

                widget.setLayout(layout)
            else:
                # For other options, use a QLabel to display the value
                value = "On" if values_1.get(word_placeholder.lower().replace(":", "").replace(" ", "_"),
                                             False) else "Off"
                value_label = QLabel(value, widget)
                value_label.setStyleSheet("background: transparent; border: none;")
                value_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                value_label.setFont(QFont("Arial", 10))

                # Set the layout for the widget
                layout = QHBoxLayout()
                layout.addWidget(status_label)
                layout.addWidget(value_label)

                widget.setLayout(layout)

            # Add the widget to the vertical layout
            vertical_layout.addWidget(widget)

        # Add the vertical layout to your main layout
        self.white_background_layout.addLayout(vertical_layout)

        # Create Apply and Reset buttons
        self.apply_button = QPushButton("Apply", self.central_widget)
        self.apply_button.setGeometry(1100, 640, 80, 30)
        self.apply_button.clicked.connect(self.apply_values)
        self.apply_button.setEnabled(True)

        self.reset_button = QPushButton("Reset", self.central_widget)
        self.reset_button.setGeometry(1190, 640, 80, 30)
        self.reset_button.clicked.connect(self.reset_values)
        self.reset_button.setEnabled(True)

        # Create the title label
        self.title_label = QLabel("Inputs:", self.rectangle_label)
        self.font = QFont()
        self.font.setPointSize(16)
        self.font.setBold(True)
        self.title_label.setFont(self.font)
        self.title_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        self.title_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.title_label.setGeometry(QRect(0, 0, self.background_widget.width(), self.background_widget.height()))

        # Create the line separator
        self.line_separator = QFrame(self.rectangle_label)
        self.line_separator.setGeometry(QRect(10, 40, 570, 2))
        self.line_separator.setFrameShape(QFrame.HLine)
        self.line_separator.setFrameShadow(QFrame.Sunken)
        self.line_separator.setStyleSheet("background-color: #000000")

        # Create a QLabel for the second rectangle
        self.rectangle_label_2 = QLabel(self.central_widget)
        self.rectangle_label_2.setGeometry(QRect(640, 170, 590, 500))
        self.rectangle_label_2.setStyleSheet("margin: 10px; padding: 0px;")

        # Create a container widget for the red and white backgrounds
        self.background_widget_2 = QWidget(self.rectangle_label_2)
        self.background_widget_2.setGeometry(QRect(0, 0, 590, 50))
        self.background_widget_2.setStyleSheet(
            "background-color: #FF0000; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the red and white background widget
        self.white_background_layout_2 = QVBoxLayout(self.background_widget_2)
        self.white_background_layout_2.setContentsMargins(0, 0, 0, 0)
        self.white_background_layout_2.setSpacing(0)

        # Create a QLabel for the white background below the red
        self.white_background_label_2 = QLabel(self.central_widget)
        self.white_background_label_2.setGeometry(QRect(640, 210, 590, 430))
        self.white_background_label_2.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the red header
        self.white_background_layout_2 = QVBoxLayout(self.white_background_label_2)
        self.white_background_layout_2.setContentsMargins(0, 0, 0, 0)
        self.white_background_layout_2.setSpacing(5)

        # Create QLabel widgets for the list of words
        self.word_list_2 = ["Speed Limit:", "Authority:", "Commanded Speed:", "Current Speed:", "Temperature:",
                            "Passengers Currently:", "Max Passengers:", "Next Station:", "Previous Station:",
                            "Engine Failure:", "Signal Pickup Failure:", "Brake Failure:", "Power:",
                            "Passenger Emergency Brake:"]

        # Defines a dictionary with actual values for second set of words
        self.values_2 = {
            "Speed Limit:": "40 mph",
            "Authority:": "6 Blocks",
            "Commanded Speed:": "37 mph",
            "Current Speed:": "35 mph",
            "Temperature:": "78 ℉",
            "Passengers Currently:": "58",
            "Max Passengers:": "72",
            "Next Station:": "Block 7",
            "Previous Station:": "Block 3",
            "Engine Failure:": True,
            "Signal Pickup Failure:": False,
            "Brake Failure:": True,
            "Power:": "83 kW",
            "Passenger Emergency Brake:": "On"
        }

        # Initialize the list at the beginning of my method
        self.word_labels = []

        for word_placeholder in self.word_list_2:
            value = self.values_2.get(word_placeholder, '')
            label_text = f"{word_placeholder} {value}"
            word_label = QLabel(label_text, self.white_background_label_2)
            word_label.setStyleSheet("color: #000000; background-color: transparent; border: none;")
            word_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            word_label.setContentsMargins(10, 5, 10, 5)
            word_label.setFont(QFont("Arial", 10))
            self.white_background_layout_2.addWidget(word_label, alignment=Qt.AlignTop)
            self.word_labels.append(word_label)

        # Create the title label
        self.title_label_2 = QLabel("Outputs:", self.rectangle_label_2)
        self.font = QFont()
        self.font.setPointSize(16)
        self.font.setBold(True)
        self.title_label_2.setFont(self.font)
        self.title_label_2.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        self.title_label_2.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.title_label_2.setGeometry(QRect(0, 0, self.background_widget.width(), self.background_widget.height()))

        # Create the line separator
        self.line_separator_2 = QFrame(self.rectangle_label_2)
        self.line_separator_2 = QFrame(self.rectangle_label_2)
        self.line_separator_2.setGeometry(QRect(10, 40, 570, 2))
        self.line_separator_2.setFrameShape(QFrame.HLine)
        self.line_separator_2.setFrameShadow(QFrame.Sunken)
        self.line_separator_2.setStyleSheet("background-color: #000000")

    def apply_values(self):
        values_wordlist_1 = {}

        # Iterate through the input text boxes and update values_wordlist_1
        for word_placeholder, value_input in self.value_inputs.items():
            input_value = value_input.text()
            if input_value:
                try:
                    # Try to convert the input to an integer
                    input_value = int(input_value)
                except ValueError:
                    pass  # If it's not a valid integer, keep it as a string
                values_wordlist_1[word_placeholder] = input_value

        # Update the corresponding output values based on the mappings
        for word_placeholder, output_key in self.mapping.items():
            if word_placeholder in values_wordlist_1:
                self.values_2[output_key] = values_wordlist_1[word_placeholder]
                # Update the corresponding text box in the second set
                self.update_wordlist2_textbox(output_key, values_wordlist_1[word_placeholder])

        return values_wordlist_1

    def reset_values(self):
        default_values_wordlist_2 = {
            "Speed Limit": "45 mph",
            "Authority": "5 Blocks",
            "Commanded Speed": "35 mph",
            "Current Speed": "32 mph",
            "Temperature": "75 ℉",
            "Passengers Currently": "60",
            "Max Passengers": "74",
            "Next Station": "Block 9",
            "Previous Station": "Block 5",
            "Engine Failure": False,
            "Signal Pickup Failure": True,
            "Brake Failure": False,
            "Power": "80 kW",
            "Passenger Emergency Brake": "Off"
        }

        for i, (word_placeholder, value) in enumerate(zip(self.word_list_2, default_values_wordlist_2.values())):
            label_text = f"{word_placeholder} {value}" if word_placeholder else value
            self.word_labels[i].setText(label_text)
    
    def update_wordlist2_values(self, reset=False):
        values_wordlist_1 = self.apply_values()

        for i, word_placeholder in enumerate(self.word_list_2):
            if word_placeholder in self.values_2:
                label = self.values_2[word_placeholder]

                # Check if there is a corresponding label in word list 1
                corresponding_label = self.get_corresponding_label(word_placeholder)

                if corresponding_label:
                    # Get the value from word list 1 and format the label
                    value = values_wordlist_1.get(corresponding_label, "")
                    label = f"{word_placeholder} {value}"

                self.word_labels[i].setText(label)

    def get_corresponding_label(self, label_wordlist2):
        # Define a mapping between word list 2 labels and their corresponding word list 1 labels
        label_mapping = {
            "Engine Failure:": "Engine Failure:",
            "Signal Pickup Failure:": "Signal Pickup Failure",
            "Brake Failure:": "Brake Failure"
        }

        # Get the corresponding label from the mapping
        return label_mapping.get(label_wordlist2, "")

    def update_clock_label(self):
        time_text = self.clock.elapsed_time.toString("HH:mm:ss")
        self.clock_label.setText(time_text)


# Output to track model module
class OutputTrackModel():
        train = SharedData()
    
        currentPassengers = train.get_value("Train 1", "passenger_status", 1)
        # TrackModelSignals.sendCurrentPassengers(currentPassengers)

        maxPassengers = train.get_value("Train 1", "passenger_status", 2)
        # TrackModelSignals.sendMaxPassengers(maxPassengers)

# Output to train controller module
class OutputTrainController():
    train = SharedData()

    speedLimit = train.get_value("Train 1", "vehicle_status", 1)
    # TrainControllerSignals.sendSpeedLimit(speedLimit)

    currentSpeed = train.get_value("Train 1", "vehicle_status", 2)
    # TrainControllerSignals.sendCurrentSpeed(currentSpeed)

    engineFailure = train.get_value("Train 1", "failure_status", 1)
    # TrainControllerSignals.sendEngineFailure(engineFailure)

    signalPickupFailure = train.get_value("Train 1", "failure_status", 2)
    # TrainControllerSignals.sendSignalPickupFailure(signalPickupFailure)

    brakeFailure = train.get_value("Train 1", "failure_status", 3)
    # TrainControllerSignals.sendBrakeFailure(brakeFailure)

    left_door = train.get_value("Train 1", "passenger_status", 3)
    # TrainControllerSignals.sendLeftDoor(left_door)

    right_door = train.get_value("Train 1", "passenger_status", 4)
    # TrainControllerSignals.sendRightDoor(right_door)

    next_station = train.get_value("Train 1", "navigation_status", 5)
    # TrainControllerSignals.sendNextStation(next_station)
     
    prev_station = train.get_value("Train 1", "navigation_status", 6)
    # TrainControllerSignals.sendPrevStation(prev_station)

    tunnel = train.get_value("Train 1", "navigation_status", 7)
    # TrainControllerSignals.sendEnterTunnel(tunnel)

    temperature = train.get_value("Train 1", "passenger_status", 7)
    # TrainControllerSignals.sendTemperature(temperature)

    def updateCurrentSpeed(new_speed):
        OutputTrainController.currentSpeed = new_speed

class InputsTrackModel():
    def get_Track_Model_Inputs():
        Track_Model_Inputs = {
            "Speed Limit:": 35,
            "Authority:": 6,
            "Beacon": 5,
            "Commanded Speed:": 30,
            "Passengers Entering": 15,
            "Block Length": 10,
            "Block Grade": 5,
            "Tunnel": True
        }
        Beacon = {
            "Station": {
                "Name": "Steel Plaza",
                "Distance": 5,
                "Side": "Left"
            },
            "Tunnel": {
                "Distance": 10,
                "EndDistance": 15
            },
            "Switch": {
                "Distance": 20
            }
        }
        return Track_Model_Inputs, Beacon


class InputsTrainController():
    def get_Train_Controller_Inputs():
        Train_Control_Inputs = {
            "Temperature": 75,
            "Power": 80,
            "Setpoint_speed": 30,
            "Announcements": 2,
            "Headlights": True,
            "Internal_lights": True,
            "Left_door": False,
            "Right_door": False,
            "Advertisements": "Buy this",
            "Brakes": False,
            "Emergency_brakes": False
        }
        return Train_Control_Inputs


class Calculations():
    # Calculates current speed of train in automatic mode
    def Current_speed_auto():
        train = SharedData()
        acceleration = 5.0
        deceleration = -5.0
        current_speed = train.get_value("Train 1", "vehicle_status", 2)
        speed_limit = train.get_value("Train 1", "vehicle_status", 1)
        commanded_speed = train.get_value("Train 1", "vehicle_status", 4)
        power = train.get_value("Train 1", "vehicle_status", 8)
        passengers_entering = InputsTrackModel.get_Track_Model_Inputs["Passengers Entering"]
        block_grade = train.get_value("Train 1", "navigation_status", 4)
        average_passenger_weight = 150
        total_train_weight = 40.9 * 2000

        signal_pickup_failure = Calculations.Failures()

        # Calculate the effect of passengers entering on the speed
        passenger_weight = passengers_entering * average_passenger_weight
        speed_due_to_passengers = passenger_weight / total_train_weight

        # Calculate the effect of block grade on the speed (you need to define grade_effect_on_speed)
        grade_effect_on_speed = 0.1
        speed_due_to_block = block_grade * grade_effect_on_speed

        # Adjust current speed based on acceleration and deceleration
        if commanded_speed > current_speed:
            current_speed += acceleration
            if current_speed > commanded_speed:
                current_speed = commanded_speed
        elif commanded_speed < current_speed:
            current_speed += deceleration
            if current_speed < commanded_speed:
                current_speed = commanded_speed

        # Ensure current speed is within the speed limit
        if current_speed > speed_limit:
            current_speed = speed_limit

        if signal_pickup_failure == True:
            # Set power to 0 and activate the emergency brake
            train.set_value("Train 1", "vehicle_status", 8, 0)
            train.set_value("Train 1", "failure_status", 4, True)

        # Update speed in the train object
        train.set_value("Train 1", "vehicle_status", 2, current_speed)

        # Update the current speed in OuputTrainController
        OutputTrainController.updateCurrentSpeed(current_speed)
        
        return current_speed

    # Calculates current speed of train in manual mode
    def Current_speed_manual():
        # Initialize train object and get current speed
        train = SharedData()
        curr_speed = train.get_value("Train 1", "vehicle_status", 1)
        power = train.get_value("Train 1", "vehicle_status", 8)
        emergencyBrake = train.get_value("Train 1", "failure_status", 4)
        brakes = train.get_value("Train 1", "vehicle_status", 9)
        speedLimit = train.get_value("Train 1", "vehicle_status", 1)

        # Define limits for acceleration and deceleration
        accel_limit = 1.2
        decel_limit = 1.5
        emg_brake_val = 2.7
        
        # Limit power to 120
        power = min(power, 120)
        
        # Calculate speed difference using speedLimit
        speed_diff = speedLimit - curr_speed 
        
        # Apply acceleration if speed difference is positive
        if speed_diff > 0:
            accel = min(accel_limit, speed_diff)
            curr_speed += accel
        
        # Apply deceleration if speed difference is negative
        elif speed_diff < 0:
            decel = min(decel_limit, -speed_diff)
            curr_speed -= decel
        
        # Apply brakes if brakes flag is True
        if brakes:
            decel = min(decel_limit, -speed_diff)
            curr_speed -= decel
        
        # Apply an emergency brake if the emergencyBrake flag is True
        if emergencyBrake:
            curr_speed -= emg_brake_val
        
        # Update speed in the train object
        train.set_value("Train 1", "vehicle_status", 2, curr_speed)

        # Update the current speed in OuputTrainController
        OutputTrainController.updateCurrentSpeed(curr_speed)
        
        return curr_speed    

    def beacon_Info():
        train = SharedData()
        track_inputs = InputsTrackModel.get_Track_Model_Inputs()
        
        door = track_inputs("Beacon", "Station", "Side")        
        if (door == "Left"):
            train.set_value("Train 1", "passenger_status", 3, door)
        else:
            train.set_value("Train 1", "passenger_status", 4, door)

        station = track_inputs("Beacon", "Station", "Name")
        prev_station = station - 1
        
        train.set_value("Train 1", "navigation_status", 5, station)
        train.set_value("Train 1", "navigation_status", 6, prev_station)
        

        return track_inputs
    
    def Tunnel():
        train = SharedData()
        tunnel = InputsTrackModel.get_Track_Model_Inputs("Tunnel")
        train.set_value("Train 1", "navigation_status", 7, tunnel)

        if tunnel == True:
            OutputTrainController.tunnel = True
        else:
            OutputTrainController.tunnel = False

        return tunnel
        
    # Checks for failures and 
    def Failures():
        train = SharedData()

        engine_failure = train.get_value("Train 1", "failure_status", 1)
        signal_pickup_failure = train.get_value("Train 1", "failure_status", 2)
        brake_failure = train.get_value("Train 1", "failure_status", 3)

        if engine_failure == True or brake_failure == True:
            OutputTrainController.engineFailure = True
            OutputTrainController.signalPickupFailure = True
            OutputTrainController.brakeFailure = True
            
        return signal_pickup_failure

    def Temperature():
        train = SharedData()
        temperature = InputsTrainController()["Train_Control_Inputs"]["Temperature"]

        current_temp = train.get_value("Train 1", "vehicle_status", 7)

        if current_temp < temperature:
            current_temp += 1
        if temperature > current_temp:
            current_temp -= 1

        train.set_value("Train 1", "vehicle_status", 7, current_temp)

        return temperature

    # Calculate the current number of passengers from the track model
    def currentPassengers():
        # Create an instance of the SharedData class
        train = SharedData()

        # Get the current number of passengers on the train
        currentPassengers = train.get_value("Train 1", "passenger_status", 1)
        
        # Get the maximum number of passengers the train can carry
        maxPassengers = train.get_value("Train 1", "passenger_status", 2)
    
        # Get the number of pasengers entering from the track model
        passengersEntering = InputsTrackModel()["Passengers_Entering"]

        # If the current number of passengers is less than the maximum, add the 
        # number of passengers the train model is expected to carry
        if currentPassengers < maxPassengers:
            currentPassengers += passengersEntering

        # Update the current number of passengers on the train
        train.set_value("Train 1", "passenger_status", 1, currentPassengers)

        # Ouput to the trian controller
        OutputTrackModel.currentPassengers = currentPassengers
        
        # Return the current number of passengers
        return currentPassengers
    
    def Occupancy():
        total_distance = 100
        block_distance = InputsTrackModel()["Block_Length"]

        if total_distance == block_distance:
            OutputTrackModel.occupancy = True

        return total_distance


def main():
    app = QApplication(sys.argv)
    ui = TrainModel()
    ui.show_gui()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
