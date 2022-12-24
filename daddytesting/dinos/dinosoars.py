import pgzrun
from pgzhelper import *
from random import random

WIDTH=1200
HEIGHT=600

BACKGROUND_IMG = 'sand.png'
ROCK_IMG = 'rock.png'
CACTUS_IMG = 'cactus.png'
runner = Actor('run1')
run_images = ['run1', 'run2', 'run3', 'run4', 'run5', 'run6', 'run7', 'run8']
runner.images = run_images
runner.scale = 0.5
walker = Actor('walk1')
walker.x = 1100
walker.y = 500
walk_images = ['walk1', 'walk2', 'walk3', 'walk4', 'walk5', 'walk6', 'walk7', 'walk8', 'walk9', 'walk10']
walker.images = walk_images
walker.scale = 0.5
slime = Actor('slime1')
slime_images = ['slime1', 'slime2', 'slime3']
slime.images = slime_images
movestep = 10
rocks = []
cactuses = []
game_over = False
walker_count = 0
score = 0

def draw():
    global rock_points, cactus_points, rocks, cactuses, game_over, score
    if game_over:
        screen.draw.text('Game Over', centerx=400, centery=270, color=(255,255,255), fontsize=60)
    else:
        screen.blit(BACKGROUND_IMG, (0,0))
        screen.blit(BACKGROUND_IMG, (800,0))
        rocks = draw_object(rock_points, ROCK_IMG)
        cactuses = draw_object(cactus_points, CACTUS_IMG)
        slime.draw()
        runner.draw()
        walker.draw()
        screen.draw.text('Score: ' + str(score), (15,10), color=(35,222,213), fontsize=50)

def update():
    global game_over, rocks, cactuses, walker_count, score
    if walker_count == 5:
        walker_count = 0
        walker.next_image()
    else:
        walker_count += 1
    runner.next_image()
    if keyboard.up:
        move('y', detect_object([rocks, cactuses]))
    if keyboard.down:
        move('y', not detect_object([rocks, cactuses]))
    if keyboard.left:
        move('x', detect_object([rocks, cactuses]))
    if keyboard.right:
        move('x', not detect_object([rocks, cactuses]))
    
    if runner.collidelist([slime]) != -1:
        slime.next_image()
        new_coords = plot_object(1)[0]
        slime.x = new_coords['x']
        slime.y = new_coords['y']
        score += 1

    if runner.collidelist([walker]) != -1:
        game_over = True

def move(axis, inc):
    if inc:
        movemotion = movestep
    else:
        movemotion = -movestep * 3
    if axis == 'x':
        runner.x += movemotion
    elif axis == 'y':
        runner.y += movemotion


def detect_object(objects):
    obstacledetected = False
    for obstacle in objects:
        if runner.collidelist(obstacle) !=-1:
            obstacledetected = True
    return obstacledetected

def draw_object(coordinate_array, obstacle):
    obstacle_array = []
    for point in coordinate_array:
        actor = Actor(obstacle)
        actor.x = point['x']
        actor.y = point['y']
        actor.draw()
        obstacle_array.append(actor)
    return obstacle_array

def plot_object(number):
    points = []
    for i in range(number):
        coords = {
            'x': random() * WIDTH,
            'y': random() * HEIGHT
        }
        points.append(coords)
    return points

slime_point = plot_object(1)
rock_points = plot_object(10)
cactus_points = plot_object(10)
pgzrun.go() # Must be last line