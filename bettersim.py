# library requirements:
# kivy

# general explanation:
# The kivy package builds graphics through building blocks called
# widgets. Widgets can be layouts such as a grid or UI elements like
# menus. Each class in the code represents a different widget,
# instances of which can be created inside each other. The rootclass widget
# is fed into the RunApp class which handles all of the runtime processing.
# Kivy apps can use a kivy language file (.kv), the name of which must be the
# same as App class without the 'App' suffix. In this case, the kivy file
# attached to bettersim.py is run.kv

import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import *
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, StringProperty, BooleanProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.image import Image
import behavior
import math
import time
import threading

# base class that handles the placing of all widgets
class rootclass(GridLayout):

    def __init__(self, **k):
        super(rootclass, self).__init__(**k)
        self.rows = 2
        self.cols = 2
        # adds an instance of the grid widget
        self.g = grid()
        self.add_widget(self.g)

        # add an instance of the Co widget
        self.color = VisionBox()
        self.add_widget(self.color)
        # adds the lcd widget
        self.lcd = Lcd()
        self.add_widget(self.lcd)
        # adds the triangulate button
        self.blayout = ButtonLayout()
        self.add_widget(self.blayout)
        self.up = self.g.update
        # update schedule for the widgets
        Clock.schedule_interval(self.up, 1 / (900))
        self.g.bind(size=self.g.resize)
        self.g.bind(size=self.lcd.upsize)
        self.g.bind(col=self.color.col.colorchange)
        self.g.bind(distance=self.color.col.valuechange)
        self.g.car.bind(center=self.lcd.upposition)
        self.g.bind(curbcode=self.color.barcodes.idupdate)
        self.blayout.boxy.tri.bind(on_release=self.lcd.dispposition)
        self.blayout.barcodes.b1.bind(on_release=self.blayout.boxy.curbar.bar1)
        self.blayout.barcodes.b2.bind(on_release=self.blayout.boxy.curbar.bar2)
        self.blayout.barcodes.b3.bind(on_release=self.blayout.boxy.curbar.bar3)
        self.blayout.barcodes.b4.bind(on_release=self.blayout.boxy.curbar.bar4)
        self.blayout.boxy.curbar.bind(id=self.color.barcodes.bidupdate)
        self.g.bind(home=self.color.barcodes.homeupdate)
        self.color.barcodes.bind(found=self.g.pickupbox)
        self.color.barcodes.bind(found=self.g.homepath)
        self.color.barcodes.bind(found=self.g.updatemode)
        self.blayout.boxy.addbox.bind(on_release=self.g.addbox)
        self.g.bind(nodechange=self.g.detectbadnodes)
        #self.color.barcodes.bind(found=self.g.updatemode)



# this is the class that draws the boxes and path for the robot to follow in additon
# to housing the main function controlling the robot
class grid(RelativeLayout):
    car = ObjectProperty(None)
    col = ListProperty(None)
    time = NumericProperty(0)
    ax = NumericProperty(0.3-0.015)
    ay = NumericProperty(0.11 - 0.0187 + 0.024)
    distance = NumericProperty(0)
    barcode = ListProperty(None)
    d = 0
    dcount = 0
    speed = 1
    turns = 0
    listofboxes = []
    barcodes = []
    wcount = 0
    bcount = 0
    ccount = []
    curbcode = ListProperty(None)
    turns = 0
    box = False
    home = BooleanProperty(False)
    nodearray = [1, 1]
    currentnode = [0, 0]
    seennodes = []
    mode = 0
    nodecount = 0
    xcount = 0
    ycount = 0
    scount = 0
    on = False
    initialdistance = [0, 0]
    emi = 0
    i = 0
    t = True
    end = False
    threadon = False
    xbool = True
    first = True
    second = False
    node = [0, 0]
    gp = 0
    distancefromnode = [0, 0]
    finaldistance = [0, 0]
    permpath = [[0, 0], [1, 0], [1, 1], [0, 1], [0, 0], [1, 0], [1, 1], [1, 2], [0, 2], [0, 1], [1, 1], [1, 2], [1, 3], [0, 3], [0, 2], [1, 2], [1, 3], [1, 4], [0, 4], [0, 3], [1, 3], [2, 3], [2, 4], [1, 4], [1, 3], [1, 2], [2, 2], [2, 3], [1, 3], [1, 2], [1, 1], [2, 1], [2, 2], [1, 2], [2, 1], [1, 1], [1, 0], [2, 0], [2, 1], [1, 1], [0, 1], [0, 0]]
    path = list.copy(permpath)
    badnodes = []
    emergencypathfinding = False
    temppath = None
    nodechange = BooleanProperty(False)
    def __init__(self, **k):
        super(grid, self).__init__(**k)
        width = 4
        length = 2
        self.nodearray[0] = length + 1
        self.nodearray[1] = width + 1
        # creates the "facility" with box widgets and path widgets according
        # to the width and
        for w in range(width):
            for l in range(length):

                for i in range(2):
                    for a in range(4):
                        bar = behavior.createbarcode()

                        if i == 0:
                            self.add_widget(box(size_hint=(.03, .03), pos_hint={
                                            'x': 0.3 + i * .04 + w * 2 * 0.05, 'y': 0.14 + a * .04 + l * 4 * 0.05}, angle=0, barcode=bar), index=1)
                        else:
                            self.add_widget(box(size_hint=(.03, .03), pos_hint={
                                            'x': 0.3 + i * .04 + w * 2 * 0.05, 'y': 0.14 + a * .04 + l * 4 * 0.05}, angle=180, barcode=bar), index=1)

                        self.listofboxes.append(
                            [0.3 + i * 0.04 + w * 2 * 0.05, 0.14 + a * 0.04 + l * 4 * 0.05])
                        self.barcodes.append(bar)
                        self.add_widget(home(size_hint=(.03, .03), pos_hint={
                                        'x': 0.3 + 0.5 * .04 + w * 2 * 0.05, 'y': 0.14 + a * .04 + l * 4 * 0.05}), index=3)



                self.add_widget(path(size_hint=((0.13 - 0.03) * width + 0.03, 0.048), pos_hint={
                                'x': 0.3 - 0.03, 'y': 0.11 + (0.1) * 2 * (l) - 0.0187}), index=1)
                self.add_widget(path(size_hint=((0.13 - 0.03) * width + 0.03, 0.048), pos_hint={
                                'x': 0.3 - 0.03, 'y': 0.11 + (0.1 * 2 * length - 0.0197)}), index=1)

            self.add_widget(path(size_hint=(0.03, (0.1) * (length * 2) - 0.05 + 0.001),
                                 pos_hint={'x': 0.27 + w * 0.1, 'y': 0.14 - 0.001}), index=1)
            self.add_widget(path(size_hint=(0.03, (0.1) * (length * 2) - 0.05 + 0.001),
                                 pos_hint={'x': 0.27 + width * 0.1, 'y': 0.14 - 0.001}), index=1)
        for w in range(width):
            for l in range(length):
                for i in range(3):
                    self.add_widget(home(size_hint=(.03, .03), pos_hint={
                                    'x': 0.3 + 0.5 * .04 + w * 2 * 0.05, 'y': 0.155 + i* .04 + l * 4 * 0.05}, alpha=1), index=(200))
                    self.listofboxes.append(
                            [0.3 + 0.5* 0.04 + w * 2 * 0.05, 0.155 + i * 0.04 + l * 4 * 0.05])
                    self.barcodes.append(0)

        #print(self.listofboxes[1])
        self.add_widget(home(size_hint=(0.03, 0.03), pos_hint={
                        'x': .27, 'y': .1 - 0.009}), index=1)
        self.add_widget(home(size_hint=(0.03, 0.03), pos_hint={
                        'x': .27 + width*0.1, 'y': .1 - 0.009}), index=1)
        self.add_widget(home(size_hint=(0.03, 0.03), pos_hint={
                        'x': .27 + width *0.1, 'y': .139 + (0.1) * (length * 2) - 0.05 + 0.02}), index=1)
        self.add_widget(home(size_hint=(0.03, 0.03), pos_hint={
                        'x': .27 , 'y': .139 + (0.1) * (length * 2) - 0.05 + 0.02}), index=1)
        #print(self.nodearray[0])
        self.nodearray = behavior.createnodematrix(self.nodearray)
        #print(self.barcodes)
        #print(self.listofboxes)
        #print(self.nodearray)
        # optional box in the path of the robot, must uncomment both lines to work
        #self.add_widget(home(size_hint=(0.03, 0.03), pos_hint={'x': 0.5, 'y': 0.31-0.009}, alpha = 1), index=1)
        #self.listofboxes.append([0.3, 0.31-0.009])

    def addbox(self, *a):
        self.add_widget(home(size_hint=(0.03, 0.03), pos_hint={'x': 0.5, 'y': 0.31-0.009}, alpha = 1), index=1)
        self.listofboxes.append([0.5, 0.31-0.009])
        self.barcodes.append(0)
    # car controlling function
    def update(self, *a):
        #print(self.col)
        self.ax = self.ax
        self.ay = self.ay
        if self.mode is 3:
            self.emergencyupdate()
        elif self.mode is 2:
            self.homeupdate()
        elif self.mode is 1:
            self.normalupdate()
        else:
            self.initialupdate()


    def emergencyupdate(self, *a):
        if self.emergencypathfinding is False:
            #print("this is{0}".format(self.path[self.emi+1]))

            self.temppath = behavior.nodepath(self.path[self.emi+1], self.currentnode, self.nodearray, badnodes=self.badnodes)
            #print(self.temppath)
            #print("badnodes{0}".format(self.badnodes))
            self.emergencypathfinding = True
            #self.emi += 1
        else:
            print(self.temppath)
            self.driver(self.speed, self.car.angle)
            self.home = False
            #print("final{0}".format(self.finaldistance))
            #path = [[0, 0], [1, 0], [1, 1], [0, 1], [0, 0], [1, 0], [1, 1], [1, 2], [1, 3]]
            self.pathvector(self.currentnode, self.temppath)
            #print(self.distancefromnode)
            if abs(self.distancefromnode[0]) >= self.finaldistance[0] or abs(self.distancefromnode[1]) >= self.finaldistance[1]:
                del self.temppath[0]
                self.currentnode = behavior.cnode(self.currentnode, self.car.angle)
                self.distancefromnode = [0, 0]
                if self.currentnode == self.path[self.emi+1]:
                    self.emergencypathfinding = False
                    self.emi += 1
                #print("hi")

            self.sensors()




    def normalupdate(self, *a):
        self.movepath()

    def movepath(self, *a):
        self.driver(self.speed, self.car.angle)
        self.home = False
        #print("final{0}".format(self.finaldistance))
        #path = [[0, 0], [1, 0], [1, 1], [0, 1], [0, 0], [1, 0], [1, 1], [1, 2], [1, 3]]
        self.pathvector(self.currentnode, self.path)
        #print(self.distancefromnode)
        if abs(self.distancefromnode[0]) >= self.finaldistance[0] or abs(self.distancefromnode[1]) >= self.finaldistance[1]:
            del self.path[0]
            self.currentnode = behavior.cnode(self.currentnode, self.car.angle)
            self.distancefromnode = [0, 0]
            self.nodechange = True

            #print(self.path)
            #print(self.permpath)
            #print(self.currentnode)
            if len(self.path) == 2:
                self.home = True
                self.path = list.copy(self.permpath)
        self.sensors()


    def pathvector(self, currentnode, path, *a):
        #print("current {0}".format(currentnode))
        if path.index(currentnode) + 1 in range(len(path)):
            next = path[path.index(currentnode) + 1]
            x = next[1] - currentnode[1]
            y = next[0] - currentnode[0]
        else:
            x = 0
            y = 0
        if x > 0:
            if self.car.angle == -90:
                self.distancefromnode[1] += 1

            self.car.angle = -90
        elif x < 0:
            if self.car.angle == 90:
                self.distancefromnode[1] -= 1
            self.car.angle = 90
        elif y > 0:
            if self.car.angle == 0:
                self.distancefromnode[0] += 1
            self.car.angle = 0
        elif y < 0:
            if self.car.angle == 180:
                self.distancefromnode[0] -= 1
            self.car.angle = 180
        else:
            self.speed = 0



    def anormalupdate(self, *a):
        self.time += 0.01
        delta = behavior.Drive(self.speed, self.car.angle)

        #print(self.dcount)
        # if car does not see a cube for a certain amount of time then turns
        #print(self.car.angle)
        #print
        if self.car.angle == 0 or self.car.angle == 180:
            #print(self.dcount)
            if self.dcount > int(self.xcount/2):
                self.defaultturn()

            else:
                self.ax = self.ax + delta[0]
                self.ay = self.ay + delta[1]
                self.nodecount += 1

                self.car.center_x = self.size[0] * self.ax
                self.car.center_y = self.size[1] * self.ay
                self.car.angle -= 0
                if self.car.angle > 180:
                    self.car.angle += -360
                elif self.car.angle <= -180:
                    self.car.angle += 360
                self.home = False
                self.sensors(self)
        elif self.car.angle == -90 or 90:
            #print("y")
            if self.dcount > int(self.ycount/2):
                self.defaultturn()
            #    print('y')
            else:
                self.ax = self.ax + delta[0]
                self.ay = self.ay + delta[1]
                self.nodecount += 1

                self.car.center_x = self.size[0] * self.ax
                self.car.center_y = self.size[1] * self.ay
                self.car.angle -= 0
                if self.car.angle > 180:
                    self.car.angle += -360
                elif self.car.angle <= -180:
                    self.car.angle += 360
                self.home = False
                self.sensors(self)


    def detectbadnodes(self, *a):
        self.dbetweennodes = [self.finaldistance[0]*self.velocity[0], self.finaldistance[1]*self.velocity[1]]
        if self.distance > 0.06:
            self.mode = 3
            if self.car.angle == 0:
                nodedelta = math.ceil(self.distance / self.dbetweennodes[1])
                a = [self.currentnode[0], self.currentnode[1] + nodedelta]
                nodedelta = math.floor(self.distance / self.dbetweennodes[1])
                self.badnodes.append([[self.currentnode[0], self.currentnode[1] + nodedelta], [a]])
                #print(self.badnodes)
            elif self.car.angle == 180:
                nodedelta = math.ceil(self.distance / self.dbetweennodes[1])
                self.badnodes.append([self.currentnode[0], self.currentnode[1]-nodedelta])
                nodedelta = math.floor(self.distance / self.dbetweennodes[1])
                self.badnodes.append([self.currentnode[0], self.currentnode[1]-nodedelta])

            elif self.car.angle == -90:
                nodedelta = math.ceil(self.distance / self.dbetweennodes[0])
                self.badnodes.append([self.currentnode[0]-nodedelta, self.currentnode[1]])
                nodedelta = math.floor(self.distance / self.dbetweennodes[0])
                self.badnodes.append([self.currentnode[0]-nodedelta, self.currentnode[1]])

            elif self.car.angle == 90:
                nodedelta = math.ceil(self.distance / self.dbetweennodes[0])
                self.badnodes.append(self.currentnode[0] + nodedelta, self.currentnode[1])
                nodedelta = math.floor(self.distance / self.dbetweennodes[0])
                self.badnodes.append(self.currentnode[0] + nodedelta, self.currentnode[1])





    def resize(self, *a):
        self.ax = self.ax
        self.ay = self.ay

        self.car.x = self.size[0] * self.ax
        self.car.y = self.size[1] * self.ay

    def sensors(self, *a):
        self.d = behavior.distancesensor(
            self.listofboxes, self.ax, self.ay, self.car.angle, self.barcodes)
        #print(self.d)
        if self.d is not None:
            self.distance = self.d[0]

            if self.d[1] is not None:
                self.boxid = self.d[1][1]

            if self.d[1] is not None:
                self.col = self.d[1]
                #print(self.col)

                if self.col[0] == [1, 1, 1, 1]:
                    self.wcount += 1
                    self.bcount = 0

                    #print(self.ccount)
                    if self.wcount > 5*1/self.speed:
                        self.ccount.append(1)
                        self.wcount = 0
                        #print(len(self.ccount))
                        if len(self.ccount) == 4:
                            #print("hehehehe")
                            self.curbcode = self.ccount

                    #print(self.wcount)
                if self.col[0] == [0, 0, 0, 1]:
                    self.bcount += 1
                    self.wcount = 0
                    #print("this is the bcount{0}".format(self.bcount))
                    if self.bcount > 5*1/self.speed:
                        self.ccount.append(0)
                        self.bcount = 0
                        #if len(self.ccount) > 2:
                            #print(len(self.ccount))
                        if len(self.ccount) == 4:
                            self.curbcode = self.ccount

                    #print("bcount:{0}".format(self.bcount))
            else:
                self.col = [[1, 0, 0, 1]]
                self.wcount = 0
                self.bcount = 0
                self.ccount = []
            self.dcount = 0

        else:
            self.distance = -1000000000
            self.col = [[0, 0, 1, 1]]
            self.wcount = 0
            self.bcount = 0
            self.dcount += 1
            self.ccount = []

    def initialupdate(self, *a):
        if self.end is False:
            delta = behavior.Drive(1*self.speed, self.car.angle)
            self.ax = self.ax + delta[0]
            self.ay = self.ay + delta[1]
            self.car.center_x = self.size[0] * self.ax
            self.car.center_y = self.size[1] * self.ay
            #print(self.initialdistance)
            self.d = behavior.distancesensor(
                self.listofboxes, self.ax, self.ay, self.car.angle, self.barcodes)

            #print(self.scount)
            if self.d is None:
                if self.first is not True and self.second is not True:
                    self.scount += 1
                #print(self.scount)
            else:
                if self.first is True:
                    self.first = self.d[0]
                    #print(self.first)
                #print(self.scount)
                if self.second is False:
                    self.second = self.d[0]
                    #print(self.second)

                if self.scount > 0:
                    if self.on is False:
                        self.xcount = self.scount
                        #print(int(self.xcount/2))
                        for i in range(int(self.xcount/2)):
                            #print('thread')
                            x = threading.Thread(target=self.Threader)
                            x.start()

                        self.initialdistance[0] += int(self.xcount)
                        self.car.angle = -90
                        self.scount = -int(self.xcount)
                        #print(self.scount)
                        self.on = True
                        self.t = False
                        self.second = False

                    else:
                        self.ycount = self.scount
                        #print(self.scount)
                        for i in range(int(self.ycount/2)):
                            x = threading.Thread(target=self.Threader)
                            x.start()
                        self.initialdistance[1] += int(self.ycount)
                        self.car.angle = -90
                        self.scount = -int(self.ycount/2)
                        #self.finaldistance = self.initialdistance
                        self.on = False
                        self.end = True

                elif self.on is True:
                    self.initialdistance[1] += 1
                elif self.on is False:
                    self.initialdistance[0] += 1
                if self.t is True:
                    self.scount = 0
                else:
                    self.scount = self.scount
                    self.t = True
            #print(self.initialdistance)
        else:
            print(self.finaldistance)
            self.driver(-1* self.speed)
            if self.xbool is True:
                #print(self.initialdistance)
                self.initialdistance[1] -= 1
                self.finaldistance[1] += 1
                if self.initialdistance[1] == 0:
                    self.xbool = False
                    self.car.angle = 0
            else:
                #print(self.initialdistance)
                #print(self.initialdistance)

                self.initialdistance[0] -= 1
                self.finaldistance[0] += 1
                if self.initialdistance[0] == 0:
                    self.mode = 1


    def driver(self, velocity, *a):
        delta = behavior.Drive(velocity, self.car.angle)
        self.ax = self.ax + delta[0]
        self.ay = self.ay + delta[1]
        #print(delta)
        self.velocity = delta
        self.car.center_x = self.size[0] * self.ax
        self.car.center_y = self.size[1] * self.ay

    def driveback(self, *a):
        self.driver(-1*self.speed)

    def Threader(self):

        self.driveback()

        self.threadon = False

    def defaultturn(self, *a):
        self.nodecount = 0
        #print(self.turns)
        if self.turns in list(range(5)) + list(range(6, 10)) + list(range(11, 15)) + list(range(16, 19)) + list(range(20, 23)) + list(range(24, 28)) + list(range(29, 33)) + list(range(34, 37)) + list(range(38, 41)):

            self.currentnode = behavior.cnode(self.currentnode, self.car.angle)

            #print(behavior.nodepath(self.currentnode, [0, 0], self.nodearray))
            self.car.angle -= 90
            self.dcount = 0
            self.turns += 1

            if self.turns == 40:
                self.dcount += -1
                self.turns = 0

                self.home = True


        elif self.turns in [5, 10, 15, 19,23, 28, 33, 37]:
            self.currentnode = behavior.cnode(self.currentnode, self.car.angle)
            self.car.angle -= 0
            self.dcount = -int(20*(1/self.speed))
            self.turns += 1

    def pickupbox(self, instance, value):
        if value == True:

            self.add_widget(replacementbox(size_hint=[0.03, 0.03], pos_hint={'x':self.listofboxes[self.boxid][0], 'y':self.listofboxes[self.boxid][1]}), index=1)
            self.barcodes[self.boxid] = 0
            #time.sleep(0.5)

    def homepath(self, *a):
        self.path = behavior.nodepath([0, 0], self.currentnode, self.nodearray)
        #print(self.nodearray)

    def homeupdate(self, *a):
        self.currentnode == self.path
        #print(self.currentnode)
        #print(self.path)
        if [self.currentnode] == self.path:
            self.driver(-self.speed, self.car.angle)
            self.distancefromnode[0] -= 1
            #print(self.distancefromnode)
            if self.distancefromnode[0] == 0:
                self.home = True
                self.path =list.copy(self.permpath)
                self.mode = 1
        else:
            self.driver(self.speed, self.car.angle)
            self.pathvector(self.currentnode, self.path)
            #print(self.currentnode)
            #print("ha{0}".format(self.path))
            if abs(self.distancefromnode[0]) >= self.finaldistance[0] or abs(self.distancefromnode[1]) >= self.finaldistance[1]:

                del self.path[0]
                self.currentnode = behavior.cnode(self.currentnode, self.car.angle)
                self.distancefromnode = [0, 0]
                if self.currentnode == [0, 0]:
                    self.home = True
                    self.path = list.copy(self.permpath)
                    self.mode = 1

                #print(self.path)
                #print(self.permpath)
                #print(self.currentnode)



    def updatemode(self, instance, value):

        if value is True:
            self.mode = 2
        else:
            self.mode = 1

class VisionBox(BoxLayout):
    col = ObjectProperty(None)
    barcodes = ObjectProperty(None)


class Barcodereader(Widget):
    id = StringProperty('black0.png')
    found = BooleanProperty(False)
    bid = ""
    aid = ""

    def idupdate(self, instance, value):
        if self.found is False:
            if value == [0, 1, 1, 1]:
                self.id = 'Barcode1.png'
            if value == [0, 1, 0, 1]:
                self.id = 'Barcode2.png'
            if value == [0, 0, 1, 1]:
                self.id = 'Barcode3.png'
            if value == [0, 1, 1, 0]:
                self.id = 'Barcode4.png'
            self.aid = self.id
        if self.aid == self.bid:
            self.found = True
            self.id = "Green.png"


    def bidupdate(self, instance, value):
        self.bid = value

    def homeupdate(self, instance, value):
        if value is True:
            self.id = 'black0.png'
            self.found = False




# class for the boxes that the robot picks up
class box(Widget):
    bc = NumericProperty(0)
    angle = NumericProperty(0)
    barcode = ListProperty(None)
    pass

class replacementbox(Widget):
    pass
# class for the "homes" that the robot uses to triangulate its position
class home(Widget):
    alpha = NumericProperty(0)


# empty widget filled with path rectangle in .kv
class path(Widget):

    pass




# car class attached to the grid widget in .kv
class Car(Widget):
    velocity = ListProperty([1, 15])
    k = 0
    angle = NumericProperty(0)

    def __init__(self, **k):
        super(Car, self).__init__(**k)


# color class indicating what the color/distance sensor is seeing
class Co(Widget):
    c = ListProperty([0, 0, 1, 1])
    txt = StringProperty("start")

    def colorchange(self, instance, value):
        #print("this is the value{0}".format(value))
        self.c = value[0]

    def valuechange(self, instance, value):
        if value == -1000000000:
            self.txt = "NULL"
        else:
            self.txt = str(value)


# class that emulates the screen of the robot
class Lcd(BoxLayout):
    a = NumericProperty(0)
    b = NumericProperty(0)
    c = NumericProperty(0)
    s = ListProperty([1, 1])
    A = StringProperty("")
    B = StringProperty("")
    C = StringProperty("")

    def upsize(self, instance, value):
        self.s = value

    def upposition(self, instance, value):

        x = value[0] / self.s[0]
        y = value[1] / self.s[1]
        self.a = ((x - 0.27)**(2) + (y - (0.1 - 0.009))**(2))**0.5
        self.b = ((x - 0.47)**(2) + (y - (0.1 - 0.009))**(2))**0.5
        self.c = ((x - 0.27)**(2) + (y - (0.915 - 0.009))**(2))**0.5

    def dispposition(self, instance):
        self.A = str(self.a)
        self.B = str(self.b)
        self.C = str(self.c)

class ButtonLayout(BoxLayout):
    boxy = ObjectProperty(None)
    barcodes = ObjectProperty(None)



class BarcodeButtonLayout(BoxLayout):
    b1 = ObjectProperty(None)
    b2 = ObjectProperty(None)
    b3 = ObjectProperty(None)
    b4 = ObjectProperty(None)

    def __init__(self, **k):
        super(BarcodeButtonLayout, self).__init__(**k)




# button class for triangulating positions
class Triangulate(Button):
    pass


class Barcode1(Button):
    pass


class Barcode2(Button):
    pass


class Barcode3(Button):
    pass


class Barcode4(Button):
    pass


class Cbar(Widget):
    current = ObjectProperty(None)
    id = StringProperty('black.png')
    def bar1(self, instance):
        self.id = 'Barcode1.png'

    def bar2(self, instance):
        self.id = 'Barcode2.png'

    def bar3(self, instance):
        self.id = 'Barcode3.png'

    def bar4(self, instance):
        self.id = 'Barcode4.png'

class Addboxbutton(Button):
    pass

class Tribox(BoxLayout):
    tri = ObjectProperty(None)
    curbar = ObjectProperty(None)
    addbox = ObjectProperty(None)
# App class, run the app
class RunApp(App):
    def build(self):
        return rootclass()


# runs the app class
if __name__ == '__main__':
    RunApp().run()
