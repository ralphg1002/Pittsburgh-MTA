import sys, re, os
import pandas as pd

# from PyQt5.QtCore import pyqtSignal
from signals import trackControllerToCTC, trackControllerToTrackModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from .trackcontrolui import MainUI


# plcSwitchChange = pyqtSignal(int, int, int, bool)
# plcLightChange = pyqtSignal(int, int, int, str)


class RunPLC:
    # Define a function to parse the text file
    def parse_text_file(self, filename):
        data = []  # List to store the parsed data
        currentSection = None  # Variable to track the current section
        insideIf = False  # Flag to indicate if we are inside an IF block
        condition = None
        operations = []  # List to store multiple operations

        with open(filename, "r") as file:
            for line in file:
                line = line.strip()

                if line.startswith("SW") or line.startswith("CRX"):
                    currentSection = line
                elif line == "IF":
                    insideIf = True
                    operations = []  # Initialize operations list for this IF block
                elif insideIf and line.startswith("Condition"):
                    condition = line.split(":")[1].strip()
                elif insideIf and line.startswith("Operation"):
                    operation = line.split(":")[1].strip()
                    operations.append(operation)
                elif line == "END" and insideIf:
                    data.append(
                        {
                            "Section": currentSection,
                            "Condition": condition,
                            "Operations": operations,
                        }
                    )
                    insideIf = False

        return data


class Block:
    def __init__(
        self,
        number,
        speed,
        authority,
        occupancyState,
        failureState,
        maintenanceState,
        direction,
    ):
        # Initialize the block variables
        self.speed = speed
        self.suggestedSpeed = speed
        self.authority = authority
        self.occupancyState = occupancyState
        self.failureState = failureState
        self.maintenanceState = maintenanceState
        self.direction = direction
        self.number = number

        # initialize authority variables
        self.ctcAuthority = None
        self.nextRedAuthority = None
        self.nextOccupiedBlockAuthority = None

    def get_number(self):
        return self.number

    def get_speed(self):
        return self.speed

    def set_speed(self, newSpeed):
        self.speed = newSpeed

    def get_authority(self):
        return self.authority

    def set_authority(self, newAuthority):
        self.authority = newAuthority

    def get_occupancystate(self):
        return self.occupancyState

    def set_occupancystate(self, newOccupancyState):
        self.occupancyState = newOccupancyState

    def get_failurestate(self):
        return self.failureState

    def set_failurestate(self, newFailureState):
        self.failureState = newFailureState

    def get_maintenancestate(self):
        return self.maintenanceState

    def set_maintenancestate(self, newMaintenanceState):
        self.maintenanceState = newMaintenanceState

    def get_direction(self):
        return self.direction

    def set_direction(self, newDirection):
        self.direction = newDirection

    def get_suggestedspeed(self):
        return self.suggestedSpeed

    def set_suggestedspeed(self, newSpeed):
        self.suggestedSpeed = newSpeed

    def get_type(self):
        return "plain"


class StationBlock(Block):
    def __init__(
        self,
        number,
        speed,
        authority,
        occupancyState,
        failureState,
        maintenanceState,
        direction,
        stationName,
    ):
        super().__init__(
            number,
            speed,
            authority,
            occupancyState,
            failureState,
            maintenanceState,
            direction,
        )
        # Initialize station name state variable
        self.stationName = stationName

    def get_stationname(self):
        return self.stationName

    def set_stationname(self, newStationName):
        self.stationName = newStationName

    def get_type(self):
        return "station"


class JunctionWSBlock(Block):
    def __init__(
        self,
        number,
        speed,
        authority,
        occupancyState,
        failureState,
        maintenanceState,
        direction,
        switchState,
        nextBlock0,
        nextBlock1,
        lightState,
    ):
        super().__init__(
            number,
            speed,
            authority,
            occupancyState,
            failureState,
            maintenanceState,
            direction,
        )
        # Initialize switch state and light state variables
        self.switchState = switchState
        self.lightState = lightState
        self.nextBlock0 = nextBlock0
        self.nextBlock1 = nextBlock1

    def get_switchstate(self):
        return self.switchState

    def set_switchstate(self, newSwitchState):
        self.switchState = newSwitchState

    def get_lightstate(self):
        return self.lightState

    def set_lightstate(self, newLightState):
        self.lightState = newLightState

    def get_type(self):
        return "junctionWS"

    def get_connected(self):
        return [self.nextBlock0, self.nextBlock1]


class JunctionNSBlock(Block):
    def __init__(
        self,
        number,
        speed,
        authority,
        occupancyState,
        failureState,
        maintenanceState,
        direction,
        lightState,
    ):
        super().__init__(
            number,
            speed,
            authority,
            occupancyState,
            failureState,
            maintenanceState,
            direction,
        )
        # Initialize light state variable
        self.lightState = lightState

    def get_lightstate(self):
        return self.lightState

    def set_lightstate(self, newLightState):
        self.lightState = newLightState

    def get_type(self):
        return "junctionNS"


class CrossingBlock(Block):
    def __init__(
        self,
        number,
        speed,
        authority,
        occupancyState,
        failureState,
        maintenanceState,
        direction,
        crossingState,
        lightState,
    ):
        super().__init__(
            number,
            speed,
            authority,
            occupancyState,
            failureState,
            maintenanceState,
            direction,
        )
        # Initialize crossing state variable
        self.crossingState = crossingState
        self.lightState = lightState

    def get_crossingstate(self):
        return self.crossingState

    def set_crossingstate(self, newSwitchState):
        self.crossingState = newSwitchState

    def get_lightstate(self):
        return self.lightState

    def set_lightstate(self, newLightState):
        self.lightState = newLightState

    def get_type(self):
        return "crossing"


class StationJunctionNSBlock(Block):
    def __init__(
        self,
        number,
        speed,
        authority,
        occupancyState,
        failureState,
        maintenanceState,
        direction,
        stationName,
        lightState,
    ):
        super().__init__(
            number,
            speed,
            authority,
            occupancyState,
            failureState,
            maintenanceState,
            direction,
        )
        # Initialize station name state variable
        self.stationName = stationName
        self.lightState = lightState

    def get_stationname(self):
        return self.stationName

    def set_stationname(self, newStationName):
        self.stationName = newStationName

    def get_type(self):
        return "stationJunctionNS"

    def get_lightstate(self):
        return self.lightState

    def set_lightstate(self, newLightState):
        self.lightState = newLightState


class StationJunctionWSBlock(Block):
    def __init__(
        self,
        number,
        speed,
        authority,
        occupancyState,
        failureState,
        maintenanceState,
        direction,
        stationName,
        switchState,
        nextBlock0,
        nextBlock1,
        lightState,
    ):
        super().__init__(
            number,
            speed,
            authority,
            occupancyState,
            failureState,
            maintenanceState,
            direction,
        )
        # Initialize station name state variable
        self.stationName = stationName
        self.lightState = lightState
        self.switchState = switchState
        self.nextBlock0 = nextBlock0
        self.nextBlock1 = nextBlock1

    def get_stationname(self):
        return self.stationName

    def set_stationname(self, newStationName):
        self.stationName = newStationName

    def get_type(self):
        return "stationJunctionWS"

    def get_lightstate(self):
        return self.lightState

    def set_lightstate(self, newLightState):
        self.lightState = newLightState

    def get_switchstate(self):
        return self.switchState

    def set_switchstate(self, newSwitchState):
        self.switchState = newSwitchState

    def get_connected(self):
        return [self.nextBlock0, self.nextBlock1]


class Wayside:
    # initialize array which will hold all of the blocks
    # that the wayside controller is responsible for
    # initialization method
    def __init__(self, waysideNumber, line):
        self.blocks = []
        self.waysideNum = waysideNumber
        self.plc = RunPLC()
        self.switches = {}
        self.line = line
        self.plcData = None
        self.plcState = True

    def switches_init(self, switchDictionary):
        self.switches = switchDictionary

    # Method for adding blocks to the block array
    def add_block(self, block):
        self.blocks.append(block)

    # get wayside number method
    def get_waysidenum(self):
        return self.waysideNum

    def get_line(self):
        return self.line

    def set_plc_state(self, mode):
        self.plcState = mode

    def get_plc_state(self):
        return self.plcState

    # This is the method that reads the PLC file and runs it accordingly
    def run_plc(self, plcFilepath):
        self.plcData = self.plc.parse_text_file(plcFilepath)
        self.refresh_plc()

    def refresh_plc(self):
        # check if it is in manual mode and exit the refresh if so
        if not self.plcState:
            return

        for item in self.plcData:
            print("Evaluating Section:", item["Section"])
            print("Condition:", item["Condition"])

            switchString = item["Section"].rstrip(":")
            if switchString in self.switches:
                # Determine what is the switch block
                switchBlock = self.get_block(self.switches[switchString])
            else:
                continue

            # Parse the conditions
            conditions = item["Condition"].split(" AND ")

            # Initialize a flag to track if any condition is satisfied
            any_condition_satisfied = False

            # Loop through each condition
            for condition in conditions:
                entry, notExist, exitRange = self.parse_condition(condition)
                condition1 = False
                condition2 = False

                # check for validity of conditon 1
                if isinstance(entry, int):
                    entry = [entry]  # Convert single integer to a list

                print(entry)

                if entry != 0:
                    # check for validity of conditon 1
                    for block in entry:
                        if self.get_block(block).get_occupancystate() == True:
                            condition1 = True
                            break
                else:
                    if self.get_block(0).get_occupancystate() == True:
                        condition1 = True

                # check for validity of condition 2
                for block in exitRange:
                    if not exitRange:
                        condition2 = True
                        break

                    if self.get_block(block).get_occupancystate() == True:
                        condition2 = True
                        break

                if condition2 == True and notExist:
                    condition2 = False
                elif condition2 == False and notExist:
                    condition2 = True

                # If both condition 1 and 2 are valid, set the flag and break the loop
                if condition1 and condition2:
                    any_condition_satisfied = True
                    break

            # If any condition is satisfied, execute the operations
            if any_condition_satisfied:
                for operation in item["Operations"]:
                    parsedOperation = self.parse_operation(operation)
                    # set the switch value
                    if parsedOperation["Type"] == "SWITCH":
                        switchValue = int(parsedOperation["Value"])

                        switchBlock.set_switchstate(switchValue)
                        switchBlock.set_switchstate(switchValue)

                        # emit that a switch value has been changed
                        trackControllerToTrackModel.switchState.emit(
                            self.line,
                            self.waysideNum,
                            self.switches[switchString],
                            switchValue,
                        )

                    # set the light value
                    elif parsedOperation["Type"] == "SIGNAL":
                        signalNumber = parsedOperation["Number"]
                        print("The number is: " + str(signalNumber))
                        print("The wayside is: " + str(self.waysideNum))
                        signalState = parsedOperation["State"]
                        if signalState == "G":
                            signalState = "green"
                        elif signalState == "R":
                            signalState = "red"

                        self.get_block(signalNumber).set_lightstate(signalState)
                        self.get_block(signalNumber).set_lightstate(signalState)
                        # emit that a light value has been changed
                        trackControllerToTrackModel.lightState.emit(
                            self.line, self.waysideNum, signalNumber, signalState
                        )

                    # Set the crossing value
                    elif parsedOperation["Type"] == "CROSS":
                        crossValue = int(parsedOperation["Value"])
                        crossNumber = parsedOperation["Number"]

                        # 2x redundancy
                        self.get_block(crossNumber).set_crosssingstate(crossValue)
                        self.get_block(crossNumber).set_crosssingstate(crossValue)

                        # called again after the handler
                        # emit that a switch value has been changed
                        trackControllerToTrackModel.crossingState.emit(
                            self.line,
                            self.waysideNum,
                            crossNumber,
                            switchValue,
                        )

        # call the authority function to set authorities throughout the map
        """
        This section of code will deal with the authority of the system for each block that is occupied and send it to the track model
        This will be calculated using block occupancy, light states, and suggested authority from the CTC.
        """

        # Loop through every block that the wayside controller has jurisdiction over
        for block in self.blocks:
            # check for occupancy of block
            if block.get_occupancystate() == True:
                pass

    # This is the method that parses the condition of a section within a PLC file
    def parse_condition(self, condition):
        entry = []
        notExist = False
        exitRange = []

        # Regular expressions to match the various patterns
        patternEntry = r"^(\d+)$"
        patternEntryRange = r"^(\d+)->(\d+)$"
        patternEntryReverseRange = r"^(\d+)<-(\d+)$"
        patternExitRange = r"^\((\d+)->(\d+)\)$"
        patternAndNotExitRange = r"^(\d+) AND NOT\((\d+)->(\d+)\)$"
        patternAndExitRange = r"^\((\d+)->(\d+)\) AND \((\d+)->(\d+)\)$"
        patternAndNotReverseExitRange = r"^\((\d+)->(\d+)\) AND NOT\((\d+)->(\d+)\)$"

        if re.match(patternEntry, condition):
            entry = [int(condition)]
        elif re.match(patternEntryRange, condition):
            match = re.match(patternEntryRange, condition)
            entry = list(range(int(match.group(1)), int(match.group(2)) + 1))
        elif re.match(patternEntryReverseRange, condition):
            match = re.match(patternEntryReverseRange, condition)
            entry = list(range(int(match.group(1)), int(match.group(2)) - 1, -1))
        elif re.match(patternExitRange, condition):
            match = re.match(patternExitRange, condition)
            exitRange = list(range(int(match.group(1)), int(match.group(2)) + 1))
        elif re.match(patternAndNotExitRange, condition):
            match = re.match(patternAndNotExitRange, condition)
            entry = [int(match.group(1))]
            notExist = True
            exitRange = list(range(int(match.group(2)), int(match.group(3)) + 1))
        elif re.match(patternAndExitRange, condition):
            match = re.match(patternAndExitRange, condition)
            exitRange.extend(range(int(match.group(1)), int(match.group(2)) + 1))
            exitRange.extend(range(int(match.group(3)), int(match.group(4)) + 1))
        elif re.match(patternAndNotReverseExitRange, condition):
            match = re.match(patternAndNotReverseExitRange, condition)
            notExist = True
            exitRange.extend(range(int(match.group(2)), int(match.group(1)) + 1))
            exitRange.extend(range(int(match.group(3)), int(match.group(4)) + 1))

        return entry, notExist, exitRange

    # This is the method that parses the operation following a condition within a PLC file
    def parse_operation(self, operationLine):
        if operationLine.startswith("SWITCH"):
            switchValue = operationLine.split("(")[1].strip(")")
            if switchValue in ["0", "1"]:
                return {"Type": "SWITCH", "Value": int(switchValue)}
        elif operationLine.endswith(" G"):
            return {"Type": "SIGNAL", "Number": operationLine.split()[0], "State": "G"}
        elif operationLine.endswith(" R"):
            return {"Type": "SIGNAL", "Number": operationLine.split()[0], "State": "R"}

    # get block by number
    def get_block(self, blockNumber):
        for block in self.blocks:
            if int(block.get_number()) == int(blockNumber):
                return block
        print(self.blocks[28].get_number())
        print("Did not find block " + str(blockNumber))
        return None  # Block not found

    # Function to get blocks of a specific type
    def get_blocks_by_type(self, blockType):
        matchingBlocks = []
        for block in self.blocks:
            if block.get_type() == blockType:
                matchingBlocks.append(block)
        return matchingBlocks

    def get_occupied_blocks(self):
        occupiedBlocks = []
        for block in self.blocks:
            if block.get_occupancystate == True:
                occupiedBlocks.append(block)
        print(occupiedBlocks)
        return occupiedBlocks


class Line:
    # initialize array which will hold all the waysides per line
    def __init__(self, trackID):
        self.waysides = []
        self.trackID = trackID

    def add_wayside(self, wayside):
        self.waysides.append(wayside)

    # Function to get the Wayside object based on an integer
    def get_wayside(self, waysideNumber):
        for wayside in self.waysides:
            if wayside.get_waysidenum() == waysideNumber:
                return wayside
        return None  # Return None if no matching Wayside is found


class TrackControl(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = MainUI()
        self.ui.setGeometry(0, 0, 960, 960)
        self.ui.hide()

        # Instantiate the track information for the Green Line
        self.greenLine = Line(1)
        self.wayside1G = Wayside(1, 1)
        switchDict = {"SW1": 12, "SW2": 29, "SW3": 58}
        self.wayside1G.switches_init(switchDict)
        self.wayside2G = Wayside(2, 1)
        switchDict = {"SW4": 62, "SW5": 77, "SW6": 85}
        self.wayside2G.switches_init(switchDict)
        self.greenLine.add_wayside(self.wayside1G)
        self.greenLine.add_wayside(self.wayside2G)

        # Instantiate the track information for the Red Line
        self.redLine = Line(2)
        self.wayside1R = Wayside(1, 2)
        switchDict = {"SW1": 9, "SW2": 16, "SW3": 27}
        self.wayside1R.switches_init(switchDict)
        self.wayside2R = Wayside(2, 2)
        switchDict = {"SW4": 33, "SW5": 38, "SW6": 44, "SW7": 52}
        self.wayside2R.switches_init(switchDict)
        self.redLine.add_wayside(self.wayside1R)
        self.redLine.add_wayside(self.wayside2R)

        self.lines = [self.greenLine, self.redLine]

        # Create a dictionary to map infrastructure types to block classes
        blockMapping = {
            "junctionNS": JunctionNSBlock,
            "station": StationBlock,
            "junctionWS": JunctionWSBlock,
            "crossing": CrossingBlock,
            "stationJunctionNS": StationJunctionNSBlock,
            "stationJunctionWS": StationJunctionWSBlock,
        }

        # Read the Excel file
        for i in range(2):
            if i == 0:
                df = pd.read_excel("src/main/TrackController/greenLine.xlsx")
            elif i == 1:
                df = pd.read_excel("src/main/TrackController/redLine.xlsx")

            # Iterate through the rows of the DataFrame
            for index, row in df.iterrows():
                waysideController = row.iloc[0]
                speedLimit = int(row.iloc[1])
                blockNumber = int(row.iloc[2])
                infrastructureData = str(row.iloc[3]).split(
                    ";"
                )  # Ensure that data in the fourth column is treated as a string

                # Extract the block class and its parameters based on the infrastructure type
                blockClass = blockMapping.get(infrastructureData[0], Block)

                # Create the block object
                if infrastructureData[0] == "station":
                    block = blockClass(
                        blockNumber,
                        speedLimit,
                        0,
                        False,
                        False,
                        False,
                        0,
                        infrastructureData[1],
                    )
                elif infrastructureData[0] == "stationJunctionNS":
                    block = blockClass(
                        blockNumber,
                        speedLimit,
                        0,
                        False,
                        False,
                        False,
                        0,
                        infrastructureData[1],
                        infrastructureData[2],
                    )
                elif infrastructureData[0] == "stationJunctionWS":
                    block = blockClass(
                        blockNumber,
                        speedLimit,
                        0,
                        False,
                        False,
                        False,
                        0,
                        infrastructureData[1],
                        int(infrastructureData[2]),
                        int(infrastructureData[3]),
                        int(infrastructureData[4]),
                        infrastructureData[5],
                    )
                elif infrastructureData[0] == "junctionWS":
                    block = blockClass(
                        blockNumber,
                        speedLimit,
                        0,
                        False,
                        False,
                        False,
                        0,
                        int(infrastructureData[1]),
                        int(infrastructureData[2]),
                        int(infrastructureData[3]),
                        infrastructureData[4],
                    )
                elif infrastructureData[0] == "junctionNS":
                    block = blockClass(
                        blockNumber,
                        speedLimit,
                        0,
                        False,
                        False,
                        False,
                        0,
                        infrastructureData[1],
                    )
                elif infrastructureData[0] == "crossing":
                    block = blockClass(
                        blockNumber,
                        speedLimit,
                        0,
                        False,
                        False,
                        False,
                        0,
                        int(infrastructureData[1]),
                        (infrastructureData[2]),
                    )
                else:
                    block = blockClass(
                        blockNumber,
                        speedLimit,
                        0,
                        False,
                        False,
                        False,
                        0,
                    )

                # Append the block to the specified wayside controller
                if i == 0:
                    wayside = self.greenLine.get_wayside(int(waysideController[-2]))
                if i == 1:
                    wayside = self.redLine.get_wayside(int(waysideController[-2]))

                wayside.add_block(block)

        # Load the default plc programs for all wayside controllers
        self.wayside1G.run_plc("src/main/TrackController/plc_green.txt")
        self.wayside2G.run_plc("src/main/TrackController/plc_green.txt")
        # self.wayside1R.run_plc("src/main/TrackController/plc_red.txt")
        # self.wayside2R.run_plc("src/main/TrackController/plc_red.txt")

        # Connect the plc load button to its handler
        self.ui.plcImportButton.clicked.connect(lambda: self.import_plc())

        # Connect the open map button to its handler
        self.ui.buttonMap.clicked.connect(lambda: self.handle_map())

        # Connect the automatic/manual mode button click to the wayside controller
        self.ui.buttonMode.clicked.connect(
            lambda: self.handle_mode(
                self.lines[self.ui.lineSelect - 1]
                .get_wayside(self.ui.waysideSelect)
                .get_plc_state()
            )
        )

        # Connect the signal (currentIndexChanged) to display the proper mode in the GUI
        self.ui.comboboxWayside.currentIndexChanged.connect(
            self.handle_selection_wayside
        )

        # Connect the signal (currentIndexChanged) to the slot (handle_selection)
        self.ui.comboboxBlockType.currentIndexChanged.connect(
            lambda: self.handle_selection_block_type()
        )
        # Connect the signal (currentIndexChanged) to the slot (handle_selection)
        self.ui.comboboxBlockNum.currentIndexChanged.connect(
            lambda: self.handle_selection_blocknum()
        )

        # Connect output signals to the track model to also call the switch state handler
        trackControllerToTrackModel.switchState.connect(self.set_switchstate_handler)

        trackControllerToTrackModel.crossingState.connect(
            self.set_crossingstate_handler
        )

        # connect the input signals from the test bench to the main ui page handlers
        # self.ui.testBenchWindow.setSwitchState.connect(self.set_switchstate_handler)
        self.ui.testBenchWindow.setLightState.connect(self.set_lightstate_handler)
        self.ui.testBenchWindow.setFailureState.connect(self.set_failurestate_handler)
        self.ui.testBenchWindow.setMaintenanceState.connect(
            self.set_maintenancestate_handler
        )
        # self.ui.testBenchWindow.setOccupancyState.connect(self.set_occupancystate_handler)
        self.ui.testBenchWindow.setOccupancyState.connect(
            lambda line, wayside, num, state: self.set_occupancystate_handler(
                line, wayside, num, state
            )
        )
        self.ui.testBenchWindow.setAuthority.connect(self.set_authoritystate_handler)
        self.ui.testBenchWindow.setSpeed.connect(self.set_speed_handler)
        self.ui.testBenchWindow.setDirection.connect(self.set_direction_handler)

        # connect the output signal requests from the test bench and send the values back
        self.ui.testBenchWindow.requestViewSwitchState.connect(
            lambda line, wayside, num: self.ui.testBenchWindow.returnViewSwitchState.emit(
                str(
                    self.lines[line - 1]
                    .get_wayside(wayside)
                    .get_block(num)
                    .get_switchstate()
                )
            )
        )
        self.ui.testBenchWindow.requestViewLightState.connect(
            lambda line, wayside, num: self.ui.testBenchWindow.returnViewLightState.emit(
                str(
                    self.lines[line - 1]
                    .get_wayside(wayside)
                    .get_block(num)
                    .get_lightstate()
                )
            )
        )
        self.ui.testBenchWindow.requestViewFailureState.connect(
            lambda line, wayside, num: self.ui.testBenchWindow.returnViewFailureState.emit(
                str(
                    self.lines[line - 1]
                    .get_wayside(wayside)
                    .get_block(num)
                    .get_failurestate()
                )
            )
        )
        self.ui.testBenchWindow.requestViewMaintenanceState.connect(
            lambda line, wayside, num: self.ui.testBenchWindow.returnViewMaintenanceState.emit(
                str(
                    self.lines[line - 1]
                    .get_wayside(wayside)
                    .get_block(num)
                    .get_maintenancestate()
                )
            )
        )
        self.ui.testBenchWindow.requestViewOccupancyState.connect(
            lambda line, wayside, num: self.ui.testBenchWindow.returnViewOccupancyState.emit(
                str(
                    self.lines[line - 1]
                    .get_wayside(wayside)
                    .get_block(num)
                    .get_occupancystate()
                )
            )
        )
        self.ui.testBenchWindow.requestViewAuthority.connect(
            lambda line, wayside, num: self.ui.testBenchWindow.returnViewAuthority.emit(
                str(
                    self.lines[line - 1]
                    .get_wayside(wayside)
                    .get_block(num)
                    .get_authority()
                )
            )
        )
        self.ui.testBenchWindow.requestViewSpeed.connect(
            lambda line, wayside, num: self.ui.testBenchWindow.returnViewSpeed.emit(
                str(
                    self.lines[line - 1].get_wayside(wayside).get_block(num).get_speed()
                )
            )
        )
        self.ui.testBenchWindow.requestViewDirection.connect(
            lambda line, wayside, num: self.ui.testBenchWindow.returnViewDirection.emit(
                str(
                    self.lines[line - 1]
                    .get_wayside(wayside)
                    .get_block(num)
                    .get_direction()
                )
            )
        )

    def show_gui(self):
        self.ui.show()

    # This method is called whenever the import plc button is clicked
    def import_plc(self):
        if self.ui.waysideSelect == 0 or self.ui.lineSelect == 0:
            print("You must select a track and wayside controller first!")
            return

        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "All Files (*);;Text Files (*.txt)", options=options
        )

        if filePath:
            self.filePath = filePath
            fileName = os.path.basename(filePath)  # Extract just the filename
            print(f"Selected file: {fileName}")
            self.lines[self.ui.lineSelect - 1].get_wayside(
                self.ui.waysideSelect
            ).run_plc(filePath)

    # Method to disable or enable the PLC program for the wayside when the mode is switched to automatic or manual mode
    def handle_mode(self, mode):
        mode = not mode
        print("Button Clicked: " + str(mode))
        self.lines[self.ui.lineSelect - 1].get_wayside(
            self.ui.waysideSelect
        ).set_plc_state(mode)

    # This is the method and code for the wayside device selection combo box handler
    def handle_selection_wayside(self, index):
        # Set the next selections to index of 0
        self.ui.comboboxBlockType.setCurrentIndex(0)
        self.ui.comboboxBlockNum.setCurrentIndex(0)

        # reset the window if a new selection is made
        self.ui.hide_devices()
        self.ui.occupancyBox.clear_table()

        selectedItem = self.ui.comboboxWayside.currentText()
        if selectedItem == "Select Wayside Controller":
            # Clear the options for the next combo boxes
            self.ui.comboboxBlockType.clear()
            self.ui.comboboxBlockNum.clear()

        else:
            self.ui.waysideSelect = self.ui.comboboxWayside.currentIndex()
            self.ui.comboboxBlockType.clear()
            self.ui.comboboxBlockType.addItem("Select Block Type")
            if (
                selectedItem == "Wayside 1 (A - J), (S - Z)"
                or selectedItem == "Wayside 2 (H - Q)"
            ):
                self.ui.comboboxBlockType.addItem("Crossing")
            self.ui.comboboxBlockType.addItem("Station")
            self.ui.comboboxBlockType.addItem("Junction w/Switch")
            self.ui.comboboxBlockType.addItem("Junction w/o Switch")
            self.ui.comboboxBlockType.addItem("Plain")

        if self.ui.waysideSelect != 0 and self.ui.waysideSelect != -1:
            self.ui.buttonMode.set_button_style(
                self.lines[self.ui.lineSelect - 1]
                .get_wayside(self.ui.waysideSelect)
                .get_plc_state()
            )
            temporaryWayside = self.lines[self.ui.lineSelect - 1].get_wayside(
                self.ui.waysideSelect
            )

            blockList = temporaryWayside.get_occupied_blocks()
            for block in blockList:
                self.ui.occupancyBox.add_item(
                    block.get_number(), block.get_type(), block.get_failurestate()
                )

            self.ui.buttonMode.set_button_style(
                self.lines[self.ui.lineSelect - 1]
                .get_wayside(self.ui.waysideSelect)
                .get_plc_state()
            )

    # This is the method and code for the block type selection combo box handler
    def handle_selection_block_type(self):
        if self.ui.lineSelect == 1:
            tempWayside = self.greenLine.get_wayside(self.ui.waysideSelect)
        elif self.ui.lineSelect == 2:
            tempWayside = self.redLine.get_wayside(self.ui.waysideSelect)

        self.ui.hide_devices()
        self.ui.comboboxBlockNum.setCurrentIndex(0)
        selectedItem = self.ui.comboboxBlockType.currentText()
        self.ui.comboboxBlockNum.clear()

        if selectedItem == "Select Block Type":
            self.ui.comboboxBlockNum.clear()

        elif selectedItem == "Station":
            self.ui.comboboxBlockNum.clear()
            self.ui.blockTypeSelect = "station"

            self.ui.comboboxBlockNum.addItem("Select Block #")
            tempBlocks = tempWayside.get_blocks_by_type("station")
            tempBlocks.extend(tempWayside.get_blocks_by_type("stationJunctionWS"))
            tempBlocks.extend(tempWayside.get_blocks_by_type("stationJunctionNS"))
            for item in tempBlocks:
                self.ui.comboboxBlockNum.addItem(
                    "Block " + str(item.get_number()) + " - " + item.get_stationname()
                )

        elif selectedItem == "Junction w/Switch":
            self.ui.blockTypeSelect = "junctionWS"
            self.ui.comboboxBlockNum.addItem("Select Block #")
            tempBlocks = tempWayside.get_blocks_by_type("junctionWS")
            tempBlocks.extend(tempWayside.get_blocks_by_type("stationJunctionWS"))
            for item in tempBlocks:
                self.ui.comboboxBlockNum.addItem("Block " + str(item.get_number()))

        elif selectedItem == "Junction w/o Switch":
            self.ui.blockTypeSelect = "junctionNS"
            self.ui.comboboxBlockNum.addItem("Select Block #")
            tempBlocks = tempWayside.get_blocks_by_type("junctionNS")
            tempBlocks.extend(tempWayside.get_blocks_by_type("stationJunctionNS"))
            for item in tempBlocks:
                self.ui.comboboxBlockNum.addItem("Block " + str(item.get_number()))

        elif selectedItem == "Crossing":
            self.ui.blockTypeSelect = "crossing"
            self.ui.comboboxBlockNum.addItem("Select Block #")
            tempBlocks = tempWayside.get_blocks_by_type("crossing")
            for item in tempBlocks:
                self.ui.comboboxBlockNum.addItem("Block " + str(item.get_number()))

        elif selectedItem == "Plain":
            self.ui.blockTypeSelect = "plain"
            self.ui.comboboxBlockNum.addItem("Select Block #")
            tempBlocks = tempWayside.get_blocks_by_type("plain")
            for item in tempBlocks:
                self.ui.comboboxBlockNum.addItem("Block " + str(item.get_number()))

    # This is the method and code for the block number selection combo box handler
    def handle_selection_blocknum(self):
        if self.ui.lineSelect == 1:
            tempWayside = self.greenLine.get_wayside(self.ui.waysideSelect)
        elif self.ui.lineSelect == 2:
            tempWayside = self.redLine.get_wayside(self.ui.waysideSelect)

        selectedItem = self.ui.comboboxBlockNum.currentText()
        self.ui.hide_devices()

        self.ui.lightState.lightChanged.connect(lambda: print(""))
        # Disconnect all lightState.lightChanged signals
        self.ui.lightState.lightChanged.disconnect()

        if selectedItem == "Select Block #" or selectedItem == "":
            # Do nothing or perform an action for the placeholder text
            pass
        else:
            match = re.search(r"Block (\d+)(?: - Station)?", selectedItem)
            if match:
                blockNum = int(match.group(1))
                print(f"Block number: {blockNum}")
            else:
                print("Pattern not matched")

            tempBlock = tempWayside.get_block(blockNum)
            blockType = self.ui.blockTypeSelect

            if tempBlock.get_maintenancestate() == False:
                if tempBlock.get_occupancystate() == True:
                    self.ui.blockStatus.set_status("Occupied")
                else:
                    self.ui.blockStatus.set_status("Unoccupied")
            else:
                self.ui.blockStatus.set_status("Maintenance")

            if blockType == "plain":
                self.ui.blockStatus.show()

            elif blockType == "junctionWS":
                self.ui.lightState.show()
                self.ui.blockStatus.show()
                self.ui.junctionSwitch.set_switch_state(tempBlock.get_switchstate())
                self.ui.lightState.set_state(tempBlock.get_lightstate())

                self.ui.junctionSwitch.update_button_visibility(
                    self.lines[self.ui.lineSelect - 1]
                    .get_wayside(self.ui.waysideSelect)
                    .get_plc_state()
                )

                self.ui.junctionSwitch.set_text_box(
                    blockNum, tempBlock.get_connected()[0], tempBlock.get_connected()[1]
                )
                self.ui.junctionSwitch.show()

                self.ui.junctionSwitch.get_signal().connect(
                    lambda: tempBlock.set_switchstate(not tempBlock.get_switchstate())
                )
                self.ui.lightState.lightChanged.connect(tempBlock.set_lightstate)

                # Pass signals on to the track model
                trackControllerToTrackModel.switchState.emit(
                    self.ui.lineSelect,
                    self.ui.waysideSelect,
                    tempBlock.get_number(),
                    tempBlock.get_switchstate(),
                )
                trackControllerToTrackModel.lightState.emit(
                    self.ui.lineSelect,
                    self.ui.waysideSelect,
                    tempBlock.get_number(),
                    tempBlock.get_lightstate(),
                )

            elif blockType == "junctionNS":
                self.ui.blockStatus.show()
                # lightBox.shift_middle()
                # lightState.shift_middle()
                self.ui.lightState.set_state(tempBlock.get_lightstate())
                self.ui.lightState.show()
                self.ui.lightState.lightChanged.connect(tempBlock.set_lightstate)
                # Pass signal on to the track model
                trackControllerToTrackModel.lightState.emit(
                    self.ui.lineSelect,
                    self.ui.waysideSelect,
                    tempBlock.get_number(),
                    tempBlock.get_lightstate(),
                )

            elif blockType == "station":
                # blockStatus.shift_middle()
                self.ui.deviceBlock.show()
                self.ui.blockStatus.show()
                self.ui.station.set_station_name(tempBlock.get_stationname())
                self.ui.station.show_station()
                self.ui.station.show()

            elif blockType == "crossing":
                # blockStatus.shift_middle()
                # self.ui.deviceBlock.show()
                self.ui.blockStatus.show()
                self.ui.crossing.set_crossing_state(tempBlock.get_crossingstate())
                self.ui.crossing.show_crossing()
                self.ui.lightState.show()

                self.ui.crossing.switchCrossChanged.connect(
                    lambda: tempBlock.set_crossingstate(
                        not tempBlock.get_crossingstate()
                    )
                )

                self.ui.lightState.set_state(tempBlock.get_lightstate())

                self.ui.lightState.lightChanged.connect(tempBlock.set_lightstate)

                # Pass signals on to the track model
                trackControllerToTrackModel.crossingState.emit(
                    self.ui.lineSelect,
                    self.ui.waysideSelect,
                    tempBlock.get_number(),
                    tempBlock.get_crossingstate(),
                )
                trackControllerToTrackModel.lightState.emit(
                    self.ui.lineSelect,
                    self.ui.waysideSelect,
                    tempBlock.get_number(),
                    tempBlock.get_lightstate(),
                )

    # These are the handle methods for the set states
    def set_switchstate_handler(self, line, wayside, num, state):
        self.lines[line - 1].get_wayside(wayside).get_block(num).set_switchstate(state)
        # check if the block is currently being displayed, if so, update the display accordingly
        blockNum = 0
        selectedItem = self.ui.comboboxBlockNum.currentText()
        match = re.search(r"Block (\d+)(?: - Station)?", selectedItem)
        if match:
            blockNum = int(match.group(1))
            if blockNum == num:
                self.ui.junctionSwitch.set_switch_state(state)
        self.ui.testBenchWindow.refreshed.emit(True)

    def set_crossingstate_handler(self, line, wayside, num, state):
        self.lines[line - 1].get_wayside(wayside).get_block(num).set_crossingstate(
            state
        )
        # check if the block is currently being displayed, if so, update the display accordingly
        blockNum = 0
        selectedItem = self.ui.comboboxBlockNum.currentText()
        match = re.search(r"Block (\d+)(?: - Station)?", selectedItem)
        if match:
            blockNum = int(match.group(1))
            if blockNum == num:
                self.ui.crossing.set_crossing_state(state)
        self.ui.testBenchWindow.refreshed.emit(True)

    def set_occupancystate_handler(self, line, wayside, num, state):
        self.lines[line - 1].get_wayside(wayside).get_block(num).set_occupancystate(
            state
        )
        self.lines[line - 1].get_wayside(wayside).refresh_plc()
        # update the occupancy table
        if state == False:
            self.ui.occupancyBox.remove_item_by_blocknumber(num)
        elif self.ui.occupancyBox.does_block_exist(
            num,
            self.lines[line - 1].get_wayside(wayside).get_block(num).get_failurestate(),
        ):
            pass
        elif state:
            blockStr = "Block {}".format(num)
            self.ui.occupancyBox.add_item(
                blockStr,
                self.lines[line - 1].get_wayside(wayside).get_block(num).get_type(),
                str(
                    self.lines[line - 1]
                    .get_wayside(wayside)
                    .get_block(num)
                    .get_failurestate()
                ),
            )

        # check if the block is currently being displayed, if so, update the display accordingly
        selectedItem = self.ui.comboboxBlockNum.currentText()
        match = re.search(r"Block (\d+)(?: - Station)?", selectedItem)
        if match:
            blockNum = int(match.group(1))
            print(f"Block number: {blockNum}")
            if blockNum == num:
                if (
                    self.lines[line - 1]
                    .get_wayside(wayside)
                    .get_block(num)
                    .get_maintenancestate()
                ):
                    pass
                elif state:
                    self.ui.blockStatus.set_status("Occupied")
                else:
                    self.ui.blockStatus.set_status("Unoccupied")
        else:
            print("Pattern not matched")

        self.ui.testBenchWindow.refreshed.emit(True)

        trackControllerToCTC.occupancyState.emit(line, num, state)

    def set_lightstate_handler(self, line, wayside, num, color):
        self.lines[line - 1].get_wayside(wayside).get_block(num).set_lightstate(color)
        # check if the block is currently being displayed, if so, update the display accordingly
        blockNum = 0
        selectedItem = self.ui.comboboxBlockNum.currentText()
        if selectedItem != "Select State" and selectedItem != "":
            blockNum = int(selectedItem[6]) * 10 + int(selectedItem[7]) - 1
        if blockNum == (num - 1):
            self.ui.lightState.set_state(color)
        self.ui.testBenchWindow.refreshed.emit(True)

    def set_failurestate_handler(self, line, wayside, num, state):
        self.lines[line - 1].get_wayside(wayside).get_block(num).set_failurestate(state)

        # update the occupancy table
        if self.ui.occupancyBox.does_block_and_state_exist(num, state):
            pass
        elif (
            state
            or self.lines[line - 1]
            .get_wayside(wayside)
            .get_block(num)
            .get_occupancystate()
        ):
            self.ui.occupancyBox.remove_item_by_blockNumber(num)
            blockStr = "Block {}".format(num)
            self.ui.occupancyBox.add_item(
                blockStr,
                self.lines[line - 1].get_wayside(wayside).get_block(num).get_type(),
                str(
                    self.lines[line - 1]
                    .get_wayside(wayside)
                    .get_block(num)
                    .get_failurestate()
                ),
            )
        else:
            self.ui.occupancyBox.remove_item_by_blockNumber(num)

        # check if the block is currently being displayed, if so, update the display accordingly
        blockNum = 0
        selectedItem = self.ui.comboboxBlockNum.currentText()
        if selectedItem != "Select State" and selectedItem != "":
            blockNum = int(selectedItem[6]) * 10 + int(selectedItem[7]) - 1
        if blockNum == (num - 1):
            if (
                self.lines[line - 1]
                .get_wayside(wayside)
                .get_block(num)
                .get_maintenancestate()
                == False
                and state
            ):
                self.ui.blockStatus.set_status("Occupied")
            elif not state:
                self.ui.blockStatus.set_status("Unoccupied")
        self.ui.testBenchWindow.refreshed.emit(True)

    def set_maintenancestate_handler(self, line, wayside, num, state):
        self.lines[line - 1].get_wayside(wayside).get_block(num).set_maintenancestate(
            state
        )
        # check if the block is currently being displayed, if so, update the display accordingly
        blockNum = 0
        selectedItem = self.ui.comboboxBlockNum.currentText()
        if selectedItem != "Select State" and selectedItem != "":
            blockNum = int(selectedItem[6]) * 10 + int(selectedItem[7]) - 1
        if blockNum == (num - 1):
            if state:
                self.ui.blockStatus.set_status("Maintenance")
            elif (
                self.lines[line - 1]
                .get_wayside(wayside)
                .get_block(num)
                .get_occupancystate()
            ):
                self.ui.blockStatus.set_status("Occupied")
            else:
                self.ui.blockStatus.set_status("Unoccupied")
        self.ui.testBenchWindow.refreshed.emit(True)

    def set_authoritystate_handler(self, line, wayside, num, authority):
        self.lines[line - 1].get_wayside(wayside).get_block(num).set_authority(
            authority
        )
        self.ui.testBenchWindow.refreshed.emit(True)

    def set_speed_handler(self, line, wayside, num, speed):
        self.lines[line - 1].get_wayside(wayside).get_block(num).set_speed(speed)
        self.ui.testBenchWindow.refreshed.emit(True)

    def set_direction_handler(self, line, wayside, num, direction):
        self.lines[line - 1].get_wayside(wayside).get_block(num).set_direction(
            direction
        )
        self.ui.testBenchWindow.refreshed.emit(True)

    def set_suggested_authority_handler(self, line, wayside, num, suggestedAuthority):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # window = MainUI()
    # window.setGeometry(0,0,960,970)
    # window.show()
    main_window = TrackControl()
    sys.exit(app.exec_())  # Start the application event loop
