import pygame
import sys
from settings import *
from level import Level
from overworld import Overworld
from ui import UI


class Game:
    def __init__(self):

        # game attributes
        self.level_unlocked = 0
        self.full_health = 100
        self.current_health = 100
        self.current_coins = 0

        # audio
        self.bg_music_level = pygame.mixer.Sound(
            'C:/Users/Jack/Documents/GitHub/collegeWork/Units/Visual_Programming/game/audio/level_music.wav')
        self.bg_music_menu = pygame.mixer.Sound(
            'C:/Users/Jack/Documents/GitHub/collegeWork/Units/Visual_Programming/game/audio/overworld_music.wav')

        # overworld creation
        self.overworld = Overworld(
            0, self.level_unlocked, screen, self.level_start)
        self.status = 'overworld'
        self.bg_music_menu.play(loops=-1)

        # user interface
        self.ui = UI(screen)

    def overworld_creation(self, current_level, new_max_level):
        if new_max_level > self.level_unlocked:
            self.level_unlocked = new_max_level
        self.overworld = Overworld(
            current_level, self.level_unlocked, screen, self.level_start)
        self.status = 'overworld'
        self.bg_music_level.stop()
        self.bg_music_menu.play(loops=-1)

    def update_coins(self, amount):
        self.current_coins += amount

    def update_health(self, amount):
        self.current_health += amount

    def reset_game(self):
        if self.current_health <= 0:
            self.current_health = 100
            self.current_coins = 0
            self.level_unlocked = 0
            self.overworld = Overworld(
                0, self.level_unlocked, screen, self.level_start)
            self.status = 'overworld'

    def level_start(self, current_level):
        self.level = Level(current_level, screen, self.overworld_creation,
                           self.update_coins, self.update_health)
        self.status = 'level'
        self.bg_music_menu.stop()
        self.bg_music_level.play(loops=-1)

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.current_health, self.full_health)
            self.ui.show_coins(self.current_coins)
            self.reset_game()


# game setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((191, 170, 140))
    game.run()

    pygame.display.update()
    clock.tick(60)
