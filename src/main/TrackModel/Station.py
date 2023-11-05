import random

class Station():
    def __init__(self):
        self.ticketSales = 0
        self.passengersWaiting = 0
        self.name = ""
        self.line = ""
    
    def get_passengers_boarding(self, name, line, max, current):
        self.name = name
        self.line = line
        
        rand = random.randint(0,100)
        self.ticketSales += rand
        self.passengersWaiting += rand
        
        if self.ticketSales > max - current:
            high = max - current
        else:
            high = self.ticketSales
        
        passengersBoarding = random.randint(0, high)
        self.passengersWaiting -= passengersBoarding
        return passengersBoarding
    
    def get_passengers_waiting(self):
        return self.passengersWaiting

    def get_station_data(self):
        return self.name, self.line
    
    def get_ticket_sales(self):
        throughput = self.ticketSales
        return throughput