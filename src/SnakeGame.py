import tkinter as tk
import random
import math


class SnakeGame:

	def __init__(self,game_settings,color_settings):
		self.score = 0
		self.root = None
		self.canvas = None
		self.food = None
		self.grid_size = game_settings[0]
		self.grid_num_vertical = game_settings[1]
		self.grid_num_horizontal = game_settings[2]
		self.snake_speed = game_settings[3]
		self.snake_wait = int(1000/self.snake_speed)
		self.starting_length = game_settings[4]
		center_x = math.floor(self.grid_num_horizontal/2)
		center_y = math.floor((self.grid_num_vertical-1)/2)

		self.background_color = color_settings[0]
		self.snake_color = color_settings[1]
		self.food_color = color_settings[2]

		self.direction = ''
		self.new_direction = None

		self.coordinates = []
		for i in range(self.starting_length):
			self.coordinates.append(
				[self.grid_size*(center_x-math.floor(self.starting_length/2)+i),self.grid_size*center_y])
		self.squares = []

	def start_game(self):
		self.root = tk.Tk()
		self.root.geometry(f"{self.grid_size*self.grid_num_horizontal}x{self.grid_size*self.grid_num_vertical+110}")
		self.root.resizable(False,False)
		self.score_label = tk.Label(self.root,text=f"Press key to start",font=("Normal",30))
		self.score_label.pack()
		self.canvas = tk.Canvas(self.root,bg=self.background_color,height=self.grid_size*self.grid_num_vertical,
								width=self.grid_size*self.grid_num_horizontal)
		self.canvas.pack()

		self.create_food()

		for x,y in self.coordinates:
			square = self.canvas.create_rectangle(x,y,x+self.grid_size,y+self.grid_size,fill=self.snake_color,tag="body")
			self.squares.append(square)

		self.new_direction = tk.StringVar(self.root)
		self.new_direction.set('')

		self.root.bind('<Left>',lambda z:self.new_direction.set('left'))
		self.root.bind('<Right>',lambda z:self.new_direction.set('right'))
		self.root.bind('<Up>',lambda z:self.new_direction.set('up'))
		self.root.bind('<Down>',lambda z:self.new_direction.set('down'))
		self.root.bind('<a>',lambda z:self.new_direction.set('left'))
		self.root.bind('<d>',lambda z:self.new_direction.set('right'))
		self.root.bind('<w>',lambda z:self.new_direction.set('up'))
		self.root.bind('<s>',lambda z:self.new_direction.set('down'))

		self.root.after(self.snake_speed,self.move)

	def create_food(self):
		foodx = random.randint(0,self.grid_num_horizontal-1)*self.grid_size
		foody = random.randint(0,self.grid_num_vertical-1)*self.grid_size
		while [foodx,foody] in self.coordinates:
			foodx = random.randint(1,self.grid_num_horizontal-1)*self.grid_size
			foody = random.randint(1,self.grid_num_vertical-1)*self.grid_size
		self.food = [foodx,foody]
		self.canvas.create_oval(foodx,foody,foodx+self.grid_size,foody+self.grid_size,fill=self.food_color,tag="food")

	def move(self):
		x,y = self.coordinates[-1]
		first_move = False

		if self.new_direction.get() == '':
			self.root.after(100,self.move)
		elif self.new_direction.get() == 'up' and self.direction != 'down':
			y -= self.grid_size
			self.direction = self.new_direction.get()
			first_move = True
		elif self.new_direction.get() == 'down' and self.direction != 'up':
			y += self.grid_size
			self.direction = self.new_direction.get()
			first_move = True
		elif self.new_direction.get() == 'right' and self.direction != 'left':
			x += self.grid_size
			self.direction = self.new_direction.get()
			first_move = True
		elif self.new_direction.get() == 'left' and self.direction != 'right':
			x -= self.grid_size
			self.direction = self.new_direction.get()
			first_move = True
		else:
			if self.direction == 'up':
				y -= self.grid_size
			elif self.direction == 'down':
				y += self.grid_size
			elif self.direction == 'right':
				x += self.grid_size
			elif self.direction == 'left':
				x -= self.grid_size
			first_move = True

		if first_move:
			self.score_label.config(text=f"Score: {self.score}")
			self.coordinates.append([x,y])
			square = self.canvas.create_rectangle(x,y,x+self.grid_size,y+self.grid_size,fill=self.snake_color,tag="body")
			self.squares.append(square)

			if self.check_collision():
				self.root.after(self.snake_wait,self.move)

	def check_collision(self):
		coords = []
		for i in range(len(self.coordinates)):
			coords.append(self.coordinates[i])

		coords.pop(-1)
		if self.coordinates[-1] in coords:
			tk.Label(self.root,text="Game Over",font=("Normal",30),fg="red").pack()
		elif self.coordinates[-1][0] >= self.grid_size*self.grid_num_horizontal\
				or self.coordinates[-1][0] < 0\
				or self.coordinates[-1][1] >= self.grid_size*self.grid_num_vertical\
				or self.coordinates[-1][1] < 0:
			tk.Label(self.root,text="Game Over",font=("Normal",30),fg="red").pack()
			return False
		elif self.coordinates[-1][0] == self.food[0] and self.coordinates[-1][1] == self.food[1]:
			self.canvas.delete("food")
			self.create_food()
			self.score += 1
			self.score_label.config(text=f"Score: {self.score}")
			return True
		else:
			self.coordinates.pop(0)
			self.canvas.delete(self.squares[0])
			self.squares.pop(0)
			return True


class Settings:
	game_settings = [20,20,20,10,3]
	game_settings_limits = [[1,100],[3,500],[3,500],[1,1000],[1,50]]
	color_settings = ["black","green","red"]

	settings_color_fg = "#aaaaaa"
	settings_color_bg = "#000000"

	root = tk.Tk()
	error_label = None
	text_widgets = None
	entry_strings = None

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
			if self.game_settings_limits[i][0] <= int(self.text_widgets[i].get()) <= self.game_settings_limits[i][1]:
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
				if self.game_settings[4]+2 > self.game_settings[2]:
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
		self.root.resizable(False,False)
		(tk.Label(text="Game Settings",font=("Normal",40),bg=self.settings_color_fg,padx=363,pady=20)
		 .grid(row=0,column=0,columnspan=6))
		# Grid size ----------------------------------------------------------------------------------------------------
		tk.Label(self.root,text="Grid Size (1-100)",
				 font=("normal",20),bg=self.settings_color_fg,width=25,pady=10).grid(row=1,column=0)
		grid_size_text = tk.StringVar(self.root,str(self.game_settings[0]))
		tk.Entry(self.root,textvar=grid_size_text,bg=self.settings_color_fg,
				 font=("normal",34),justify="center",width=5,bd=3).grid(row=1,column=1)
		# Grid number vertical -----------------------------------------------------------------------------------------
		tk.Label(self.root,text="Grid Number Vertical (3-500)",
				 font=("normal",20),bg=self.settings_color_fg,width=25,pady=10).grid(row=2,column=0)
		grid_num_vertical_text = tk.StringVar(self.root,str(self.game_settings[1]))
		tk.Entry(self.root,textvar=grid_num_vertical_text,bg=self.settings_color_fg,
				 font=("normal",34),justify="center",width=5,bd=3).grid(row=2,column=1)
		# Grid number horizontal ---------------------------------------------------------------------------------------
		tk.Label(self.root,text="Grid Number Horizontal (3-500)",
				 font=("normal",20),bg=self.settings_color_fg,width=25,pady=10).grid(row=3,column=0)
		grid_num_horizontal_text = tk.StringVar(self.root,str(self.game_settings[2]))
		tk.Entry(self.root,textvar=grid_num_horizontal_text,bg=self.settings_color_fg,
				 font=("normal",34),justify="center",width=5,bd=3).grid(row=3,column=1)
		# Snake speed --------------------------------------------------------------------------------------------------
		tk.Label(self.root,text="Snake Speed (1-1000)",
				 font=("normal",20),bg=self.settings_color_fg,width=25,pady=10).grid(row=1,column=3)
		snake_speed_text = tk.StringVar(self.root,str(self.game_settings[3]))
		tk.Entry(self.root,textvar=snake_speed_text,bg=self.settings_color_fg,
				 font=("normal",34),justify="center",width=5,bd=3).grid(row=1,column=4)
		# Starting length ----------------------------------------------------------------------------------------------
		tk.Label(self.root,text="Starting Length (1-50)",
				 font=("normal",20),bg=self.settings_color_fg,width=25,pady=10).grid(row=2,column=3)
		starting_length_text = tk.StringVar(self.root,str(self.game_settings[4]))
		tk.Entry(self.root,textvar=starting_length_text,bg=self.settings_color_fg,
				 font=("normal",34),justify="center",width=5,bd=3).grid(row=2,column=4)
		# Start button -------------------------------------------------------------------------------------------------
		self.entry_strings = ["grid_size","grid_num_vertical","grid_num_horizontal","snake_speed","starting_length"]
		self.text_widgets = [grid_size_text,grid_num_vertical_text,grid_num_horizontal_text,snake_speed_text,
							 starting_length_text]
		(tk.Button(self.root,text="Start Game",font=("normal",20),bg=self.settings_color_fg,
				   command=self.start_game,width=33).grid(row=3,column=3,columnspan=3))
		# Error label --------------------------------------------------------------------------------------------------
		self.error_label = tk.Label(self.root,text="",font=("normal",30),bg=self.settings_color_fg,width=30,padx=192)
		self.error_label.grid(row=7,column=0,columnspan=6)

		self.root.mainloop()


if __name__ == '__main__':
	settings = Settings()
	settings.create_menu()
	game = SnakeGame(settings.game_settings,settings.color_settings)
	game.start_game()
	game.root.mainloop()
