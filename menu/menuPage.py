import os

from kivy.core.window import Window

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen


class menuPage(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.menuPage()

	def menuPage(self):
		myMenuPage = GridLayout(cols=1, size_hint=(1.,1.))

		topBar = GridLayout(cols=1, size_hint = (1., 0.2))
		topBar.add_widget(Label(text='Galley Manager'))
		myMenuPage.add_widget(topBar)

		menuOptions = GridLayout(cols = 1, size_hint = (1,0.6))
		myMenuPage.pantryButton = Button(text = 'Pantry', size_hint_x = 0.2)
		myMenuPage.pantryButton.bind(on_press = self.pantryButtonFunc)
		menuOptions.add_widget(myMenuPage.pantryButton)
		myMenuPage.recipeButton = Button(text = 'Recipes', size_hint_x = 0.2)
		myMenuPage.recipeButton.bind(on_press = self.recipeButtonFunc)
		menuOptions.add_widget(myMenuPage.recipeButton)
		myMenuPage.add_widget(menuOptions)

		self.add_widget(myMenuPage)

	def pantryButtonFunc(self, instance):
		self.manager.current = 'PantryPage'
		

	def recipeButtonFunc(self, instance):
		self.manager.current = 'RecipePage'
