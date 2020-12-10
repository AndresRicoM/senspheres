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
import networkx as nx
import numpy as np
import random
import re
from mayavi import mlab

def flat_graph_net(nodes, online):
	G = nx.DiGraph(nodes)
	fig = plt.figure()
	pos = nx.spring_layout(G)
	#nx.draw_networkx_nodes(G,pos, node_size = 20, nodelist = online[0], node_color = 'xkcd:red', with_labels = True)
	nx.draw_networkx_nodes(G,pos, node_size = 500, node_color = 'xkcd:green') #, nodelist = online[1]
	nx.draw_networkx_edges(G,pos, edge_color = 'w', arrows = False)
	fig.set_facecolor('xkcd:black')
	plt.axis('off')
    #fig.canvas.draw()
    #fig.canvas.flush_events()
	plt.show()
    #plt.close()

def d3_graph_net(population):
	mlab.options.offscreen = False
	graph = nx.DiGraph(population)
	fig = plt.figure()
	pos = nx.random_layout(graph, dim=3)
	#pos = nx.spring_layout(graph, dim=3, k=50)
	xyz = np.array([pos[v] for v in sorted(graph)])

	mlab.figure(1, bgcolor=(0, 0, 0))
	mlab.clf()
	pts = mlab.points3d(xyz[:, 0], xyz[:, 1], xyz[:, 2],
	                    scale_factor=0.025,
	                    scale_mode='none',
	                    colormap='blue-red',
	                    resolution=50)

	pts.mlab_source.dataset.lines = np.array(list(graph.edges()))
	tube = mlab.pipeline.tube(pts, tube_radius=0.005)
	mlab.pipeline.surface(tube, color=(1, 1, 1), opacity = .05)

	mlab.show()


#while True:

dataList = []

with open("current_data.csv") as f:
    current_data = current_data = f.readline()
current_data = re.sub('"', '', current_data)

for i in range(4):
    indexingValue = current_data.find(']')
    dataList.append(current_data[0:indexingValue+1])
    current_data = current_data[(indexingValue+2):]
adjacencyNodes = {'Mother Node': set(dataList[1].strip('][').split(', ') )}
print(adjacencyNodes)

#flat_graph_net(adjacencyNodes, dataList[2])
d3_graph_net(adjacencyNodes)
