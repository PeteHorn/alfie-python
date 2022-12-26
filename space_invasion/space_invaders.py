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
    global direction
    direction = move_baddies(direction)

def move_baddies(direction):
    global baddies
    movestep = baddie_spacing / 2
    for baddie in baddies:
        if direction == 'r':
            baddie.x += movestep
            if baddie.x > 924:
                direction = 'dl'
        elif direction == 'l':
            baddie.x -= movestep
            if baddie.x < 100:
                direction = 'dr'
        elif direction == 'dl':
            baddie.y += movestep
            direction == 'l'
        elif direction == 'dr':
            baddie.y += movestep
            direction = 'r'

def new_baddie(x, y):
    baddie = Actor('christmas_tree')
    baddie.x = x
    baddie.y = y
    baddie.scale = 0.5
    return baddie

baddies =[]
baddie_offset = 100
baddie_spacing = 70
direction = 'r'
for x in range(5):
    for y in range(4):
        baddies.append(
            new_baddie(
                baddie_offset + x * baddie_spacing, 
                baddie_offset + y * baddie_spacing))

pgzrun.go() # Must be last line