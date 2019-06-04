import os
import pickle

from kivy.core.window import Window

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen

from pantry.pantryItem import pantryItem


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
            pantry = pickle.load(open('data/pantryContent.pickle', 'rb'))
            if len(pantry.keys()):
                l = list(pantry.keys())
                l.sort()
                for n in l:
                    self.createItemInList(pantry[n])

        self.scrollItemList = ScrollView()
        self.scrollItemList.add_widget(self.itemsList)
        self.masterGrid.add_widget(self.scrollItemList)


        self.masterGrid.add_widget(Label(text='Add items', size_hint = (1., 0.07)))

        addBox = GridLayout(cols=4, size_hint = (1., 0.07))
        self.newItemName = TextInput(text='', hint_text='(Name)', multiline=False, size_hint_x=0.6)
        addBox.add_widget(self.newItemName)
        self.newItemAmount = TextInput(text='', hint_text='(Amount)', multiline=False, size_hint_x=0.12)
        addBox.add_widget(self.newItemAmount)
        self.newItemUnits = TextInput(text='', hint_text='(Units)', multiline=False, size_hint_x=0.08)
        addBox.add_widget(self.newItemUnits)

        self.addButton = Button(text='+', size_hint_x=0.2)
        self.addButton.bind(on_release=self.addButtonFunc)
        addBox.add_widget(self.addButton)
        self.masterGrid.add_widget(addBox)

        self.add_widget(self.masterGrid)

    def addButtonFunc(self,instance):
        name = self.newItemName.text.capitalize()
        amount = int(self.newItemAmount.text)
        units = self.newItemUnits.text

        pantry = {}
        if os.path.isfile('data/pantryContent.pickle'):
            pantry = pickle.load(open('data/pantryContent.pickle', 'rb'))

        pantry[name] = pantryItem(name, amount, units)
        pickle.dump(pantry, open('data/pantryContent.pickle', 'wb'))

        self.createItemInList(pantry[name])

        self.newItemName.text = ''
        self.newItemAmount.text = ''
        self.newItemUnits.text = ''


    def createItemInList(self, item):
        ln = Label(text='   '+item.name, halign='left', valign='center', size_hint_x=0.6)
        ln.bind(size=ln.setter('text_size'))

        txt = str(item.amount)
        if item.units:
            txt += ' ' + item.units
        lu = Label(text=txt, halign='right', valign='center', size_hint_x=0.2)
        lu.bind(size=lu.setter('text_size'))

        b = Button(text='X', size_hint_x=0.2)
        # i_row = len(self.itemsList.children)
        row = GridLayout(cols=3)
        row.add_widget(ln)
        row.add_widget(lu)
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
