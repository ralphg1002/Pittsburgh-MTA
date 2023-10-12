# importing libraries
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import types

class MainWindow(QMainWindow):
    # engineer input variables
    uiKP = 0
    uiKI = 0

    # driver input variables
    uiMode = 1
    # uiEmergencyBrake = 0
    # uiServiceBrake = 0
    # uiSetpointCommand = 0
    # uiAnnouncement = ''
    # uiLeftDoor = 0
    # uiRightDoor = 0
    # uiExternalLights = 0
    # uiInternalLights = 0
    # uiSetpointTemp = 0
    # uiAdvertisement = 0
    uiTrainID = ''

    # train model input variables
    tmTrainID = ''
    tmSpeedLimit = 0
    tmAuthority = 0
    tmCurrentSpeed = 0
    tmCommandedSpeed = 0
    tmBeaconData = ''
    tmCurrentTemp = 0
    tmEmergencyBrake = 0
    tmSignalFail = 0
    tmEngineFail = 0
    tmBrakeFail = 0

    # train controller output variables
    tcPowerCommand = 0
    tcEmergencyBrake = 0
    tcServiceBrake = 0
    tcSetpointCommand = 0
    tcAnnouncement = ''
    tcLeftDoor = 0
    tcRightDoor = 0
    tcExternalLights = 0
    tcInternalLights = 0
    tcSetpointTemp = 0
    tcAdvertisement = 0

    # misc. variables
    checkTrainID = False
    systemBaseSpeed = 1.0

    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle('Train Controller Module (SW)')

        # setting geometry
        self.setFixedWidth(1600)
        self.setFixedHeight(1100)
        self.move(1100, 500)

        """actual (well, temporary) home layout"""
        # home background
        self.homeBackground = QLabel(self)
        self.homeBackground.setGeometry(123, 64, 1368, 962)
        self.homeBackground.setStyleSheet('background-color: #9FC5F8; border: 5px solid black')

        # home title
        self.homeTitle = QLabel('Pittsburgh Metropolitan Transportation Authority', self)
        self.homeTitle.setGeometry(208, 116, 1197, 68)
        self.homeTitle.setFont(QFont('Calibri', 20))
        self.homeTitle.setAlignment(Qt.AlignCenter)
        self.homeTitle.setStyleSheet('background-color: #9FC5F8; color: black')

        # home cat
        self.homeCat = QLabel(self)
        self.pixmapCat = QtGui.QPixmap('homecat.png')
        self.homeCat.setPixmap(self.pixmapCat)
        self.homeCat.setGeometry(723, 283, 729, 200)
        self.homeCat.setAlignment(Qt.AlignCenter)
        self.homeCat.setStyleSheet('background-color: #9FC5F8')

        # train controller sw module button
        self.traincontrollerswButton = QPushButton('Train Controller\n(SW)', self)
        self.traincontrollerswButton.setGeometry(801, 529, 202, 129)
        self.traincontrollerswButton.setFont(QFont('Calibri', 10))
        self.traincontrollerswButton.setStyleSheet('QPushButton{background-color: white; color: black; border: 3px solid black}'
                                                   'QPushButton::pressed{background-color: #EEEEEE; color: black; border: 3px solid black}')
        self.traincontrollerswButton.clicked.connect(self.wireframe)

        # home logo
        self.homeLogo = QLabel(self)
        self.pixmapLogo = QtGui.QPixmap('MTA_NYC_logo.svg.png')
        self.pixmapLogo = self.pixmapLogo.scaled(563, 584)
        self.homeLogo.setPixmap(self.pixmapLogo)
        self.homeLogo.setGeometry(128, 229, 563, 584)
        self.homeLogo.setStyleSheet('background-color: #9FC5F8')

        self.actualHomeWidgets = [self.homeBackground,
                                  self.homeTitle,
                                  self.homeCat,
                                  self.traincontrollerswButton,
                                  self.homeLogo]

        self.show()

        """template layout"""
        # creating background
        self.background = QLabel(self)
        self.background.setGeometry(123, 64, 1368, 962)
        self.background.setStyleSheet('background-color: #2B78E4; border: 1px solid black')

        # creating header
        self.whiteRectangle1 = QLabel('', self)
        self.whiteRectangle1.setGeometry(129, 105, 1355, 113)
        self.whiteRectangle1.setStyleSheet('background-color: white')

        # logo
        self.logo = QLabel(self)
        self.pixmap = QtGui.QPixmap('MTA_NYC_logo.svg.png')
        self.pixmap = self.pixmap.scaled(88, 97)
        self.logo.setPixmap(self.pixmap)
        self.logo.setGeometry(132, 113, 88, 97)
        self.logo.setStyleSheet('background-color: white')

        # title
        self.title = QLabel('Train Controller Module (SW)', self)
        self.title.setGeometry(256, 134, 831, 64)
        self.title.setFont(QFont('Calibri', 24))
        self.title.setStyleSheet('background-color: white; color: #085394')

        # creating body
        self.whiteRectangle2 = QLabel('', self)
        self.whiteRectangle2.setGeometry(129, 274, 1355, 734)
        self.whiteRectangle2.setStyleSheet('background-color: white')

        self.blueVerticalLine1 = QLabel(self)
        self.blueVerticalLine1.setGeometry(336, 257, 5, 764)
        self.blueVerticalLine1.setStyleSheet('background-color: #2B78E4')

        """tabs layout"""
        # wireframe
        self.wireframeButton = QPushButton('Wireframe', self)
        self.wireframeButton.setGeometry(157, 297, 156, 40)
        self.wireframeButton.setFont(QFont('Calibri', 13))
        self.wireframeButton.setStyleSheet('QPushButton{background-color: white; color: #085394; border: 1px solid white}'
                                           'QPushButton::pressed{background-color: white; color: #9FC5F8; border: 1px solid white}')
        self.wireframeButton.clicked.connect(self.wireframe)

        # test bench
        self.testbenchButton = QPushButton('Test Bench', self)
        self.testbenchButton.setGeometry(151, 431, 171, 40)
        self.testbenchButton.setFont(QFont('Calibri', 13))
        self.testbenchButton.setStyleSheet('QPushButton{background-color: white; color: #085394; border: 1px solid white}'
                                           'QPushButton::pressed{background-color: white; color: #9FC5F8; border: 1px solid white}')
        self.testbenchButton.clicked.connect(self.testbench)

        # home
        self.homeButton = QPushButton('Home', self)
        self.homeButton.setGeometry(187, 949, 95, 40)
        self.homeButton.setFont(QFont('Calibri', 13))
        self.homeButton.setStyleSheet('QPushButton{background-color: white; color: #085394; border: 1px solid white}'
                                      'QPushButton::pressed{background-color: white; color: #9FC5F8; border: 1px solid white}')
        self.homeButton.clicked.connect(self.homepage)

        self.basicLayoutWidgets = [self.background,
                                   self.whiteRectangle1,
                                   self.logo,
                                   self.title,
                                   self.whiteRectangle2,
                                   self.blueVerticalLine1,
                                   self.wireframeButton,
                                   self.testbenchButton,
                                   self.homeButton]

        """homepage layout"""
        # list of homepage widgets

        # enter train ID
        self.enterTrainID = QLineEdit(self)
        self.enterTrainID.setPlaceholderText('Enter Train ID')
        self.enterTrainID.setGeometry(820, 316, 223, 61)
        self.enterTrainID.setFont(QFont('Calibri', 13))
        self.enterTrainID.setStyleSheet('background-color: #2B78E4; color: white')
        self.enterTrainID.returnPressed.connect(self.input_train_id)

        self.pixmapRightChevron = QtGui.QPixmap('chevron-right.svg')
        self.pixmapRightChevron = self.pixmapRightChevron.scaled(48, 48)

        self.rightChevron1 = QPushButton(self)
        self.rightChevron1.setIcon(QtGui.QIcon(self.pixmapRightChevron))
        self.rightChevron1.setGeometry(1064, 323, 48, 48)
        self.rightChevron1.setStyleSheet('QPushButton{background-color: white; color: #085394; border: 1px solid #085394; border-radius: 24px}'
                                         'QPushButton::pressed{background-color: #9FC5F8; color: #085394; border: 1px solid #085394; border-radius: 24px}')
        self.rightChevron1.clicked.connect(self.ui_wireframe)

        # filter block
        self.blueHorizontalBlock1 = QLabel(self)
        self.blueHorizontalBlock1.setGeometry(339, 415, 1145, 34)
        self.blueHorizontalBlock1.setStyleSheet('background-color: #085394')

        self.filterLabel = QLabel('or filter by', self)
        self.filterLabel.setGeometry(883, 421, 96, 21)
        self.filterLabel.setFont(QFont('Calibri', 7))
        self.filterLabel.setStyleSheet('background-color: #085394; color: white')

        # departure
        self.departure = QComboBox(self)
        self.departure.setGeometry(477, 475, 311, 49)
        self.departure.setFont(QFont('Calibri', 8))
        self.departure.setStyleSheet('background-color: #2B78E4; color: white')
        self.departure.addItem('Departure')
        self.departure.addItem('Morning (6:00am-11:59pm)')
        self.departure.addItem('Afternoon (12:00pm-5:59pm)')
        self.departure.addItem('Evening (6:00pm-11:59am)')
        self.departure.addItem('Night (12:00am-5:59am)')

        # station list
        stationList = ['Shadyside',
                       'Herron Ave',
                       'Swissville',
                       'Penn Station',
                       'Steel Plaza',
                       'First Ave',
                       'Station Square',
                       'South Hills',
                       'Pioneer',
                       'EdgeBrook',
                       'Station',
                       'Whited',
                       'South Bank',
                       'Central',
                       'Inglewood',
                       'Overbrook',
                       'Glenbury',
                       'Dormont',
                       'MT Lebanon',
                       'Poplar',
                       'Castle Shannon']

        # origin
        self.origin = QComboBox(self)
        self.origin.setGeometry(788, 475, 212, 49)
        self.origin.setFont(QFont('Calibri', 10))
        self.origin.setStyleSheet('background-color: #085394; color: white')
        self.origin.addItem('Origin')
        self.origin.addItems(stationList)
        self.origin.setEditable(True)
        self.origin.setInsertPolicy(QComboBox.NoInsert)
        self.origin.completer().setCompletionMode(QCompleter.PopupCompletion)

        # destination
        self.destination = QComboBox(self)
        self.destination.setGeometry(1000, 475, 212, 49)
        self.destination.setFont(QFont('Calibri', 10))
        self.destination.setStyleSheet('background-color: #2B78E4; color: white')
        self.destination.addItem('Destination')
        self.destination.addItems(stationList)
        self.destination.setEditable(True)
        self.destination.setInsertPolicy(QComboBox.NoInsert)
        self.destination.completer().setCompletionMode(QCompleter.PopupCompletion)

        # number
        self.number = QSpinBox(self)
        self.number.setRange(0, 225)
        self.number.setValue(0)
        self.number.setGeometry(1211, 475, 174, 49)
        self.number.setFont(QFont('Calibri', 10))
        self.number.setAlignment(Qt.AlignCenter)
        self.number.setStyleSheet('background-color: #085394; color: white')

        # autofill train ID
        self.autoTrainID = QLineEdit(self)
        self.autoTrainID.setPlaceholderText('# - - - - - - - -')
        self.autoTrainID.setGeometry(820, 862, 223, 61)
        self.autoTrainID.setFont(QFont('Calibri', 13))
        self.autoTrainID.setAlignment(Qt.AlignCenter)
        self.autoTrainID.setStyleSheet('background-color: #999999; color: white')
        self.autoTrainID.setReadOnly(True)

        self.rightChevron2 = QPushButton(self)
        self.rightChevron2.setIcon(QtGui.QIcon(self.pixmapRightChevron))
        self.rightChevron2.setGeometry(1064, 869, 48, 48)
        self.rightChevron2.setStyleSheet('QPushButton{background-color: white; color: #085394; border: 1px solid #085394; border-radius: 24px}'
                                         'QPushButton::pressed{background-color: #9FC5F8; color: #085394; border: 1px solid #085394; border-radius: 24px}')
        self.rightChevron2.clicked.connect(self.ui_wireframe)

        self.homepageWidgets = [self.enterTrainID,
                                self.rightChevron1,
                                self.blueHorizontalBlock1,
                                self.filterLabel,
                                self.departure,
                                self.origin,
                                self.destination,
                                self.number,
                                self.autoTrainID,
                                self.rightChevron2]

        """display layout"""
        # divider
        self.blueVerticalLine2 = QLabel(self)
        self.blueVerticalLine2.setGeometry(684, 261, 5, 764)
        self.blueVerticalLine2.setStyleSheet('background-color: #2B78E4')

        # display header
        self.blueHorizontalBlock2 = QLabel(self)
        self.blueHorizontalBlock2.setGeometry(689, 290, 795, 46)
        self.blueHorizontalBlock2.setStyleSheet('background-color: #085394')

        self.displayLabel = QLabel('DISPLAY', self)
        self.displayLabel.setGeometry(1029, 297, 114, 32)
        self.displayLabel.setFont(QFont('Calibri', 10))
        self.displayLabel.setStyleSheet('background-color: #085394; color: white')

        # change train
        self.changeTrainLabel = QPushButton('Change Train', self)
        self.changeTrainLabel.setGeometry(978, 824, 223, 54)
        self.changeTrainLabel.setFont(QFont('Calibri', 13))
        self.changeTrainLabel.setStyleSheet('QPushButton{background-color: #085394; color: white; border: 1px solid #085394}'
                                            'QPushButton::pressed{background-color: #9FC5F8; color: white; border: 1px solid #085394}')
        self.changeTrainLabel.clicked.connect(self.wireframe)

        # display elements
        self.greyRectangle = QLabel(self)
        self.greyRectangle.setGeometry(689, 346, 795, 377)
        self.greyRectangle.setStyleSheet('background-color: #CCCCCC')

        # system speed
        self.systemSpeedLabel = QLabel('System Speed', self)
        self.systemSpeedLabel.setGeometry(956, 681, 209, 40)
        self.systemSpeedLabel.setFont(QFont('Calibri', 13))
        self.systemSpeedLabel.setStyleSheet('background-color: #CCCCCC; color: #085394')

        self.systemSpeedVal = QLineEdit(self)
        self.systemSpeedVal.setPlaceholderText('1.0')
        self.systemSpeedVal.setGeometry(1177, 685, 39, 32)
        self.systemSpeedVal.setFont(QFont('Calibri', 9))
        self.systemSpeedVal.setStyleSheet('background-color: #CCCCCC; color: black')

        # system speed variation
        self.pixmapFastForward = QtGui.QPixmap('fast-forward.svg')
        self.pixmapFastForward = self.pixmapFastForward.scaled(24, 24)

        self.fastforward = QPushButton(self)
        self.fastforward.setIcon(QtGui.QIcon(self.pixmapFastForward))
        self.fastforward.setGeometry(1259, 689, 24, 24)
        self.fastforward.setStyleSheet('QPushButton{background-color: #CCCCCC}'
                                       'QPushButton::pressed{background-color: #CCCCCC; border: 1px solid #274E13}')
        self.fastforward.clicked.connect(self.systemSpeedUp)

        self.pixmapRewind = QtGui.QPixmap('rewind.svg')
        self.pixmapRewind = self.pixmapRewind.scaled(24, 24)

        self.rewind = QPushButton(self)
        self.rewind.setIcon(QtGui.QIcon(self.pixmapRewind))
        self.rewind.setGeometry(885, 689, 24, 24)
        self.rewind.setStyleSheet('QPushButton{background-color: #CCCCCC}'
                                  'QPushButton::pressed{background-color: #CCCCCC; border: 1px solid #274E13}')
        self.fastforward.clicked.connect(self.systemSlowDown)

        # black display blocks
        # current speed
        self.blackRectangle1 = QLabel(self)
        self.blackRectangle1.setGeometry(700, 429, 104, 115)
        self.blackRectangle1.setStyleSheet('background-color: black')

        self.speedLabel = QLabel('Speed', self)
        self.speedLabel.setGeometry(725, 465, 60, 26)
        self.speedLabel.setFont(QFont('Calibri', 7))
        self.speedLabel.setAlignment(Qt.AlignCenter)
        self.speedLabel.setStyleSheet('background-color: black; color: white')

        self.speedUnitLabel = QLabel('mph', self)
        self.speedUnitLabel.setGeometry(740, 490, 24, 20)
        self.speedUnitLabel.setFont(QFont('Calibri', 5))
        self.speedUnitLabel.setStyleSheet('background-color: black; color: white')

        self.currentSpeedVal = QLabel(self)
        self.currentSpeedVal.setText(str(self.tmCurrentSpeed))
        self.currentSpeedVal.setGeometry(738, 441, 30, 26)
        self.currentSpeedVal.setFont(QFont('Calibri', 7))
        self.currentSpeedVal.setAlignment(Qt.AlignCenter)
        self.currentSpeedVal.setStyleSheet('background-color: black; color: white')

        self.suggestedSpeedLabel = QLabel('Suggested:', self)
        self.suggestedSpeedLabel.setGeometry(710, 519, 62, 20)
        self.suggestedSpeedLabel.setFont(QFont('Calibri', 5))
        self.suggestedSpeedLabel.setStyleSheet('background-color: black; color: #9FC5F8')

        self.suggestedSpeedVal = QLabel(self)
        self.suggestedSpeedVal.setText(str(self.tmCommandedSpeed))
        self.suggestedSpeedVal.setGeometry(777, 519, 23, 20)
        self.suggestedSpeedVal.setFont(QFont('Calibri', 5))
        self.suggestedSpeedVal.setStyleSheet('background-color: black; color: #9FC5F8')

        # current power
        self.blackRectangle2 = QLabel(self)
        self.blackRectangle2.setGeometry(700, 547, 104, 115)
        self.blackRectangle2.setStyleSheet('background-color: black')

        self.powerLabel = QLabel('Power', self)
        self.powerLabel.setGeometry(725, 597, 60, 26)
        self.powerLabel.setFont(QFont('Calibri', 7))
        self.powerLabel.setAlignment(Qt.AlignCenter)
        self.powerLabel.setStyleSheet('background-color: black; color: white')

        self.powerUnitLabel = QLabel('Watts', self)
        self.powerUnitLabel.setGeometry(735, 622, 39, 20)
        self.powerUnitLabel.setFont(QFont('Calibri', 5))
        self.powerUnitLabel.setStyleSheet('background-color: black; color: white')

        self.currentPowerVal = QLabel(self)
        self.currentPowerVal.setText(str(self.tcPowerCommand))
        self.currentPowerVal.setGeometry(736, 570, 30, 26)
        self.currentPowerVal.setFont(QFont('Calibri', 7))
        self.currentPowerVal.setAlignment(Qt.AlignCenter)
        self.currentPowerVal.setStyleSheet('background-color: black; color: white')

        # other display items
        self.blackRectangle3 = QLabel(self)
        self.blackRectangle3.setGeometry(820, 348, 663, 328)
        self.blackRectangle3.setStyleSheet('background-color: black')

        # authority
        self.authorityLabel = QLabel('Authority', self)
        self.authorityLabel.setGeometry(850, 574, 75, 26)
        self.authorityLabel.setFont(QFont('Calibri', 7))
        self.authorityLabel.setAlignment(Qt.AlignCenter)
        self.authorityLabel.setStyleSheet('background-color: black; color: white')

        self.pixmapUpArrow = QtGui.QPixmap('up-arrow.png')
        self.pixmapUpArrow = self.pixmapUpArrow.scaled(32, 32)

        self.upArrow1 = QLabel(self)
        self.upArrow1.setPixmap(self.pixmapUpArrow)
        self.upArrow1.setGeometry(850, 611, 32, 32)
        self.upArrow1.setStyleSheet('background-color: black')

        self.authorityVal = QLabel(self)
        self.authorityVal.setText(str(self.tmAuthority))
        self.authorityVal.setGeometry(879, 607, 36, 27)
        self.authorityVal.setAlignment(Qt.AlignCenter)
        self.authorityVal.setFont(QFont('Calibri', 5))
        self.authorityVal.setStyleSheet('background-color: black; color: white')

        self.authorityUnitLabel = QLabel('mi', self)
        self.authorityUnitLabel.setGeometry(883, 627, 28, 27)
        self.authorityUnitLabel.setAlignment(Qt.AlignCenter)
        self.authorityUnitLabel.setFont(QFont('Calibri', 5))
        self.authorityUnitLabel.setStyleSheet('background-color: black; color: white')

        # warning block
        self.warningHeader = QLabel('WARNINGS', self)
        self.warningHeader.setGeometry(1202, 346, 281, 64)
        self.warningHeader.setFont(QFont('Calibri', 10))
        self.warningHeader.setAlignment(Qt.AlignCenter)
        self.warningHeader.setStyleSheet('background-color: #CF2A27; color: white; border: 1px solid #CF2A27')

        self.warningBody = QLabel(self)
        self.warningBody.setGeometry(1202, 410, 281, 265)
        self.warningBody.setStyleSheet('background-color: #EA9999; border: 1px solid #CF2A27')

        # signal pickup failure
        self.signalPickupFailureLabel = QLabel('Signal Pickup Failure', self)
        self.signalPickupFailureLabel.setGeometry(1218, 438, 180, 26)
        self.signalPickupFailureLabel.setFont(QFont('Calibri', 8))
        self.signalPickupFailureLabel.setStyleSheet('background-color: #EA9999; color: white')

        self.pixmapAlert = QtGui.QPixmap('bell-off.svg')
        self.pixmapAlert = self.pixmapAlert.scaled(26, 26)

        self.pixmapAlert2 = QtGui.QPixmap('bell.svg')
        self.pixmapAlert2 = self.pixmapAlert2.scaled(26, 26)

        self.failureIcon1 = QLabel(self)
        self.failureIcon1.setPixmap(self.pixmapAlert)
        self.failureIcon1.setGeometry(1434, 439, 28, 28)
        self.failureIcon1.setStyleSheet('background-color: #EA9999')

        # train engine failure
        self.trainEngineFailureLabel = QLabel('Train Engine Failure', self)
        self.trainEngineFailureLabel.setGeometry(1218, 524, 180, 26)
        self.trainEngineFailureLabel.setFont(QFont('Calibri', 8))
        self.trainEngineFailureLabel.setStyleSheet('background-color: #EA9999; color: white')

        self.failureIcon2 = QLabel(self)
        self.failureIcon2.setPixmap(self.pixmapAlert)
        self.failureIcon2.setGeometry(1434, 524, 28, 28)
        self.failureIcon2.setStyleSheet('background-color: #EA9999')

        # brake failure
        self.brakeFailureLabel = QLabel('Brake Failure', self)
        self.brakeFailureLabel.setGeometry(1218, 614, 180, 26)
        self.brakeFailureLabel.setFont(QFont('Calibri', 8))
        self.brakeFailureLabel.setStyleSheet('background-color: #EA9999; color: white')

        self.failureIcon3 = QLabel(self)
        self.failureIcon3.setPixmap(self.pixmapAlert)
        self.failureIcon3.setGeometry(1434, 614, 28, 28)
        self.failureIcon3.setStyleSheet('background-color: #EA9999')

        # current temperature
        self.internalTempVal = QLabel(self)
        self.internalTempVal.setText(str(self.tmCurrentTemp))
        self.internalTempVal.setGeometry(821, 349, 26, 20)
        self.internalTempVal.setFont(QFont('Calibri', 5))
        self.internalTempVal.setAlignment(Qt.AlignCenter)
        self.internalTempVal.setStyleSheet('background-color: black; color: white')

        self.internalTempUnit = QLabel('°F', self)
        self.internalTempUnit.setGeometry(843, 349, 16, 20)
        self.internalTempUnit.setFont(QFont('Calibri', 5))
        self.internalTempUnit.setStyleSheet('background-color: black; color: white')

        # system clock
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.displayTime)
        self.timer.start(1000)

        self.systemClock = QLabel(self)
        self.systemClock.setGeometry(987, 349, 53, 20)
        self.systemClock.setFont(QFont('Calibri', 5))
        self.systemClock.setStyleSheet('background-color: black; color: white')

        # train ID
        self.trainID = QLabel(self)
        self.trainID.setText('#' + self.uiTrainID)
        self.trainID.setGeometry(1128, 349, 73, 20)
        self.trainID.setAlignment(Qt.AlignRight)
        self.trainID.setFont(QFont('Calibri', 5))
        self.trainID.setStyleSheet('background-color: black; color: white')

        # previous stop
        self.prevStop = QLabel('Herron Ave', self)
        self.prevStop.setGeometry(1060, 430, 141, 20)
        self.prevStop.setFont(QFont('Calibri', 5))
        self.prevStop.setStyleSheet('background-color: black; color: white')

        # next stop
        self.nextStop = QLabel('Shadyside', self)
        self.nextStop.setGeometry(1060, 625, 141, 20)
        self.nextStop.setFont(QFont('Calibri', 5))
        self.nextStop.setStyleSheet('background-color: black; color: white')

        # speed limit
        self.whiteRectangle3 = QLabel(self)
        self.whiteRectangle3.setGeometry(847, 421, 80, 90)
        self.whiteRectangle3.setStyleSheet('background-color: white')

        self.whiteRectangle4 = QLabel(self)
        self.whiteRectangle4.setGeometry(858, 430, 57, 71)
        self.whiteRectangle4.setStyleSheet('background-color: white; border: 3px solid black')

        self.speedLimitLabel = QLabel('Speed\nLimit', self)
        self.speedLimitLabel.setGeometry(869, 439, 37, 29)
        self.speedLimitLabel.setAlignment(Qt.AlignCenter)
        self.speedLimitLabel.setFont(QFont('Calibri', 5))
        self.speedLimitLabel.setStyleSheet('background-color: white; color: black')

        self.speedLimitVal = QLabel(self)
        self.speedLimitVal.setText(str(self.tmSpeedLimit))
        self.speedLimitVal.setGeometry(871, 474, 33, 24)
        self.speedLimitVal.setAlignment(Qt.AlignCenter)
        self.speedLimitVal.setFont(QFont('Calibri', 7))
        self.speedLimitVal.setStyleSheet('background-color: white; color: black')

        # train location display
        # connectors
        self.whiteVerticalLine1 = QLabel(self)
        self.whiteVerticalLine1.setGeometry(999, 450, 21, 82)
        self.whiteVerticalLine1.setStyleSheet('background-color: white')

        self.blueVerticalLine3 = QLabel(self)
        self.blueVerticalLine3.setGeometry(999, 539, 21, 82)
        self.blueVerticalLine3.setStyleSheet('background-color: #9FC5F8')

        # destination
        self.nextStopIcon = QLabel(self)
        self.nextStopIcon.setGeometry(979, 416, 60, 60)
        self.nextStopIcon.setStyleSheet('background-color: white; border: 10px solid #EA9999; border-radius: 30')

        # train icon
        self.pixmapTrain = QtGui.QPixmap('train-icon.png')
        self.pixmapTrain = self.pixmapTrain.scaled(30, 30)

        self.trainIcon = QLabel(self)
        self.trainIcon.setGeometry(979, 503, 60, 60)
        self.trainIcon.setAlignment(Qt.AlignCenter)
        self.trainIcon.setPixmap(self.pixmapTrain)
        self.trainIcon.setStyleSheet('background-color: white; border: 10px solid #9FC5F8; border-radius: 30')

        # origin
        self.previousStopIcon = QLabel(self)
        self.previousStopIcon.setGeometry(979, 596, 60, 60)
        self.previousStopIcon.setStyleSheet('background-color: white; border: 10px solid #9FC5F8; border-radius: 30')

        self.displayLayoutWidgets = [self.blueVerticalLine2,
                                     self.blueHorizontalBlock2,
                                     self.displayLabel,
                                     self.changeTrainLabel,
                                     self.greyRectangle,
                                     self.systemSpeedLabel,
                                     self.systemSpeedVal,
                                     self.fastforward,
                                     self.rewind,
                                     self.blackRectangle1,
                                     self.speedLabel,
                                     self.speedUnitLabel,
                                     self.currentSpeedVal,
                                     self.suggestedSpeedLabel,
                                     self.suggestedSpeedVal,
                                     self.blackRectangle2,
                                     self.powerLabel,
                                     self.powerUnitLabel,
                                     self.currentPowerVal,
                                     self.blackRectangle3,
                                     self.authorityLabel,
                                     self.authorityUnitLabel,
                                     self.upArrow1,
                                     self.authorityVal,
                                     self.warningHeader,
                                     self.warningBody,
                                     self.signalPickupFailureLabel,
                                     self.failureIcon1,
                                     self.trainEngineFailureLabel,
                                     self.failureIcon2,
                                     self.brakeFailureLabel,
                                     self.failureIcon3,
                                     self.internalTempVal,
                                     self.internalTempUnit,
                                     self.systemClock,
                                     self.trainID,
                                     self.prevStop,
                                     self.nextStop,
                                     self.whiteRectangle3,
                                     self.whiteRectangle4,
                                     self.speedLimitLabel,
                                     self.speedLimitVal,
                                     self.whiteVerticalLine1,
                                     self.blueVerticalLine3,
                                     self.nextStopIcon,
                                     self.trainIcon,
                                     self.previousStopIcon]

        """user section layout"""
        # engineer
        self.engineerLabel = QLabel('Engineer', self)
        self.engineerLabel.setGeometry(392, 295, 155, 40)
        self.engineerLabel.setFont(QFont('Calibri', 13))
        self.engineerLabel.setStyleSheet('background-color: white; color: #085394')

        # kp
        self.kpLabel = QLabel('Kp', self)
        self.kpLabel.setGeometry(392, 356, 131, 38)
        self.kpLabel.setFont(QFont('Calibri', 10))
        self.kpLabel.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')

        self.kpVal = QLineEdit(self)
        self.kpVal.setPlaceholderText('--')
        self.kpVal.setGeometry(436, 356, 87, 38)
        self.kpVal.setFont(QFont('Calibri', 10))
        self.kpVal.setAlignment(Qt.AlignCenter)
        self.kpVal.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
        self.kpVal.returnPressed.connect(self.input_engineer_kp)
        # ki
        self.kiLabel = QLabel('Kp', self)
        self.kiLabel.setGeometry(392, 426, 131, 38)
        self.kiLabel.setFont(QFont('Calibri', 10))
        self.kiLabel.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')

        self.kiVal = QLineEdit(self)
        self.kiVal.setPlaceholderText('--')
        self.kiVal.setGeometry(436, 426, 87, 38)
        self.kiVal.setFont(QFont('Calibri', 10))
        self.kiVal.setAlignment(Qt.AlignCenter)
        self.kiVal.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
        self.kiVal.returnPressed.connect(self.input_engineer_ki)

        # train driver
        self.driverLabel = QLabel('Train Driver', self)
        self.driverLabel.setGeometry(392, 485, 171, 40)
        self.driverLabel.setFont(QFont('Calibri', 13))
        self.driverLabel.setStyleSheet('background-color: white; color: #085394')

        self.userSectionWidgets = [self.engineerLabel,
                                   self.kpLabel,
                                   self.kpVal,
                                   self.kiLabel,
                                   self.kiVal,
                                   self.driverLabel]

        """driver input p1"""
        # modes
        self.manualButton = QPushButton('Manual', self)
        self.manualButton.setGeometry(374, 531, 115, 38)
        self.manualButton.setFont(QFont('Calibri', 10))
        self.manualButton.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')

        self.automaticButton = QPushButton('Automatic', self)
        self.automaticButton.setGeometry(538, 531, 125, 38)
        self.automaticButton.setFont(QFont('Calibri', 10))
        self.automaticButton.setStyleSheet('QPushButton{background-color: white; color: #085394; border: 1px solid #085394}'
                                           'QPushButton::pressed{background-color: #9FC5F8; color: #085394; border: 1px solid #085394}')

        self.manualButton.clicked.connect(self.input_driver_manual_mode)
        self.automaticButton.clicked.connect(self.input_driver_automatic_mode)

        # brakes
        self.emergencyBrakeLabel = QLabel('Emergency Brake', self)
        self.emergencyBrakeLabel.setGeometry(354, 598, 209, 38)
        self.emergencyBrakeLabel.setFont(QFont('Calibri', 10))
        self.emergencyBrakeLabel.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')

        self.emergencyBrakeButton = QPushButton('Toggle', self)
        self.emergencyBrakeButton.setGeometry(591, 598, 38, 38)
        self.emergencyBrakeButton.setFont(QFont('Calibri', 5))
        self.emergencyBrakeButton.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
        self.emergencyBrakeButton.setCheckable(True)

        self.serviceBrakeLabel = QLabel('Service Brake', self)
        self.serviceBrakeLabel.setGeometry(354, 665, 209, 38)
        self.serviceBrakeLabel.setFont(QFont('Calibri', 10))
        self.serviceBrakeLabel.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')

        self.serviceBrakeButton = QPushButton('Toggle', self)
        self.serviceBrakeButton.setGeometry(591, 665, 38, 38)
        self.serviceBrakeButton.setFont(QFont('Calibri', 5))
        self.serviceBrakeButton.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
        self.serviceBrakeButton.setCheckable(True)

        self.emergencyBrakeButton.clicked.connect(self.input_driver_emergency_brake)
        self.serviceBrakeButton.clicked.connect(self.input_driver_service_brake)

        # setpoint speed
        self.setpointSpeedLabel = QLabel('Setpoint Speed', self)
        self.setpointSpeedLabel.setGeometry(354, 731, 183, 38)
        self.setpointSpeedLabel.setFont(QFont('Calibri', 10))
        self.setpointSpeedLabel.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')

        self.setpointSpeedVal = QSpinBox(self)
        self.setpointSpeedVal.setRange(0, 43)
        self.setpointSpeedVal.setValue(0)
        self.setpointSpeedVal.setGeometry(550, 732, 123, 38)
        self.setpointSpeedVal.setFont(QFont('Calibri', 10))
        self.setpointSpeedVal.setAlignment(Qt.AlignCenter)
        self.setpointSpeedVal.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
        self.setpointSpeedVal.setSuffix(' mph')
        self.setpointSpeedVal.valueChanged.connect(self.input_driver_setpoint_command)

        # announcements
        self.announcements = QComboBox(self)
        self.announcements.setGeometry(353, 802, 327, 38)
        self.announcements.setFont(QFont('Calibri', 10))
        self.announcements.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
        self.announcements.addItem('Announcements')
        self.announcements.addItem('Time/Prev_Stop/Next_Stop')
        self.announcements.addItem('Custom')
        self.announcements.currentTextChanged.connect(self.input_driver_announcement)
        self.announcements.setInsertPolicy(self.announcements.NoInsert)

        # driver input p2
        self.pixmapChevronsDown = QtGui.QPixmap('chevrons-down.svg')
        self.pixmapChevronsDown = self.pixmapChevronsDown.scaled(48, 48)

        self.ChevronsDown1 = QPushButton(self)
        self.ChevronsDown1.setIcon(QtGui.QIcon(self.pixmapChevronsDown))
        self.ChevronsDown1.setGeometry(473, 956, 48, 48)
        self.ChevronsDown1.setStyleSheet('QPushButton{background-color: white; color: #085394; border: 1px solid #085394; border-radius: 24px}'
                                         'QPushButton::pressed{background-color: #9FC5F8; color: #085394; border: 1px solid #085394; border-radius: 24px}')
        self.ChevronsDown1.clicked.connect(self.ui_wireframe2)

        self.driverInputP1Widgets = [self.manualButton,
                                     self.automaticButton,
                                     self.emergencyBrakeLabel,
                                     self.emergencyBrakeButton,
                                     self.serviceBrakeLabel,
                                     self.serviceBrakeButton,
                                     self.setpointSpeedLabel,
                                     self.setpointSpeedVal,
                                     self.announcements,
                                     self.ChevronsDown1]

        """driver input p2"""
        # driver input p1
        self.pixmapChevronsUp = QtGui.QPixmap('chevrons-up.svg')
        self.pixmapChevronsUp = self.pixmapChevronsUp.scaled(48, 48)

        self.ChevronsUp1 = QPushButton(self)
        self.ChevronsUp1.setIcon(QtGui.QIcon(self.pixmapChevronsUp))
        self.ChevronsUp1.setGeometry(473, 521, 48, 48)
        self.ChevronsUp1.setStyleSheet('QPushButton{background-color: white; color: #085394; border: 1px solid #085394; border-radius: 24px}'
                                       'QPushButton::pressed{background-color: #9FC5F8; color: #085394; border: 1px solid #085394; border-radius: 24px}')
        self.ChevronsUp1.clicked.connect(self.ui_wireframe)

        # doors
        self.doorLabel = QLabel('Doors', self)
        self.doorLabel.setGeometry(352, 590, 171, 38)
        self.doorLabel.setFont(QFont('Calibri', 10))
        self.doorLabel.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')

        # left door
        self.pixmapLeftChevron = QtGui.QPixmap('chevron-left.svg')
        self.pixmapLeftChevron = self.pixmapLeftChevron.scaled(32, 32)

        self.doorLeftButton = QPushButton(self)
        self.doorLeftButton.setIcon(QtGui.QIcon(self.pixmapLeftChevron))
        self.doorLeftButton.setGeometry(559, 590, 38, 38)
        self.doorLeftButton.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
        self.doorLeftButton.setCheckable(True)
        self.doorLeftButton.clicked.connect(self.input_driver_left_door)

        # right door
        self.pixmapRightChevron1 = self.pixmapRightChevron.scaled(32, 32)

        self.doorRightButton = QPushButton(self)
        self.doorRightButton.setIcon(QtGui.QIcon(self.pixmapRightChevron1))
        self.doorRightButton.setGeometry(627, 590, 38, 38)
        self.doorRightButton.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
        self.doorRightButton.setCheckable(True)
        self.doorRightButton.clicked.connect(self.input_driver_right_door)

        # external lights
        self.externalLightsLabel = QLabel('Headlights', self)
        self.externalLightsLabel.setGeometry(352, 664, 172, 38)
        self.externalLightsLabel.setFont(QFont('Calibri', 10))
        self.externalLightsLabel.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')

        self.externalLightsButton = QPushButton('Toggle', self)
        self.externalLightsButton.setGeometry(589, 671, 38, 38)
        self.externalLightsButton.setFont(QFont('Calibri', 5))
        self.externalLightsButton.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
        self.externalLightsButton.setCheckable(True)
        self.externalLightsButton.clicked.connect(self.input_driver_external_lights)

        # internal lights
        self.internalLightsLabel = QLabel('Internal Lights', self)
        self.internalLightsLabel.setGeometry(352, 726, 172, 38)
        self.internalLightsLabel.setFont(QFont('Calibri', 10))
        self.internalLightsLabel.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')

        self.internalLightsButton = QPushButton('Toggle', self)
        self.internalLightsButton.setGeometry(589, 733, 38, 38)
        self.internalLightsButton.setFont(QFont('Calibri', 5))
        self.internalLightsButton.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
        self.internalLightsButton.setCheckable(True)
        self.internalLightsButton.clicked.connect(self.input_driver_internal_lights)

        # internal setpoint temperature
        self.setpointTempLabel = QLabel('Setpoint Temp', self)
        self.setpointTempLabel.setGeometry(352, 798, 172, 38)
        self.setpointTempLabel.setFont(QFont('Calibri', 10))
        self.setpointTempLabel.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')

        self.setpointTempVal = QSpinBox(self)
        self.setpointTempVal.setRange(0, 100)
        self.setpointTempVal.setValue(70)
        self.setpointTempVal.setGeometry(559, 798, 107, 38)
        self.setpointTempVal.setFont(QFont('Calibri', 10))
        self.setpointTempVal.setAlignment(Qt.AlignCenter)
        self.setpointTempVal.setSuffix(' °F')
        self.setpointTempVal.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
        self.setpointTempVal.valueChanged.connect(self.input_driver_setpoint_temp)

        # advertisements
        self.advertisementLabel = QLabel('Advertisement', self)
        self.advertisementLabel.setGeometry(352, 869, 172, 38)
        self.advertisementLabel.setFont(QFont('Calibri', 10))
        self.advertisementLabel.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')

        self.advertisementButton = QPushButton('Toggle', self)
        self.advertisementButton.setGeometry(589, 869, 38, 38)
        self.advertisementButton.setFont(QFont('Calibri', 5))
        self.advertisementButton.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
        self.advertisementButton.setCheckable(True)
        self.advertisementButton.clicked.connect(self.input_driver_advertisement)

        self.driverInputP2Widgets = [self.ChevronsUp1,
                                     self.doorLabel,
                                     self.doorLeftButton,
                                     self.doorRightButton,
                                     self.externalLightsLabel,
                                     self.externalLightsButton,
                                     self.internalLightsLabel,
                                     self.internalLightsButton,
                                     self.setpointTempLabel,
                                     self.setpointTempVal,
                                     self.advertisementLabel,
                                     self.advertisementButton]

        """test bench layout"""
        # background shapes
        self.largeRectangle1 = QLabel(self)
        self.largeRectangle1.setGeometry(374, 303, 401, 678)
        self.largeRectangle1.setStyleSheet('background-color: white; border: 5px solid #2B78E4')

        self.largeRectangle2 = QLabel(self)
        self.largeRectangle2.setGeometry(1058, 303, 401, 678)
        self.largeRectangle2.setStyleSheet('background-color: #CCCCCC; border: 5px solid #CF2A27')

        self.blueDivider = QLabel(self)
        self.blueDivider.setGeometry(374, 359, 401, 5)
        self.blueDivider.setStyleSheet('background-color: #2B78E4')

        self.redDivider = QLabel(self)
        self.redDivider.setGeometry(1058, 359, 401, 5)
        self.redDivider.setStyleSheet('background-color: #CF2A27')

        self.pixmapChevronsRight = QtGui.QPixmap('chevrons-right-blue.png')

        self.resultButton = QPushButton(self)
        self.resultButton.setIcon(QtGui.QIcon(self.pixmapChevronsRight))
        self.resultButton.setGeometry(853, 602, 128, 128)
        self.resultButton.setStyleSheet('QPushButton{background-color: white; color: #085394; border: 1px solid #085394; border-radius: 64px}'
                                        'QPushButton::pressed{background-color: #2B78E4; color: #085394; border: 1px solid white; border-radius: 64px}')
        self.resultButton.clicked.connect(self.testbench_button)

        # input label
        self.inputLabel = QLabel('Inputs', self)
        self.inputLabel.setGeometry(399, 313, 95, 40)
        self.inputLabel.setFont(QFont('Calibri', 13))
        self.inputLabel.setStyleSheet('background-color: white; color: #2B78E4')

        # train inputs
        self.trainInputLabel = QLabel('Train', self)
        self.trainInputLabel.setGeometry(399, 385, 65, 36)
        self.trainInputLabel.setFont(QFont('Calibri', 11))
        self.trainInputLabel.setStyleSheet('background-color: white; color: #2B78E4')

        self.trainInputVal = QLineEdit(self)
        self.trainInputVal.setGeometry(477, 386, 96, 33)
        self.trainInputVal.setFont(QFont('Calibri', 11))
        self.trainInputVal.setStyleSheet('background-color: white; color: #2B78E4; border: 1px solid #2B78E4')
        self.trainInputVal.returnPressed.connect(self.input_tm_train_id)

        # speed limit input
        self.testbenchSpeedLimitLabel = QLabel('Speed Limit', self)
        self.testbenchSpeedLimitLabel.setGeometry(399, 440, 194, 28)
        self.testbenchSpeedLimitLabel.setFont(QFont('Calibri', 8))
        self.testbenchSpeedLimitLabel.setStyleSheet('background-color: white; color: #085394')

        self.testbenchSpeedLimitVal = QLineEdit(self)
        self.testbenchSpeedLimitVal.setGeometry(615, 440, 60, 33)
        self.testbenchSpeedLimitVal.setFont(QFont('Calibri', 8))
        self.testbenchSpeedLimitVal.setStyleSheet('background-color: white; color: #2B78E4; border: 1px solid #2B78E4')
        self.testbenchSpeedLimitVal.returnPressed.connect(self.input_tm_speed_limit)

        # authority input
        self.testbenchAuthorityLabel = QLabel('Authority', self)
        self.testbenchAuthorityLabel.setGeometry(399, 480, 194, 28)
        self.testbenchAuthorityLabel.setFont(QFont('Calibri', 8))
        self.testbenchAuthorityLabel.setStyleSheet('background-color: white; color: #085394')

        self.testbenchAuthorityVal = QLineEdit(self)
        self.testbenchAuthorityVal.setGeometry(615, 480, 60, 33)
        self.testbenchAuthorityVal.setFont(QFont('Calibri', 8))
        self.testbenchAuthorityVal.setStyleSheet('background-color: white; color: #2B78E4; border: 1px solid #2B78E4')
        self.testbenchAuthorityVal.returnPressed.connect(self.input_tm_authority)

        # current speed input
        self.testbenchCurrentSpeedLabel = QLabel('Current Speed', self)
        self.testbenchCurrentSpeedLabel.setGeometry(399, 520, 194, 28)
        self.testbenchCurrentSpeedLabel.setFont(QFont('Calibri', 8))
        self.testbenchCurrentSpeedLabel.setStyleSheet('background-color: white; color: #085394')

        self.testbenchCurrentSpeedVal = QLineEdit(self)
        self.testbenchCurrentSpeedVal.setGeometry(615, 520, 60, 33)
        self.testbenchCurrentSpeedVal.setFont(QFont('Calibri', 8))
        self.testbenchCurrentSpeedVal.setStyleSheet('background-color: white; color: #2B78E4; border: 1px solid #2B78E4')
        self.testbenchCurrentSpeedVal.returnPressed.connect(self.input_tm_current_speed)

        # commanded speed input
        self.testbenchCommandedSpeedLabel = QLabel('Commanded Speed', self)
        self.testbenchCommandedSpeedLabel.setGeometry(399, 560, 194, 28)
        self.testbenchCommandedSpeedLabel.setFont(QFont('Calibri', 8))
        self.testbenchCommandedSpeedLabel.setStyleSheet('background-color: white; color: #085394')

        self.testbenchCommandedSpeedVal = QLineEdit(self)
        self.testbenchCommandedSpeedVal.setGeometry(615, 560, 60, 33)
        self.testbenchCommandedSpeedVal.setFont(QFont('Calibri', 8))
        self.testbenchCommandedSpeedVal.setStyleSheet('background-color: white; color: #2B78E4; border: 1px solid #2B78E4')
        self.testbenchCommandedSpeedVal.returnPressed.connect(self.input_tm_commanded_speed)

        # beacon data input
        self.testbenchBeaconLabel = QLabel('Beacon Data', self)
        self.testbenchBeaconLabel.setGeometry(399, 600, 194, 28)
        self.testbenchBeaconLabel.setFont(QFont('Calibri', 8))
        self.testbenchBeaconLabel.setStyleSheet('background-color: white; color: #085394')

        self.testbenchBeaconButton = QPushButton(self)
        self.testbenchBeaconButton.setGeometry(615, 600, 60, 28)
        self.testbenchBeaconButton.setFont(QFont('Calibri', 8))
        self.testbenchBeaconButton.setStyleSheet('QPushButton{background-color: white; color: #085394; border: 1px solid #085394}'
                                                 'QPushButton::pressed{background-color: #9FC5F8; color: #085394; border: 1px solid #085394}')
        self.testbenchBeaconButton.clicked.connect(self.input_tm_beacon_data)

        # current temperature input
        self.testbenchTempLabel = QLabel('Current Temperature', self)
        self.testbenchTempLabel.setGeometry(399, 640, 194, 28)
        self.testbenchTempLabel.setFont(QFont('Calibri', 8))
        self.testbenchTempLabel.setStyleSheet('background-color: white; color: #085394')

        self.testbenchTempVal = QLineEdit(self)
        self.testbenchTempVal.setGeometry(615, 640, 60, 33)
        self.testbenchTempVal.setFont(QFont('Calibri', 8))
        self.testbenchTempVal.setStyleSheet('background-color: white; color: #2B78E4; border: 1px solid #2B78E4')
        self.testbenchTempVal.returnPressed.connect(self.input_tm_current_temp)

        # passenger input
        self.passengerInputLabel = QLabel('Passenger', self)
        self.passengerInputLabel.setGeometry(399, 680, 139, 36)
        self.passengerInputLabel.setFont(QFont('Calibri', 11))
        self.passengerInputLabel.setStyleSheet('background-color: white; color: #2B78E4')

        # emergency brake input
        self.testbenchEmergencyBrakeLabel = QLabel('Emergency Brake', self)
        self.testbenchEmergencyBrakeLabel.setGeometry(399, 735, 194, 28)
        self.testbenchEmergencyBrakeLabel.setFont(QFont('Calibri', 8))
        self.testbenchEmergencyBrakeLabel.setStyleSheet('background-color: white; color: #085394')

        self.testbenchEmergencyBrakeButton = QPushButton(self)
        self.testbenchEmergencyBrakeButton.setGeometry(615, 735, 60, 33)
        self.testbenchEmergencyBrakeButton.setFont(QFont('Calibri', 8))
        self.testbenchEmergencyBrakeButton.setStyleSheet('QPushButton{background-color: white; color: #085394; border: 1px solid #085394}'
                                                         'QPushButton::pressed{background-color: #9FC5F8; color: #085394; border: 1px solid #085394}')
        self.testbenchEmergencyBrakeButton.setCheckable(True)
        self.testbenchEmergencyBrakeButton.clicked.connect(self.input_tm_emergency_brake)

        # murphy inputs
        self.murphyInputLabel = QLabel('Murphy', self)
        self.murphyInputLabel.setGeometry(399, 775, 100, 36)
        self.murphyInputLabel.setFont(QFont('Calibri', 11))
        self.murphyInputLabel.setStyleSheet('background-color: white; color: #2B78E4')

        # signal pickup failure
        self.testbenchSignalFailLabel = QLabel('Signal Pickup Failure', self)
        self.testbenchSignalFailLabel.setGeometry(399, 815, 194, 28)
        self.testbenchSignalFailLabel.setFont(QFont('Calibri', 8))
        self.testbenchSignalFailLabel.setStyleSheet('background-color: white; color: #085394')

        self.testbenchSignalFailButton = QPushButton(self)
        self.testbenchSignalFailButton.setGeometry(615, 815, 60, 33)
        self.testbenchSignalFailButton.setFont(QFont('Calibri', 8))
        self.testbenchSignalFailButton.setStyleSheet('QPushButton{background-color: white; color: #085394; border: 1px solid #085394}'
                                                     'QPushButton::pressed{background-color: #9FC5F8; color: #085394; border: 1px solid #085394}')
        self.testbenchSignalFailButton.setCheckable(True)
        self.testbenchSignalFailButton.clicked.connect(self.input_tm_signal_fail)

        # engine failure
        self.testbenchEngineFailLabel = QLabel('Train Engine Failure', self)
        self.testbenchEngineFailLabel.setGeometry(399, 855, 194, 28)
        self.testbenchEngineFailLabel.setFont(QFont('Calibri', 8))
        self.testbenchEngineFailLabel.setStyleSheet('background-color: white; color: #085394')

        self.testbenchEngineFailButton = QPushButton(self)
        self.testbenchEngineFailButton.setGeometry(615, 855, 60, 33)
        self.testbenchEngineFailButton.setFont(QFont('Calibri', 8))
        self.testbenchEngineFailButton.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
        self.testbenchEngineFailButton.setCheckable(True)
        self.testbenchEngineFailButton.clicked.connect(self.input_tm_engine_fail)

        # brake failure
        self.testbenchBrakeFailLabel = QLabel('Brake Failure', self)
        self.testbenchBrakeFailLabel.setGeometry(399, 895, 194, 28)
        self.testbenchBrakeFailLabel.setFont(QFont('Calibri', 8))
        self.testbenchBrakeFailLabel.setStyleSheet('background-color: white; color: #085394')

        self.testbenchBrakeFailButton = QPushButton(self)
        self.testbenchBrakeFailButton.setGeometry(615, 895, 60, 33)
        self.testbenchBrakeFailButton.setFont(QFont('Calibri', 8))
        self.testbenchBrakeFailButton.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
        self.testbenchBrakeFailButton.setCheckable(True)
        self.testbenchBrakeFailButton.clicked.connect(self.input_tm_brake_fail)

        # output label
        self.outputLabel = QLabel('Outputs', self)
        self.outputLabel.setGeometry(1083, 313, 123, 40)
        self.outputLabel.setFont(QFont('Calibri', 13))
        self.outputLabel.setStyleSheet('background-color: #CCCCCC; color: black')

        # power command
        self.testbenchPowerCommandLabel = QLabel('Power Command', self)
        self.testbenchPowerCommandLabel.setGeometry(1098, 385, 194, 28)
        self.testbenchPowerCommandLabel.setFont(QFont('Calibri', 8))
        self.testbenchPowerCommandLabel.setStyleSheet('background-color: #CCCCCC; color: black')

        self.testbenchPowerCommandVal = QLineEdit(self)
        self.testbenchPowerCommandVal.setGeometry(1325, 385, 60, 33)
        self.testbenchPowerCommandVal.setFont(QFont('Calibri', 8))
        self.testbenchPowerCommandVal.setStyleSheet('background-color: #666666; color: white; border: 1px solid black')
        self.testbenchPowerCommandVal.setReadOnly(True)
        # setpoint command
        self.testbenchSetpointCommandLabel = QLabel('Setpoint Command', self)
        self.testbenchSetpointCommandLabel.setGeometry(1098, 425, 194, 28)
        self.testbenchSetpointCommandLabel.setFont(QFont('Calibri', 8))
        self.testbenchSetpointCommandLabel.setStyleSheet('background-color: #CCCCCC; color: black')

        self.testbenchSetpointCommandVal = QLineEdit(self)
        self.testbenchSetpointCommandVal.setGeometry(1325, 425, 60, 33)
        self.testbenchSetpointCommandVal.setFont(QFont('Calibri', 8))
        self.testbenchSetpointCommandVal.setStyleSheet('background-color: #666666; color: white; border: 1px solid black')
        self.testbenchSetpointCommandVal.setReadOnly(True)

        # announcement
        self.testbenchAnnouncementLabel = QLabel('Announcement', self)
        self.testbenchAnnouncementLabel.setGeometry(1098, 465, 194, 28)
        self.testbenchAnnouncementLabel.setFont(QFont('Calibri', 8))
        self.testbenchAnnouncementLabel.setStyleSheet('background-color: #CCCCCC; color: black')

        self.testbenchAnnouncementVal = QLineEdit(self)
        self.testbenchAnnouncementVal.setGeometry(1325, 465, 60, 33)
        self.testbenchAnnouncementVal.setFont(QFont('Calibri', 8))
        self.testbenchAnnouncementVal.setStyleSheet('background-color: #666666; color: white; border: 1px solid black')
        self.testbenchAnnouncementVal.setReadOnly(True)

        # internal lights
        self.testbenchInternalLightsLabel = QLabel('Internal Lights', self)
        self.testbenchInternalLightsLabel.setGeometry(1098, 505, 194, 28)
        self.testbenchInternalLightsLabel.setFont(QFont('Calibri', 8))
        self.testbenchInternalLightsLabel.setStyleSheet('background-color: #CCCCCC; color: black')

        self.testbenchInternalLightsButton = QPushButton(self)
        self.testbenchInternalLightsButton.setGeometry(1325, 505, 60, 33)
        self.testbenchInternalLightsButton.setFont(QFont('Calibri', 8))
        self.testbenchInternalLightsButton.setStyleSheet('QPushButton{background-color: #666666; color: white; border: 1px solid black}'
                                                         'QPushButton::pressed{background-color: black; color: white; border: 1px solid black}')
        # external lights
        self.testbenchExternalLightsLabel = QLabel('External Lights', self)
        self.testbenchExternalLightsLabel.setGeometry(1098, 545, 194, 28)
        self.testbenchExternalLightsLabel.setFont(QFont('Calibri', 8))
        self.testbenchExternalLightsLabel.setStyleSheet('background-color: #CCCCCC; color: black')

        self.testbenchExternalLightsButton = QPushButton(self)
        self.testbenchExternalLightsButton.setGeometry(1325, 545, 60, 33)
        self.testbenchExternalLightsButton.setFont(QFont('Calibri', 8))
        self.testbenchExternalLightsButton.setStyleSheet('QPushButton{background-color: #666666; color: white; border: 1px solid black}'
                                                         'QPushButton::pressed{background-color: black; color: white; border: 1px solid black}')

        # door state
        self.testbenchDoorLabel = QLabel('Door State', self)
        self.testbenchDoorLabel.setGeometry(1098, 585, 194, 28)
        self.testbenchDoorLabel.setFont(QFont('Calibri', 8))
        self.testbenchDoorLabel.setStyleSheet('background-color: #CCCCCC; color: black')

        self.testbenchDoorLeft = QPushButton('Left', self)
        self.testbenchDoorLeft.setGeometry(1325, 585, 55, 33)
        self.testbenchDoorLeft.setFont(QFont('Calibri', 8))
        self.testbenchDoorLeft.setStyleSheet('QPushButton{background-color: #666666; color: white; border: 1px solid black}'
                                             'QPushButton::pressed{background-color: black; color: white; border: 1px solid black}')

        self.testbenchDoorRight = QPushButton('Right', self)
        self.testbenchDoorRight.setGeometry(1385, 585, 55, 33)
        self.testbenchDoorRight.setFont(QFont('Calibri', 8))
        self.testbenchDoorRight.setStyleSheet('QPushButton{background-color: #666666; color: white; border: 1px solid black}'
                                              'QPushButton::pressed{background-color: black; color: white; border: 1px solid black}')

        # temperature setpoint
        self.testbenchSetpointTempLabel = QLabel('Setpoint Temperature', self)
        self.testbenchSetpointTempLabel.setGeometry(1098, 625, 194, 28)
        self.testbenchSetpointTempLabel.setFont(QFont('Calibri', 8))
        self.testbenchSetpointTempLabel.setStyleSheet('background-color: #CCCCCC; color: black')

        self.testbenchSetpointTempVal = QLineEdit(self)
        self.testbenchSetpointTempVal.setGeometry(1325, 625, 60, 33)
        self.testbenchSetpointTempVal.setFont(QFont('Calibri', 8))
        self.testbenchSetpointTempVal.setStyleSheet('background-color: #666666; color: white; border: 1px solid black')
        self.testbenchSetpointTempVal.setReadOnly(True)

        # advertisement
        self.testbenchAdvertisementLabel = QLabel('Advertisement', self)
        self.testbenchAdvertisementLabel.setGeometry(1098, 665, 194, 28)
        self.testbenchAdvertisementLabel.setFont(QFont('Calibri', 8))
        self.testbenchAdvertisementLabel.setStyleSheet('background-color: #CCCCCC; color: black')

        self.testbenchAdvertisementButton = QPushButton(self)
        self.testbenchAdvertisementButton.setGeometry(1325, 665, 60, 33)
        self.testbenchAdvertisementButton.setFont(QFont('Calibri', 8))
        self.testbenchAdvertisementButton.setStyleSheet('QPushButton{background-color: #666666; color: white; border: 1px solid black}'
                                                        'QPushButton::pressed{background-color: black; color: white; border: 1px solid black}')

        self.testbenchWidgets = [self.largeRectangle1,
                                 self.largeRectangle2,
                                 self.blueDivider,
                                 self.redDivider,
                                 self.resultButton,
                                 self.inputLabel,
                                 self.trainInputLabel,
                                 self.trainInputVal,
                                 self.passengerInputLabel,
                                 self.murphyInputLabel,
                                 self.outputLabel,
                                 self.testbenchSpeedLimitLabel,
                                 self.testbenchSpeedLimitVal,
                                 self.testbenchAuthorityLabel,
                                 self.testbenchAuthorityVal,
                                 self.testbenchCurrentSpeedLabel,
                                 self.testbenchCurrentSpeedVal,
                                 self.testbenchCommandedSpeedLabel,
                                 self.testbenchCommandedSpeedVal,
                                 self.testbenchBeaconLabel,
                                 self.testbenchBeaconButton,
                                 self.testbenchTempLabel,
                                 self.testbenchTempVal,
                                 self.testbenchEmergencyBrakeLabel,
                                 self.testbenchEmergencyBrakeButton,
                                 self.testbenchSignalFailLabel,
                                 self.testbenchSignalFailButton,
                                 self.testbenchEngineFailLabel,
                                 self.testbenchEngineFailButton,
                                 self.testbenchBrakeFailLabel,
                                 self.testbenchBrakeFailButton,
                                 self.testbenchPowerCommandLabel,
                                 self.testbenchPowerCommandVal,
                                 self.testbenchSetpointCommandLabel,
                                 self.testbenchSetpointCommandVal,
                                 self.testbenchAnnouncementLabel,
                                 self.testbenchAnnouncementVal,
                                 self.testbenchInternalLightsLabel,
                                 self.testbenchInternalLightsButton,
                                 self.testbenchExternalLightsLabel,
                                 self.testbenchExternalLightsButton,
                                 self.testbenchDoorLabel,
                                 self.testbenchDoorLeft,
                                 self.testbenchDoorRight,
                                 self.testbenchSetpointTempLabel,
                                 self.testbenchSetpointTempVal,
                                 self.testbenchAdvertisementLabel,
                                 self.testbenchAdvertisementButton]

    def homepage(self):
        for w in self.actualHomeWidgets:
            w.show()
        for w in self.basicLayoutWidgets:
            w.hide()
        for w in self.homepageWidgets:
            w.hide()
        for w in self.userSectionWidgets:
            w.hide()
        for w in self.driverInputP1Widgets:
            w.hide()
        for w in self.driverInputP2Widgets:
            w.hide()
        for w in self.displayLayoutWidgets:
            w.hide()
        for w in self.testbenchWidgets:
            w.hide()

    def wireframe(self):
        for w in self.actualHomeWidgets:
            w.hide()
        for w in self.basicLayoutWidgets:
            w.show()
        for w in self.homepageWidgets:
            w.show()
        for w in self.userSectionWidgets:
            w.hide()
        for w in self.driverInputP1Widgets:
            w.hide()
        for w in self.driverInputP2Widgets:
            w.hide()
        for w in self.displayLayoutWidgets:
            w.hide()
        for w in self.testbenchWidgets:
            w.hide()

    def ui_wireframe(self):
        if self.checkTrainID == False:
            print('ERROR!')
            return

        for w in self.actualHomeWidgets:
            w.hide()
        for w in self.basicLayoutWidgets:
            w.show()
        for w in self.homepageWidgets:
            w.hide()
        for w in self.userSectionWidgets:
            w.show()
        for w in self.driverInputP1Widgets:
            w.show()
        for w in self.driverInputP2Widgets:
            w.hide()
        for w in self.displayLayoutWidgets:
            w.show()
        for w in self.testbenchWidgets:
            w.hide()

    def ui_wireframe2(self):
        for w in self.actualHomeWidgets:
            w.hide()
        for w in self.basicLayoutWidgets:
            w.show()
        for w in self.homepageWidgets:
            w.hide()
        for w in self.userSectionWidgets:
            w.show()
        for w in self.driverInputP1Widgets:
            w.hide()
        for w in self.driverInputP2Widgets:
            w.show()
        for w in self.displayLayoutWidgets:
            w.show()
        for w in self.testbenchWidgets:
            w.hide()

    def testbench(self):
        for w in self.actualHomeWidgets:
            w.hide()
        for w in self.basicLayoutWidgets:
            w.show()
        for w in self.homepageWidgets:
            w.hide()
        for w in self.userSectionWidgets:
            w.hide()
        for w in self.driverInputP1Widgets:
            w.hide()
        for w in self.driverInputP2Widgets:
            w.hide()
        for w in self.displayLayoutWidgets:
            w.hide()
        for w in self.testbenchWidgets:
            w.show()

    def input_train_id(self):
        self.uiTrainID = self.enterTrainID.text()
        self.trainID.setText('#' + self.uiTrainID)
        if self.uiTrainID != self.tmTrainID:
            self.checkTrainID = False
        else:
            self.checkTrainID = True
        print('ID ENTERED: ' + self.uiTrainID)

    def input_engineer_kp(self):
        self.uiKP = self.kpVal.text()
        print('CHANGED KP TO: ' + self.uiKP)

    def input_engineer_ki(self):
        self.uiKI = self.kiVal.text()
        print('CHANGED KI TO: ' + self.uiKI)

    def input_driver_manual_mode(self):
        self.uiMode = 0
        self.manualButton.setDown(True)
        self.manualButton.setStyleSheet('background-color: #9FC5F8; color: #085394; border: 1px solid #085394')
        self.automaticButton.setDown(False)
        self.automaticButton.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
        print('MANUAL MODE SELECTED')

        disableWidgets = [self.serviceBrakeButton,
                          self.setpointSpeedVal,
                          self.announcements,
                          self.doorLeftButton,
                          self.doorRightButton,
                          self.internalLightsButton,
                          self.externalLightsButton,
                          self.setpointTempVal,
                          self.advertisementButton]

        for w in disableWidgets:
            w.setDisabled(False)

    def input_driver_automatic_mode(self):
        self.uiMode = 1
        self.automaticButton.setDown(True)
        self.automaticButton.setStyleSheet('background-color: #9FC5F8; color: #085394; border: 1px solid #085394')
        self.manualButton.setDown(False)
        self.manualButton.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
        print('AUTOMATIC MODE SELECTED')

        disableWidgets = [self.serviceBrakeButton,
                          self.setpointSpeedVal,
                          self.announcements,
                          self.doorLeftButton,
                          self.doorRightButton,
                          self.internalLightsButton,
                          self.externalLightsButton,
                          self.setpointTempVal,
                          self.advertisementButton]

        for w in disableWidgets:
            w.setDisabled(True)

    def input_driver_emergency_brake(self):
        if self.emergencyBrakeButton.isChecked():
            self.tcEmergencyBrake = 1
            self.emergencyBrakeButton.setText('ON')
            self.emergencyBrakeButton.setStyleSheet('background-color: #9FC5F8; color: #085394; border: 1px solid #085394')
            self.tcServiceBrake = 0
            self.serviceBrakeButton.setText('OFF')
            self.serviceBrakeButton.setChecked(False)
            self.serviceBrakeButton.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
            print('EMERGENCY BRAKE: ON')
        else:
            self.tcEmergencyBrake = 0
            self.emergencyBrakeButton.setText('OFF')
            self.emergencyBrakeButton.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
            print('EMERGENCY BRAKE: OFF')

    def input_driver_service_brake(self):
        if self.serviceBrakeButton.isChecked():
            self.tcServiceBrake = 1
            self.serviceBrakeButton.setText('ON')
            self.serviceBrakeButton.setStyleSheet('background-color: #9FC5F8; color: #085394; border: 1px solid #085394')
            self.tcEmergencyBrake = 0
            self.emergencyBrakeButton.setText('OFF')
            self.emergencyBrakeButton.setChecked(False)
            self.emergencyBrakeButton.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
            print('SERVICE BRAKE: ON')
        else:
            self.tcEmergencyBrake = 0
            self.serviceBrakeButton.setText('OFF')
            self.serviceBrakeButton.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
            print('SERVICE BRAKE: OFF')

    def input_driver_setpoint_command(self):
        self.tcSetpointCommand = self.setpointSpeedVal.value()
        print('SETPOINT SPEED CHANGED TO: ' + str(self.tcSetpointCommand))

    def input_driver_announcement(self):
        if self.announcements.currentIndex() == 2:
            self.announcements.setEditable(True)
        else:
            self.announcements.setEditable(False)

        if self.announcements.currentIndex() == 1:
            self.tcAnnouncement = 'Time/Prev/Next'
            print(self.tcAnnouncement + ': This is a _ bound train. The next stop is: _')
        elif self.announcements.currentIndex() == 2:
            self.tcAnnouncement = self.announcements.currentText()
            print('CUSTOM ANNOUNCEMENT: ' + self.tcAnnouncement)
        else:
            self.tcAnnouncement = ''

    def input_driver_left_door(self):
        if self.doorLeftButton.isChecked():
            self.tcLeftDoor = 1
            self.doorLeftButton.setStyleSheet('background-color: #9FC5F8; color: #085394; border: 1px solid #085394')
            print('LEFT DOOR: OPEN')
        else:
            self.tcLeftDoor = 0
            self.doorLeftButton.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
            print('LEFT DOOR: CLOSED')

    def input_driver_right_door(self):
        if self.doorRightButton.isChecked():
            self.tcRightDoor = 1
            self.doorRightButton.setStyleSheet('background-color: #9FC5F8; color: #085394; border: 1px solid #085394')
            print('RIGHT DOOR: OPEN')
        else:
            self.tcRightDoor = 0
            self.doorRightButton.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
            print('RIGHT DOOR: CLOSED')

    def input_driver_external_lights(self):
        if self.externalLightsButton.isChecked():
            self.tcExternalLights = 1
            self.externalLightsButton.setText('ON')
            self.externalLightsButton.setStyleSheet('background-color: #9FC5F8; color: #085394; border: 1px solid #085394')
            print('HEADLIGHTS: ON')
        else:
            self.tcExternalLights = 0
            self.externalLightsButton.setText('OFF')
            self.externalLightsButton.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
            print('HEADLIGHTS: OFF')

    def input_driver_internal_lights(self):
        if self.internalLightsButton.isChecked():
            self.tcInternalLights = 1
            self.internalLightsButton.setText('ON')
            self.internalLightsButton.setStyleSheet('background-color: #9FC5F8; color: #085394; border: 1px solid #085394')
            print('INTERIOR LIGHTS: ON')
        else:
            self.tcInternalLights = 0
            self.internalLightsButton.setText('OFF')
            self.internalLightsButton.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
            print('INTERIOR LIGHTS: OFF')

    def input_driver_setpoint_temp(self):
        self.tcSetpointTemp = self.setpointTempVal.value()
        print('SETPOINT TEMP CHANGED TO: ' + str(self.tcSetpointTemp))

    def input_driver_advertisement(self):
        if self.advertisementButton.isChecked():
            self.tcAdvertisement = 1
            self.advertisementButton.setText('ON')
            self.advertisementButton.setStyleSheet('background-color: #9FC5F8; color: #085394; border: 1px solid #085394')
            print('ADS: ON')
        else:
            self.tcAdvertisement = 0
            self.advertisementButton.setText('OFF')
            self.advertisementButton.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
            print('ADS: OFF')

    def input_tm_train_id(self):
        self.tmTrainID = self.trainInputVal.text()
        print('EXISTING TRAIN UPDATED: ' + self.tmTrainID)

    def input_tm_speed_limit(self):
        self.tmSpeedLimit = self.testbenchSpeedLimitVal.text()
        self.speedLimitVal.setText(str(self.tmSpeedLimit))
        print('EXISTING SPEED LIMIT UPDATED: ' + self.tmSpeedLimit)

    def input_tm_authority(self):
        self.tmAuthority = self.testbenchAuthorityVal.text()
        self.authorityVal.setText(str(self.tmAuthority))
        print('EXISTING AUTHORITY UPDATED: ' + self.tmAuthority)

    def input_tm_current_speed(self):
        self.tmCurrentSpeed = self.testbenchCurrentSpeedVal.text()
        self.currentSpeedVal.setText(str(self.tmCurrentSpeed))
        print('EXISTING CURRENT SPEED UPDATED: ' + self.tmCurrentSpeed)

    def input_tm_commanded_speed(self):
        self.tmCommandedSpeed = self.testbenchCommandedSpeedVal.text()
        self.suggestedSpeedVal.setText(str(self.tmCommandedSpeed))
        print('EXISTING COMMANDED SPEED UPDATED: ' + self.tmCommandedSpeed)

    def input_tm_beacon_data(self):
        self.testbenchBeaconButton.setText(QFileDialog.getOpenFileName())

    def input_tm_current_temp(self):
        self.tmCurrentTemp = self.testbenchTempVal.text()
        self.internalTempVal.setText(str(self.tmCurrentTemp))
        print('EXISTING CURRENT TEMP UPDATED: ' + self.tmCurrentTemp)

    def input_tm_emergency_brake(self):
        if self.testbenchEmergencyBrakeButton.isChecked():
            self.tmEmergencyBrake = 1
            self.testbenchEmergencyBrakeButton.setText('ON')
            self.testbenchEmergencyBrakeButton.setStyleSheet('background-color: #9FC5F8; color: #085394; border: 1px solid #085394')
            print('EMERGENCY BRAKE: ON')

            self.tcEmergencyBrake = 1
            self.emergencyBrakeButton.setChecked(True)
            self.emergencyBrakeButton.setText('ON')
            self.emergencyBrakeButton.setStyleSheet('background-color: #9FC5F8; color: #085394; border: 1px solid #085394')
            self.tcServiceBrake = 0
            self.serviceBrakeButton.setText('OFF')
            self.serviceBrakeButton.setChecked(False)
            self.serviceBrakeButton.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
        else:
            self.tmEmergencyBrake = 0
            self.testbenchEmergencyBrakeButton.setText('OFF')
            self.testbenchEmergencyBrakeButton.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
            print('EMERGENCY BRAKE: OFF')

    def input_tm_signal_fail(self):
        if self.testbenchSignalFailButton.isChecked():
            self.tmSignalFail = 1
            self.testbenchSignalFailButton.setText('ON')
            self.failureIcon1.setPixmap(self.pixmapAlert2)
            self.testbenchSignalFailButton.setStyleSheet('background-color: #9FC5F8; color: #085394; border: 1px solid #085394')
            print('SIGNAL PICKUP FAILURE: OCCURRING')
        else:
            self.tmSignalFail = 0
            self.testbenchSignalFailButton.setText('OFF')
            self.failureIcon1.setPixmap(self.pixmapAlert)
            self.testbenchSignalFailButton.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
            print('SIGNAL PICKUP FAILURE: RESOLVED')

    def input_tm_engine_fail(self):
        if self.testbenchEngineFailButton.isChecked():
            self.tmEngineFail = 1
            self.testbenchEngineFailButton.setText('ON')
            self.failureIcon2.setPixmap(self.pixmapAlert2)
            self.testbenchEngineFailButton.setStyleSheet('background-color: #9FC5F8; color: #085394; border: 1px solid #085394')
            print('TRAIN ENGINE FAILURE: OCCURRING')
        else:
            self.tmEngineFail = 0
            self.testbenchEngineFailButton.setText('OFF')
            self.failureIcon2.setPixmap(self.pixmapAlert)
            self.testbenchEngineFailButton.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
            print('TRAIN ENGINE FAILURE: RESOLVED')


    def input_tm_brake_fail(self):
        if self.testbenchBrakeFailButton.isChecked():
            self.tmBrakeFail = 1
            self.testbenchBrakeFailButton.setText('ON')
            self.failureIcon3.setPixmap(self.pixmapAlert2)
            self.testbenchBrakeFailButton.setStyleSheet('background-color: #9FC5F8; color: #085394; border: 1px solid #085394')
            print('BRAKE FAILURE: OCCURRING')
        else:
            self.tmBrakeFail = 0
            self.testbenchBrakeFailButton.setText('OFF')
            self.failureIcon3.setPixmap(self.pixmapAlert)
            self.testbenchBrakeFailButton.setStyleSheet('background-color: white; color: #085394; border: 1px solid #085394')
            print('BRAKE FAILURE: RESOLVED')

    def testbench_button(self):
        self.tcPowerCommand = 100
        #self.tcPowerCommand = abs(self.tmCurrentSpeed - self.tcSetpointCommand) / self.tmCurrentSpeed * (self.uiKP + self.uiKI)
        self.testbenchPowerCommandVal.setText(str(self.tcPowerCommand))

        self.testbenchSetpointCommandVal.setText(str(self.tcSetpointCommand))

        self.testbenchAnnouncementVal.setText(self.tcAnnouncement)

        if  self.tcExternalLights == 1:
            self.testbenchExternalLightsButton.setText('ON')
            self.testbenchExternalLightsButton.setStyleSheet('background-color: black; color: white; border: 1px solid #666666')
        else:
            self.testbenchExternalLightsButton.setText('OFF')
            self.testbenchExternalLightsButton.setStyleSheet('background-color: #666666; color: white; border: 1px solid black')

        if  self.tcInternalLights == 1:
            self.testbenchInternalLightsButton.setText('ON')
            self.testbenchInternalLightsButton.setStyleSheet('background-color: black; color: white; border: 1px solid #666666')
        else:
            self.testbenchInternalLightsButton.setText('OFF')
            self.testbenchInternalLightsButton.setStyleSheet('background-color: #666666; color: white; border: 1px solid black')

        if  self.tcLeftDoor == 1:
            self.testbenchDoorLeft.setText('OPEN')
            self.testbenchDoorLeft.setStyleSheet('background-color: black; color: white; border: 1px solid #666666')
        else:
            self.testbenchDoorLeft.setText('CLOSED')
            self.testbenchDoorLeft.setStyleSheet('background-color: #666666; color: white; border: 1px solid black')

        if  self.tcRightDoor == 1:
            self.testbenchDoorRight.setText('OPEN')
            self.testbenchDoorRight.setStyleSheet('background-color: black; color: white; border: 1px solid #666666')
        else:
            self.testbenchDoorRight.setText('CLOSED')
            self.testbenchDoorRight.setStyleSheet('background-color: #666666; color: white; border: 1px solid black')

        self.testbenchSetpointTempVal.setText(str(self.tcSetpointTemp))

        if  self.tcAdvertisement == 1:
            self.testbenchAdvertisementButton.setText('ON')
            self.testbenchAdvertisementButton.setStyleSheet('background-color: black; color: white; border: 1px solid #666666')
        else:
            self.testbenchAdvertisementButton.setText('OFF')
            self.testbenchAdvertisementButton.setStyleSheet('background-color: #666666; color: white; border: 1px solid black')

    def displayTime(self):
        currentTime = QTime.currentTime()
        displayText = currentTime.toString('hh:mm:ss')
        self.systemClock.setText(displayText)

    def systemSpeedUp(self):
        #self.systemBaseSpeed = self.systemBaseSpeed + 0.25
        #self.timer.start(1000 * self.systemBaseSpeed)
        print('SYSTEM INTERVAL: ' + str(self.systemBaseSpeed))
    def systemSlowDown(self):
        #if self.systemBaseSpeed <= 0.25:
         #   return
        #self.systemBaseSpeed = self.systemBaseSpeed - 0.25
        #self.timer.start(1000 * self.systemBaseSpeed)
        print('SYSTEM INTERVAL: ' + str(self.systemBaseSpeed))


# create app
app = QApplication(sys.argv)

# create window instance
window = MainWindow()

# run app
app.exec()
