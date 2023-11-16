import sys, re, os
import pandas as pd

# from PyQt5.QtCore import pyqtSignal
from signals import (
    trackControllerToCTC,
    trackControllerToTrackModel,
    ctcToTrackController,
    masterSignals,
)
from signals import (
    trackControllerToCTC,
    trackControllerToTrackModel,
    ctcToTrackController,
    masterSignals,
)
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

        try:
            with open(filename, "r") as file:
                for line in file:
                    line = line.strip()

                    if line.startswith("SW") or line.startswith("CRX"):
                        currentSection = line
                        sections = []
                        ifBlock = 0
                    elif line == "IF":
                        insideIf = True
                        operations = []  # Initialize operations list for this IF block
                    elif insideIf and line.startswith("Condition"):
                        condition = line.split(":")[1].strip()
                    elif insideIf and line.startswith("Operation"):
                        operation = line.split(":")[1].strip()
                        operations.append(operation)
                    elif insideIf and line == "end":
                        sections.append(
                            {
                                "Section": currentSection,
                                "IfBlock": ifBlock,
                                "Condition": condition,
                                "Operations": operations,
                            }
                        )
                        ifBlock = ifBlock + 1
                    elif line == "END" and insideIf:
                        data.append(sections)
                        insideIf = False
        except Exception as e:
            print(f"An error occurred while parsing the file: {e}")
            # You can choose to continue or raise an exception here if needed

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
        # print(self.plcData)
        self.refresh_plc()

    def refresh_plc(self):
        # print("refreshing...")
        # check if it is in manual mode and exit the refresh if so
        if not self.plcState:
            return

        for item in self.plcData:
            # Initialize a flag to track if any condition is satisfied
            any_condition_satisfied = False

            for ifBlock in range(0, len(item)):
                switchString = item[ifBlock]["Section"].rstrip(":")
                if switchString in self.switches:
                    # Determine what is the switch block
                    switchBlock = self.get_block(self.switches[switchString])
                else:
                    continue

                # Parse the conditions
                condition = item[ifBlock]["Condition"]

                entry, exitRange, notExist = self.parse_condition(condition)
                condition1 = False
                condition2 = False

                # check for validity of conditon 1
                if isinstance(entry, int):
                    entry = [entry]  # Convert single integer to a list

                # print("Wayside Number: ", self.waysideNum)

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
                if exitRange != None:
                    for block in exitRange:
                        if exitRange == None:
                            condition2 = True
                            break

                        elif self.get_block(block).get_occupancystate() == True:
                            condition2 = True
                            break
                else:
                    condition2 = True
                    # print("Here I set the condition2 to true")

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
                for operation in item[ifBlock]["Operations"]:
                    parsedOperation = self.parse_operation(operation)
                    # set the switch value
                    if parsedOperation["Type"] == "SWITCH":
                        switchValue = int(parsedOperation["Value"])

                        switchBlock.set_switchstate(switchValue)

                        # emit that a switch value has been changed to the Track Model
                        trackControllerToTrackModel.switchState.emit(
                            self.line,
                            self.waysideNum,
                            self.switches[switchString],
                            switchValue,
                        )
                        # emit that the switch value has bene changed to the CTC
                        trackControllerToCTC.switchState.emit(self.line, self.switches[switchString], switchValue)

                    # set the light value
                    elif parsedOperation["Type"] == "SIGNAL":
                        signalNumber = parsedOperation["Number"]
                        # print("The number is: " + str(signalNumber))
                        # print("The wayside is: " + str(self.waysideNum))
                        signalState = parsedOperation["State"]
                        if signalState == "G":
                            signalState = "green"
                        elif signalState == "R":
                            signalState = "red"

                        self.get_block(signalNumber).set_lightstate(signalState)
                        # print(self.line, self.waysideNum, signalNumber, signalState)
                        # emit that a light value has been changed
                        trackControllerToTrackModel.lightState.emit(
                            self.line, self.waysideNum, int(signalNumber), signalState
                        )

                    # Set the crossing value
                    elif parsedOperation["Type"] == "CROSS":
                        crossValue = int(parsedOperation["Value"])
                        crossNumber = parsedOperation["Number"]

                        self.get_block(crossNumber).set_crosssingstate(crossValue)

                        # called again after the handler
                        # emit that a switch value has been changed
                        trackControllerToTrackModel.crossingState.emit(
                            self.line,
                            self.waysideNum,
                            crossNumber,
                            switchValue,
                        )

    # This is the method that parses the condition of a section within a PLC file
    def parse_condition(self, condition):
        entry = []
        exit = []
        notExist = False

        patterns = {
            "patternEntry": r"^(\d+)$",
            "patternEntryRange": r"^\((\d+)->(\d+)\)$",
            "patternEntryReverseRange": r"^\((\d+)<-(\d+)\)$",
            "patternEntryAndExitRange": r"^(\d+) AND \((\d+)->(\d+)\)$",
            "patternEntryAndExitReverseRange": r"^(\d+) AND \((\d+)<-(\d+)\)$",
            "patternEntryRangeAndExit": r"^\((\d+)->(\d+)\) AND (\d+)$",
            "patternEntryRangeAndExitRange": r"^\((\d+)->(\d+)\) AND \((\d+)->(\d+)\)$",
            "patternEntryReverseRangeAndExitRange": r"^\((\d+)<-(\d+)\) AND \((\d+)->(\d+)\)$",
            "patternEntryRangeAndExitReverseRange": r"^\((\d+)->(\d+)\) AND \((\d+)<-(\d+)\)$",
            "patternEntryReverseRangeAndExitReverseRange": r"^\((\d+)<-(\d+)\) AND \((\d+)<-(\d+)\)$",
            "patternEntryAndNotExitRange": r"^(\d+) AND NOT\((\d+)->(\d+)\)$",
            "patternEntryAndNotExitReverseRange": r"^(\d+) AND NOT\((\d+)<-(\d+)\)$",
            "patternEntryRangeAndNotExit": r"^\((\d+)->(\d+)\) AND NOT(\d+)$",
            "patternEntryRangeAndNotExitRange": r"^\((\d+)->(\d+)\) AND NOT\((\d+)->(\d+)\)$",
            "patternEntryReverseRangeAndNotExitRange": r"^\((\d+)<-(\d+)\) AND NOT\((\d+)->(\d+)\)$",
            "patternEntryRangeAndNotExitReverseRange": r"^\((\d+)->(\d+)\) AND NOT\((\d+)<-(\d+)\)$",
            "patternEntryReverseRangeAndNotExitReverseRange": r"^\((\d+)<-(\d+)\) AND NOT\((\d+)<-(\d+)\)$",
        }

        for pattern, regex in patterns.items():
            match = re.match(regex, condition)
            if match:
                if pattern == "patternEntry":
                    entry = [int(match.group(1))]
                    exit = None
                    notExist = False
                    break
                elif pattern == "patternEntryRange":
                    start, end = map(int, match.groups())
                    entry = list(range(start, end + 1))
                    exit = None
                    notExist = False
                    break
                elif pattern == "patternEntryReverseRange":
                    end, start = map(int, match.groups())
                    entry = list(range(start, end - 1, -1))
                    exit = None
                    notExist = False
                    break
                elif pattern == "patternEntryAndExitRange":
                    entry = [int(match.group(1))]
                    exit = list(range(int(match.group(2)), int(match.group(3)) + 1))
                    notExist = False
                    break
                elif pattern == "patternEntryAndExitReverseRange":
                    entry = [int(match.group(1))]
                    exit = list(range(int(match.group(3)), int(match.group(2)) + 1))
                    notExist = False
                    break
                elif pattern == "patternEntryRangeAndExit":
                    entry = list(range(int(match.group(1)), int(match.group(2)) + 1))
                    exit = [int(match.group(3))]
                    notExist = False
                    break
                elif pattern == "patternEntryRangeAndExitRange":
                    entry = list(range(int(match.group(1)), int(match.group(2)) + 1))
                    exit = list(range(int(match.group(3)), int(match.group(4)) + 1))
                    notExist = False
                    break
                elif pattern == "patternEntryReverseRangeAndExitRange":
                    entry = list(range(int(match.group(2)), int(match.group(1)) + 1))
                    exit = list(range(int(match.group(3)), int(match.group(4)) + 1))
                    notExist = False
                    break
                elif pattern == "patternEntryRangeAndExitReverseRange":
                    entry = list(range(int(match.group(1)), int(match.group(2)) + 1))
                    exit = list(range(int(match.group(3)), int(match.group(4)) + 1))
                    notExist = False
                    break
                elif pattern == "patternEntryReverseRangeAndExitReverseRange":
                    entry = list(range(int(match.group(2)), int(match.group(1)) + 1))
                    exit = list(range(int(match.group(4)), int(match.group(3)) + 1))
                    notExist = False
                    break
                elif pattern == "patternEntryAndNotExitRange":
                    entry = [int(match.group(1))]
                    exit = list(range(int(match.group(2)), int(match.group(3)) + 1))
                    notExist = True
                    break
                elif pattern == "patternEntryAndNotExitReverseRange":
                    entry = [int(match.group(1))]
                    exit = list(range(int(match.group(3)), int(match.group(2)) + 1))
                    notExist = True
                    break
                elif pattern == "patternEntryRangeAndNotExit":
                    entry = list(range(int(match.group(1)), int(match.group(2)) + 1))
                    exit = [int(match.group(3))]
                    notExist = True
                    break
                elif pattern == "patternEntryRangeAndNotExitRange":
                    entry = list(range(int(match.group(1)), int(match.group(2)) + 1))
                    exit = list(range(int(match.group(3)), int(match.group(4)) + 1))
                    notExist = True
                    break
                elif pattern == "patternEntryReverseRangeAndNotExitRange":
                    entry = list(range(int(match.group(2)), int(match.group(1)) + 1))
                    exit = list(range(int(match.group(3)), int(match.group(4)) + 1))
                    notExist = True
                    break
                elif pattern == "patternEntryRangeAndNotExitReverseRange":
                    entry = list(range(int(match.group(1)), int(match.group(2)) + 1))
                    exit = list(range(int(match.group(3)), int(match.group(4)) + 1))
                    notExist = True
                    break
                elif pattern == "patternEntryReverseRangeAndNotExitReverseRange":
                    entry = list(range(int(match.group(1)), int(match.group(2)) + 1))
                    exit = list(range(int(match.group(3)), int(match.group(4)) + 1))
                    notExist = True
                    break

        # print("Entry: ", entry)
        # print("Exit: ", exit)
        return entry, exit, notExist

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
        # print(self.blocks[28].get_number())
        # print("Did not find block " + str(blockNumber))
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
        if self.waysideNum == 2:
            print("Block State: ", self.get_block(0).get_occupancystate())
        for block in self.blocks:
            if block.get_occupancystate() == True:
                occupiedBlocks.append(block)
        # print("Here are the occupied blocks: ", occupiedBlocks)
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
        self.ui.show()

        # Instantiate the track information for the Green Line
        self.greenLine = Line(1)
        self.wayside1G = Wayside(1, 1)
        switchDict = {"SW1": 12, "SW2": 29}
        self.wayside1G.switches_init(switchDict)
        self.wayside2G = Wayside(2, 1)
        switchDict = {"SW3": 57, "SW4": 62, "SW5": 77, "SW6": 85}
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

        self.godWaysideGreen = Wayside(0, 1)

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
                    self.godWaysideGreen.add_block(block)
                if i == 1:
                    wayside = self.redLine.get_wayside(int(waysideController[-2]))

                wayside.add_block(block)

        # Load the default plc programs for all wayside controllers
        self.wayside1G.run_plc("src/main/TrackController/plc_green.txt")
        self.wayside2G.run_plc("src/main/TrackController/plc_green.txt")
        # self.wayside1R.run_plc("src/main/TrackController/plc_red.txt")
        # self.wayside2R.run_plc("src/main/TrackController/plc_red.txt")

        """ REFRESH THE PLCS FOR EACH WAYSIDE ON THE TIME INTERVAL """
        self.ui.timer.timeout.connect(lambda: self.wayside1G.refresh_plc())
        self.ui.timer.timeout.connect(lambda: self.wayside2G.refresh_plc())
        
       
        """ Connect handlers for GUI actions """
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
         # Connect the plc load button to its handler
        self.ui.plcImportButton.clicked.connect(lambda: self.import_plc())
        # Connect the open map button to its handler
        self.ui.buttonMap.clicked.connect(lambda: self.ui.buttonMap.on_button_click(self.ui.lineSelect))
        # Connect the automatic/manual mode button click to the wayside controller
        self.ui.buttonMode.clicked.connect(
            lambda: self.handle_mode(
                self.lines[self.ui.lineSelect - 1]
                .get_wayside(self.ui.waysideSelect)
                .get_plc_state()
            )
        )

        """ This section of code is for the connections from signals from the Track Controller to the handler"""
        trackControllerToTrackModel.switchState.connect(self.set_switchstate_handler)
        trackControllerToTrackModel.crossingState.connect(
            self.set_crossingstate_handler
        )
        trackControllerToTrackModel.lightState.connect(self.set_lightstate_handler)

        """ This section of code is for the connections from signals from the CTC to the handler"""
        ctcToTrackController.sendAuthority.connect(self.handle_authority)
        ctcToTrackController.sendSuggestedSpeed.connect(self.handle_suggested_speed)
        ctcToTrackController.sendTrainDispatched.connect(self.handle_dispatch)

        """ Connect the input signals from the test bench to the main ui page handlers """
        self.ui.testBenchWindow.requestInput.connect(self.handle_input_apply)


    def show_gui(self):
        self.ui.show()

    """ Handler methods for the CTC input signals (and internally change gui)"""
    def handle_authority(self, line, wayside, blockNum, authority):
        # set the authority value
        self.lines[line - 1].get_wayside(wayside).get_block(blockNum).set_authority(
            authority
        )
        # send signal to the track model
        trackControllerToTrackModel.authority.emit(line, wayside, blockNum, authority)
        self.ui.testBenchWindow.refreshed.emit(True)

    def handle_suggested_speed(self, line, wayside, blockNum, suggestedSpeed):
        print("Blocknum in handle suggested speed: ", blockNum)
        self.lines[line - 1].get_wayside(wayside).get_block(blockNum).set_suggestedspeed(suggestedSpeed)
        # send signal to the track model
        trackControllerToTrackModel.suggestedSpeed.emit(line, wayside, blockNum, suggestedSpeed)
        self.ui.testBenchWindow.refreshed.emit(True)

    def handle_dispatch(self, line, wayside, trainID, authority):
        #print("line #: ", line)
        #print("wayside #:, ", wayside)
        #print("trainID: ", trainID)
        #print("authority: ", authority)
        self.lines[line - 1].get_wayside(wayside).get_block(0).set_authority(authority)
        self.lines[line - 1].get_wayside(wayside).get_block(0).set_occupancystate(True)
        self.set_occupancystate_handler(line,wayside,0,True)
        self.ui.testBenchWindow.refreshed.emit(True)

    def handle_maintenance(self, line, wayside, num, state):
        self.lines[line - 1].get_wayside(wayside).get_block(num).set_maintenancestate(
            state
        )
        # check if the block is currently being displayed, if so, update the display accordingly
        blockNum = 0
        selectedItem = self.ui.comboboxBlockNum.currentText()
        if selectedItem != "Select State" and selectedItem != "":
            try:
                blockNum = int(selectedItem[6]) * 10 + int(selectedItem[7]) - 1
            except Exception as e:
                blockNum = -1
            
        if blockNum == (num):
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

        # send maintenance state signal to the track model
        trackControllerToTrackModel.maintenance.emit(line, wayside, num, state)
        self.ui.testBenchWindow.refreshed.emit(True)

    def handle_failure(self, line, wayside, num, state):
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
    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """ Handler methods for the  Track Model input signals (and internally change gui) """
    def set_occupancystate_handler(self, line, wayside, num, state):
        self.lines[line - 1].get_wayside(wayside).get_block(num).set_occupancystate(
            state
        )

        # update the occupancy table
        if state == False:
            self.ui.occupancyBox.clear_table()
            blockList = self.lines[line - 1].get_wayside(wayside).get_occupied_blocks()
            for block in blockList:
                self.ui.occupancyBox.add_item(
                    block.get_number(), block.get_type(), block.get_failurestate()
                )

        #elif self.ui.occupancyBox.does_block_exist(num,self.lines[line - 1].get_wayside(wayside).get_block(num).get_failurestate()):
            
        
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
            #print("Pattern not matched")
            pass

        self.ui.testBenchWindow.refreshed.emit(True)
        """print("sending signal to CTC...")
        print("line: ", line)
        print("blocknumber: ", num)
        print("state: ", state)"""
        trackControllerToCTC.occupancyState.emit(line, int(num), state)
    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """ Handler methods for internal GUI """
        # Set state handlers
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

    def set_switchstate_handler(self, line, wayside, num, state):
        self.lines[line - 1].get_wayside(wayside).get_block(num).set_switchstate(state)
        # check if the block is currently being displayed, if so, update the display accordingly
        blockNum = -1
        selectedItem = self.ui.comboboxBlockNum.currentText()
        match = re.search(r"Block (\d+)(?: - Station)?", selectedItem)
        if match:
            blockNum = int(match.group(1))
            if blockNum == num:
                self.ui.junctionSwitch.set_switch_state(state)
        self.ui.testBenchWindow.refreshed.emit(True)

    def set_lightstate_handler(self, line, wayside, num, color):
        self.lines[line - 1].get_wayside(wayside).get_block(num).set_lightstate(color)
        # check if the block is currently being displayed, if so, update the display accordingly
        blockNum = -1
        selectedItem = self.ui.comboboxBlockNum.currentText()
        match = re.search(r"Block \d{1,3}", selectedItem)
        if match:
            try:
                blockNum = int(match.group(1))
            except Exception as e:
                pass
            else:
                if blockNum == num:
                    self.ui.lightState.set_state(color)
            self.ui.testBenchWindow.refreshed.emit(True)
        
    def set_direction_handler(self, line, wayside, num, direction):
        self.lines[line - 1].get_wayside(wayside).get_block(num).set_direction(
            direction
        )
        self.ui.testBenchWindow.refreshed.emit(True)

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
                #print(f"Block number: {blockNum}")
            else:
                # print("Pattern not matched")
                pass

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

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """ Main Testbench Input Handler """

    def handle_input_apply(self, action, line, blockNum, state):
        if action == 0:
            print("You must select an input action.")
            return

        if line == 0:
            print("You must select a line.")
            return

        # green line selected
        elif line == 1:
            print(int(blockNum))
            if not (int(blockNum) >= 0 and int(blockNum) <= 150):
                print("Enter a valid block number for the green line (0-150)")
                print("You entered: ", blockNum)
                return

            # call the block
            block = self.wayside1G.get_block(blockNum)
            waysideNum = 1
            if block == None:
                block = self.wayside2G.get_block(blockNum)
                waysideNum = 2

            # set switch state
            if action == 1:
                if state == "true" or state == "True" or state == "1":
                    finalState = True
                elif state == "false" or state == "False" or state == "0":
                    finalState = False
                else:
                    print("This is not a valid input for the state. (True/False)")
                    return

                try:
                    block.set_switchstate(finalState)
                except Exception as e:
                    print(
                        "This action cannot be performed on a block of type: ",
                        block.get_type(),
                    )
                else:
                    self.set_switchstate_handler(line, waysideNum, blockNum, finalState)

            # Set Crossing State
            elif action == 2:
                pass
            # Set Light State
            elif action == 3:
                pass
            # Set Maintenance State
            elif action == 4:
                pass
            # Set Occupancy State
            elif action == 5:
                if state == "true" or state == "True" or state == "1":
                    finalState = True
                elif state == "false" or state == "False" or state == "0":
                    finalState = False
                else:
                    print("This is not a valid input for the state. (True/False)")
                    return

                try:
                    block.set_occupancystate(finalState)
                except Exception as e:
                    print("This action cannot be performed on a block of type: ", None)
                else:
                    self.set_occupancystate_handler(
                        line, waysideNum, blockNum, finalState
                    )

            # Set Authority
            elif action == 6:
                if state == "true" or state == "True" or state == "1":
                    finalState = 1
                elif state == "false" or state == "False" or state == "0":
                    finalState = 0
                else:
                    print(
                        "This is not a valid input for the state. (True/False or 1/0)"
                    )
                    return

                try:
                    block.set_authority(finalState)
                except Exception as e:
                    print("This action cannot be performed on a block of type: ", None)
                else:
                    self.handle_authority(line, waysideNum, blockNum, finalState)

            # Set Suggested Speed
            elif action == 7:
                finalState = float(state)
                if finalState < 0 or finalState > block.get_speed():
                    print(
                        "This is not a valid input for the state. (Must range from 0 to block.get_speed)"
                    )
                    return

                try:
                    block.set_suggestedspeed(finalState)
                except Exception as e:
                    print("This action cannot be performed on a block of type: ", None)
                else:
                    self.handle_suggested_speed(line, waysideNum, blockNum, finalState)

            # Set Direction
            elif action == 8:
                pass

        elif line == 2:
            if not (blockNum >= 0 and blockNum <= 75):
                print("Enter a valid block number for the red line (0-75)")
                return


"""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # window = MainUI()
    # window.setGeometry(0,0,960,970)
    # window.show()
    main_window = TrackControl()
    sys.exit(app.exec_())  # Start the application event loop
"""
