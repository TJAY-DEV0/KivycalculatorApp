from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color,RoundedRectangle,Ellipse
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget

class EllipsedWidget(Widget):
    def __init__(self,ball_color,**kwargs):
        super(EllipsedWidget,self).__init__(**kwargs)
        
        with self.canvas.before:
            self.ball_color = Color(ball_color)
            self.ball = Ellipse(pos=self.pos,size=self.size)
        
            self.bind(pos=self.update_ball,size=self.update_ball)
        
        
        
    def update_ball(self,instance,value):
        self.ball.pos = instance.pos
        self.ball.size = instance.size 
        
class  SwitchS(FloatLayout):
    def __init__(self,toggle,**kwarg):
        super(SwitchS,self).__init__(**kwarg)
        self.toggle = toggle
        with self.canvas.before:
            self.rect_color = Color(.4,.8,.4)
            self.rect = RoundedRectangle(pos=self.pos,size=self.size,radius=[50])
            self.bind(pos=self.update_rect,size=self.update_rect)
            
        default_color = ()
        default_pos = 0
        if self.toggle:
            self.rect_color.rgb = (.4,.8,.4)
            default_color =  (.3,.3,.3)
            default_pos = 0.702
        else:
            self.rect_color.rgb = (.3,.3,.3)
            default_color =  (.4,.8,.4)
            default_pos = 0.298
                    
        self.ball = EllipsedWidget(Color(default_color),pos_hint={'center_x':default_pos , 'center_y': 0.5},size_hint=(.5,0.9))
        self.add_widget(self.ball)
            
        
        if self.toggle:
                self.ball.ball_color.rgb = (.3,.3,.3)
        else:
                self.ball.ball_color.rgb = (.4,.8,.4)
        
    def update_rect(self,instance,value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_touch_down(self,touch):
        if self.collide_point(*touch.pos):
            self.toggle = not self.toggle
            if self.toggle:
                self.ball.pos_hint = {'center_x':0.702}
                self.rect_color.rgb = (.4,.8,.4)
                self.ball.ball_color.rgb = (.3,.3,.3)
            else:
                self.ball.pos_hint = {'center_x':0.298}
                self.rect_color.rgb = (.3,.3,.3)
                self.ball.ball_color.rgb = (.4,.8,.4)
                