from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from data import DIVISIONS

class DivisionScreen(BoxLayout):
    def __init__(self, division_name, back_callback, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.division_name = division_name
        self.back_callback = back_callback

        data = DIVISIONS[division_name]

        self.add_widget(Label(text=f"[ {division_name} Division ]", font_size=24))

        self.add_widget(Label(text="Districts: " + ", ".join(data["districts"])))
        self.add_widget(Label(text="Famous Food: " + ", ".join(data["food"])))
        self.add_widget(Label(text="Tourist Places: " + ", ".join(data["places"])))

        back = Button(text="⬅ Back", size_hint_y=None, height=60)
        back.bind(on_release=lambda x: self.back_callback())
        self.add_widget(back)
