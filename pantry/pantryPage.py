import os
import pickle

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
        self.masterGrid = GridLayout(cols=1, size_hint=(1.,1.))

        topBar = GridLayout(cols=3, size_hint = (1., 0.07))
        self.backButton = Button(text='<-', size_hint_x=0.05)
        self.backButton.background_normal = 'imgs/buttons/menu_circle_hamburger.png'
        self.backButton.background_down = 'imgs/buttons/menu_hamburger.png'

        self.backButton.bind(on_release=self.backButtonFunc)
        topBar.add_widget(self.backButton)
        topBar.add_widget(Label(text='Pantry', size_hint_x=0.90))
        self.quitButton = Button(text='X', size_hint_x=0.05)
        self.quitButton.bind(on_release=quit)
        topBar.add_widget(self.quitButton)
        self.masterGrid.add_widget(topBar)

        self.itemsList = GridLayout(cols=1, spacing=10, size_hint_y=None, row_force_default=True, row_default_height=40)
        self.itemsList.bind(minimum_height=self.itemsList.setter('height'))

        if not os.path.isdir('data'):
            os.mkdir('data')

        if os.path.isfile('data/pantryContent.pickle'):
            with open('data/pantryContent.pickle', 'rb') as f:
                pantry = pickle.load(f)
                for item in pantry.keys():
                    self.createItemInList(item)

        self.scrollItemList = ScrollView()
        self.scrollItemList.add_widget(self.itemsList)
        self.masterGrid.add_widget(self.scrollItemList)


        self.masterGrid.add_widget(Label(text='Add items', size_hint = (1., 0.07)))

        addBox = GridLayout(cols=2, size_hint = (1., 0.07))
        self.newItem = TextInput(text='', multiline=False)
        addBox.add_widget(self.newItem)

        self.addButton = Button(text="Add Item", size_hint_x=0.15)
        self.addButton.bind(on_release=self.addButtonFunc)
        addBox.add_widget(self.addButton)
        self.masterGrid.add_widget(addBox)

        self.add_widget(self.masterGrid)

    def addButtonFunc(self,instance):
        new_item = self.newItem.text.capitalize()

        pantry = {}
        if os.path.isfile('data/pantryContent.pickle'):
            pantry = pickle.load(open('data/pantryContent.pickle', 'rb'))
            
        pantry[new_item] = None
        pickle.dump(pantry, open('data/pantryContent.pickle', 'wb'))

        self.createItemInList(new_item)

        self.newItem.text = ''

    def createItemInList(self, itemName):
        l = Label(text='   '+itemName, halign='left', valign='center', size_hint_x=0.8)
        l.bind(size=l.setter('text_size'))

        b = Button(text='X', size_hint_x=0.2)
        # i_row = len(self.itemsList.children)
        row = GridLayout(cols=2)
        row.add_widget(l)
        row.add_widget(b)
        self.itemsList.add_widget(row)

        b.bind(on_release=lambda *kwargs: self.removeItemInList(row, *kwargs))

    def removeItemInList(self, row, *kwargs):
        itemName = row.children[1].text[3:]

        pantry = pickle.load(open('data/pantryContent.pickle', 'rb'))
        pantry.pop(itemName, None)
        pickle.dump(pantry, open('data/pantryContent.pickle', 'wb'))

        self.itemsList.remove_widget(row)

    def backButtonFunc(self,instance):
        self.manager.current = 'MenuPage'
