import kivy
from kivy.app import App

from pantry.pantryPage import pantryPage

kivy.require("1.10.1")


class GalleyManager(App):
	def build(self):
		return pantryPage()


if __name__ == "__main__":
	GalleyManager().run()
