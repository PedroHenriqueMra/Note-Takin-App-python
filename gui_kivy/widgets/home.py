from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class HomeScreen(GridLayout):

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text="App notations:"))
        self.content = TextInput(multiline=True)
        self.add_widget(self.content)
        
