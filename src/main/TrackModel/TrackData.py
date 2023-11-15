import pandas as pd
from .Station import Station
from signals import trackControllerToTrackModel

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
        trackControllerToTrackModel.suggestedSpeed.connect(self.set_suggested_speed)
        trackControllerToTrackModel.authority.connect(self.set_authority)

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
        # data.insert(0, {"Block Number": 0.0}) #<-- not needed
        for block in data:
            block["Failures"] = ["None"]
            block["Occupancy"] = 0
            block["Maintenance"] = 0
            block["Suggested Speed"] = 0
            block["Authority"] = 0
            if lineName == "Green Line":
                if block["Block Number"] == 2:  # Section A, Pioneer
                    block["Beacon"] = {
                        "Next Station1": "Station",
                        "Next Station2": "",
                        "Current Station": "Pioneer",
                        "Door Side": block["Station Side"],
                    }
                if block["Block Number"] == 9:  # Section C, Edgebrook
                    block["Beacon"] = {
                        "Next Station1": "Pioneer",
                        "Next Station2": "",
                        "Current Station": "Edgebrook",
                        "Door Side": block["Station Side"],
                    }
                if block["Block Number"] == 16:  # Section D, Station
                    block["Beacon"] = {
                        "Next Station1": "Edgebrook",
                        "Next Station2": "Whited",
                        "Current Station": "Station",
                        "Door Side": block["Station Side"],
                    }
                if block["Block Number"] == 22:  # Section F, Whited
                    block["Beacon"] = {
                        "Next Station1": "Station",
                        "Next Station2": "South Bank",
                        "Current Station": "Whited",
                        "Door Side": block["Station Side"],
                    }
                if block["Block Number"] == 31:  # Section G, South Bank
                    block["Beacon"] = {
                        "Next Station1": "Central",
                        "Next Station2": "",
                        "Current Station": "South Bank",
                        "Door Side": block["Station Side"],
                    }
                if block["Block Number"] == 39:  # Section I, Central
                    block["Beacon"] = {
                        "Next Station1": "Inglewood",
                        "Next Station2": "",
                        "Current Station": "Central",
                        "Door Side": block["Station Side"],
                    }
                if block["Block Number"] == 48:  # Section I, Inglewood
                    block["Beacon"] = {
                        "Next Station1": "Overbrook",
                        "Next Station2": "",
                        "Current Station": "Inglewood",
                        "Door Side": block["Station Side"],
                    }
                if block["Block Number"] == 57:  # Section I, Overbrook
                    block["Beacon"] = {
                        "Next Station1": "Glenbury",
                        "Next Station2": "",
                        "Current Station": "Overbrook",
                        "Door Side": block["Station Side"],
                    }
                if block["Block Number"] == 65:  # Section K, Glenbury
                    block["Beacon"] = {
                        "Next Station1": "Dormont",
                        "Next Station2": "",
                        "Current Station": "Glenbury",
                        "Door Side": block["Station Side"],
                    }
                if block["Block Number"] == 73:  # Section L, Dormont
                    block["Beacon"] = {
                        "Next Station1": "Mt Lebanon",
                        "Next Station2": "",
                        "Current Station": "Dormont",
                        "Door Side": block["Station Side"],
                    }
                if block["Block Number"] == 77:  # Section N, Mt Lebanon
                    block["Beacon"] = {
                        "Next Station1": "Poplar",
                        "Next Station2": "Dormont",
                        "Current Station": "Mt Lebanon",
                        "Door Side": block["Station Side"],
                    }
                if block["Block Number"] == 88:  # Section O, Poplar
                    block["Beacon"] = {
                        "Next Station1": "Castle Shannon",
                        "Next Station2": "Mt Lebanon",
                        "Current Station": "Poplar",
                        "Door Side": block["Station Side"],
                    }
                if block["Block Number"] == 96:  # Section P, Castle Shannon
                    block["Beacon"] = {
                        "Next Station1": "Mt Lebanon",
                        "Next Station2": "",
                        "Current Station": "Castle Shannon",
                        "Door Side": block["Station Side"],
                    }
                if block["Block Number"] == 105:  # Section T, Dormont
                    block["Beacon"] = {
                        "Next Station1": "Glenbury",
                        "Next Station2": "",
                        "Current Station": "Dormont",
                        "Door Side": block["Station Side"],
                    }
                if block["Block Number"] == 114:  # Section U, Glenbury
                    block["Beacon"] = {
                        "Next Station1": "Overbrook",
                        "Next Station2": "",
                        "Current Station": "Glenbury",
                        "Door Side": block["Station Side"],
                    }
                if block["Block Number"] == 123:  # Section W, Overbrook
                    block["Beacon"] = {
                        "Next Station1": "Inglewood",
                        "Next Station2": "",
                        "Current Station": "Overbrook",
                        "Door Side": block["Station Side"],
                    }
                if block["Block Number"] == 132:  # Section W, Inglewood
                    block["Beacon"] = {
                        "Next Station1": "Central",
                        "Next Station2": "",
                        "Current Station": "Inglewood",
                        "Door Side": block["Station Side"],
                    }
                if block["Block Number"] == 141:  # Section W, Central
                    block["Beacon"] = {
                        "Next Station1": "Whited",
                        "Next Station2": "",
                        "Current Station": "Central",
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
    
    def set_suggested_speed(self, line, _, blockNum, suggestedSpeed):
        if line == 1:
            for block in self.greenTrackData:
                if block["Block Number"] == blockNum:
                    block["Suggested Speed"] == suggestedSpeed
        if line == 2:
            for block in self.redTrackData:
                if block["Block Number"] == blockNum:
                    block["Suggested Speed"] == suggestedSpeed
    
    def set_authority(self, line, _, blockNum, authority):
        if line == 1:
            for block in self.greenTrackData:
                if block["Block Number"] == blockNum:
                    block["Authority"] == authority
        if line == 2:
            for block in self.redTrackData:
                if block["Block Number"] == blockNum:
                    block["Authority"] == authority

    def update_station_data(self):
        station = Station()
        ticketSales = station.get_ticket_sales()
        waiting = station.get_passengers_waiting()
        stationName, line = station.get_station_data()
        if line == "Red":
            for block in self.redTrackData:
                if stationName in block["Infrastructure"]:
                    block["Ticket Sales"] = ticketSales
                    block["Waiting at Station"] = waiting
        elif line == "Green":
            for block in self.greenTrackData:
                if stationName in block["Infrastructure"]:
                    block["Ticket Sales"] = ticketSales
                    block["Waiting at Station"] = waiting

    def get_ticket_sales(self, line):
        throughput = 0
        if line == "Red":
            for block in self.redTrackData:
                if "Station" in block["Infrastructure"]:
                    throughput += block["Ticket Sales"]
        elif line == "Green":
            for block in self.greenTrackData:
                if "Station" in block["Infrastructure"]:
                    throughput += block["Ticket Sales"]
        return throughput

    def set_occupancy(self):
        # If block 0's occupancy is set to 1, the first block in the track is set to occupied
        # Only applies to a train being dispatched
        # Now the train will calculate when it enters a new block and send me a signal to if it is entering a new block
        # Upon receiving this signal, the next block in the train's path will be updated to occupied
        # and the previous block will be set to unoccupied
        return
        # line, trainID, enteringNewBlock = trainModel.get_entering_block()
        # if line == "Red":
        #     if trainID in self.redOccupancy:
        #         self.update_occupancy(trainID, line)
        #     else:
        #         self.redOccupancy[trainID] = "0" #Block Number that is occupied
        # if line == "Green":
        #     if trainID in self.greenOccupancy:
        #         self.update_occupancy(trainID, line)
        #     else:
        #         self.greenOccupancy[trainID] = "0"

    # Given the previous occupancy, set the next occupied block
    def update_occupancy(self, trainID, line):
        return

    # def set_suggested_speed(self):
    #     suggested_speed, blockNumber, line = trackController.get_suggested_speed()
    #     if line == "Red":
    #         for data in self.redTrackData:
    #             if data["Block Number"] == blockNumber:
    #                 data["Suggested Speed"] = suggested_speed
    #     else:
    #         for data in self.greenTrackData:
    #             if data["Block Number"] == blockNumber:
    #                 data["Suggested Speed"] = suggested_speed

    # def set_authority(self):
    #     authority, blockNumber, line = trackController.get_authority()
    #     if line == "Red":
    #         for data in self.redTrackData:
    #             if data["Block Number"] == blockNumber:
    #                 data["Authority"] = authority
    #     else:
    #         for data in self.greenTrackData:
    #             if data["Block Number"] == blockNumber:
    #                 data["Authority"] = authority

    # Send occupancy to the Track Controller
    def get_occupancy(self, blockNumber):
        for data in self.redTrackData:
            if data["Block Number"] == blockNumber:
                return data["Occupancy"]

    # #Call signals for train model inputs here
    # def get_train_model_inputs(self):
    #     return

    # def get_maintenance(self, blockNumber):
    #     for data in self.trackData:
    #         if data["Block Number"] == blockNumber:
    #             return blockNumber, self.maintenance

    # # Receive Maintenance from Track Controller
    # def set_maintenance(self, blockNumber, maintenance):
    #     blockNumber, self.maintenance = trackController.get_maintenance()
    #     for data in self.trackData:
    #         if data["Block Number"] == blockNumber:
    #             data["Maintenance"] = self.maintenance

    # def get_station_data(self):
    #     return blockNum, ticketSales, waiting
