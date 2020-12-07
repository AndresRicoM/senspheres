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
import csv
import matplotlib
matplotlib.use("tkAgg")
import matplotlib.pyplot as plt
import numpy as np

def get_temp(temp_string):
    return float(temp_string[9:15])

ser = serial.Serial('/dev/tty.usbserial-AR0K4YH6')
ser.baudrate = 115200
ser.flushInput()

available_temp_nodes = []
available_light_nodes = []
received_temp = []
received_light = []

plot_window = 20
y_var = np.array(np.zeros([plot_window]))

plt.ion()
fig, ax = plt.subplots()
line, = ax.plot(y_var)


while True:

    try:
        ser_bytes = ser.readline()
        ser_string = str(ser_bytes)
        #print(ser_string)
    except:
        print("No Serial Available")

    #Create network.
    if ser_string[4] == 'L':
        #Check if node is new
        if not (int(ser_string[7]) in available_light_nodes):
            print('New Light Node Has Connected! =) ')
            print('Adding Node', ser_string[2:8], 'To Network...')
            available_light_nodes.append(int(ser_string[7]))
            print('Node has been added! =) ')

    if ser_string[4] == 'T':
        #print(get_temp(ser_string))
        with open("test_data.csv","a") as f:
            writer = csv.writer(f,delimiter=",")
            writer.writerow([time.time(),get_temp(ser_string)])

        plt.style.use('dark_background')
        y_var = np.append(y_var,get_temp(ser_string))
        y_var = y_var[1:plot_window+1]
        line.set_ydata(y_var)
        ax.relim()
        ax.autoscale_view()
        fig.canvas.draw()
        fig.canvas.flush_events()

        if not (int(ser_string[7]) in available_light_nodes):
            print('New Temperature Node Has Connected! =) ')
            print('Adding Node', ser_string[2:8], 'To Network...')
            available_light_nodes.append(int(ser_string[7]))
            print('Node has been added! =) ')
        #print('Temperature Node Connected')

    #Check if node has been disconnected
