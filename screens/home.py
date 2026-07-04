from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from data import DIVISIONS

class HomeScreen(BoxLayout):
    def __init__(self, switch_screen, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.switch_screen = switch_screen

        for div in DIVISIONS.keys():
            btn = Button(text=div, size_hint_y=None, height=60)
            btn.bind(on_release=lambda x, d=div: self.open_division(d))
            self.add_widget(btn)

    def open_division(self, name):
        self.switch_screen(name)
