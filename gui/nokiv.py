
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.stencilview import StencilView
from random import random as r
from functools import partial
from kivy.clock import Clock

class StencilTestWidget(StencilView):
    '''Drag to define stencil area
    '''
    def defineMask(self, x=20, y=360):
        self.pos = (x, y)
        self.size = (325, 500)
        self.level = 1
        Clock.schedule_interval(self.on_timeout, 0.01)
        
    def on_timeout(self, *args): 
        self.level +=1
        if self.level > 265:
            self.level = 265
        self.pos = (15, self.level)
        
    def on_touch_down(self, touch):
        self.pos = touch.pos
        self.size = (1, 1)

    def on_touch_move(self, touch):
        self.size = (touch.x - touch.ox, touch.y - touch.oy)


class StencilCanvasApp(App):

    def add_rects(self, wid, x, *largs):
        with wid.canvas:
            Color(0, 1, 0, mode="rgb")
            Ellipse(pos=(x, 30), size=(300, 500)) 
        
    def build(self):
        wid = StencilTestWidget(size_hint=(None, None), size=(200,500), pos=(0,360))
        sec = StencilTestWidget(size_hint=(None, None), size=Window.size, pos=(0, 350))
        

##        btn_add500 = Button(text='+ 200 rects')
##        btn_add500.bind(on_press=partial(self.add_rects, wid))
##
##        btn_reset = Button(text='Reset Rectangles')
##        btn_reset.bind(on_press=partial(self.reset_rects, label, wid))
##
##        btn_stencil = Button(text='Reset Stencil')
##        btn_stencil.bind(on_press=partial(self.reset_stencil, wid))
##
        layout = BoxLayout(size_hint=(1, None), height=50)
##        layout.add_widget(btn_add500)
##        layout.add_widget(btn_reset)
##        layout.add_widget(btn_stencil)
##        layout.add_widget(label)

        #Define the ovals
        self.add_rects(wid, 30)
        self.add_rects(sec, 30)
        
        #define the masks
        wid.defineMask(20, 360)
        sec.defineMask(360,30)
        
        #self.addEye()
        root = FloatLayout()
        canvas = FloatLayout()
        with canvas.canvas:
            Color(1, 1, 1, mode="rgb")
            but = Ellipse(pos=(30,30), size=(300, 500))
            Color(0, 0, 0, mode="rgb")
            but = Ellipse(pos=(100,90), size=(75, 130))
            Color(1, 1, 1, mode="rgb")
            but = Ellipse(pos=(360,30), size=(300, 500))
            Color(0, 0, 0, mode="rgb")
            but = Ellipse(pos=(420,90), size=(75, 130))
    
        rfl = FloatLayout()
        #rfl.add_widget(wid)
        rfl.add_widget(sec)
        root.add_widget(canvas)
        root.add_widget(rfl)
        root.add_widget(layout)

        return root


if __name__ == '__main__':
    StencilCanvasApp().run()
