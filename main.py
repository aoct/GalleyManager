import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from pantry.pantryPage import pantryPage
from menu.menuPage import menuPage
from recipe.recipePage import recipePage


kivy.require("1.10.1")



class GalleyManager(App):
	def build(self):
		self.screenManager = ScreenManager()
		
		self.menuPage = menuPage(name='MenuPage')
		self.screenManager.add_widget(self.menuPage)

		self.pantryPage = pantryPage(name='PantryPage')
		self.screenManager.add_widget(self.pantryPage)

		self.recipePage = recipePage(name='RecipePage')
		self.screenManager.add_widget(self.recipePage)

		return self.screenManager


if __name__ == "__main__":
	GalleyManager().run()	
