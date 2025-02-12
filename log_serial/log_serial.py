
# pip install pyserial
import serial
import datetime

# Change 'COM3' to your Arduino port (e.g., '/dev/ttyUSB0' for Linux)
ser = serial.Serial('/dev/cu.usbserial-59010053471', 115200, timeout=1)

with open("serial_log.txt", "w") as file:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Milliseconds precision
            log_entry = f"{timestamp}, {line}"
            print(log_entry)
            file.write(log_entry + "\n")