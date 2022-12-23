import pgzrun
from pgzhelper import *
import random

WIDTH=1200
HEIGHT=600

runner = Actor('run__000')
run_images = ['run__000', 'run__001', 'run__002', 'run__003', 'run__004', 'run__005', 'run__006', 'run__007', 'run__008', 'run__009']
runner.images = run_images
velocity_y = 0
gravity = 1
obstacles = []
obstacles_timeout = 0
runner.x = 200
runner.y = 400
score = 0

def draw():
  global score
  screen.draw.filled_rect(Rect(0,0,1200,400), (19, 21, 97))
  screen.draw.filled_rect(Rect(0,400,1200,200), (17, 84, 28))
  runner.draw()
  for actor in obstacles:
    actor.draw()
  screen.draw.text('Score: ' + str(score), (15,10), color=(35,222,213), fontsize=50, fontname="nitemare")
 
def update():
  global velocity_y, obstacles_timeout, score
  obstacles_timeout += 1
  runner.next_image()
  if obstacles_timeout > 100:
    scale = random.random()
    actor = Actor('tree1')
    actor.scale = 0.15 +(scale * 0.55)
    actor.x = 1250
    actor.y = 400
    obstacles.append(actor)
    obstacles_timeout = 0

  for actor in obstacles:
    actor.x -= 8
    if actor.x < -50:
      obstacles.remove(actor)
      score += 1

  
  if keyboard.up:
    velocity_y = -15

  runner.y += velocity_y
  velocity_y += gravity
  if runner.y > 400:
    velocity_y = 0
    runner.y = 400


pgzrun.go() # Must be last line