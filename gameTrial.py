import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

import os

kivy.require ("1.10.1")


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


class FirstPage(GridLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.rows = 3

		if os.path.isfile("testFile.txt"):
			with open("testFile.txt", "r") as f:
				d = f.readlines()
				oldItems = '\n'.join(d)

		else:
			oldItems = "Empty"


		self.xxx = TextInput(multiline=False)
		self.add_widget(self.xxx)

		self.add = Button(text="Add Item")
		self.add.bind(on_press=self.add_button)
		self.add_widget(self.add)

		self.items = Label(text=oldItems)
		self.add_widget(self.items)

	def showList(self):

		if os.path.isfile("testFile.txt"):
			with open("testFile.txt", "r") as f:
				d = f.readlines()
				oldItems = '\n'.join(d)

		else:
			oldItems = []

		self.items.text = oldItems

	def add_button(self,instance):

		#if we want to grab some data from this page, recreate the variables as xxx = self.xxx.text
		#could also be interesting to save data to a file or read data from a file
		#data can also be loaded from a txt file to autofill (just read froma file) --> does this work also when loaded on the iOS?
		"""
		with open(filename, "w") as f:
			f.write(f"{variable1},{variable2},etc")
		"""

		variable1 = self.xxx.text

		with open("testFile.txt", "a+") as f:
			f.write(variable1+'\n')

		self.xxx.text = ""

		self.showList()
		# self.update_list(variable1)


class firstApp(App):
	def build(self):
		return FirstPage()


if __name__ == "__main__":
	firstApp().run()