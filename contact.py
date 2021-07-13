import kivy
from kivy.app import App

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.properties import ObjectProperty
from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.write()

from kivy.core.window import Window
import os
#database
import sqlitecon


class ContactForm(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        sqlitecon.create_connection(os.path.dirname(os.path.realpath(__file__))+"/contact.db")

    def clear_inputs(self):         
        for inp  in reversed(self.ids.inputs.children):
            if isinstance(inp,TextInput):
                inp.text = ''
                
    def insert_data(self):
        name = self.ids.name.text
        address = self.ids.address.text
        email = self.ids.email.text
        phone = self.ids.phone.text
        sqlitecon.insert_data_db(os.path.dirname(os.path.realpath(__file__))+"/contact.db",name,address,email,phone)
    def db_display(self,*args):
        self.manager.get_screen("displayer").refresh_layout()
        self.manager.transition.direction="left"
        self.manager.current = "displayer"
   
        
class ContactDisplayer(Screen):
    layout = ObjectProperty(None)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout.bind(minimum_height=self.layout.setter('height'))
    
    def refresh_layout(self):
        
        self.conn = sqlitecon.display(os.path.dirname(os.path.realpath(__file__))+"/contact.db")
        layout = self.ids.layout
        layout.clear_widgets()
        for data in self.conn:
            self.check_btn = CheckBox(group="edit")
            self.check_btn.size_hint = (.1,None)
            self.check_btn.height = 30
            self.check_btn.id = str(data[0])
            self.check_btn.bind(active=self.check_btn_active)
            layout.add_widget(self.check_btn)
            # self.add_widget(self.check_btn)
            for item in data:
                self.t = TextInput(multiline=False)
                self.t.size_hint = (.1, None)
                self.t.height = 30
                self.t.readonly = True
                self.t.text = str(item)
                layout.add_widget(self.t)
           
        self.ids.edit.disabled = True
        self.ids.delete.disabled=True
        
        
    def check_btn_active(self,checkbox,value):
        self.id = checkbox.id
        if value:
            self.ids.edit.disabled = False
            self.ids.delete.disabled=False
        else:
            self.ids.edit.disabled = True
            self.ids.delete.disabled=True
            
        
    def delete_item(self):
        id = self.id
        sqlitecon.delete_entry(os.path.dirname(os.path.realpath(__file__))+"/contact.db",id)
        self.refresh_layout()
        
    def edit_item(self):
        id = self.id
        self.manager.get_screen("editor").editor_display_with_value()
        
        
        
        
        
        
class Editor(Screen): 
    def editor_display_with_value(self):
        id = self.manager.get_screen("displayer").id
        self.ids.title.text= "Editing ID : "+str(id)
        self.conn=sqlitecon.display(os.path.dirname(os.path.realpath(__file__))+"/contact.db",id)
        self.ids.name.text = self.conn[0][1]
        self.ids.address.text = self.conn[0][2]
        self.ids.email.text = self.conn[0][3]
        self.ids.phone.text = self.conn[0][4]
      
    def update_entry(self):
        id = self.manager.get_screen("displayer").id
        name = self.ids.name.text 
        address = self.ids.address.text 
        email = self.ids.email.text 
        phone = self.ids.phone.text
        sqlitecon.update_data(os.path.dirname(os.path.realpath(__file__))+"/contact.db",id,name,address,email,phone)
        self.manager.get_screen("displayer").refresh_layout()
        

class MyApp(App):
    def build(self):
        Window.size = (800,600)
        sm = ScreenManager()
        sm.add_widget(ContactForm(name="contactForm"))
        sm.add_widget(ContactDisplayer(name="displayer"))
        sm.add_widget(Editor(name="editor"))
        return sm


if __name__ == '__main__':   
    MyApp().run()