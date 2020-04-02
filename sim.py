import kivy
from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '700')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button

from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *
from kivy.core.window import Window
from kivy.properties import (ObjectProperty, ReferenceListProperty, ListProperty)
import random
from kivy.clock import Clock
from kivy.vector import Vector


class board(FloatLayout):
    car = ObjectProperty(None)
    def __init__(self, **k):
        super(board, self).__init__(**k)
        with self.canvas.before:
            l = 5
            w = 4
            for b in range(1, l+1):
                for a in range(1,w+1):
                    for i in range(3):
                        for x in range(2):
                            numb = random.randint(1, 2)

                            if numb == 1:

                                Color(1, 0, 0, 1)
                                Rectangle(pos=(a*70+20*(x)-50, b*80+20*(i)-20), size=(10, 10))
                    Color(0,1,0,1)
                    print(a)
                    print(b)

                    Rectangle(pos=(a*70-10, 20), size=(20, l*80+35))
                    Rectangle(pos=(0, 20), size=(20, l*80+35))
                    Rectangle(pos=(20, 20), size=(w*70-30, 20))
                Rectangle(pos=(20, b*80 + 35), size=(w*70-30, 20))




class Car(Widget):
    velocity = ListProperty([0, 1])
    def __init__(self, **k):
        super(Car, self).__init__(**k)
        self.canvas.add(Color(1,0,0,1))

        Clock.schedule_interval(self.update, 1.0/60.0)


    def update(self, *args):
        self.x += self.velocity[0]
        self.y += self.velocity[1]




class RobotApp(App):

    def build(self):
        ba= Car()

        return board()


if __name__ == '__main__':
    RobotApp().run()
