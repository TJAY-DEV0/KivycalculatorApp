from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.graphics import RoundedRectangle,Color,Rectangle
from kivy.clock import Clock
import math
import time

class RoundedInput(FloatLayout):
    def __init__(self,**kwargs):
        super(RoundedInput,self).__init__(**kwargs)
        
        
        
        with self.canvas.before:
            Color(0.4,0.4,0.4)
            self.rect = RoundedRectangle(pos=self.pos,size=self.size,radius=[10])
            self.bind(pos=self.update_rect,size=self.update_rect)
            
        self.text_input = TextInput(background_color=(0,0,0,0),multiline=False,pos=self.pos,size=self.size,font_size=100,hint_text='2+2',keyboard=False,focus=True)
        self.add_widget(self.text_input)
        self.bind(pos=self.update_pos,size=self.update_pos)
        
        
        
        #Dropmenu
        self.menu = DropDown()
        self.btn_drop_menu = Button(size_hint=(.2,.4),background_normal="assets/images/menu_dots.png",background_down="assets/images/menu_dots.png",pos_hint={'right':0.98,'top':0.95})
        self.add_widget(self.btn_drop_menu)
        self.btn_drop_menu.bind(on_release=self.menu.open)
        
        self.history_button = Button(text='history',size_hint_y=None,height=40)
        self.setting_button = Button(text='setting',size_hint_y=None,height=40)
        self.menu.add_widget(self.history_button)
        self.menu.add_widget(self.setting_button)
        
        self.result_label = IncrementLabel(text="0",font_size=70,size_hint=(.2,.4),pos_hint={"right":0.95,"top":0.40})
        self.add_widget(self.result_label)
        
        
    def update_rect(self,instance,value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    def update_pos(self,instance,value):
        self.text_input.pos = instance.pos
        self.text_input.size = instance.size


class IncrementLabel(Label):
    def __init__(self, **kwargs):
        super(IncrementLabel, self).__init__(**kwargs)
        self.count = 0
        self.target = 0
        self.increment_by = 0
        self.incrementing = True
        self.event = None # Store the clock event

    def increment(self, dt):
        if self.incrementing:
            if self.count < self.target:
                self.count += self.increment_by
                # Ensure we don't overshoot
                if self.count > self.target:
                    self.count = self.target
            else:
                self.count = self.target
                self.event.cancel() # Cancel the event here for increasing values
        else:
            if self.count > self.target:
                self.count -= self.increment_by
                # Ensure we don't overshoot
                if self.count < self.target:
                    self.count = self.target
            else:
                self.count = self.target
                self.event.cancel() # Cancel the event here for decreasing values

        self.text = str(int(self.count))

    def start_increment(self, start_value, end_value):
        # Cancel any previous increment event to prevent conflicts
        if self.event:
            self.event.cancel()

        self.count = start_value
        self.target = end_value
        self.text = str(self.count)
        difference = abs(end_value - start_value)
        if difference == 0:
            return

        self.incrementing = end_value > start_value
        place_value = 10 ** math.floor(math.log10(difference))
        self.increment_by = max(1, place_value // 10)

        self.event = Clock.schedule_interval(self.increment, 0.5 / (difference / self.increment_by))



        
        
class RoundedButton(Button):
    def __init__(self,btn_color,**kwargs):
        super(RoundedButton,self).__init__(**kwargs)
        self.btn_color = btn_color
        
        self.background_color = 0.2,0.6,1,0
        with self.canvas.before:
            self.button_color = Color(.3,.4,1)
            self.rect =  RoundedRectangle(pos=self.pos,size=self.size,radius=[20])
            
            self.bind(pos=self.update_rect,size=self.update_rect)
            Clock.schedule_interval(self.update_btn_color,1)
    def update_rect(self,instance,value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    def update_btn_color(self,instance):
        if self.btn_color['color'] == 'white':
            self.button_color.rgb = (.8,.8,.8)
        elif self.btn_color['color'] == 'red':
            self.button_color.rgb = (1,.2,.2)
        elif self.btn_color['color'] == 'orange':
            self.button_color.rgb = (1,.5,.3)
        elif self.btn_color['color'] == 'yellow':
            self.button_color.rgb = (.9589,.9297,0)
        elif self.btn_color['color'] == 'green':
            update_btn_color.rgb = (.2,.8,.2)
        elif self.btn_color['color'] == 'blue':
            self.button_color.rgb = (.3,.4,1)
        elif self.btn_color['color'] == 'purple':
            self.button_color.rgb = (.8,.2,.8)
             
        self.canvas.ask_update()
        
class CustomLayout(BoxLayout):
    def __init__(self,**kwargs):
        super(CustomLayout,self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = '10dp'
        self.spacing = '5dp'
        
        with self.canvas.before:
            Color(1,1,1,1)
            self.rect = RoundedRectangle(pos=self.pos,size=self.size)
            self.bind(pos=self.update_rect,size=self.update_rect)
            
            
    def update_rect(self,instance,value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class RoundedLayout(BoxLayout):
    def __init__(self,**kwargs):
        super(RoundedLayout,self).__init__(**kwargs)
        
        with self.canvas.before:
            Color(.3,.3,.3,1)
            
            self.rect = Rectangle(pos=self.pos,size=self.size)
            self.bind(pos=self.update_rect,size=self.update_rect)
            
            Color(1,1,1,1)
            self.rect_after = Rectangle(pos=self.pos,size=self.size)
                       
    def update_rect(self,instance,value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
        self.rect_after.pos = (instance.pos[0]+3.25,instance.pos[1]+3.25)
        self.rect_after.size = (instance.size[0]-6.5,instance.size[1]-6.5)

class CustomizedLayout(FloatLayout):
    def __init__(self,**kwargs):
        super(CustomizedLayout,self).__init__(**kwargs)
        
        with self.canvas.before:
            Color(1,1,1)
            
            self.rect = Rectangle(pos=self.pos,size=self.size)
            self.bind(pos=self.update_rect,size=self.update_rect)
                       
    def update_rect(self,instance,value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
class DeleteCustom(Button):
    def __init__(self,btn_color,**kwargs):
        super(DeleteCustom,self).__init__(**kwargs)
        
        self.long_pressed = False
        self.btn_color = btn_color
        
        self.background_color = 0.2,0.6,1,0
        with self.canvas.before:
            self.button_color = Color(.3,.4,1)
            self.rect =  RoundedRectangle(pos=self.pos,size=self.size,radius=[20])
            
            self.bind(pos=self.update_rect,size=self.update_rect)
            Clock.schedule_interval(self.update_btn_color,1)
    def update_rect(self,instance,value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    def update_btn_color(self,instance):
        if self.btn_color['color'] == 'white':
            self.button_color.rgb = (.8,.8,.8)
        elif self.btn_color['color'] == 'red':
            self.button_color.rgb = (1,.2,.2)
        elif self.btn_color['color'] == 'orange':
            self.button_color.rgb = (1,.5,.3)
        elif self.btn_color['color'] == 'yellow':
            self.button_color.rgb = (.9589,.9297,0)
        elif self.btn_color['color'] == 'green':
            update_btn_color.rgb = (.2,.8,.2)
        elif self.btn_color['color'] == 'blue':
            self.button_color.rgb = (.3,.4,1)
        elif self.btn_color['color'] == 'purple':
            self.button_color.rgb = (.8,.2,.8)
             
        self.canvas.ask_update()
       

    def on_touch_down(self,touch):
        if self.collide_point(*touch.pos):
            self.touch_time = float(time.strftime("%s"))
        return super().on_touch_down(touch)
    def on_touch_up(self,touch):
        if self.collide_point(*touch.pos):
            self.leave_time = time.strftime("%s")
            if float(self.leave_time) - float(self.touch_time) > 1.3:
                self.text = "Clear"
                self.long_pressed = True
            else:
                self.long_pressed = False
        return super().on_touch_up(touch)
            
