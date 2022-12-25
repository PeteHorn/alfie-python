import pgzrun
from pgzhelper import *
from random import random, randrange

WIDTH=1200
HEIGHT=600

BACKGROUND_IMG = 'sand.png'
ROCK_IMG = 'rock.png'
CACTUS_IMG = 'cactus.png'
runner = Actor('run1')
runner.x = 100
runner.y = 100
run_images = ['run1', 'run2', 'run3', 'run4', 'run5', 'run6', 'run7', 'run8']
runner.images = run_images
runner.scale = 0.5
slime = Actor('slime1')
slime_images = ['slime1', 'slime2', 'slime3']
slime.images = slime_images
movestep = 5
rocks = []
cactuses = []
walkers = []
directions = []
boundary = []
game_over = False
walker_count = 0
score = 0
OOB_square = 200
updatecount = 0

def draw():
    global rock_points, cactus_points, slime_point, rocks, cactuses, game_over, score, walkers, perimeter, boundary
    if game_over:
        screen.draw.text('Game Over', centerx=400, centery=270, color=(255,255,255), fontsize=60)
    else:
        screen.blit(BACKGROUND_IMG, (0,0))
        screen.blit(BACKGROUND_IMG, (800,0))
        rocks = draw_object(rock_points, ROCK_IMG)
        cactuses = draw_object(cactus_points, CACTUS_IMG)
        boundary = draw_object(perimeter, ROCK_IMG)
        slime.draw()
        runner.draw()
        for walker in walkers:
            walker.draw()
        screen.draw.text('Score: ' + str(score), (15,10), color=(35,222,213), fontsize=50)

def update():
    global game_over, rocks, cactuses, walker_count, score, walkers, directions, updatecount
    updatecount += 1
    if walker_count == 5:
        walker_count = 0
        for walker in walkers:
            walker.next_image()
    else:
        walker_count += 1
    keyboard_actions(runner, [rocks, cactuses])
    
    if runner.collidelist([slime]) != -1 or updatecount % 500 == 0:
        slime.next_image()
        new_coords = new_item_plot()
        slime.x = new_coords['x']
        slime.y = new_coords['y']
        if updatecount % 500 != 0:
            score += 1
        if score % 3 == 0:
            zombie, direction = new_walker()
            walkers.append(zombie)
            directions.append(direction)
        updatecount = 0
    
    for i, walker in enumerate(walkers):
        if directions:
            directions[i] = move_zombie(walker, directions[i])

    if runner.collidelist(walkers) != -1:
        game_over = True

def move_zombie(zombie:Actor, direction):
    global rocks, cactuses, boundary
    currentlocation = {
        'x': zombie.x,
        'y': zombie.y
    }
    if direction == 'up':
        zombie.y -= 1
    elif direction == 'down':
        zombie.y += 1
    elif direction == 'right':
        zombie.x += 1
        zombie.flip_x = False
    elif direction == 'left':
        zombie.x -= 1
        zombie.flip_x = True
    if detect_object(zombie, [rocks, cactuses, boundary]):
        zombie.x = currentlocation['x']
        zombie.y = currentlocation['y']
        pos_directions = ['up', 'down', 'left', 'right']
        pos_directions.remove(direction)
        direction = pos_directions[randrange(1, 3, 1)]
    return direction

def keyboard_actions(actor:Actor, objects):
    if keyboard.up:
        move(actor, 'y', detect_object(actor, objects))
    if keyboard.down:
        move(actor, 'y', not detect_object(actor, objects))
    if keyboard.left:
        move(actor, 'x', detect_object(actor, objects))
        actor.flip_x = True
    if keyboard.right:
        move(actor, 'x', not detect_object(actor, objects))
        actor.flip_x = False
    if keyboard.up or keyboard.down or keyboard.left or keyboard.right:
        actor.next_image()

def move(actor:Actor, axis, inc):
    global rocks, cactuses, boundary
    currentlocation = {
        'x': actor.x,
        'y': actor.y
    }
    if inc:
        movemotion = movestep
    else:
        movemotion = -movestep
    if axis == 'x':
        actor.x += movemotion
    elif axis == 'y':
        actor.y += movemotion
    if detect_object(actor, [rocks, cactuses, boundary]):
        actor.x = currentlocation['x']
        actor.y = currentlocation['y']

def new_walker():
    walker = Actor('walk1')
    coords = new_item_plot()
    walker.x = coords['x']
    walker.y = coords['y']
    walk_images = ['walk1', 'walk2', 'walk3', 'walk4', 'walk5', 'walk6', 'walk7', 'walk8', 'walk9', 'walk10']
    walker.images = walk_images
    walker.scale = 0.5
    return walker, 'up'

def detect_object(actor:Actor, objects):
    obstacledetected = False
    for obstacle in objects:
        if actor.collidelist(obstacle) !=-1 or actor.x < 0 or actor.x > WIDTH or actor.y < 0 or actor.y > HEIGHT:
            obstacledetected = True
    return obstacledetected

def draw_object(coordinate_array, obstacle):
    obstacle_array = []
    for point in coordinate_array:
        actor = Actor(obstacle)
        actor.x = point['x']
        actor.y = point['y']
        if 'angle' in point:
            actor.angle = point['angle']
        actor.draw()
        obstacle_array.append(actor)
    return obstacle_array

def plot_object(number):
    global OOB_square
    points = []
    for i in range(number):
        rect1 = {'x': OOB_square, 'y': HEIGHT - OOB_square, 'x_offset': 0, 'y_offset': OOB_square}
        rect2 = {'x': WIDTH - (2 * OOB_square), 'y': HEIGHT, 'x_offset': OOB_square, 'y_offset': 0}
        rect3 = {'x': OOB_square, 'y': HEIGHT - OOB_square, 'x_offset': WIDTH - OOB_square, 'y_offset': 0}
        select = [rect1, rect2, rect2, rect2, rect2, rect3]
        selected_rect = select[randrange(len(select))]
        coords = {
            'x': selected_rect['x_offset'] + (random() * selected_rect['x']),
            'y': selected_rect['y_offset'] + (random() * selected_rect['y'])
        }
        points.append(coords)
    return points

def create_perimeter():
    perimeter = []
    for x in range(20):
        coords = {
            'x': x * 60,
            'y': 0,
            'angle': 180
        }
        perimeter.append(coords)
    for x in range(20):
        coords = {
            'x': x * 60,
            'y': HEIGHT - 1
        }
        perimeter.append(coords)
    for y in range(15):
        coords = {
            'x': 0,
            'y': y * 40,
            'angle': 270
        }
        perimeter.append(coords)
    for y in range(15):
        coords = {
            'x': WIDTH - 1,
            'y': y * 40,
            'angle': 90
        }
        perimeter.append(coords)
    return perimeter

def new_item_plot():
    minx = 50
    xrange = 1100
    miny = 50
    yrange = 500
    coords = {
            'x': minx + (random() * xrange),
            'y': miny + (random() * yrange)
        }
    return coords
    
perimeter = create_perimeter()
slime_point = new_item_plot()
slime.x = slime_point['x']
slime.y = slime_point['y']
rock_points = plot_object(10)
cactus_points = plot_object(10)
zombie, direction = new_walker()
walkers.append(zombie)
directions.append(direction)
pgzrun.go() # Must be last line