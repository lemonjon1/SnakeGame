import tkinter as tk
import random
import math
import time


class SnakeGame:

	def __init__(self,game_settings,color_settings):
		self.grid_size = game_settings[0]
		self.grid_num_vertical = game_settings[1]
		self.grid_num_horizontal = game_settings[2]
		self.snake_speed = game_settings[3]
		self.starting_length = game_settings[4]

		self.background_color = color_settings[0]
		self.snake_color = color_settings[1]
		self.food_color = color_settings[2]

		self.direction = "right"

	def start_game(self):
		root = tk.Tk()
		root.geometry(f"{self.grid_size*self.grid_num_horizontal}x{self.grid_size*self.grid_num_vertical}")
		root.resizable(False,False)
		self.canvas = tk.Canvas(root,bg=self.background_color,height=self.grid_size*self.grid_num_vertical,width=self.grid_size*self.grid_num_horizontal)
		self.canvas.pack()

		root.bind('<Left>', lambda event: self.change_direction('left'))
		root.bind('<Right>', lambda event: self.change_direction('right'))
		root.bind('<Up>', lambda event: self.change_direction('up'))
		root.bind('<Down>', lambda event: self.change_direction('down'))

		root.bind('<a>', lambda event: self.change_direction('left'))
		root.bind('<d>', lambda event: self.change_direction('right'))
		root.bind('<w>', lambda event: self.change_direction('up'))
		root.bind('<s>', lambda event: self.change_direction('down'))

		root.mainloop()


	def next_turn(self):
		pass

	def change_direction(self,new_direction):
		print(new_direction)

	def check_collision(self):
		pass

	def game_over(self):
		pass

class Settings():

	game_settings = [20,20,20,10,3]
	game_settings_limits = [[1,100],[3,500],[3,500],[1,1000],[1,50]]
	color_settings = ["black","green","red"]

	settings_color_fg = "#aaaaaa"
	settings_color_bg = "#000000"
	root = tk.Tk()

	def check_text_type(self):
		try:
			for i in range(len(self.text_widgets)):
				int(self.text_widgets[i].get())
			return True
		except ValueError:
			return False

	def update(self):
		limits_met = True
		for i in range(len(self.text_widgets)):
			if int(self.text_widgets[i].get()) >= self.game_settings_limits[i][0] and int(self.text_widgets[i].get()) <= self.game_settings_limits[i][1]:
				self.error_label.config(text="")
				self.game_settings[i] = int(self.text_widgets[i].get())
			else:
				limits_met = False

		if limits_met:
			return True
		else:
			return False

	def start_game(self):
		type_match = self.check_text_type()
		if type_match:
			limits_met = self.update()
			if limits_met:
				if self.game_settings[4] + 2 >= self.game_settings[2]:
					self.error_label.config(text="Starting Length must at least 2 less than Grid Number Vertical")
				else:
					self.error_label.config(text="Game Starting...")
					self.root.destroy()
			else:
				self.error_label.config(text="All settings must be between designated limits")
		else:
			self.error_label.config(text="Settings must be integers")

	def create_menu(self):
		self.root.config(bg=self.settings_color_bg)
		self.root.title("Snake Game Settings")
		settings_label = (tk.Label(text="Game Settings", font=("Normal", 40), bg=self.settings_color_fg, padx=363, pady=20)
						  .grid(row=0, column=0, columnspan=6))
		# Grid size ----------------------------------------------------------------------------------------------------
		grid_size_label = tk.Label(self.root, text="Grid Size (1-100)",
										font=("normal",20), bg=self.settings_color_fg, width=25, pady=10).grid(row=1, column=0)
		grid_size_text = tk.StringVar(self.root, str(self.game_settings[0]))
		grid_size_entry = tk.Entry(self.root, textvar=grid_size_text, bg=self.settings_color_fg,
										font=("normal", 34), justify="center", width=5, bd=3).grid(row=1, column=1)
		# Grid number vertical -----------------------------------------------------------------------------------------
		grid_num_vertical_label = tk.Label(self.root, text="Grid Number Vertical (3-500)",
												font=("normal", 20), bg=self.settings_color_fg, width=25, pady=10).grid(row=2, column=0)
		grid_num_vertical_text = tk.StringVar(self.root, str(self.game_settings[1]))
		grid_num_vertical_entry = tk.Entry(self.root, textvar=grid_num_vertical_text, bg=self.settings_color_fg,
												font=("normal", 34), justify="center", width=5, bd=3).grid(row=2, column=1)
		# Grid number horizontal ---------------------------------------------------------------------------------------
		grid_num_horizontal_label = tk.Label(self.root, text="Grid Number Horizontal (3-500)",
												  font=("normal", 20), bg=self.settings_color_fg, width=25, pady=10).grid(row=3, column=0)
		grid_num_horizontal_text = tk.StringVar(self.root, str(self.game_settings[2]))
		grid_num_horizontal_entry = tk.Entry(self.root, textvar=grid_num_horizontal_text, bg=self.settings_color_fg,
												  font=("normal", 34), justify="center", width=5, bd=3).grid(row=3, column=1)
		# Snake speed --------------------------------------------------------------------------------------------------
		snake_speed_label = tk.Label(self.root, text="Snake Speed (1-1000)",
										  font=("normal", 20), bg=self.settings_color_fg, width=25, pady=10).grid(row=1, column=3)
		snake_speed_text = tk.StringVar(self.root, str(self.game_settings[3]))
		snake_speed_entry = tk.Entry(self.root, textvar=snake_speed_text, bg=self.settings_color_fg,
										  font=("normal", 34), justify="center", width=5, bd=3).grid(row=1, column=4)
		# Starting length ----------------------------------------------------------------------------------------------
		starting_length_label = tk.Label(self.root, text="Starting Length (1-50)",
											  font=("normal", 20), bg=self.settings_color_fg, width=25, pady=10).grid(row=2, column=3)
		starting_length_text = tk.StringVar(self.root, str(self.game_settings[4]))
		starting_length_entry = tk.Entry(self.root, textvar=starting_length_text, bg=self.settings_color_fg,
											  font=("normal", 34), justify="center", width=5, bd=3).grid(row=2, column=4)
		# Start button -------------------------------------------------------------------------------------------------
		self.entry_strings = ["grid_size", "grid_num_vertical", "grid_num_horizontal", "snake_speed", "starting_length"]
		self.text_widgets = [grid_size_text, grid_num_vertical_text, grid_num_horizontal_text, snake_speed_text, starting_length_text]
		start_button = (tk.Button(self.root, text="Start Game", font=("normal", 20), bg=self.settings_color_fg,
									   command=self.start_game, width=33).grid(row=3, column=3, columnspan=3))
		# Error label --------------------------------------------------------------------------------------------------
		self.error_label = tk.Label(self.root, text="", font=("normal",30), bg=self.settings_color_fg, width=30, padx=192)
		self.error_label.grid(row=7,column=0,columnspan=6)

		self.root.mainloop()

		# TODO: Add option for color-picker

if __name__ == '__main__':
	settings = Settings()
	settings.create_menu()
	game = SnakeGame(settings.game_settings,settings.color_settings)
	game.start_game()
