# library requirements:
# kivy

import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import *
from kivy.properties import ListProperty
from kivy.clock import Clock
from math import sin
from kivy.core.window import Window


# base class that handles the placing of all widgets
class rootclass(GridLayout):
    def __init__(self, **k):
        super(rootclass, self).__init__(**k)
        self.rows = 2
        self.cols = 2
        self.add_widget(grid())


# this is the class that draws the boxes and path for the robot to follow
class grid(RelativeLayout):

    def __init__(self, **k):
        super(grid, self).__init__(**k)
        width = 5
        length = 4
        for w in range(width):
            for l in range(length):
                for i in range(2):
                    for a in range(4):
                        self.add_widget(box(size_hint=(.03, .03), pos_hint={'x': 0.3 + i * .04 + w*2*0.05, 'y': 0.14 + a*.04+l*4*0.05}), index = 1)
                self.add_widget(path(size_hint=((0.13-0.03)*width+0.03, 0.048), pos_hint={'x':0.3-0.03, 'y':0.11+(0.1)*2*(l)-0.0187}), index=1)
                self.add_widget(path(size_hint=((0.13-0.03)*width+0.03, 0.048), pos_hint={'x':0.3-0.03, 'y':0.11+(0.1*2*length-0.0197)}), index=1)

            self.add_widget(path(size_hint=(0.03, (0.1)*(length*2)-0.05+0.001), pos_hint={'x':0.27+w*0.1, 'y':0.14-0.001}), index=1)
            self.add_widget(path(size_hint=(0.03, (0.1)*(length*2)-0.05+0.001), pos_hint={'x':0.27+width*0.1, 'y':0.14-0.001}), index=1)


# empty widget class filled with a box in .kv
class box(Widget):

    pass


# empty widget filled with path rectangle in ,kv
class path(Widget):

    pass


class Car(Widget):
    velocity = ListProperty([1, 15])
    k = 0

    def __init__(self, **k):
        super(Car, self).__init__(**k)
        Clock.schedule_interval(self.update, 1/(60))

    def update(self, *a):
        self.k += 1
        self.x = Window.size[0] * (0.5 + self.k/100)
        self.y = Window.size[1] * .5
        print(self.pos)


# App class, run the app
class RunApp(App):
    def build(self):
        return rootclass()


# runs the app class
if __name__ == '__main__':
    RunApp().run()
