import pyray as pr
import random
import math

# Constants for screen dimensions
WIN_WIDTH = 800
WIN_HEIGHT = 800

# Constants for colors
GREEN = pr.GREEN
RED = pr.RED

DISTANCE_THRESHOLD = 100
COLLISION_RADIUS = 10
CREATURE_DAMAGE = 1
class Creature:
    def __init__(self, x, y, color, hp) -> None:
        self.x = x
        self.y = y
        self.color = color
        self.hp = hp
        self.random = True
        self.dead = False

    def move_towards(self, target_x, target_y, speed):
        if not self.random:
            direction_x = target_x - self.x
            direction_y = target_y - self.y
            distance = math.sqrt(direction_x**2 + direction_y**2)
            
            if distance > 0:
                direction_x /= distance
                direction_y /= distance
            
            self.x += direction_x * speed
            self.y += direction_y * speed
        else:
            self.x += random.randint(-speed, speed)
            self.y += random.randint(-speed, speed)
                # Ensure the player stays within the screen bounds
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x > WIN_WIDTH:
            self.x = WIN_WIDTH
        if self.y > WIN_HEIGHT:
            self.y = WIN_HEIGHT

class Player(Creature):
    def __init__(self, x, y, color, hp) -> None:
        super().__init__(x, y, color, hp)
        self.vx = 0
        self.vy = 0
        self.speed = 0.25
        self.control = True 

    def kill(self):
        self.hp = 10
        self.x = WIN_WIDTH / 2
        self.y = WIN_HEIGHT / 2
        self.vx = 0
        self.vy = 0
        self.control = False
        print("BOO")

    def update(self):
        self.x += self.vx
        self.y += self.vy

        if self.vx > 0:
            self.vx -= 0.2
            if self.vx < 0:
                self.vx = 0
        if self.vx < 0:
            self.vx += 0.2
            if self.vx > 0:
                self.vx = 0
        if self.vy > 0:
            self.vy -= 0.2
            if self.vy < 0:
                self.vy = 0
        if self.vy < 0:
            self.vy += 0.2
            if self.vy > 0:
                self.vy = 0
        if self.vx > 3:
            self.vx = 3
        if self.vx < -3:
            self.vx = -3
        if self.vy > 3:
            self.vy = 3
        if self.vy < -3:
            self.vy = -3

        # Ensure the player stays within the screen bounds
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x > WIN_WIDTH:
            self.x = WIN_WIDTH
        if self.y > WIN_HEIGHT:
            self.y = WIN_HEIGHT

        if self.hp <= 0:
            self.kill()

fryd = Player(400, 400, GREEN, 10)
creatures = []
for _ in range(100):
    creatures.append(Creature(random.randint(0, WIN_WIDTH),
                              random.randint(0, WIN_HEIGHT),
                              RED, 1))

def update_game():
        # TODO:
    # 1 - instantiate a player (creature subclass) DONE
    # 2 - use keypresses to modify player velocity (skate physics w/drag) DONE
    # 3 - creatures that are within N distance from the player, move towards the player DONE
    # 4 - creature within radius of the player dies, but does damage to player DONE
    # 5 - creatures collide as well DONE 
    # 6 - one pass through the creature list per update NOT DONE
    global creatures
    new_creatures = []

    for i, creature in enumerate(creatures):
        creatures[i] = creature.x, creature.y
        distance_to_player = math.sqrt((creature.x - fryd.x) ** 2 + (creature.y - fryd.y) ** 2)
        if fryd.control:
            if distance_to_player <= COLLISION_RADIUS:
                fryd.hp -= CREATURE_DAMAGE
            elif distance_to_player <= DISTANCE_THRESHOLD:
                creature.random = False
                creature.move_towards(fryd.x, fryd.y, 1)  # Move towards player with speed 1
                if not creature.dead:
                    new_creatures.append(creature)       
            else:
                creature.random = True
                creature.move_towards(random.randint(0, WIN_WIDTH), random.randint(0, WIN_HEIGHT), 5)
                if not creature.dead:
                    new_creatures.append(creature)
        else:
            creature.random = True
            creature.move_towards(random.randint(0, WIN_WIDTH), random.randint(0, WIN_HEIGHT), 5)
            if not creature.dead:
                new_creatures.append(creature)

        for j in range (i + 1, len(creatures)):
            other_creature = creatures[j]
            distance = math.sqrt((creature.x - other_creature.x) ** 2 + (creature.y - other_creature.y) ** 2)
            if distance < COLLISION_RADIUS:
                creature.dead = True
                other_creature.dead = True

        pr.draw_circle(int(creature.x), int(creature.y), 5, creature.color)

    creatures = new_creatures

    pr.draw_circle(int(fryd.x), int(fryd.y), 10, fryd.color)

    if fryd.control:
        if pr.is_key_down(pr.KEY_D):
            fryd.vx += fryd.speed
        if pr.is_key_down(pr.KEY_A):
            fryd.vx -= fryd.speed
        if pr.is_key_down(pr.KEY_W):
            fryd.vy -= fryd.speed
        if pr.is_key_down(pr.KEY_S):
            fryd.vy += fryd.speed

    fryd.update()

# Initialization
pr.init_window(WIN_WIDTH, WIN_HEIGHT, "game 01")
pr.set_target_fps(60)

# Main game loop
while not pr.window_should_close():
    pr.begin_drawing()
    pr.clear_background(pr.RAYWHITE)
    update_game()
    pr.end_drawing()

pr.close_window()
