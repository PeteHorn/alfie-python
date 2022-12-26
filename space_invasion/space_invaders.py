import pgzrun
from pgzhelper import *
from random import random, randrange

WIDTH=1024
HEIGHT=768

BACKGROUND_IMG = 'space.png'

def draw():
    global baddies
    screen.blit(BACKGROUND_IMG, (0,0))
    for baddie in baddies:
        baddie.draw()

def update():
    global direction, timer
    timer += 1
    if timer % 30 == 0:
        direction = move_baddies()

def move_baddies():
    global baddies, direction, move_down
    movestep = baddie_spacing / 2
    move_dir = direction
    if move_down:
        for baddie in baddies:
            baddie.y += movestep
        move_down = False
    else:
        for baddie in baddies:
            if move_dir == 'r':
                baddie.x += movestep
                if baddie.x > 924:
                    direction = 'l'
                    move_down = True
            elif move_dir == 'l':
                baddie.x -= movestep
                if baddie.x < 100:
                    direction = 'r'
                    move_down = True
        print(f'x = {baddie.x}, y = {baddie.y}. dir = {direction}')
    return direction

def new_baddie(x, y):
    baddie = Actor('christmas_tree')
    baddie.x = x
    baddie.y = y
    baddie.scale = 0.5
    return baddie

timer = 0
baddies =[]
baddie_offset = 100
baddie_spacing = 70
direction = 'r'
move_down = False
for x in range(5):
    for y in range(4):
        baddies.append(
            new_baddie(
                baddie_offset + x * baddie_spacing, 
                baddie_offset + y * baddie_spacing))

pgzrun.go() # Must be last line