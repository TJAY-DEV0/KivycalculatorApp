from kivy.app import App
from kivy.base import stopTouchApp
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.graphics import RoundedRectangle,Color,Rectangle
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.accordion import Accordion,AccordionItem
from kivy.core.window import Window
from functools import partial
import numexpr
import math
import re
import os
#my .py files
import files
import switch
import check
from others import RoundedInput,IncrementLabel,RoundedButton,CustomLayout,RoundedLayout,CustomizedLayout,DeleteCustom


class MainLayout(BoxLayout):
    def __init__(self,**kwargs):
        super(MainLayout,self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = '10dp'
        self.spacing = '5dp'
        self.signs = ["÷","×","-","+"]
        #directory
        dir = App.get_running_app().user_data_dir
        self.full_path = os.path.join(dir,'calculator')
        self.files = files.MyFile(self.full_path)
        self.files.create_files()
        self.history = self.files.read_file('history.json')
        self.theme_light = self.files.read_file('theme.json')
        self.btn_color = self.files.read_file('button.json')
        self.cresult = 0
        self.last_result = 0
        self.reset_input = False
        self.auto_close = False
        self.more_inputs = ["inv","sin(","cos(","tan(","log(","!","π","^","(",")","√","²"]
        self.check = check.BracketChecker()
        self.invert = False
        self.tri = ["sin(","cos(","tan(","log("]
        self.tri_inverse  = ["sin-¹(","cos-¹(","tan-¹(","10^"]
        self.buttons = []
        self.error_displayed=False
        
            
        
            
        self.background_color = 0,0,0,0
        self.text_input = RoundedInput(size_hint_y=.4)
        self.add_widget(self.text_input)
        self.result_label = self.text_input.result_label
        
        self.remove_button = BoxLayout(orientation='horizontal',spacing='10dp',size_hint_y=.2)
        self.add_widget(self.remove_button)
        btn_percent = RoundedButton(self.btn_color,text='%')
        self.remove_button.add_widget(btn_percent)
        btn_percent.bind(on_press=partial(self.insert,"%"))
        btn_clear = DeleteCustom(self.btn_color,text="Del")
        self.remove_button.add_widget(btn_clear)
        btn_clear.bind(on_release=self.clear)
        
        self.accordion = Accordion()
        self.accordion_basic = AccordionItem(title="Basics",min_space=30)
        
        self.accordion.add_widget(self.accordion_basic)
        
        self.main_btn_layout = BoxLayout(orientation='horizontal',spacing='5dp')
        self.add_widget(self.main_btn_layout)
        
        self.main_btn_layout.add_widget(self.accordion)
        self.main_btn_layout2 = BoxLayout(orientation='horizontal',spacing='5dp')
        
        self.accordion_basic.add_widget(self.main_btn_layout2)
        
        self.number_layout = GridLayout(cols=3,spacing='5dp',size_hint_x=.6)
        self.main_btn_layout2.add_widget(self.number_layout)
        self.main_sign_layout = BoxLayout(orientation='vertical',spacing='5dp',size_hint_x=.4)
        self.main_btn_layout2.add_widget(self.main_sign_layout)
        
        self.accordion_more = AccordionItem(min_space=10,size_hint_x=None)
        self.accordion.add_widget(self.accordion_more)
        
        self.more_layout = GridLayout(cols=4,spacing="5dp",padding="5dp")
        self.accordion_more.add_widget(self.more_layout)
        self.callbacks = {}
        for child in self.more_inputs:
            if child == "inv":
                btn = RoundedButton(self.btn_color,text=child)
                btn.bind(on_press=self.invert_tri)
                self.more_layout.add_widget(btn)
            else:
                
                btn = RoundedButton(self.btn_color,text=child)
                self.buttons.append(btn)
                callback = partial(self.insert,child)
                self.callbacks[btn] = callback
                btn.bind(on_press=callback)
                self.more_layout.add_widget(btn)
            
        for i in range(9,-3,-1):
            if i > 0:
                btn = RoundedButton(self.btn_color,text=str(i))
                self.number_layout.add_widget(btn)
                btn.bind(on_press=partial(self.insert,i))
            elif i == 0:
                btn = RoundedButton(self.btn_color,text=".")
                self.number_layout.add_widget(btn)
                btn.bind(on_press=partial(self.insert,"."))
            elif i == -1:
                btn = RoundedButton(self.btn_color,text="0")
                self.number_layout.add_widget(btn)
                btn.bind(on_press=partial(self.insert,"0"))
            elif i == -2:
                btn = RoundedButton(self.btn_color,text="=")
                self.number_layout.add_widget(btn)
                btn.bind(on_press=partial(self.execute))
        
        for i in self.signs:
            btn = RoundedButton(self.btn_color,text=str(i))
            self.main_sign_layout.add_widget(btn)
            btn.bind(on_press=partial(self.insert,i))
            
        
        
        with self.canvas.before:
            self.theme_color = Color(1,1,1,1)
            self.rect = RoundedRectangle(pos=self.pos,size=self.size)
            self.bind(pos=self.update_rect,size=self.update_rect)
        
        Clock.schedule_interval(self.update_theme,1)
        
            
    def update_rect(self,instance,value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
    def update_theme(self,instance):
        self.theme_light = self.files.read_file('theme.json')
        if self.theme_light['bg']:
            self.theme_color.rgb = (1,1,1)
        else:
            self.theme_color.rgb = (0,0,0)
        self.canvas.ask_update()
        
    def modify(self, input):
        
        input = input.replace('×', '*')
        input = input.replace('÷', '/')
        input = input.replace('π', str(22/7)) 
        input = input.replace('10^', 'exp10(')
        input = input.replace('^', '**')
        input = input.replace('²', '**2')


        input = input.replace('sin(', 'sin(')
        input = input.replace('cos(', 'cos(')
        input = input.replace('tan(', 'tan(')
        input = input.replace('log(', 'log(') 
        input = input.replace('√', 'sqrt(')

        input = input.replace('sin-¹(', 'arcsin(')
        input = input.replace('cos-¹(', 'arccos(')
        input = input.replace('tan-¹(', 'arctan(')
        
        
        if '!' in input:
            try:
                
                matches = re.findall(r'(\d+)!', input)
                for match in matches:
                    num = int(match)
                    factorial_result = math.factorial(num)
                    input = input.replace(f'{num}!', str(factorial_result))
            except (ValueError, IndexError):
                
                
                pass
        
        print(f'Final expression for numexpr : {input}')
        return input

        
    def show_more(self,instance):
        pass
    def before_insert(self,text):
        input = self.text_input.text_input.text
        others = ["π"]
        signs = {"add":['+','-'],"mul":['×','÷',"!","^"],"tri":self.tri+self.tri_inverse+others}
        if not input:
            if text in signs['add']:
                return True
            elif text in signs['tri']:
                return True
            elif text == "(" or text == ")":
                return True
            else:
                return False
        else:
            if input[-1].isdigit() and text in signs['tri']:
                return False
            elif input[-1].isdigit():
                return True
            elif len(input) > 0 and input[-1] in signs['add'] and text in signs['add'] or text in signs['mul']:
                  self.text_input.text_input.text = self.text_input.text_input.text[:-1]
                  return True
            elif input[-1] in signs['mul'] and text in signs['add']:
                return True
            elif input[-1] in signs['mul'] or input[-1] in signs['add'] and text in signs['tri']:
                return True
            elif text == "(" or text == ")":
                return True
            
    def shift_label_back(self):
        #shift label
          self.result_label = self.text_input.result_label
          lenght =1 - len(self.result_label.text)/38
          self.result_label.pos_hint = {"right":lenght}
    def shift_label(self):
        #shift label
          self.result_label = self.text_input.result_label
          lenght =1 - len(self.result_label.text)/38
          self.result_label.pos_hint = {"right":lenght}
    def insert(self, *args):
        text = str(args[0])
        input_text = self.text_input.text_input.text
        try:
            int(input_text)
            if len(input_text) > 12:
                self.text_input.text_input.text = self.text_input.text_input.text[:-1]
                
        except ValueError:
            pass
                
        
        
        if self.reset_input:
            self.text_input.text_input.text = ''
            self.reset_input = False
            
        
        if text.isdigit() or text == '.':
            self.text_input.text_input.text += text
        elif input_text and input_text[-1] in self.signs and text in self.signs:
            
            self.text_input.text_input.text = input_text[:-1] + text
        else:
            self.text_input.text_input.text += text
        
        
        try:
            
            evaluated_text = self.modify(self.check.check_brackets(self.text_input.text_input.text))
            
            
            if self.check.check_brackets(evaluated_text):
                
                self.cresult = numexpr.evaluate(evaluated_text)
                
                
                self.result_label.start_increment(self.last_result, self.cresult)
                self.last_result = self.cresult
                self.error_displayed = False
        except (SyntaxError, ZeroDivisionError, TypeError, ValueError,OverflowError) as e:
            
            if not self.error_displayed:
                self.result_label.text = ''
            self.error_displayed = False

    def delete(self):
        if len(self.text_input.text_input.text) > 0:
            if self.reset_input:
                self.text_input.text_input.text = ""
            elif self.text_input.text_input.text[-1] == '(' and not self.text_input.text_input.text[-2].isdigit():
                self.text_input.text_input.text = self.text_input.text_input.text[:0-len('sin(')]
            
            elif self.text_input.text_input.text[-1] == '(' and self.text_input.text_input.text[-2] == '¹':
                self.text_input.text_input.text = self.text_input.text_input.text[:0-len('sin-¹(')]
            else:
                self.text_input.text_input.text = self.text_input.text_input.text[:-1]
        
        
        try:
            if self.text_input.text_input.text:
                evaluated_text = self.modify(self.text_input.text_input.text)
                if self.check.check_brackets(evaluated_text):
                    self.cresult = numexpr.evaluate(evaluated_text)
                    self.result_label.start_increment(self.last_result, self.cresult)
                    self.last_result = self.cresult
                    self.error_displayed = False
                else:
                    self.result_label.text = ''
            else:
                self.result_label.text = '0'
        except (SyntaxError, ZeroDivisionError, TypeError, ValueError) as e:
            if not self.error_displayed:
                self.result_label.text = ''

    def clear(self, instance):
        if instance.long_pressed:
            self.text_input.text_input.text = ''
            instance.text = "Del"
            self.result_label.text = '0'
            self.last_result = 0
            self.cresult = 0
            self.error_displayed = False
        else:
            self.delete()
    def execute(self, instance):
        raw_input = self.text_input.text_input.text
        if not raw_input:
            self.text_input.text_input.text = '0'
            return
        try:
            
            input_expression = self.modify(raw_input)
            final_result = numexpr.evaluate(input_expression)
            
            
            if float(final_result).is_integer():
                self.text_input.text_input.text = str(int(final_result))
            else:
                self.text_input.text_input.text = f'{float(final_result):.4f}'
                
            
            self.history.append(f'{raw_input} = {final_result}')
            self.files.write_file('history.json', self.history)
            self.result_label.text = ''
            self.last_result = final_result
            self.cresult = final_result
            self.reset_input = True 
            

        except (SyntaxError, ZeroDivisionError, TypeError, ValueError,OverflowError) as e:
            
            self.text_input.text_input.text = 'Error'
            
            self.result_label.text = ''
            self.error_displayed = True
            self.reset_input = True

        
    def invert_tri(self,instance):
        self.invert = not self.invert
        if self.invert:
            for child in self.more_layout.children:  
                for button in self.buttons:
                    button.funbind('on_press',self.callbacks[button])
                child.unbind(on_press=None)
                for j in self.tri:
                    if child.text == j:
                         ctext = self.tri_inverse[self.tri.index(child.text)]
                         child.text = ctext
                       
                         child.bind(on_press=partial(self.insert, ctext))
    
        else:
            for child in self.more_layout.children:  
                for button in self.buttons:
                    button.funbind('on_press',self.callbacks[button])
                child.unbind(on_press=None)
                for j in self.tri_inverse:
                    if child.text == j:
                         ctext = self.tri[self.tri_inverse.index(child.text)]
                         child.text = ctext
                       
                         child.bind(on_press=partial(self.insert, ctext))
            
                        
                
        
    
        
    def add_smoothly(self,instance):
        self.cresult += 1
        self.text_input.result_label.text = str(self.cresult)
        
class Manager(ScreenManager):
    def __init__(self,**kwargs):
        super(Manager,self).__init__(**kwargs)
        self.add_widget(MyFirstScreen(name='FirstScreen'))
        self.add_widget(MainScreen(name="Main"))
        self.add_widget(HistoryScreen(name='History'))
        self.add_widget(SettingScreen(name='Setting'))
        



class MainScreen(Screen):
    def __init__(self,**kwargs):
        super(MainScreen,self).__init__(**kwargs)
        
        self.main_layout = MainLayout()
        self.file = files.MyFile(self.main_layout.full_path)

        self.add_widget(self.main_layout)
        self.layout_btn = self.main_layout.text_input.history_button
        self.layout_btn.bind(on_release=self.switch_screen)
        self.layout_btn_setting = self.main_layout.text_input.setting_button
        self.layout_btn_setting.bind(on_release=self.switch_screen2)
        

    def switch_screen(self,instance):
        self.history = self.file.read_file('history.json')      
        self.history.reverse()
        
        history_layout = self.manager.get_screen('History')
        history_layout.add_history(None)
        self.manager.current = "History"
    def switch_screen2(self,instance):
        self.manager.current = "Setting"
    
        
class HistoryScreen(Screen):
    def __init__(self,**kwargs):
        super(HistoryScreen,self).__init__(**kwargs)
        self.main_screen = MainScreen()
       
        self.theme = self.main_screen.file.read_file('theme.json')
        
    def switch_screen(self,instance):
        self.manager.current = "Main"
        self.layout.clear_widgets()
        
    def add_history(self,instance):
        self.history = self.manager.get_screen('Main').history
        scroll_screen = ScrollView()
        self.layout = CustomLayout(orientation='vertical',size_hint=(1,None),height=150*len(self.history),padding='10dp')
        self.add_widget(scroll_screen)
        
        
        if not self.history:
            scroll_screen.add_widget(Button(text="No history! \nBack to Main Screen?",background_color=(0,0,0,1),font_size=50,on_press=self.switch_screen)) 
        else:
            self.btn_back = Button(text="Back",height=80,size_hint_y=None)
            self.layout.add_widget(self.btn_back)
            self.btn_back.bind(on_release=self.switch_screen)
            history_layout = BoxLayout(orientation='vertical')
            for i in self.history:
                scroll_label = ScrollView(do_scroll_y=False, bar_width=10, size_hint=(1,None),height=50)
                lbl_history = Label(text=i, font_size=50, bold=True, color=(0,0,0,1), size_hint_x=None,width=len(i)*30)
                lbl_history.bind(texture_size=lambda instance, value: setattr(lbl_history, 'width', value[0]))
                scroll_label.add_widget(lbl_history)
                history_layout.add_widget(scroll_label)
                history_layout.add_widget(Label(text='_____________________________________________________', color=(0,0,0,1)))
            self.layout.add_widget(history_layout)
            scroll_screen.add_widget(self.layout)

            
class SettingScreen(Screen):
    def __init__(self,**kwargs):
        super(SettingScreen,self).__init__(**kwargs)
        dir = App.get_running_app().user_data_dir
        full_path = os.path.join(dir,'calculator')
        self.file = files.MyFile(full_path)
        self.t = self.file.read_file('theme.json')
        self.layout = CustomLayout(spacing='5dp')
        self.add_widget(self.layout)
        
        self.header = BoxLayout(orientation='horizontal',size_hint_y=.05,spacing='10dp')
        self.layout.add_widget(self.header)
        
        self.back_button = Button(text="Back",background_color=(0,0,0,0),color=(0,0,0,1),size_hint_x=.2,font_size=30)
        self.back_button.bind(on_release=self.switch_to_main)
        self.header.add_widget(self.back_button)
        self.header.add_widget(Label(text="Settings",color=(0,0,0,1)))
        
        self.layout_theme = RoundedLayout(orientation='horizontal',size_hint_y=.12,padding='5dp')
        self.layout.add_widget(self.layout_theme)
        self.layout_theme.add_widget(Label(text="Theme light/dark",color=(0,0,0,1)))
        self.switch = switch.SwitchS(self.t['bg']    ,size_hint=(.4,.8))
        self.layout_theme.add_widget(self.switch)
        
        
        self.layout_btn_color = RoundedLayout(orientation='horizontal',size_hint_y=.15,padding='5dp')
        self.layout.add_widget(self.layout_btn_color)
        self.layout_btn_color.add_widget(Label(text='Choose button color',color=(0,0,0,1)))
        self.drop_menu = DropDown(size_hint=(.4,None),height=40)
        self.drop_menu.bind(on_select=self.on_color_selected)
        self.drop_menu_btn = Button(text="select color")
        self.drop_menu_btn.bind(on_release=self.drop_menu.open)
        self.layout_btn_color.add_widget(self.drop_menu_btn)
        
        #list of colors ROYGBI excluded white and purple as indigo
        colors = ["white","red","orange","yellow","green","blue","purple"]
        for color in colors:
            btn_color = Button(text=color,size_hint_y=None,height=60)
            btn_color.bind(on_release=lambda btn_color: self.drop_menu.select(btn_color.text))
            self.drop_menu.add_widget(btn_color)
            self.drop_menu.bind(on_select=lambda instance, x: setattr(self.drop_menu_btn,'text',x))
            
            
        
        self.btn_about = RoundedButton({"color":"white"},text="About",size_hint_y=.2)
        self.layout.add_widget(self.btn_about )
        self.btn_about.bind(on_press=self.show_about)
        self.btn_quit = RoundedButton({"color":"white"},text="Quit",size_hint_y=.2)
        self.btn_quit.bind(on_release=self.end)
        self.layout.add_widget(self.btn_quit )
        self.layout.add_widget(Label(text="Empty",size_hint_y=.4))
        
        
        
        Clock.schedule_interval(self.check_switch,1)
        
    def on_color_selected(self,instance,selected_color_text):
        dict = {}
        
        self.current_selected_color = selected_color_text
        dict['color'] = self.current_selected_color
        self.file.write_file('button.json',dict)
        
    def end(self,instance) :
        stopTouchApp()
    def show_about(self,instance):     
        layout = CustomLayout(size_hint=(1,1))
        
        popup = Popup(title="About",content=layout,size_hint=(1,.5),auto_dismiss=False)
        popup.open()
        
        layout.add_widget(Label(text="""
A modern and intuitive scientific\ncalculator with advanced features\nlike calculation history, customizable\nthemes, and a clean interface designed\nfor all your mathematical needs.

long press the ''Del'' button to clear input""",size_hint=(1,.5),color=(0,0,0,1),bold=True,font_size=30,pos_hint={"y":.7,"x":.01}))
        btn = Button(text="ok",size_hint=(.1¹¹¹8.3),pos_hint={"y":.3,"x":.05})
        btn.bind(on_release=popup.dismiss)
        
        layout.add_widget(btn)
    def switch_screen(self,instance):
        self.manager.current = "History"
    def switch_to_main(self,instance):
        self.manager.current = "Main"
    def check_switch(self,*arg):
        light = (1,1,1)
        dark = (0,0,0)
        if self.switch.toggle:
            self.file.write_file('theme.json',{'bg':True})
        else:
            self.file.write_file('theme.json',{'bg':False})

                        
class MyFirstScreen(Screen):
    def __init__(self,**kwargs):
            super(MyFirstScreen,self).__init__(**kwargs)
        
        
            self.per = 0
            layout = CustomizedLayout()
            self.add_widget(layout)
            
            optimal_logo = Image(source='assets/images/optimal_logo.jpg',size_hint=(1,.7),pos_hint={'center_y':.5,'center_x':.5})
            layout.add_widget(optimal_logo)
            
            
            loading_label = Label(text='Loading resources...',color=(0,0,0,),pos_hint={'center_y':.13,'center_x':.5})
            layout.add_widget(loading_label)
            self.progress_bar = ProgressBar(pos_hint={'center_y':.1,'center_x':.5},size_hint_x=.85)
            layout.add_widget(self.progress_bar)
            
            Clock.schedule_interval(self.update_bar,0.01)
           
            
    def update_bar(self,instance):
        self.per += 2
        
        self.progress_bar.value = self.per
        if self.per == 100:
            Clock.unschedule(self.update_bar)
            self.manager.current = 'Main'
        
    def update_rect(self,instance,value):
            self.rect.pos = instance.pos
            self.rect.size = instance.size
        
class ModernCalculator(App):
    def build(self):
        Window.bind(on_request_close=self.ask_stop)
        return Manager()
        
    def ask_stop(self,*args,**kwargs):
        self.show_stop()
        return True
    def show_stop(self):     
        layout = FloatLayout(size_hint=(1,1))
        
        popup = Popup(title="Application Exit",content=layout,size_hint=(.7,.2),auto_dismiss=False)
        popup.open()
        
        layout.add_widget(Label(text="Are you sure you want to quit?",size_hint=(1,.3),pos_hint={"y":.7,"x":.01}))
        btn = Button(text="yes",size_hint=(.3,.3),pos_hint={"y":.3,"x":.05})
        btn.bind(on_release=self.close_app)
        btn2 = Button(text="no",size_hint=(.3,.3),pos_hint={"y":.3,"x":.65})
        btn2.bind(on_release=popup.dismiss)
        layout.add_widget(btn)
        layout.add_widget(btn2)
    def close_app(self,*args):
        stopTouchApp()
    
    def on_pause(self):
        
        store = JsonStore('app_state.json')
        
        main_layout = self.root.get_screen('Main').main_layout
        current_text = main_layout.text_input.text_input.text
        
        store.put('state', input_text=current_text)
        print("App paused, state saved.")
        return True 

    def on_resume(self):
        store = JsonStore('app_state.json')
        if store.exists('state'):
            saved_state = store.get('state')
            main_layout = self.root.get_screen('Main').main_layout
            main_layout.text_input.text_input.text = saved_state['input_text']
            print("App resumed, state restored.")
        
if __name__ == '__main__':
    ModernCalculator().run()