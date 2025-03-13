from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup


class MainScreen(TabbedPanel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # create button
        button_create_tab = Button(text="+", font_size=10, background_color="white")
        button_create_tab.bind(on_press=self.adicionar_aba)

        self.add_widget(button_create_tab)

    def create_text_popup(self):
        popup = Popup(label="create a new text")
               
        popup.add_widget
        popup.open()
        pass

    def create_note_popup(self):
        pass

    def adicionar_aba(self, instance=None):
        new_tab = TabbedPanelItem(text='Aba')
        new_tab.content = TextInput()
        self.add_widget(new_tab)
