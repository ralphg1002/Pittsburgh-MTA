import pandas as pd
from .Station import Station
from signals import (
    trackControllerToTrackModel,
    trainModelToTrackModel,
    ctcToTrackModel,
    trackModelToCTC,
    trackModelToTrainModel,
    trackModelToTrackController,
)


class TrackData:
    redTrackData = {}
    greenTrackData = {}

    def __init__(self):
        self.redTrackData = self.read_track_data(
            "src\main\TrackModel\Track Layout & Vehicle Data vF2.xlsx", "Red Line"
        )
        self.greenTrackData = self.read_track_data(
            "src\main\TrackModel\Track Layout & Vehicle Data vF2.xlsx", "Green Line"
        )

        # From CTC
        ctcToTrackModel.requestThroughput.connect(self.get_ticket_sales)

        # From Wayside
        trackControllerToTrackModel.suggestedSpeed.connect(self.set_suggested_speed)
        trackControllerToTrackModel.authority.connect(self.set_authority)
        trackControllerToTrackModel.maintenance.connect(self.set_maintenance)

        trackControllerToTrackModel.switchState.connect(self.set_switch_state)
        trackControllerToTrackModel.lightState.connect(self.set_light_state)
        trackControllerToTrackModel.crossingState.connect(self.set_crossing_state)

        # From Train Model
        trainModelToTrackModel.sendCurrentPassengers.connect(self.update_station_data)
        trainModelToTrackModel.sendPolarity.connect(self.send_block_data)

    def read_track_data(self, filePath, lineName):
        excelData = pd.read_excel(filePath, sheet_name=lineName)
        if lineName == "Red Line":
            data = excelData.head(76).to_dict(orient="records")
        elif lineName == "Green Line":
            data = excelData.head(150).to_dict(orient="records")
        self.initialize_data(data, lineName)
        return data

    def initialize_data(self, data, lineName):
        # Set default values for track
        for block in data:
            block["Failures"] = ["None"]
            block["Occupancy"] = 0
            block["Maintenance"] = False
            block["Suggested Speed"] = 0
            block["Authority"] = 0
            # Initialize all infrastructure data
            if type(block["Infrastructure"]) == str:
                if "STATION" in block["Infrastructure"]:
                    block["Ticket Sales"] = 0
                    block["Passengers Waiting"] = 0
                    block["Passengers Boarding"] = 0
                    block["Passengers Disembarking"] = 0
                if "SWITCH" in block["Infrastructure"]:
                    block["Switch State"] = 0
                if "RAILWAY CROSSING" in block["Infrastructure"]:
                    block["Crossing State"] = 0
            if lineName == "Green Line":
                if block["Block Number"] == 2:  # Section A, Pioneer
                    block["Beacon"] = {
                        "Next Station1": "STATION",
                        "Next Station2": "",
                        "Current Station": "PIONEER",
                        "Door Side": block["Station Side"],
                    }
                elif block["Block Number"] == 9:  # Section C, Edgebrook
                    block["Beacon"] = {
                        "Next Station1": "PIONEER",
                        "Next Station2": "",
                        "Current Station": "EDGEBROOK",
                        "Door Side": block["Station Side"],
                    }
                elif block["Block Number"] == 16:  # Section D, Station
                    block["Beacon"] = {
                        "Next Station1": "EDGEBROOK",
                        "Next Station2": "WHITED",
                        "Current Station": "STATION",
                        "Door Side": block["Station Side"],
                    }
                elif block["Block Number"] == 22:  # Section F, Whited
                    block["Beacon"] = {
                        "Next Station1": "STAION",
                        "Next Station2": "SOUTH BANK",
                        "Current Station": "WHITED",
                        "Door Side": block["Station Side"],
                    }
                elif block["Block Number"] == 31:  # Section G, South Bank
                    block["Beacon"] = {
                        "Next Station1": "CENTRAL",
                        "Next Station2": "",
                        "Current Station": "SOUTH BANK",
                        "Door Side": block["Station Side"],
                    }
                elif block["Block Number"] == 39:  # Section I, Central
                    block["Beacon"] = {
                        "Next Station1": "INGLEWOOD",
                        "Next Station2": "",
                        "Current Station": "CENTRAL",
                        "Door Side": block["Station Side"],
                    }
                elif block["Block Number"] == 48:  # Section I, Inglewood
                    block["Beacon"] = {
                        "Next Station1": "OVERBROOK",
                        "Next Station2": "",
                        "Current Station": "INGLEWOOD",
                        "Door Side": block["Station Side"],
                    }
                elif block["Block Number"] == 57:  # Section I, Overbrook
                    block["Beacon"] = {
                        "Next Station1": "GLENBURY",
                        "Next Station2": "",
                        "Current Station": "OVERBROOK",
                        "Door Side": block["Station Side"],
                    }
                elif block["Block Number"] == 65:  # Section K, Glenbury
                    block["Beacon"] = {
                        "Next Station1": "DORMONT",
                        "Next Station2": "",
                        "Current Station": "GLENBURY",
                        "Door Side": block["Station Side"],
                    }
                elif block["Block Number"] == 73:  # Section L, Dormont
                    block["Beacon"] = {
                        "Next Station1": "MT LEBANON",
                        "Next Station2": "",
                        "Current Station": "DORMONT",
                        "Door Side": block["Station Side"],
                    }
                elif block["Block Number"] == 77:  # Section N, Mt Lebanon
                    block["Beacon"] = {
                        "Next Station1": "POPULAR",
                        "Next Station2": "DORMONT",
                        "Current Station": "MT LEBANON",
                        "Door Side": block["Station Side"],
                    }
                elif block["Block Number"] == 88:  # Section O, Poplar
                    block["Beacon"] = {
                        "Next Station1": "CASTLE SHANNON",
                        "Next Station2": "MT LEBANON",
                        "Current Station": "POPLAR",
                        "Door Side": block["Station Side"],
                    }
                elif block["Block Number"] == 96:  # Section P, Castle Shannon
                    block["Beacon"] = {
                        "Next Station1": "MT LEBANON",
                        "Next Station2": "",
                        "Current Station": "CASTLE SHANNON",
                        "Door Side": block["Station Side"],
                    }
                elif block["Block Number"] == 105:  # Section T, Dormont
                    block["Beacon"] = {
                        "Next Station1": "GLENBURY",
                        "Next Station2": "",
                        "Current Station": "DORMONT",
                        "Door Side": block["Station Side"],
                    }
                elif block["Block Number"] == 114:  # Section U, Glenbury
                    block["Beacon"] = {
                        "Next Station1": "OVERBROOK",
                        "Next Station2": "",
                        "Current Station": "GLENBURY",
                        "Door Side": block["Station Side"],
                    }
                elif block["Block Number"] == 123:  # Section W, Overbrook
                    block["Beacon"] = {
                        "Next Station1": "INGLEWOOD",
                        "Next Station2": "",
                        "Current Station": "OVERBROOK",
                        "Door Side": block["Station Side"],
                    }
                elif block["Block Number"] == 132:  # Section W, Inglewood
                    block["Beacon"] = {
                        "Next Station1": "CENTRAL",
                        "Next Station2": "",
                        "Current Station": "INGLEWOOD",
                        "Door Side": block["Station Side"],
                    }
                elif block["Block Number"] == 141:  # Section W, Central
                    block["Beacon"] = {
                        "Next Station1": "WHITED",
                        "Next Station2": "",
                        "Current Station": "CENTRAL",
                        "Door Side": block["Station Side"],
                    }

    def set_data(self, line, data):
        if line == "Red":
            self.redTrackData = data
            for block in self.redTrackData:
                print(block["Failures"])
        elif line == "Green":
            self.greenTrackData = data
            for block in self.greenTrackData:
                print(block["Failures"])

    def get_data(self, line):
        if line == "Red":
            return self.redTrackData
        return self.greenTrackData

    def update_station_data(self, line, stationName, currentPassengers):
        # stationName must be caps
        station = Station()

        print(line, stationName, currentPassengers)
        # print(self.greenTrackData)
        if line == "Red":
            for block in self.redTrackData:
                if type(block["Infrastructure"]) == str:
                    if stationName in block["Infrastructure"]:
                        ticketSales = (
                            station.get_ticket_sales()
                        )  # random number generated
                        block["Ticket Sales"] += ticketSales

                        waiting = block["Passengers Waiting"] + ticketSales
                        (
                            disembarkingPassengers,
                            newPassengers,
                            passengersWaiting,
                        ) = station.get_passenger_exchange(currentPassengers, waiting)

                        block["Passengers Disembarking"] = disembarkingPassengers
                        block["Passengers Boarding"] = newPassengers
                        block["Passengers Waiting"] = passengersWaiting

                        trackModelToTrainModel.newCurrentPassengers.emit(newPassengers)

                        # blockNumber = block["Block Number"]
                        # for block in self.
                        # if stationName in block["Infrastructure"] and blockNumber != block["Block Number"]:
                        #     print(f"Another Block Found: {block['Block Number']}")
                        # return
        elif line == "Green":
            for block in self.greenTrackData:
                # print(block["Block Number"])
                if type(block["Infrastructure"]) == str:
                    if stationName in block["Infrastructure"]:
                        ticketSales = (
                            station.get_ticket_sales()
                        )  # random number generated
                        tempTicketSales = block["Ticket Sales"]
                        tempTicketSales += ticketSales
                        block["Ticket Sales"] = tempTicketSales
                        print(block["Ticket Sales"])

                        waiting = block["Passengers Waiting"] + ticketSales
                        (
                            disembarkingPassengers,
                            newPassengers,
                            passengersWaiting,
                        ) = station.get_passenger_exchange(currentPassengers, waiting)

                        block["Passengers Disembarking"] = disembarkingPassengers
                        block["Passengers Boarding"] = newPassengers
                        block["Passengers Waiting"] = passengersWaiting
                        print(
                            ticketSales,
                            passengersWaiting,
                            disembarkingPassengers,
                            newPassengers,
                        )

                        trackModelToTrainModel.newCurrentPassengers.emit(newPassengers)

                        # Check if another block has the same station
                        blockNumRepeat = block["Block Number"]
                        for block in self.greenTrackData:
                            if type(block["Infrastructure"]) == str:
                                if stationName in block["Infrastructure"] and block["Block Number"] != blockNumRepeat:
                                    print(f"Another Block Found: {block['Block Number']}")
                                    block["Ticket Sales"] = tempTicketSales
                                    block["Passengers Disembarking"] = disembarkingPassengers
                                    block["Passengers Boarding"] = newPassengers
                                    block["Passengers Waiting"] = passengersWaiting
                                    print(
                                        block["Ticket Sales"],
                                        block["Passengers Waiting"],
                                        block["Passengers Disembarking"],
                                        block["Passengers Boarding"]                                        
                                    )
                                    return                      

    def get_ticket_sales(self, line):
        greenRepeats = [105, 114, 123, 132, 141] # Avoid double counted ticket sales
        throughput = 0  # Reset
        if line == "Red":
            for block in self.redTrackData:
                if type(block["Infrastructure"]) == str:
                    if "STATION" in block["Infrastructure"]:
                        throughput += block["Ticket Sales"]
                        block["Ticket Sales"] = 0  # Reset
        elif line == "Green":
            for block in self.greenTrackData:
                if type(block["Infrastructure"]) == str:
                    if "STATION" in block["Infrastructure"] and block["Block Number"] not in greenRepeats:
                        throughput += block["Ticket Sales"]
                        block["Ticket Sales"] = 0  # Reset
                        print(f"block num: {block['Block Number']}")
                    elif "STATION" in block["Infrastructure"] and block["Block Number"] in greenRepeats:
                        block["Ticket Sales"] = 0  # Reset
        print("SENDING THROUGHPUT", throughput)
        trackModelToCTC.throughput.emit(throughput)

    def set_suggested_speed(self, line, _, blockNum, suggestedSpeed):
        if line == 1:
            for block in self.greenTrackData:
                if block["Block Number"] == blockNum:
                    block["Suggested Speed"] == suggestedSpeed
        elif line == 2:
            for block in self.redTrackData:
                if block["Block Number"] == blockNum:
                    block["Suggested Speed"] == suggestedSpeed

    def set_authority(self, line, _, blockNum, authority):
        if line == 1:
            for block in self.greenTrackData:
                if block["Block Number"] == blockNum:
                    block["Authority"] == authority
        elif line == 2:
            for block in self.redTrackData:
                if block["Block Number"] == blockNum:
                    block["Authority"] == authority

    def set_maintenance(self, line, _, blockNum, maintenance):
        if line == 1:
            for block in self.greenTrackData:
                if block["Block Number"] == blockNum:
                    block["Maintenance"] == maintenance
        elif line == 2:
            for block in self.redTrackData:
                if block["Block Number"] == blockNum:
                    block["Maintenance"] == maintenance

    def set_switch_state(self, line, _, blockNum, state):
        # # Initial Green Line Occupancy
        # if blockNum == 62 and state == 1 and line == 1:
        #     self.send_block_data("Green", 0, 999)
        # # Initial Red Line Occupancy
        # elif blockNum == 9 and state == 1 and line == 2:
        #     self.send_block_data("Red", 0, 999)
        if line == 1:
            for block in self.greenTrackData:
                if block["Block Number"] == blockNum:
                    block["Switch State"] = state
        elif line == 2:
            for block in self.redTrackData:
                if block["Block Number"] == blockNum:
                    block["Switch State"] == state

    def set_light_state(self, line, _, blockNum, state):
        if line == 1:
            for block in self.greenTrackData:
                if block["Block Number"] == blockNum:
                    block["Light State"] = state
        elif line == 2:
            for block in self.redTrackData:
                if block["Block Number"] == blockNum:
                    block["Light State"] == state
        print(line, blockNum, state)

    def set_crossing_state(self, line, _, blockNum, state):
        if line == 1:
            for block in self.greenTrackData:
                if block["Block Number"] == blockNum:
                    block["Crossing State"] = state
        elif line == 2:
            for block in self.redTrackData:
                if block["Block Number"] == blockNum:
                    block["Crossing State"] == state

    def send_block_data(self, line, curBlock, prevBlock):
        greenBeforeStation = [3, 10, 30, 38, 47, 56, 64, 72, 87, 95, 113, 122, 131, 140]
        if line == "Green":
            # Regular block data emission
            if curBlock == 999 and prevBlock == 999:
                trackModelToTrainModel.blockInfo.emit(0, 0, 0, 0, 0, 0)
                trackModelToTrackController.occupancyState.emit(
                            1,
                            self.get_wasyside_num(0),
                            0,
                            True,
                        )
            elif curBlock == 0 and prevBlock == 999:
                # Set first block's occupancy, no need to clear any occupancy
                for block in self.greenTrackData:
                    if block["Block Number"] == 63:
                        trackModelToTrainModel.blockInfo.emit(
                            block["Block Number"],
                            block["Block Length (m)"],
                            block["Block Grade (%)"],
                            block["Speed Limit (Km/Hr)"],
                            block["Suggested Speed"],
                            block["Authority"],
                        )
                        trackModelToTrackController.occupancyState.emit(
                            1,
                            self.get_wasyside_num(block["Block Number"]),
                            block["Block Number"],
                            True,
                        )
                        trackModelToTrackController.occupancyState.emit(
                            1, self.get_wasyside_num(curBlock), curBlock, False
                        )
                        block["Occupancy"] = 1
            else:
                # Clear occupancy of previous block
                for block in self.greenTrackData:
                    if block["Block Number"] == curBlock:
                        block["Occupancy"] = 0
            if curBlock == 1:
                for block in self.greenTrackData:
                    if block["Block Number"] == 13:
                        trackModelToTrainModel.blockInfo.emit(
                            block["Block Number"],
                            block["Block Length (m)"],
                            block["Block Grade (%)"],
                            block["Speed Limit (Km/Hr)"],
                            block["Suggested Speed"],
                            block["Authority"],
                        )
                        trackModelToTrackController.occupancyState.emit(
                            1,
                            self.get_wasyside_num(block["Block Number"]),
                            block["Block Number"] - 1,
                            True,
                        )
                        trackModelToTrackController.occupancyState.emit(
                            1, self.get_wasyside_num(curBlock), curBlock - 1, False
                        )
                        block["Occupancy"] = 1
            elif curBlock == 100:
                for block in self.greenTrackData:
                    if block["Block Number"] == 85:
                        trackModelToTrainModel.blockInfo.emit(
                            block["Block Number"],
                            block["Block Length (m)"],
                            block["Block Grade (%)"],
                            block["Speed Limit (Km/Hr)"],
                            block["Suggested Speed"],
                            block["Authority"],
                        )
                        trackModelToTrackController.occupancyState.emit(
                            1,
                            self.get_wasyside_num(block["Block Number"]),
                            block["Block Number"] - 1,
                            True,
                        )
                        trackModelToTrackController.occupancyState.emit(
                            1, self.get_wasyside_num(curBlock), curBlock - 1, False
                        )
                        block["Occupancy"] = 1
            elif curBlock == 77 and prevBlock == 78:
                for block in self.greenTrackData:
                    if block["Block Number"] == 101:
                        trackModelToTrainModel.blockInfo.emit(
                            block["Block Number"],
                            block["Block Length (m)"],
                            block["Block Grade (%)"],
                            block["Speed Limit (Km/Hr)"],
                            block["Suggested Speed"],
                            block["Authority"],
                        )
                        trackModelToTrackController.occupancyState.emit(
                            1,
                            self.get_wasyside_num(block["Block Number"]),
                            block["Block Number"] - 1,
                            True,
                        )
                        trackModelToTrackController.occupancyState.emit(
                            1, self.get_wasyside_num(curBlock), curBlock - 1, False
                        )
                        block["Occupancy"] = 1
            elif curBlock == 150:
                for block in self.greenTrackData:
                    if block["Block Number"] == 28:
                        trackModelToTrainModel.blockInfo.emit(
                            block["Block Number"],
                            block["Block Length (m)"],
                            block["Block Grade (%)"],
                            block["Speed Limit (Km/Hr)"],
                            block["Suggested Speed"],
                            block["Authority"],
                        )
                        trackModelToTrackController.occupancyState.emit(
                            1,
                            self.get_wasyside_num(block["Block Number"]),
                            block["Block Number"] - 1,
                            True,
                        )
                        trackModelToTrackController.occupancyState.emit(
                            1, self.get_wasyside_num(curBlock), curBlock - 1, False
                        )
                        block["Occupancy"] = 1
            elif curBlock > prevBlock:
                for block in self.greenTrackData:
                    if block["Block Number"] == curBlock + 1:
                        trackModelToTrainModel.blockInfo.emit(
                            block["Block Number"],
                            block["Block Length (m)"],
                            block["Block Grade (%)"],
                            block["Speed Limit (Km/Hr)"],
                            block["Suggested Speed"],
                            block["Authority"],
                        )
                        trackModelToTrackController.occupancyState.emit(
                            1,
                            self.get_wasyside_num(block["Block Number"]),
                            block["Block Number"] - 1,
                            True,
                        )
                        trackModelToTrackController.occupancyState.emit(
                            1, self.get_wasyside_num(curBlock), curBlock - 1, False
                        )
                        block["Occupancy"] = 1
            elif curBlock < prevBlock:
                for block in self.greenTrackData:
                    if block["Block Number"] == curBlock - 1:
                        trackModelToTrainModel.blockInfo.emit(
                            block["Block Number"],
                            block["Block Length (m)"],
                            block["Block Grade (%)"],
                            block["Speed Limit (Km/Hr)"],
                            block["Suggested Speed"],
                            block["Authority"],
                        )
                        trackModelToTrackController.occupancyState.emit(
                            1,
                            self.get_wasyside_num(block["Block Number"]),
                            block["Block Number"] - 1,
                            True,
                        )
                        trackModelToTrackController.occupancyState.emit(
                            1, self.get_wasyside_num(curBlock), curBlock - 1, False
                        )
                        block["Occupancy"] = 1
            # Beacon data emission below
            if curBlock in greenBeforeStation:
                if prevBlock > curBlock:
                    for block in self.greenTrackData:
                        if block["Block Number"] == curBlock - 1:
                            trackModelToTrainModel.beacon.emit(block["Beacon"])
                elif prevBlock < curBlock:
                    for block in self.greenTrackData:
                        if block["Block Number"] == curBlock + 1:
                            trackModelToTrainModel.beacon.emit(block["Beacon"])
                elif (
                    (curBlock == 15 and prevBlock == 14)
                    or (curBlock == 21 and prevBlock == 20)
                    or (curBlock == 76 and prevBlock == 75)
                ):
                    for block in self.greenTrackData:
                        if block["Block Number"] == curBlock + 1:
                            trackModelToTrainModel.beacon.emit(block["Beacon"])
                elif (
                    (curBlock == 17 and prevBlock == 18)
                    or (curBlock == 23 and prevBlock == 24)
                    or (curBlock == 78 and prevBlock == 79)
                ):
                    for block in self.greenTrackData:
                        if block["Block Number"] == curBlock - 1:
                            trackModelToTrainModel.beacon.emit(block["Beacon"])
        elif line == "Red":
            if curBlock == 0 and prevBlock == 0:
                for block in self.redTrackData:
                    if block["Block Number"] == 9:
                        trackModelToTrainModel.blockInfo.emit(
                            9,
                            block["Block Length (m)"],
                            block["Block Grade (%)"],
                            block["Speed Limit (Km/Hr)"],
                            block["Suggested Speed"],
                            block["Authority"],
                        )
                        trackModelToTrackController.occupancyState.emit(
                            1,
                            self.get_wasyside_num(block["Block Number"]),
                            block["Block Number"] - 1,
                            True,
                        )
                        trackModelToTrackController.occupancyState.emit(
                            1, self.get_wasyside_num(curBlock), curBlock - 1, False
                        )
                        block["Occupancy"] = 1
                        # self.updateOccupancyGUI.emit("Green", 62)

    def get_wasyside_num(self, blockNum):
        if (blockNum >= 1 and blockNum <= 30) or (blockNum >= 102 and blockNum <= 150):
            return 1
        else:
            return 2
