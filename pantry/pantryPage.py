import os

from kivy.core.window import Window

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView


class pantryPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mainPage()

    def mainPage(self):
        self.cols = 1

        topBar = GridLayout(cols=2, size_hint = (1., 0.07))
        topBar.add_widget(Label(text='Pantry', size_hint_x=0.95))
        self.quitButton = Button(text='X', size_hint_x=0.05)
        self.quitButton.bind(on_press=quit)
        topBar.add_widget(self.quitButton)
        self.add_widget(topBar)

        self.itemsList = GridLayout(cols=1, spacing=10, size_hint_y=None, row_force_default=True, row_default_height=40)
        self.itemsList.bind(minimum_height=self.itemsList.setter('height'))

        if os.path.isfile("data/pantryContent.txt"):
            with open("data/pantryContent.txt", "r") as f:
                pantryItems = f.readlines()
                for item in pantryItems:
                    self.createItemInList(item)

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
        new_item = self.newItem.text.capitalize()

        with open("data/pantryContent.txt", "a+") as f:
            f.write(new_item+'\n')

        self.createItemInList(new_item)

        self.newItem.text = ''

    def createItemInList(self, itemName):
        l = Label(text='   '+itemName, halign='left', size_hint_x=0.8)
        l.bind(size=l.setter('text_size'))

        b = Button(text='X', size_hint_x=0.2)
        # i_row = len(self.itemsList.children)
        row = GridLayout(cols=2)
        row.add_widget(l)
        row.add_widget(b)
        self.itemsList.add_widget(row)

        b.bind(on_release=lambda *kwargs: self.removeItemInList(row, *kwargs))

    def removeItemInList(self, row, *kwargs):
        itemName = row.children[1].text[3:-1]
        print(itemName)

        for i in range(len(self.itemsList.children)):
            if row == self.itemsList.children[i]:
                print('Found at:', i)
        # TODO: Remove item from the memory as well
        with open("data/pantryContent.txt", "r") as f:
            lines = f.readlines()
        with open("data/pantryContent.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != itemName:
                    f.write(line)

        self.itemsList.remove_widget(row)
        pass
