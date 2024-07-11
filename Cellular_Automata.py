import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import seaborn as sns
from PIL import Image
import imageio
import os

"""
The functions initialise_food and initialise_ants are used to set up the two grids I created using arrays. The grids are both 10x10 in size.
In the food grid, each cell has an initial value of 3, indicating the amount of food present.
The ant grid uses the value 0 to denote an empty space and the value 1 to indicate the presence of an ant.
"""

scale = 10
def initialise_food(scale):
  food_grid = np.empty(shape=(scale, scale))
  for x in range(scale): #make x and y axis = scale which is 10
      for y in range(scale):
        food_grid[x,y] = 3 # change the values to 2
  return(food_grid)

food_grid = initialise_food(scale)

scale = 10
def initialise_ants(scale):
  ant_grid = np.empty(shape=(scale, scale))
  for x in range(scale):
    for y in range(scale):
      ant_grid[x,y] = 0
      ant_grid[5][5] = 1
  return(ant_grid)

ant_grid = initialise_ants(scale)

"""
The below functions are part of a program that simulates ants interacting with a food grid.
They handle tasks such as checking for dead ants, simulating ant feeding behavior, ant reproduction, and the regrowth of food in the grid.
These functions collectively contribute to the simulation of the ants' behavior and the dynamics of the food grid.
"""

# ant_dead programs the death of ants when the food source they are standing on reaches 0.
def ant_dead(ant_positions, ant_grid, food_grid):
  for x, y in ant_positions:
    if food_grid[x, y] < 0:
      ant_grid[x,y] = 0
  return ant_grid

# ant_eat programs the consumption of 1 unit of food from every grid spot in a 1 unit radius from the location of the ant.
def ants_eat(food_grid, ant_positions):
  for x, y in ant_positions:
    for row in range(x-1, x+2):
      for col in range(y-1, y+2):
        if row > len(food_grid)-1:
          row = 0
        if col > len(food_grid)-1:
          col = 0
        food_grid[row, col] -= 1
        if food_grid[row, col] < 0:
          food_grid[row,col] = -1
  return food_grid

#The ant_baby function generates 1 offspring ant within a one-unit radius from the parent ant's position. It also ensures that the new ant does not spawn on top of any existing ants.
def ant_baby(ant_positions, ant_grid):
  new_ant_positions = []
  for ant in ant_positions:
    x,y = ant[0],ant[1]
    new_x = random.randint(x-1, x+1)
    new_y = random.randint(y-1, y+1)
    if new_x > len(ant_grid)-1:
      new_x = 0
    if new_y > len(ant_grid)-1:
      new_y = 0
    new_ant_positions.append([new_x, new_y])
  for ant in new_ant_positions:
    ant_grid[ant[0]][ant[1]] = 1
  return ant_grid

# food_grow results in the food on the food_grid regenerating at an arbitary regrwoth rate that can be modified.
def food_grow(food_grid,regrowth_rate):
  food_grid += regrowth_rate
  return food_grid


""" This loop runs throught all the prviosuly created functions and applies them onto my food_grid and ant_grid in order to generate a simulation of ants eating and reproducing
and the effects on population dynamic at different stages
"""
scale = 10
regrowth_rate = 0.7 # can be altered to change the rate at which food regrows

ant_grid = initialise_ants(scale)
food_grid = initialise_food(scale)

ant_n = []

frames = []

print("Start")

for turn in range(500):
  print("turn", turn)
  if np.all(ant_grid == 1):
    break
  if np.all(ant_grid == 0):
    break
  # check the grid for ants, kill ants where there is no food, check grid again for ants.
  ant_positions = np.argwhere(ant_grid == 1)
  ant_grid = ant_dead(ant_positions, ant_grid, food_grid)
  ant_positions = np.argwhere(ant_grid == 1)

  # ant eat
  food_grid = ants_eat(food_grid, ant_positions)

  # ant reproduce
  ant_grid = ant_baby(ant_positions, ant_grid)

  # grow food
  food_grid = food_grow(food_grid,regrowth_rate)

  # count the ants
  ant_n.append(len(ant_positions))

  # Plot ant grid and food grid using plt.imshow
  plt.figure()
  plt.subplot(1, 2, 1)
  plt.imshow(ant_grid, cmap='Blues', interpolation='none')
  plt.title(f'Ant Grid {turn:03d}')
  plt.axis('off')


  plt.subplot(1, 2, 2)
  plt.imshow(food_grid, cmap='Greens', interpolation='none')
  plt.title('Food Grid')
  plt.axis('off')
  cbar1 = plt.colorbar(orientation='vertical')
  cbar1.set_label('Food Density')
  #plt.save

 # Save the current frame as an image and add it to the list of frames
  
  output_directory_frame = 'output_frames'
  os.makedirs(output_directory_frame, exist_ok=True) 
  frame_path = os.path.join(output_directory_frame, f'frame_{turn:03d}.png')
  plt.savefig(frame_path)
  frames.append(Image.open(frame_path))
  plt.close()

  print(turn)


""" This code mounts your google drive to the notebook and then takes the frames saved earlier that are stored in the directory and compiles them into a gif
which is sent saved into your google drive as "simulation.gif"
"""

output_directory_gif = 'output_gifs'
gif_path = os.path.join(output_directory_gif, 'simulation.gif')
imageio.mimsave(gif_path, frames)
imageio.mimsave(gif_path, frames, duration=0.1, loop=0)


"""
Using the same simulation loop and adding a linear spacing loop to plot graphs showing the variation in different simulation runs across variable regrowth rates.
"""

allruns = []
print("Start")
for run, regrowth_rate in zip(range(50), np.linspace(0.1, 0.9, 20)): #range in this loop represents how many simulation attempts will take place.
    ant_grid = initialise_ants(scale)
    food_grid = initialise_food(scale)
    ant_n = []

    for turn in range(300):
      if np.all(ant_grid == 1):
        break
      if np.all(ant_grid == 0):
        break
      # check the grid for ants, kill ants where there is no food, check grid again for ants.
      ant_positions = np.argwhere(ant_grid == 1)
      ant_grid = ant_dead(ant_positions, ant_grid, food_grid)
      ant_positions = np.argwhere(ant_grid == 1)

      # ant eat
      food_grid = ants_eat(food_grid, ant_positions)

      # ant reproduce
      ant_grid = ant_baby(ant_positions, ant_grid)

      # grow food
      food_grid = food_grow(food_grid,regrowth_rate)

      # count the ants
      ant_n.append(len(ant_positions))
    allruns.append(ant_n)

#Plotting the graph
    sns.set()

custom_palette = sns.color_palette("Reds", len(allruns))

fig, ax = plt.subplots(figsize=(10, 3))

plt.ylabel('Number of Ants')
plt.xlabel('Turns')

for i, run in enumerate(allruns):
    plt.plot(run, label=f'Run {i}', color=custom_palette[i])

plt.show()