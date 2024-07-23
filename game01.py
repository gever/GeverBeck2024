from pyray import *
import random

WIN_WIDTH = 800
WIN_HEIGHT = 800

init_window(WIN_WIDTH, WIN_HEIGHT, "game 01")

class Creature:
    def __init__(self, x, y, color) -> None:
        self.x = x
        self.y = y
        self.color = color

creatures = []
for _ in range(100):
    creatures.append( Creature(random.randint(0, WIN_WIDTH),
                               random.randint(0, WIN_HEIGHT),
                               (128, random.randint(64, 128+64), 128)))

def update_game():
    # TODO:
    # 1 - instantiate a player (creature subclass)
    # 2 - use keypresses to modify player velocity (skate physics w/drag)
    # 3 - creatures that are within N distance from the player, move towards the player
    # 4 - creature within radius of the player dies, but does damage to player
    # 5 - creatures collide as well
    # 6 - one pass through the creature list per update
    pass

while not window_should_close():
    begin_drawing()
    clear_background(RAYWHITE)
    # draw_text("Hello world", 190, 200, 20, VIOLET)
    update_game()
    end_drawing()
close_window()
