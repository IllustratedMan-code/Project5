'''from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color'''
import behavior

'''class CornerRectangleWidget(Widget):
    def __init__(self, **kwargs):
        super(CornerRectangleWidget, self).__init__(**kwargs)

        with self.canvas:
            Color(1, 0, 0, 1)  # set the colour to red
            self.rect = Rectangle(pos=self.center,
                                  size=(self.width/2.,
                                        self.height/2.))

        self.bind(pos=self.update_rect,
                  size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class theApp(App):
    def build(self):
        return CornerRectangleWidget()


if __name__ == '__main__':
    theApp().run()'''
import behavior
array = behavior.createnodematrix([5, 3])
a=behavior.nodesense([1, 0], array)[0]
behavior.nodesense([2, 2], array)
print(behavior.nodepath([4, 2], [0, 0], array))
