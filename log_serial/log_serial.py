
# pip install pyserial
import serial
import datetime

# Change 'COM3' to your Arduino port (e.g., '/dev/ttyUSB0' for Linux)
# ser = serial.Serial('/dev/cu.usbserial-59010053471', 115200, timeout=1)
ser = serial.Serial('COM4', 115200, timeout=1)
log_name = "serial_log_" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3].replace(":", "_")
with open(log_name, "w") as file:
    while True:
        line = ser.readline().decode('utf-8', errors='replace').strip()
        if line:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Milliseconds precision
            log_entry = f"{timestamp}, {line}"
            print(log_entry)
            file.write(log_entry + "\n")