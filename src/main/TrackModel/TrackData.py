import pandas as pd
from Station import Station
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
            if lineName == "Red":
                if data["Block Number"] == 7:  # Block C
                    block["Beacon"] = {
                        "Next Station": "Herron Ave",
                        "Current Station": {
                            "Name": "ShadySide",
                            "Side": "Left/Right",  # Don't need for red line
                        },
                    }
                if data["Block Number"] == 16:  # Block F
                    block["Beacon"] = {
                        "Next Station 1": "Shadyside",
                        "Next Station 2": "Swissville",
                        "Current Station": {
                            "Name": "Herron Ave",
                            "Side": "Left/Right",  # Don't need for red line
                        },
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
