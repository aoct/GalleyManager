import os

from kivy.core.window import Window

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen


class pantryPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mainPage()

    def mainPage(self):

        myPantryPage = GridLayout(cols=1, size_hint=(1.,1.))

        topBar = GridLayout(cols=3, size_hint = (1., 0.07))
        myPantryPage.backButton = Button(text='<-', size_hint_x=0.05)
        myPantryPage.backButton.bind(on_press=self.backButtonFunc)
        topBar.add_widget(myPantryPage.backButton)
        topBar.add_widget(Label(text='Pantry', size_hint_x=0.90))
        myPantryPage.quitButton = Button(text='X', size_hint_x=0.05)
        myPantryPage.quitButton.bind(on_press=quit)
        topBar.add_widget(myPantryPage.quitButton)
        myPantryPage.add_widget(topBar)

        myPantryPage.itemsList = GridLayout(cols=1, spacing=10, size_hint_y=None, row_force_default=True, row_default_height=40)
        myPantryPage.itemsList.bind(minimum_height=myPantryPage.itemsList.setter('height'))

        if os.path.isfile("data/pantryContent.txt"):
            with open("data/pantryContent.txt", "r") as f:
                pantryItems = f.readlines()
                for item in pantryItems:
                    self.createItemInList(item[:-1], myPantryPage)

        myPantryPage.scrollItemList = ScrollView()
        myPantryPage.scrollItemList.add_widget(myPantryPage.itemsList)
        myPantryPage.add_widget(myPantryPage.scrollItemList)


        myPantryPage.add_widget(Label(text='Add items', size_hint = (1., 0.07)))

        addBox = GridLayout(cols=2, size_hint = (1., 0.07))
        myPantryPage.newItem = TextInput(text='', multiline=False)
        addBox.add_widget(myPantryPage.newItem)

        myPantryPage.addButton = Button(text="Add Item", size_hint_x=0.15)
        myPantryPage.addButton.bind(on_press=self.addButtonFunc)
        addBox.add_widget(myPantryPage.addButton)
        myPantryPage.add_widget(addBox)

        self.add_widget(myPantryPage)

    def addButtonFunc(self,instance):
        new_item = self.newItem.text.capitalize()

        with open("data/pantryContent.txt", "a+") as f:
            f.write(new_item+'\n')

        self.createItemInList(new_item)

        self.newItem.text = ''

    def createItemInList(self, itemName, myPantryPage):
        l = Label(text='   '+itemName, halign='left', valign='center', size_hint_x=0.8)
        l.bind(size=l.setter('text_size'))

        b = Button(text='X', size_hint_x=0.2)
        # i_row = len(self.itemsList.children)
        row = GridLayout(cols=2)
        row.add_widget(l)
        row.add_widget(b)
        myPantryPage.itemsList.add_widget(row)

        b.bind(on_release=lambda *kwargs: self.removeItemInList(row, *kwargs))

    def removeItemInList(self, row, *kwargs):
        itemName = row.children[1].text[3:-1]

        with open("data/pantryContent.txt", "r") as f:
            lines = f.readlines()
        with open("data/pantryContent.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != itemName:
                    f.write(line)

        self.itemsList.remove_widget(row)
        pass

    def backButtonFunc(self,instance):
        self.manager.current = 'MenuPage'
