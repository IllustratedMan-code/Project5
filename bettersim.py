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
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, StringProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.image import Image
import behavior


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
        self.color = Co()
        self.add_widget(self.color)
        # adds the lcd widget
        self.lcd = Lcd()
        self.add_widget(self.lcd)
        # adds the triangulate button
        self.tri = triangulate()
        self.add_widget(self.tri)

        # update schedule for the widgets
        Clock.schedule_interval(self.g.update, 1/(60))
        self.g.bind(size=self.g.resize)
        self.g.bind(size=self.lcd.upsize)
        self.g.bind(col=self.color.colorchange)
        self.g.bind(distance=self.color.valuechange)
        self.g.car.bind(center=self.lcd.upposition)
        self.tri.bind(on_release=self.lcd.dispposition)


# this is the class that draws the boxes and path for the robot to follow
class grid(RelativeLayout):
    car = ObjectProperty(None)
    col = NumericProperty(0)
    time = NumericProperty(0)
    ax = NumericProperty(0.285)
    ay = NumericProperty(0.14)
    distance = NumericProperty(0)
    d = 0
    dcount = 0
    speed = 1
    turns = 0
    listofboxes = []
    def __init__(self, **k):
        super(grid, self).__init__(**k)
        width = 2
        length = 4


        for w in range(width):
            for l in range(length):
                for i in range(2):
                    for a in range(4):
                        self.add_widget(box(size_hint=(.03, .03), pos_hint={'x': 0.3 + i * .04 + w*2*0.05, 'y': 0.14 + a*.04+l*4*0.05}), index = 1)
                        self.listofboxes.append([0.3+i*0.04+w*2*0.05, 0.14+a*0.04+l*4*0.05])

                self.add_widget(path(size_hint=((0.13-0.03)*width+0.03, 0.048), pos_hint={'x':0.3-0.03, 'y':0.11+(0.1)*2*(l)-0.0187}), index=1)
                self.add_widget(path(size_hint=((0.13-0.03)*width+0.03, 0.048), pos_hint={'x':0.3-0.03, 'y':0.11+(0.1*2*length-0.0197)}), index=1)

            self.add_widget(path(size_hint=(0.03, (0.1)*(length*2)-0.05+0.001), pos_hint={'x':0.27+w*0.1, 'y':0.14-0.001}), index=1)
            self.add_widget(path(size_hint=(0.03, (0.1)*(length*2)-0.05+0.001), pos_hint={'x':0.27+width*0.1, 'y':0.14-0.001}), index=1)
        print(self.listofboxes[1])
        self.add_widget(box(size_hint=(0.03, 0.03), pos_hint={'x': .27, 'y': .1-0.009}, bc=1), index=1)
        self.add_widget(box(size_hint=(0.03, 0.03), pos_hint={'x': .47, 'y': .1-0.009}, bc=1), index=1)
        self.add_widget(box(size_hint=(0.03, 0.03), pos_hint={'x': .47, 'y': .915-0.009}, bc=1), index=1)
        #self.add_widget(box(size_hint=(0.03, 0.03), pos_hint={'x': 0.3, 'y': 0.31-0.009}, bc = 0), index=1)
        #self.listofboxes.append([0.3, 0.31-0.009])

    def update(self, *a):
        self.time += 0.01
        delta = behavior.Drive(self.speed, self.car.angle)

        if self.dcount > 15*abs(self.speed):
            self.ax = self.ax
            self.ay = self.ay
            self.car.angle -= 90
            self.dcount = 0
            self.turns += 1
        else:
            self.ax = self.ax + delta[0]
            self.ay = self.ay + delta[1]

            self.car.center_x = self.size[0]*self.ax
            self.car.center_y = self.size[1]*self.ay
            self.car.angle -= 0
            if self.car.angle > 180:
                self.car.angle += -360
            elif self.car.angle <= -180:
                self.car.angle += 360

            self.d = behavior.distancesensor(self.listofboxes, self.ax, self.ay, self.car.angle)
            if self.d != None:
                self.distance = self.d
                self.col = 1
                self.dcount = 0

            else:
                self.distance = -1000000000
                self.col = 0
                self.dcount += 1

    def resize(self, *a):
        self.ax = self.ax
        self.ay = self.ay

        self.car.x = self.size[0]*self.ax
        self.car.y = self.size[1]*self.ay


# empty widget class filled with a box in .kv
class box(Widget):
    bc = NumericProperty(0)
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
    c = NumericProperty(0)
    txt = StringProperty("start")

    def colorchange(self, instance, value):
        self.c = value

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

        x = value[0]/self.s[0]
        y = value[1]/self.s[1]
        self.a = ((x-0.27)**(2)+(y-(0.1-0.009))**(2))**0.5
        self.b = ((x-0.47)**(2)+(y-(0.1-0.009))**(2))**0.5
        self.c = ((x-0.27)**(2)+(y-(0.915-0.009))**(2))**0.5

    def dispposition(self, instance):
        self.A = str(self.a)
        self.B = str(self.b)
        self.C = str(self.c)


# button class for triangulating positions
class triangulate(Button):
    pass


# App class, run the app
class RunApp(App):
    def build(self):
        return rootclass()


# runs the app class
if __name__ == '__main__':
    RunApp().run()
