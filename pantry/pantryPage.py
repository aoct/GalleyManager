import os

from kivy.core.window import Window

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
        self.mainPage()

    def mainPage(self):
        self.cols = 1

        topBar = GridLayout(cols=2, size_hint = (1., 0.07))
        topBar.add_widget(Label(text='Pantry', size_hint_x=0.8))
        self.quitButton = Button(text='X', size_hint_x=0.2)
        self.quitButton.bind(on_press=quit)
        topBar.add_widget(self.quitButton)
        self.add_widget(topBar)

        self.itemsList = GridLayout(cols=1, spacing=10, row_force_default=True, row_default_height=40)
        if os.path.isfile("data/pantryContent.txt"):
            with open("data/pantryContent.txt", "r") as f:
                pantryItems = f.readlines()
                for item in pantryItems:
                    self.itemsList.add_widget(Label(text=item))
        self.scrollItemList = ScrollView()
        self.scrollItemList.add_widget(self.itemsList)
        self.add_widget(self.scrollItemList)


        self.add_widget(Label(text='Add items', size_hint = (1., 0.07)))

        addBox = GridLayout(cols=2, size_hint = (1., 0.07))
        self.newItem = TextInput(text='', multiline=False)
        addBox.add_widget(self.newItem)

        self.addButton = Button(text="Add Item", size_hint_x=0.15)
        self.addButton.bind(on_press=self.addButtonFunc)
        addBox.add_widget(self.addButton)
        self.add_widget(addBox)


    def addButtonFunc(self,instance):
        new_item = self.newItem.text

        with open("data/pantryContent.txt", "a+") as f:
            f.write(new_item+'\n')
        self.itemsList.add_widget(Label(text=new_item))

        self.newItem.text = ''
