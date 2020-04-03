import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import *


# base class that handles the placing of all widgets
class rootclass(BoxLayout):
    def __init__(self, **k):
        super(rootclass, self).__init__(**k)
        self.add_widget(grid())


# this is the class that draws the boxes and path for the robot to follow
class grid(RelativeLayout):

    def __init__(self, **k):
        super(grid, self).__init__(**k)
        width = 2
        length = 4
        for w in range(width):
            for l in range(length):
                for i in range(2):
                    for a in range(4):
                        self.add_widget(box(size_hint=(.03, .03), pos_hint={'center_x': 0.3 + i * .04 + w*width*0.05, 'center_y': 0.2 + a*.04+l*length*0.05}))


# empty widget class filled with a box in .kv
class box(Widget):

    pass


# App class, run the app
class RunApp(App):
    def build(self):
        return rootclass()


# runs the app class
if __name__ == '__main__':
    RunApp().run()
