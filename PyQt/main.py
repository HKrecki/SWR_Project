from PyQt6.QtWidgets import QApplication, QDialog
import sys
import serial

''' Read data and display in terminal
ser = serial.Serial("COM4", 115000)
while True:
    cc = str(ser.readline())
    print(cc)

app = QApplication(sys.argv)
window = QDialog()
window.show()
sys.exit(app.exec())
'''

command = input("Write start to begin measurement: ")
if command == "start":
    print("Measurement starts")
    ## Send start to STM32

    ## STM32 resending data

    ## waiting for stop command from user








