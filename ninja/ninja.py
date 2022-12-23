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
game_over = False

def draw():
  global score, game_over
  screen.draw.filled_rect(Rect(0,0,1200,400), (19, 21, 97))
  screen.draw.filled_rect(Rect(0,400,1200,200), (17, 84, 28))
  if game_over:
    screen.draw.text('Game Over', centerx=400, centery=270, color=(255,255,255), fontsize=60)
    screen.draw.text('Score: ' + str(score), centerx=400, centery=330, color=(255,255,255), fontsize=60)
  else:   
    runner.draw()
    for actor in obstacles:
        actor.draw()
    screen.draw.text('Score: ' + str(score), (15,10), color=(35,222,213), fontsize=50, fontname="nitemare")
 
def update():
  global velocity_y, obstacles_timeout, score, game_over
  ground = 400
  obstacles_timeout += 1
  runner.next_image()
  if obstacles_timeout > 100:
    scale = random.random()
    actor = Actor('tree1')
    actor.scale = 0.15 +(scale * 0.05)
    actor.x = 1250
    actor.y = ground
    obstacles.append(actor)
    obstacles_timeout = 0

  for actor in obstacles:
    actor.x -= 8
    if actor.x < -50:
      obstacles.remove(actor)
      score += 1
  
  if keyboard.up and runner.y == ground:
    velocity_y = -25

  runner.y += velocity_y
  velocity_y += gravity
  if runner.y > ground:
    velocity_y = 0
    runner.y = ground
  
  if runner.collidelist(obstacles) != -1:
    game_over = True


pgzrun.go() # Must be last line