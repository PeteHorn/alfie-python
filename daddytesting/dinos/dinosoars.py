import pgzrun
from pgzhelper import *
from random import random, randrange

WIDTH=1200
HEIGHT=600

BACKGROUND_IMG = 'sand.png'
ROCK_IMG = 'rock.png'
CACTUS_IMG = 'cactus.png'
runner = Actor('run1')
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
game_over = False
walker_count = 0
score = -1
OOB_square = 200
add_walker = 0

def draw():
    global rock_points, cactus_points, rocks, cactuses, game_over, score, walkers, perimeter
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
    global game_over, rocks, cactuses, walker_count, score, walkers, add_walker, directions
    if walker_count == 5:
        walker_count = 0
        for walker in walkers:
            walker.next_image()
    else:
        walker_count += 1
    runner.next_image()
    keyboard_actions(runner, [rocks, cactuses])
    
    if runner.collidelist([slime]) != -1:
        slime.next_image()
        new_coords = plot_object(1)[0]
        slime.x = new_coords['x']
        slime.y = new_coords['y']
        score += 1
        add_walker += 1
        if add_walker == 10:
            zombie, direction = new_walker()
            walkers.append(zombie)
            directions.append(direction)
    
    for i, walker in enumerate(walkers):
        if directions:
            directions[i] = move_zombie(walker, directions[i])

    if runner.collidelist(walkers) != -1:
        game_over = True

def move_zombie(zombie:Actor, direction):
    global rocks, cactuses
    if direction == 'up':
        zombie.y -= 1
    elif direction == 'down':
        zombie.y += 1
    elif direction == 'right':
        zombie.x += 1
    elif direction == 'left':
        zombie.x -= 1
    if detect_object(zombie, [rocks, cactuses]):
        pos_directions = ['up', 'down', 'left', 'right']
        pos_directions.remove(direction)
        direction = pos_directions[randrange(0, 2, 1)]
    return direction

def keyboard_actions(actor, objects):
    if keyboard.up:
        move(actor, 'y', detect_object(actor, objects))
    if keyboard.down:
        move(actor, 'y', not detect_object(actor, objects))
    if keyboard.left:
        move(actor, 'x', detect_object(actor, objects))
    if keyboard.right:
        move(actor, 'x', not detect_object(actor, objects))

def move(actor:Actor, axis, inc):
    if inc:
        movemotion = movestep
    else:
        movemotion = -movestep
    if axis == 'x':
        actor.x += movemotion
    elif axis == 'y':
        actor.y += movemotion

def new_walker():
    walker = Actor('walk1')
    walker.x = 1100
    walker.y = 500
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
            'y': 0
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
            'y': y * 40
        }
        perimeter.append(coords)
    for y in range(15):
        coords = {
            'x': WIDTH - 1,
            'y': y * 40
        }
        perimeter.append(coords)
    print(perimeter)
    return perimeter
    
perimeter = create_perimeter()
slime_point = plot_object(1)
rock_points = plot_object(10)
cactus_points = plot_object(10)
zombie, direction = new_walker()
walkers.append(zombie)
directions.append(direction)
pgzrun.go() # Must be last line