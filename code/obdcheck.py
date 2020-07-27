'''
Attempting OBD-II connection...
Connected!
( DECODER )                  123456789ABCDEF0123456789ABCDEF0
PIDs Supported (0x01-0x20) = 10111110000111111111100000010000
01, 03, 04, 05, 06, 07, 0C, 0D, 0E, 0F, 10, 11, 12, 13, 14, 15, 1C
PIDs Supported (0x21-0x40) = None
PIDs Supported (0x41-0x60) = None
PIDs Supported (0x61-0x80) = None
PIDs Supported (0x81-0xA0) = None
PIDs Supported (0xA1-0xC0) = None
Sampling RPM
RPM = 751.75 revolutions_per_minute
RPM = 737.5 revolutions_per_minute
RPM = 756.5 revolutions_per_minute
RPM = 767.5 revolutions_per_minute
RPM = 748.25 revolutions_per_minute
RPM = 758.25 revolutions_per_minute
RPM = 785.5 revolutions_per_minute
RPM = 751.25 revolutions_per_minute
RPM = 762.5 revolutions_per_minute
RPM = 754.75 revolutions_per_minute
Test complete

Supported:
    OBDCommand("STATUS"                     , "Status since DTCs cleared"               , b"0101", 6, status,                ECU.ENGINE, True),
    OBDCommand("FUEL_STATUS"                , "Fuel System Status"                      , b"0103", 4, fuel_status,           ECU.ENGINE, True),
x   OBDCommand("ENGINE_LOAD"                , "Calculated Engine Load"                  , b"0104", 3, percent,               ECU.ENGINE, True),
x   OBDCommand("COOLANT_TEMP"               , "Engine Coolant Temperature"              , b"0105", 3, temp,                  ECU.ENGINE, True),
x   OBDCommand("SHORT_FUEL_TRIM_1"          , "Short Term Fuel Trim - Bank 1"           , b"0106", 3, percent_centered,      ECU.ENGINE, True),
x   OBDCommand("LONG_FUEL_TRIM_1"           , "Long Term Fuel Trim - Bank 1"            , b"0107", 3, percent_centered,      ECU.ENGINE, True),
x   OBDCommand("RPM"                        , "Engine RPM"                              , b"010C", 4, uas(0x07),             ECU.ENGINE, True),
x   OBDCommand("SPEED"                      , "Vehicle Speed"                           , b"010D", 3, uas(0x09),             ECU.ENGINE, True),
    OBDCommand("TIMING_ADVANCE"             , "Timing Advance"                          , b"010E", 3, timing_advance,        ECU.ENGINE, True),
x   OBDCommand("INTAKE_TEMP"                , "Intake Air Temp"                         , b"010F", 3, temp,                  ECU.ENGINE, True),
x   OBDCommand("MAF"                        , "Air Flow Rate (MAF)"                     , b"0110", 4, uas(0x27),             ECU.ENGINE, True),
x   OBDCommand("THROTTLE_POS"               , "Throttle Position"                       , b"0111", 3, percent,               ECU.ENGINE, True),
    OBDCommand("AIR_STATUS"                 , "Secondary Air Status"                    , b"0112", 3, air_status,            ECU.ENGINE, True),
    OBDCommand("O2_SENSORS"                 , "O2 Sensors Present"                      , b"0113", 3, o2_sensors,            ECU.ENGINE, True),
    OBDCommand("O2_B1S1"                    , "O2: Bank 1 - Sensor 1 Voltage"           , b"0114", 4, sensor_voltage,        ECU.ENGINE, True),
    OBDCommand("O2_B1S2"                    , "O2: Bank 1 - Sensor 2 Voltage"           , b"0115", 4, sensor_voltage,        ECU.ENGINE, True),
    OBDCommand("OBD_COMPLIANCE"             , "OBD Standards Compliance"                , b"011C", 3, obd_compliance,        ECU.ENGINE, True),
'''
import obd
from obd import OBDStatus
import time
from obd import OBDCommand, Unit
from obd.protocols import ECU
from obd.utils import bytes_to_int

MAX_ATTEMPTS = 7

# Copied from python-obd source
# hex in, bitstring out
def pid(messages):
    d = messages[0].data[2:]
    return BitArray(d)

# Setup connection
print("Attempting OBD-II connection...")
connection = obd.OBD("/dev/ttyAMA0")
attempts = 0

con = False

# Attempt retries as necessary
while (connection.status() != OBDStatus.CAR_CONNECTED and attempts < MAX_ATTEMPTS):
    attempts += 1
    print("Attempting reconnect", attempts, "...")
    time.sleep(1)
    connection = obd.OBD("/dev/ttyAMA0")

if (connection.status() != OBDStatus.CAR_CONNECTED):
    print("Could not connect after", attempts, "retries!")
    connection.close()
    exit()
else:
    print("Connected!")

#connection = obd.OBD("/dev/ttyAMA0", 9600, 3, True, 3, True)
#print("Sleep 20...")
#time.sleep(20)

# Custom PIDs
PIDS_D = OBDCommand("PIDS_B", "Supported PIDs [21-40]", b"0120", 6, pid, ECU.ENGINE, True)
PIDS_B = OBDCommand("PIDS_C", "Supported PIDs [41-60]", b"0140", 6, pid, ECU.ENGINE, True)
PIDS_C = OBDCommand("PIDS_D", "Supported PIDs [61-80]", b"0160", 6, pid, ECU.ENGINE, True)
PIDS_E = OBDCommand("PIDS_E", "Supported PIDs [81-A0]", b"0180", 6, pid, ECU.ENGINE, True)
PIDS_F = OBDCommand("PIDS_F", "Supported PIDs [A1-C0]", b"01A0", 6, pid, ECU.ENGINE, True)

# Read out all mode 01 supported PIDs
pids = connection.query(obd.commands.PIDS_A)
print("PIDs Supported (0x01-0x20) =", pids.value)
pids = connection.query(PIDS_B, force=True)
print("PIDs Supported (0x21-0x40) =", pids.value)
pids = connection.query(PIDS_C, force=True)
print("PIDs Supported (0x41-0x60) =", pids.value)
pids = connection.query(PIDS_D, force=True)
print("PIDs Supported (0x61-0x80) =", pids.value)
pids = connection.query(PIDS_E, force=True)
print("PIDs Supported (0x81-0xA0) =", pids.value)
pids = connection.query(PIDS_F, force=True)
print("PIDs Supported (0xA1-0xC0) =", pids.value)

# Proof-of-concept RPM reads
print("Sampling RPM")
count = 0
while (count < 10):
    rpm = connection.query(obd.commands.RPM)
    print("RPM =", rpm.value)
    time.sleep(1)
    count += 1

#spd = connection.query(obd.commands.SPEED)
#print("Speed =", spd.value)

print("Test complete")
connection.close()   
