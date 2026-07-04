from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from screens.home import HomeScreen
from screens.division import DivisionScreen

class Home(Screen):
    pass

class Division(Screen):
    pass

class TravelApp(App):
    def build(self):
        self.sm = ScreenManager()

        self.home_screen = Screen(name="home")
        self.home_screen.add_widget(HomeScreen(self.open_division))

        self.sm.add_widget(self.home_screen)

        return self.sm

    def open_division(self, name):
        screen = Screen(name=name)
        screen.add_widget(DivisionScreen(name, self.go_home))

        self.sm.add_widget(screen)
        self.sm.current = name

    def go_home(self):
        self.sm.current = "home"

if __name__ == "__main__":
    TravelApp().run()
