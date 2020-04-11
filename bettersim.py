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
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import *
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
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
        self.add_widget(Button())
        self.add_widget(Button())

        # update schedule for the widgets
        Clock.schedule_interval(self.g.update, 1/(60))
        self.g.bind(size=self.g.update)
        self.g.bind(col=self.color.colorchange)


# this is the class that draws the boxes and path for the robot to follow
class grid(RelativeLayout):
    car = ObjectProperty(None)
    col = NumericProperty(0)
    time = NumericProperty(0)
    ax = NumericProperty(0.27)
    ay = NumericProperty(0.14)
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

    def update(self, *a):
        self.time += 0.01
        delta = behavior.Drive(self.speed, self.car.angle)
        #print(self.dcount)
        if self.dcount > 20*abs(self.speed):
            self.ax = self.ax
            self.ay = self.ay
            self.car.angle -= 90
            self.dcount = 0
            self.turns += 1
        else:
            self.ax = self.ax + delta[0]
            self.ay = self.ay + delta[1]

            self.car.x = self.size[0]*self.ax
            self.car.y = self.size[1]*self.ay
            self.car.angle -= 0
            if self.car.angle > 180:
                self.car.angle += -360
            elif self.car.angle <= -180:
                self.car.angle +=360

            distance = behavior.distancesensor(self.listofboxes, self.ax+0.01, self.ay+0.01, self.car.angle)
            if distance != None:
                self.col = 1
                print(self.car.angle)
                self.dcount = 0

            else:
                self.col = 0
                self.dcount += 1


# empty widget class filled with a box in .kv
class box(Widget):

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


# color class indicating what the color sensor is seeing
class Co(Widget):
    c = NumericProperty(0)

    def colorchange(self, instance, value):
        self.c = value



# App class, run the app
class RunApp(App):
    def build(self):
        return rootclass()


# runs the app class
if __name__ == '__main__':
    RunApp().run()
