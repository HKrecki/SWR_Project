import sys
import time
import numpy as np
import cv2
from matplotlib import pyplot as plt
import serial
import Frame_data

class Frame_data:
    start_symbol = "default"
    line_data = [-1]*32
    end_symbol = "default"

    frame_data = [line_data]*24

    def print_frame(self):
        print(self.start_symbol)
        print(self.line_data)
        print(self.end_symbol, "\n")

    def is_frame_default(self):
        if self.start_symbol == "default" and self.line_data == "default" and self.end_symbol == "default":
            return True



# User input to start communication
start_user_input = "default"
while start_user_input != "":
    start_user_input = input("Press Enter to start measurement: ")

# Connect to stm
STM32F4 = serial.Serial('COM4', 115200, timeout=0.2)

# Send command to STM to start measurement
STM32F4.write(b'1')

frame_started_flag = False
frame_ended_flag = False

while True:
    frame = Frame_data

    data = STM32F4.readline()

    # Frame starts
    if data == b"s\r\r\n":
        frame.start_symbol = "s"
        frame_started_flag = True

        #aux
        print("Frame started")

        # Read data in loop and save to 24 lines -> it's itereting 24 times
        for i in frame.frame_data:
            print(i)


'''
    # Line starts
    if frame_started_flag == True:

        data = str(data)
        data = data.split(" ")

        if data[0] == "b'sl" and data[-1] == "el\\r\\r\\n'" and len(data) == 34:
            frame.line_data = data[1:33]
            #print(frame.line_data)

        print("Frame data: ")
        print(frame.frame_data)
'''







'''
img = np.ones((24, 32), dtype = np.uint8)

img[5,:] = [29.41, 28.23, 28.23, 28.95, 28.94, 28.00, 28.81, 28.11, 28.32, 28.28, 28.56, 28.11, 28.69, 27.99, 28.63, 27.97, 28.26, 28.23, 28.43, 28.40, 28.80, 28.60, 28.31, 28.31, 28.83, 28.62, 28.94, 28.74, 29.31, 29.38, 29.23, 28.82]

print('Original Dimensions : ', img.shape)

scale_percent = 500  # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)

# resize image
resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

print('Resized Dimensions : ', resized.shape)

cv2.imshow("Resized image", resized)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''


