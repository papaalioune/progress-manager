from random import randrange
from time import sleep

class simulatedSimulator():
    def __init__(self) -> None:
        self.simulation_time = randrange(3, 7)
        #print("\n My simulation time is", self.simulation_time,"\n")
        sleep(self.simulation_time)
        #print("\nMy simulation finish ...\n")

        

ss = simulatedSimulator()