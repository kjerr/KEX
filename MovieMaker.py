import numpy
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import animation
from matplotlib import pyplot as plt
from matplotlib import colors as mcolors
import csv

frameArray = []
ncolE, nrowE = 30, 30

simtime = 1000
framesize = 10
numberOfFrames = int(simtime)/int(framesize)


with open("framesPerlinTest.csv", "rb") as csvfile:
    reader = csv.reader(csvfile, delimiter='*')
    for row in reader:
        frame = []
        for elem in row:
            outputList = elem[1:-1].split(",")
            outputList = map(int, outputList)
            frame.append(outputList)
        frameArray.append(frame)

# make animation

fig = plt.figure()
ax = plt.axes(xlim=(0,ncolE), ylim=(0,nrowE))
ax.grid(True)
line, = ax.plot([], [], lw=2)

def init():
    line.set_data([], [])
    return line

def animate(i):
    frame = frameArray[i]
    output = plt.pcolormesh(frame, edgecolors = "#774387")
    return output

anim = animation.FuncAnimation(fig, animate, interval=200, frames=numberOfFrames)

# anim.save('simulationTest.mp4', writer=mywriter, fps=20)

plt.show()
