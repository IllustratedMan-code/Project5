import matplotlib.pyplot as plt
import matplotlib.patches as patches
import Warehouse
from time import sleep

fig,ax = plt.subplots(1)
[M,fig,ax] = Warehouse.Warehouse(fig,ax)

plt.ion()
plt.show()
#plt.plot(1,1)

for y in range(0,7):
    #Draw Robot
    robot = patches.Rectangle((6,y),4,6,linewidth=1,edgecolor='black',facecolor='red')
    ax.add_patch(robot)
    plt.pause(0.05)
    #Clear Robot
    robot.remove()
#Turn Right
Row = 12
for x in range(6,50):
    #Draw Robot
    robot = patches.Rectangle((x,6),6,4,linewidth=1,edgecolor='black',facecolor='red')
    ax.add_patch(robot)
    #Check Matrix M[Row][x] for Box - if Box, scan Bar Code
    #If no box, continue to move
    plt.pause(0.05)
    #Clear Robot
    robot.remove()
