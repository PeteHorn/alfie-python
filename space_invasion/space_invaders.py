import pgzrun
from pgzhelper import *
from random import random, randrange

WIDTH=1024
HEIGHT=768

BACKGROUND_IMG = 'space.png'

def draw():
    screen.blit(BACKGROUND_IMG, (0,0))
    for baddie in baddies:
        baddie.draw()
    goody.draw()
    for laser in lasers:
        lb = laser['laser']
        lb.draw()

def update():
    global direction, timer
    timer += 1
    if timer % 30 == 0:
        direction = move_baddies()
    for laser in lasers:
        lb = laser['laser']
        ep = laser['ep']
        if lb.x == ep[0] and lb.y == ep[1]:
            lasers.remove(laser)
    active_lasers = [laser['laser'] for laser in lasers]
    for baddie in baddies:
        if baddie.collidelist(active_lasers) != -1:
            baddies.remove(baddie)

def move_baddies():
    global direction, move_down
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
    return direction

def new_spaceship(x, y, type):
    baddie = Actor(type)
    baddie.x = x
    baddie.y = y
    baddie.scale = 0.5
    return baddie

def on_mouse_move(pos):
    goody.angle = goody.angle_to(pos) - 90

def on_mouse_down(pos):
    global ss_loc
    laser = Actor('laser')
    laser.x = ss_loc['x']
    laser.y = ss_loc['y']
    laser.angle = goody.angle + 90
    endpoint = calculate_laser_endpoint(pos)
    lasers.append({
        'laser': laser,
        'ep': list(endpoint)
        })
    animate(laser, pos=endpoint)
    sounds.flashlaser01.play()


def calculate_laser_endpoint(mouse_pos):
    global ss_loc
    ss_x = ss_loc['x']
    ss_y = ss_loc['y']
    mp_x = mouse_pos[0]
    mp_y = mouse_pos[1]
    x_diff = mp_x - ss_x
    y_diff = mp_y - ss_y
    scale = remove_negative(WIDTH / x_diff)
    endpoint = {
        x_diff * scale + ss_loc['x'],
        y_diff * scale + ss_loc['y']
    }
    return endpoint

def remove_negative(number):
    sq = number * number
    sqrt = math.sqrt(sq)
    return sqrt

timer = 0
baddies =[]
lasers = []
baddie_offset = 100
baddie_spacing = 70
direction = 'r'
move_down = False
for x in range(5):
    for y in range(4):
        baddies.append(
            new_spaceship(
                baddie_offset + x * baddie_spacing, 
                baddie_offset + y * baddie_spacing,
                'christmas_tree'))
ss_loc = {
    'x': WIDTH / 2,
    'y': HEIGHT - 50
}
goody = new_spaceship(ss_loc['x'], ss_loc['y'], 'christmas_tree_farm')
pgzrun.go() # Must be last line