import os

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView


# class ScrollableLabel(ScrollView):
# 	def __init__(self, **kwargs):
# 		super().__init__(**kwargs)
# 		self.layout = GridLayout(cols=1, size_hint_y = None)
# 		self.add_widget(self.layout)

# 		self.item_list = Label(size_hint_y=None, markup = True)
# 		self.scroll_to_point = Label()

# 		self.layout.add_widget(self.item_list)
# 		self.layout.add_widget(self.scroll_to_point)

# 	def update_list(self,message):
# 		self.item_list.text += '\n' + message

# 		self.layout.height = self.item_list.texture_size[1]+15
# 		self.item_list.height = self.item_list.texture_size[1]
# 		self.item_list.text_size = (self.item_list.width*0.98, None)

# 		self.scroll_to(self.scroll_to_point)

class pantryPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 3

        self.xxx = TextInput(multiline=False)
        self.add_widget(self.xxx)

        self.add = Button(text="Add Item")
        self.add.bind(on_press=self.add_button)
        self.add_widget(self.add)

        self.items = Label(text='')
        self.updateList()
        self.add_widget(self.items)

    def updateList(self):
        if os.path.isfile("data/pantryContent.txt"):
            with open("data/pantryContent.txt", "r") as f:
                d = f.readlines()
                oldItems = '\n'.join(d)
        else:
            oldItems = ''
        self.items.text = oldItems

    def add_button(self,instance):
        new_item = self.xxx.text

        with open("data/pantryContent.txt", "a+") as f:
            f.write(new_item+'\n')

        self.xxx.text = ""
        self.updateList()
