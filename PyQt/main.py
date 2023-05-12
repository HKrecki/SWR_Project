import sys
import time
import numpy as np
import cv2
from matplotlib import pyplot as plt
import serial
import Frame_data
from matplotlib.animation import FuncAnimation

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


fig,ax = plt.subplots(1,1)
image = np.array([[20,21,22], [28,29,30], [31,32,33]])
im = ax.imshow(image)



# Connect to stm
STM32F4 = serial.Serial('COM4', 115200, timeout=0.1)

# Send command to STM to start measurement
STM32F4.write(b'1')

frame_started_flag = False
frame_ended_flag = False

iterator = 0

# MAIN LOOP - read data from STM #
while True:
    # Waiting for frame starts signal: "s"
    data = STM32F4.readline()

    #print(data)

    # Get start frame signal from STM
    if data == b"s\r\r\n":
        frame_started_flag = True
        frame_ended_flag = False
        frame = Frame_data
        iterator = 0
        print("Frame starts")


    if data == b"e\r\r\n" and frame_started_flag == True:
        frame_started_flag = False
        frame_ended_flag = True

        print("Frame done")
        iterator = 0

    if frame_started_flag == True and frame_ended_flag == False:
        #print(data)

        data = str(data)
        print(len(data))

        if len(data) >= 204:
            data_array = data.split(" ")

            if "sl" in data_array[0] and "el" in data_array[33]:
                #print("for iterator: ", iterator, "values: ", data_array[1:32])

                # Save only lines starts at sl end ends at el
                frame.frame_data[iterator] = data_array[1:33]

                if iterator == 23:
                    #print(frame.frame_data)
                    print(len(frame.frame_data))
                    print(len(frame.frame_data[0]))
                    frame_np = np.array(frame.frame_data)
                    frame_np_float = frame_np.astype(float)
                    print(frame_np_float)
                    print(type(frame_np_float))

                    image = frame_np_float
                    im.set_data(image)
                    fig.canvas.draw_idle()
                    plt.pause(0.1)

                    #image = frame_np_float
                    #im.set_data(image)
                    #fig.canvas.draw_idle()
                    #plt.pause(1)

                    #im = plt.imshow(image)


                #print("Line no. ", iterator, ", values: ", frame.frame_data[iterator])

                iterator = iterator + 1





    #if frame_started_flag == True
    #    frame = Frame_data
    #    print(data)





