
import time
import random
import obd
from obd import OBDStatus
from obd import OBDCommand, Unit
from obd.protocols import ECU
from obd.utils import bytes_to_int

class TrixieModel_OBD():
    def __init__(self):
        print("OBD: OBD model initialized")

    def connect(self, address, max_attempts):
        print("OBD: Attempting OBD-II connection...")
        self.connection = obd.OBD(address)
        attempts = 0
        # Attempt retries as necessary
        while (self.connection.status() != OBDStatus.CAR_CONNECTED and attempts < max_attempts):
            attempts += 1
            print("OBD: Attempting reconnect", attempts, "...")
            time.sleep(1)
            self.connection = obd.OBD(address)

        if (self.connection.status() != OBDStatus.CAR_CONNECTED):
            print("OBD: Could not connect after", attempts, "retries!")
            self.connection.close()
            return False
        else:
            print("OBD: Connected!")
            return True

    def getEngineLoad(self):
        retrun = self.connection.query(obd.commands.ENGINE_LOAD)
        return retrun.value.magnitude

class TrixieModel_Demo():
    def __init__(self):
        print("Demo: Demo model initialized!")
        self.engine_load = 0

    def connect(self, address, max_attempts):
        print("Demo: Attempting OBD-II connection...")
        time.sleep(1.0)
        print("Demo: Connected!")
        return True

    def getEngineLoad(self):
        if (self.engine_load > 50):
            new_load = self.engine_load + random.randint(-7, 3)
        else:
            new_load = self.engine_load + random.randint(-3, 7)
            
        if (new_load < 0):
            new_load = 0
        if (new_load > 100):
            new_load = 100

        self.engine_load = new_load
        return self.engine_load