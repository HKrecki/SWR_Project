import sys
import time
import numpy as np
import cv2
from matplotlib import pyplot as plt
import serial
import datetime
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

# Image variables
min_temperature = 0
max_temperature = 0
avg_temperature = 0
med_temperature = 0

# Maximum temperatures from first 10 frames
max_temperature_first_10_frames_array = np.zeros(10, dtype=float)

# Average maximum temperature from first 10 frames
avg_max_temperature_first_10_frames = 0

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
debug_iterator = 0
frame_number = 0

# MAIN LOOP - read data from STM32 #
while True:
    # Waiting for frame starts signal: "s"
    data = STM32F4.readline()

    ################################################
    # DEBUG - to check. printing not this data
    # Debug info
    #debug_iterator = debug_iterator + 1
    #if debug_iterator == 1:
    #    print("===== DEBUG =====")
    #    print(data)
    #    print("===== DEBUG =====")
    ################################################

    # Get start frame signal from STM
    if data == b"s\r\r\n":
        frame_started_flag = True
        frame_ended_flag = False
        frame = Frame_data
        iterator = 0

    if data == b"e\r\r\n" and frame_started_flag == True:
        frame_started_flag = False
        frame_ended_flag = True

        iterator = 0

    if frame_started_flag == True and frame_ended_flag == False:
        data = str(data)

        if len(data) >= 150: #204:
            data_array = data.split(" ")

            if "sl" in data_array[0] and "el" in data_array[33]:

                # Save only lines starts at sl end ends at el
                frame.frame_data[iterator] = data_array[1:33]

                if iterator == 23:
                    print("============================== FRAME STARTS ==============================")

                    # Convert to float array
                    frame_np = np.array(frame.frame_data)
                    frame_np_float = frame_np.astype(float)
                    image = frame_np_float

                    # Correction of dead pixel
                    image[18][21] = (image[18][20] + image[18][22] + image[17][21] + image[19][21]) / 4

                    ############################## STATISTICS ##############################
                    # Get statistics values of image:
                    min_temperature = np.nanmin(image)
                    max_temperature = np.nanmax(image)
                    avg_temperature = round(np.nanmean(image),2)
                    med_temperature = round(np.nanmedian(image), 2)

                    # Calculate max temperature from last 10 frames (before welding)
                    if frame_number < 10:
                        max_temperature_first_10_frames_array[frame_number] = max_temperature
                    elif frame_number == 10:
                        avg_max_temperature_first_10_frames = np.mean(max_temperature_first_10_frames_array)
                    else:
                        # Get number of pixels with values bigger than avg. temperature from first 10 frames
                        object_size = np.sum(image > round(avg_max_temperature_first_10_frames + 3,2)) # +/- 3 degrees (camera accuracy)
                        print("Object size ( number of pixels with value greater then ", round((avg_max_temperature_first_10_frames + 3),2),"): ", object_size)

                    # Find pixel of highest temperature and color it black:
                    maxindex = np.unravel_index(image.argmax(), image.shape)
                    image[maxindex[0], maxindex[1]] = np.nan

                    # Display statistics:
                    print("Min: ", min_temperature, ", Max: ", max_temperature, "Mean: ", avg_temperature, "Median: ",med_temperature)
                    ############################## STATISTICS ##############################

                    # Display image
                    im.set_data(image)
                    fig.canvas.draw_idle()
                    plt.pause(0.1)

                    # Frame number
                    frame_number = frame_number + 1
                    now = datetime.datetime.now()
                    print("Frame number: ", frame_number, "Time: ", now.time())
                    print("============================== FRAME ENDS ==============================")

                iterator = iterator + 1
