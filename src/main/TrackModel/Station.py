import random


class Station:
    disembarkingPassengers = 0
    passengersBoarding = 0

    def get_ticket_sales(self):
        return random.randint(0, 40)

    def get_passenger_exchange(self, currentPassengers, waiting):
        # Max passenger capacity for a train
        TRAINMAX = 75

        # Crew Count for train
        CREW = 6

        # Determine passengers disembarking
        if currentPassengers > CREW:
            self.disembarkingPassengers = random.randint(CREW + 1, currentPassengers)
            currentPassengers -= self.disembarkingPassengers

        # Find max passengers that can be send to board
        if waiting > TRAINMAX - currentPassengers:
            high = TRAINMAX - currentPassengers
        else:
            high = waiting

        self.passengersBoarding = random.randint(0, high)
        waiting -= self.passengersBoarding

        return self.disembarkingPassengers, self.passengersBoarding, waiting
