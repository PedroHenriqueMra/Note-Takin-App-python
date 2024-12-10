from kivy.app import App

# screens import
from screnns.home import HomeScreen

class MyApp(App):

    def build(self):
       return HomeScreen()
    

if __name__ == "__main__":
    MyApp().run()
