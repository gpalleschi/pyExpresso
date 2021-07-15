from kivy_deps import sdl2, glew, gstreamer
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
import re
import os

def reset():
    import kivy.core.window as window
    from kivy.base import EventLoop
    if not EventLoop.event_listeners:
        from kivy.cache import Cache
        window.Window = window.core_select_lib('window', window.window_impl, True)
        Cache.print_usage()
        for cat in Cache._categories:
            Cache._objects[cat] = {}

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class pyExpressoRE:
    def reset(objTest):
        objTest.background_color = [1, 1, 1, 1]

    def execute(pattern, objTest):
        if len(pattern) > 0:
            if len(objTest.text) > 0:
                result = re.match(pattern, objTest.text)
                if result:
# Expression is Ok
                    objTest.background_color = [0, 1, 0, 1]
                else:
# Expression is Ko 
                    objTest.background_color = [1, 0, 0, 1]
            else:
                 objTest.background_color = [1, 1, 1, 1]

class PyExpressoForm(BoxLayout):
    test1 = ObjectProperty(None)
    test2 = ObjectProperty(None)
    test3 = ObjectProperty(None)
    regexp = ObjectProperty(None)
    def validate_regexp(self):
        if len(self.regexp.text) > 0:
            if len(self.test1.text) > 0:
                self.validate_test1()
            if len(self.test2.text) > 0:
                 self.validate_test2()
            if len(self.test3.text) > 0:
                self.validate_test3()
        else:
            pyExpressoRE.reset(self.test1) 
            pyExpressoRE.reset(self.test2) 
            pyExpressoRE.reset(self.test3) 
    
    def validate_test1(self):
        pyExpressoRE.execute(self.regexp.text,self.test1)
    def validate_test2(self):
        pyExpressoRE.execute(self.regexp.text,self.test2)
    def validate_test3(self):
        pyExpressoRE.execute(self.regexp.text,self.test3)

    def popHelp(self):
        box = BoxLayout(orientation='vertical')
        box.add_widget(Image(source='.\img\pyExpresso.png'))
        box.add_widget(Label(text='           Version : 1.1\nAuthor  : Giovanni Palleschi'))
        pop = Popup(title='pyExpresso',content=box,
                    size_hint=(None,None), size=(300, 300))
        pop.open()
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.regexp.text = stream.read()
            self.test1.text = ""
            self.test2.text = ""
            self.test3.text = ""

        self.dismiss_popup()

    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.regexp.text)

        self.dismiss_popup()


class pyExpresso(App):
    def build(self):
        self.icon = '.\img\pyExpresso.png'
        return PyExpressoForm()

if __name__ == '__main__':
    reset()
    pyExpresso().run()