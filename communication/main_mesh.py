# -*- coding: UTF-8 -*-
#
#                                                    oooo
#                                                    `888
#   .oooo.o  .ooooo.  ooo. .oo.    .oooo.o oo.ooooo.   888 .oo.    .ooooo.  oooo d8b  .ooooo.   .oooo.o
#  d88(  "8 d88' `88b `888P"Y88b  d88(  "8  888' `88b  888P"Y88b  d88' `88b `888""8P d88' `88b d88(  "8
#  `"Y88b.  888ooo888  888   888  `"Y88b.   888   888  888   888  888ooo888  888     888ooo888 `"Y88b.
#  o.  )88b 888    .o  888   888  o.  )88b  888   888  888   888  888    .o  888     888    .o o.  )88b
#  8""888P' `Y8bod8P' o888o o888o 8""888P'  888bod8P' o888o o888o `Y8bod8P' d888b    `Y8bod8P' 8""888P'
#                                           888
#                                          o888o


#       ╔═╗┬┌┬┐┬ ┬  ╔═╗┌─┐┬┌─┐┌┐┌┌─┐┌─┐       ╔╦╗╦╔╦╗  ╔╦╗┌─┐┌┬┐┬┌─┐  ╦  ┌─┐┌┐
#       ║  │ │ └┬┘  ╚═╗│  │├┤ ││││  ├┤   ───  ║║║║ ║   ║║║├┤  │││├─┤  ║  ├─┤├┴┐
#       ╚═╝┴ ┴  ┴   ╚═╝└─┘┴└─┘┘└┘└─┘└─┘       ╩ ╩╩ ╩   ╩ ╩└─┘─┴┘┴┴ ┴  ╩═╝┴ ┴└─┘


    #                                   .|
    #                                  | |
    #                                  |'|            ._____
    #                          ___    |  |            |.   |' .---"|
    #                  _    .-'   '-. |  |     .--'|  ||   | _|    |
    #               .-'|  _.|  |    ||   '-__  |   |  |    ||      |
    #               |' | |.    |    ||       | |   |  |    ||      |
    #            ___|  '-'     '    ""       '-'   '-.'    '`      |____
    #
    #

# Andres Rico - MIT Media Lab - City Science Group - 2020 - aricom@mit.edu


import serial
import time
import datetime
import csv
import matplotlib
matplotlib.use("tkAgg")
import matplotlib.pyplot as plt
import numpy as np

def get_value(sensor_string):
    return float(sensor_string[9:15])

def reset_status(input_status):
    for i in range(len(input_status)):
        input_status[i] = False

ser = serial.Serial('/dev/tty.usbserial-AR0K4YH6')
ser.baudrate = 115200
ser.flushInput()

typeIndex = 4  # - Use 2 if sending incomplete value.
numberIdIndex = 7 # - Use 5 if sending incomplete value.
startValueIndex = 2
endValueIndex = 8

available_temp_nodes = []
available_light_nodes = []
network_ids = []
network_status = []
current_values = []

last_time = time.time()
now_time = 0

while True:

    try:
        ser_bytes = ser.readline()
        ser_string = str(ser_bytes)
        #print(ser_string)
    except:
        print("No Serial Available")

    #Create network.
    if ser_string[typeIndex] == 'L':

        if not (int(ser_string[numberIdIndex]) in available_light_nodes): #Check if node is new
            print('New Light Node Has Connected! =) ')
            print('Adding Node', ser_string[startValueIndex:endValueIndex], 'To Network...')
            network_ids.append(ser_string[startValueIndex:endValueIndex])
            network_status.append(True)
            available_light_nodes.append(int(ser_string[numberIdIndex]))
            network_size = len(available_temp_nodes) + len(available_light_nodes)
            current_values.append(0)
            print('Node has been added! =) ')
            print('Network Members: ', network_ids)
            print('Total Nodes: ', network_size)
            print('-> Temperature Nodes: ', available_temp_nodes)
            print('-> Light Nodes: ', available_light_nodes)

    if ser_string[4] == 'T': # - Use 4 if sending complete value.

        if not (int(ser_string[numberIdIndex]) in available_temp_nodes): #Check if node is new
            print('New Temperature Node Has Connected! =) ')
            print('Adding Node', ser_string[startValueIndex:endValueIndex], 'To Network...')
            network_ids.append(ser_string[startValueIndex:endValueIndex])
            network_status.append(True)
            available_temp_nodes.append(int(ser_string[numberIdIndex]))
            network_size = len(available_temp_nodes) + len(available_light_nodes)
            current_values.append(0)
            print('Node has been added! =) ')
            print('Network Members: ', network_ids)
            print('Total Nodes: ', network_size)
            print('-> Temperature Nodes: ', available_temp_nodes)
            print('-> Light Nodes: ', available_light_nodes)

    #Check that all nodes are still connected!
    end_time = time.time()
    if (end_time - last_time) > 5:
        last_time = time.time()
        if not all(network_status):
            for i in range(len(network_status)):
                if not network_status[i]:
                    print('Node: ', network_ids[i], 'is non responsive.')
                    current_values[i] = -1000
        reset_status(network_status)

    file_2_write = 'main_data_base.csv'
    status_index = network_ids.index(ser_string[startValueIndex:endValueIndex])
    network_status[status_index] = True
    current_values[status_index] = get_value(ser_string)
    print(current_values)

    with open(file_2_write,"a") as f:
        writer = csv.writer(f,delimiter=",")
        writer.writerow([datetime.datetime.now(), current_values[0:len(current_values)]])


    #if ser_string[0:6] == network_ids[0]:
    #    print('All set to make new line!')
