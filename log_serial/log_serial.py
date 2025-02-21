
# pip install pyserial
import serial
import datetime

# Change 'COM3' to your Arduino port (e.g., '/dev/ttyUSB0' for Linux)
# ser = serial.Serial('/dev/cu.usbserial-59010053471', 115200, timeout=1)
ser = serial.Serial('COM4', 115200, timeout=1)
idx = 0
isCreateNewFile = True


log_name = "serial_log_" + "20mm_20mm_" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3].replace(":", "_")
file = open(log_name + ".txt", "w")

while True:
    line = ser.readline().decode('utf-8', errors='replace').strip()
    if line:
        # check if line has the substring "1.50"
        if "1.50" in line:
            if isCreateNewFile:
                file.close()
                idx += 2
                # open a new file
                file = open(log_name + "_" + str(idx) + ".txt", "w")
                isCreateNewFile = False
        else:
            isCreateNewFile = True
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Milliseconds precision
        log_entry = f"{timestamp}, {line}"
        print(log_entry)
        file.write(log_entry + "\n")