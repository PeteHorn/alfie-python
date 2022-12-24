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
slime = Actor('slime')
slime_images = ['slime', 'slimeblue', 'slimegreen']
slime.images = slime_images
movestep = 10
rocks = []
cactuses = []
game_over = False

def draw():
    global rock_points, cactus_points, rocks, cactuses, game_over
    if game_over:
        screen.draw.text('Game Over', centerx=400, centery=270, color=(255,255,255), fontsize=60)
    else:
        screen.blit(BACKGROUND_IMG, (0,0))
        screen.blit(BACKGROUND_IMG, (800,0))
        rocks = draw_object(rock_points, ROCK_IMG)
        cactuses = draw_object(cactus_points, CACTUS_IMG)
        slime.draw()
        runner.draw()

def update():
    global game_over, rocks, cactuses
    runner.next_image()
    if keyboard.up:
        runner.y -= movestep
    if keyboard.down:
        runner.y += movestep
    if keyboard.left:
        runner.x -= movestep
    if keyboard.right:
        runner.x += movestep
    
    if runner.collidelist([slime]) != -1:
        slime.next_image()
        new_coords = plot_object(1)[0]
        slime.x = new_coords['x']
        slime.y = new_coords['y']

    if runner.collidelist(rocks) != -1 or runner.collidelist(cactuses) != -1:
        game_over = True

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