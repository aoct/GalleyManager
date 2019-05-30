import os

from kivy.core.window import Window

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen


class recipePage(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.mainPage()

	def mainPage(self):
		myRecipePage = GridLayout(cols = 1)

		topBar = GridLayout(cols=3, size_hint = (1., 0.07))
		myRecipePage.backButton = Button(text='<-', size_hint_x=0.05)
		myRecipePage.backButton.bind(on_press=self.backButtonFunc)
		topBar.add_widget(myRecipePage.backButton)
		topBar.add_widget(Label(text='Recipes', size_hint_x=0.90))
		myRecipePage.quitButton = Button(text='X', size_hint_x=0.05)
		myRecipePage.quitButton.bind(on_press=quit)
		topBar.add_widget(myRecipePage.quitButton)
		myRecipePage.add_widget(topBar)

		self.add_widget(myRecipePage)

	def backButtonFunc(self,instance):
		self.manager.current = 'MenuPage'
