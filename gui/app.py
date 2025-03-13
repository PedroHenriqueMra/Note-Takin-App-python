from kivy.app import App

from gui.widgets.main import MainScreen

from kivy.uix.boxlayout import BoxLayout

class MyApp(App):

    def build(self):
        layout = BoxLayout(orientation='vertical', minimum_height=15)
        layout.add_widget(MainScreen())
        return layout


if __name__ == "__main__":
    MyApp().run()
