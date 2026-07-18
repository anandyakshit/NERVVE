import serial
ser=serial.Serial("COM3", 9600)
print("Listening....")
while True:
        packet = ser.readline().decode(errors="ignore").strip()
        if packet:
            print(packet)
