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
        #self.color.barcodes.bind(found=self.g.updatemode)



# this is the class that draws the boxes and path for the robot to follow in additon
# to housing the main function controlling the robot
class grid(RelativeLayout):
    car = ObjectProperty(None)
    col = ListProperty(None)
    time = NumericProperty(0)
    ax = NumericProperty(0.285)
    ay = NumericProperty(0.14)
    distance = NumericProperty(0)
    barcode = ListProperty(None)
    d = 0
    dcount = 0
    speed = 4
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
    mode = False
    nodecount = 0



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

                self.add_widget(path(size_hint=((0.13 - 0.03) * width + 0.03, 0.048), pos_hint={
                                'x': 0.3 - 0.03, 'y': 0.11 + (0.1) * 2 * (l) - 0.0187}), index=1)
                self.add_widget(path(size_hint=((0.13 - 0.03) * width + 0.03, 0.048), pos_hint={
                                'x': 0.3 - 0.03, 'y': 0.11 + (0.1 * 2 * length - 0.0197)}), index=1)

            self.add_widget(path(size_hint=(0.03, (0.1) * (length * 2) - 0.05 + 0.001),
                                 pos_hint={'x': 0.27 + w * 0.1, 'y': 0.14 - 0.001}), index=1)
            self.add_widget(path(size_hint=(0.03, (0.1) * (length * 2) - 0.05 + 0.001),
                                 pos_hint={'x': 0.27 + width * 0.1, 'y': 0.14 - 0.001}), index=1)

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

        #print(self.nodearray)
        # optional box in the path of the robot, must uncomment both lines to work
        #self.add_widget(box(size_hint=(0.03, 0.03), pos_hint={'x': 0.3, 'y': 0.31-0.009}, bc = 0), index=1)
        #self.listofboxes.append([0.3, 0.31-0.009])

    # car controlling function
    def update(self, *a):
        #print(self.col)
        if self.mode is True:
            self.homeupdate()
        else:
            self.normalupdate()

    def normalupdate(self, *a):
        self.time += 0.01
        delta = behavior.Drive(self.speed, self.car.angle)

        #print(self.dcount)
        # if car does not see a cube for a certain amount of time then turns
        if self.dcount > 15 * (1/abs(self.speed)):
            print(self.nodecount)
            self.nodecount = 0
            if self.turns in list(range(5)) + list(range(6, 10)) + list(range(11, 15)) + list(range(16, 19)) + list(range(20, 23)) + list(range(24, 28)) + list(range(29, 33)) + list(range(34, 37)) + list(range(38, 41)):


                self.currentnode = behavior.cnode(self.currentnode, self.car.angle)

                #print(behavior.nodepath(self.currentnode, [0, 0], self.nodearray))
                self.car.angle -= 90
                self.dcount = 0
                self.turns += 1

                if self.turns == 40:
                    self.turns = 0
                    self.home = True


            elif self.turns in [5, 10, 15, 19,23, 28, 33, 37]:
                self.currentnode = behavior.cnode(self.currentnode, self.car.angle)
                self.car.angle -= 0
                self.dcount = -int(20*(1/self.speed))
                self.turns += 1




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

    def resize(self, *a):
        self.ax = self.ax
        self.ay = self.ay

        self.car.x = self.size[0] * self.ax
        self.car.y = self.size[1] * self.ay

    def sensors(self, *a):
        self.d = behavior.distancesensor(
            self.listofboxes, self.ax, self.ay, self.car.angle, self.barcodes)
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
                    if self.wcount > math.floor(6*1/self.speed):
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
                    if self.bcount > math.floor(6*1/self.speed):
                        self.ccount.append(0)
                        self.bcount = 0
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

    def pickupbox(self, instance, value):
        if value == True:

            self.add_widget(replacementbox(size_hint=[0.03, 0.03], pos_hint={'x':self.listofboxes[self.boxid][0], 'y':self.listofboxes[self.boxid][1]}), index=1)
            self.barcodes[self.boxid] = 0
            #time.sleep(0.5)

    def homeupdate(self, *a):
        print(self.nodecount)
        if self.nodecount > 0:
            delta = behavior.Drive(-1*self.speed, self.car.angle)
            self.ax = self.ax + delta[0]
            self.ay = self.ay + delta[1]

            self.car.center_x = self.size[0] * self.ax
            self.car.center_y = self.size[1] * self.ay
            self.nodecount -= 1


    def updatemode(self, instance, value):

        self.mode = value

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
    pass


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


class Tribox(BoxLayout):
    tri = ObjectProperty(None)
    curbar = ObjectProperty(None)

# App class, run the app
class RunApp(App):
    def build(self):
        return rootclass()


# runs the app class
if __name__ == '__main__':
    RunApp().run()
