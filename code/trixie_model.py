
import time
import random
import obd
from obd import OBDStatus
from obd import OBDCommand, Unit
from obd.protocols import ECU
from obd.utils import bytes_to_int

class TrixieModel():
    def __init__(self):
        print("baseclass")

    def getEngineLoad(self):
        return 0

    def getEngineTemp(self):
        return 0

    def getShortFuelTrim(self):
        return 0

    def getLongFuelTrim(self):
        return 0

    def getRPM(self):
        return 0
    def getSpeed(self):
        return 0

    def getIntakeTemp(self):
        return 0

    def getMAF(self):
        return 0

    def getThrottle(self):
        return 0

class TrixieModel_OBD(TrixieModel):
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
        return '{:d}'.format(int(retrun.value.magnitude))

    def getEngineTemp(self):
        retrun = self.connection.query(obd.commands.COOLANT_TEMP)
        return '{:d}'.format(int(retrun.value.to('degF').magnitude))

    def getShortFuelTrim(self):
        retrun = self.connection.query(obd.commands.SHORT_FUEL_TRIM_1)
        return '{:.2f}'.format(retrun.value.magnitude)

    def getLongFuelTrim(self):
        retrun = self.connection.query(obd.commands.LONG_FUEL_TRIM_1)
        return '{:.2f}'.format(retrun.value.magnitude)

    def getRPM(self):
        retrun = self.connection.query(obd.commands.RPM)
        return '{:d}'.format(int(retrun.value.magnitude))

    def getSpeed(self):
        retrun = self.connection.query(obd.commands.SPEED)
        return '{:d}'.format(int(retrun.value.to('mph').magnitude))

    def getIntakeTemp(self):
        retrun = self.connection.query(obd.commands.INTAKE_TEMP)
        return '{:d}'.format(int(retrun.value.to('degF').magnitude))

    def getMAF(self):
        retrun = self.connection.query(obd.commands.MAF)
        return '{:.1f}'.format(retrun.value.magnitude)

    def getThrottle(self):
        retrun = self.connection.query(obd.commands.THROTTLE_POS)
        return '{:d}'.format(int(retrun.value.magnitude))

class TrixieModel_Demo(TrixieModel):
    def __init__(self):
        print("Demo: Demo model initialized!")
        self.engine_load = 0
        self.engine_temp = 0
        self.short_fuel = 0
        self.long_fuel = 0
        self.RPM = 0
        self.speed = 0
        self.intake_temp = 0
        self.MAF = 0
        self.throttle = 0

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

    def getEngineTemp(self):
        return self.engine_temp

    def getShortFuelTrim(self):
        return self.short_fuel

    def getLongFuelTrim(self):
        return self.long_fuel

    def getRPM(self):
        return self.RPM

    def getSpeed(self):
        return self.speed

    def getIntakeTemp(self):
        return self.intake_temp

    def getMAF(self):
        return self.MAF

    def getThrottle(self):
        return self.throttle