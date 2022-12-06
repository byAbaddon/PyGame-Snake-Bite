import pygame.sprite

from src.settings import *
from src.classes.sound import Sound
from src.classes.snake import Snake
from src.classes.fruit import Fruit
from src.classes.grid import Grid
from src.classes.figure import Figure
from src.classes.table import Table

# ======================================================================== create Sprite groups
snake_group = pygame.sprite.Group()
fruit_group = pygame.sprite.Group()
figure_group = pygame.sprite.Group()
#
# # add to all_sprite_groups
all_spite_groups_dict = {'snake': snake_group, 'fruit': fruit_group, 'figure': figure_group}
#
# # ======================================================================= initialize  Classes
#
snake = Snake(all_spite_groups_dict)
fruit = Fruit(all_spite_groups_dict, snake)
#
#
# # add to group
snake_group.add(snake)
fruit_group.add(fruit)

# ==================================================================
table = Table(snake, fruit)


# Game State
class GameState(Sound):
    COOLDOWN = 1000  # milliseconds
    start_timer = pygame.time.get_ticks()
    start_game_counter = 3

    def __init__(self,):
        self.state = 'intro'
        self.current_music = ''
        self.is_music_play = False
        self.background = None
        self.is_bg_created = False
        self.reset_data = False

    def game(self):
        # text_creator(f'FPS: {int(CLOCK.get_fps())}', 'brown3', 250, 20, 22)
        # # ++++++++++++++++++++++++++++++ developer utils +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # text_creator(f'FPS {int(CLOCK.get_fps())}', 'white', 10, 5, 25)
        # text_creator(f'Direction: x= {int(snake.direction.x)} y= {int(snake.direction.y)}', 'white', 90, 15, 22)
        # text_creator(f'Pos: x= {int(snake.pos.x)} y= {int(snake.pos.y)}', 'white', 86, 33, 22)
        # text_creator(f'MousePos: x= {pygame.mouse.get_pos()}', 'white', 490, 5)

        if self.reset_data:
            self.state = 'game'  # must be Intro
            self.current_music = ''
            self.is_music_play = False
            self.background = None
            self.is_bg_created = False
            self.start_game_counter = 3
            self.reset_data = False

        if snake.is_pause:
            snake.is_pause = False
            self.state = 'pause'

        if snake.is_back_to_game_state:   # TODO:
            Sound.stop_all_sounds()
            snake.reset_current_data()  # reset current snake data
            self.state = 'get_ready'
            return

        if not self.is_bg_created:
            Sound.background_music(self)
            figure_group.add(Figure('./src/assets/images/figures/level_2.png'))
            self.is_bg_created = True

        if snake.is_eat_fruit and not len(fruit_group):
            fruit_group.add(Fruit(all_spite_groups_dict, snake))
            snake.is_eat_fruit = False

        # # =================================================== UPDATE
        Grid.draw_grid(self)
        table.update()

        # #  --------------------------- draw sprite group
        snake_group.draw(SCREEN)
        figure_group.draw(SCREEN)
        fruit_group.draw(SCREEN)
        #
        # # # # --------------------------- update sprite group
        snake_group.update()
        fruit_group.update()

    def intro(self):
        background_image('./src/assets/images/backgrounds/bg_snake.png')
        text_creator('Start game - SPACE', 'firebrick', S_W - 280, S_H - 140, 35)
        text_creator('Credits - C', 'firebrick', S_W - 280, S_H - 100, 35)
        text_creator('Menu - M', 'firebrick', S_W - 280, S_H - 60, 35)
        text_creator('Copyright ©2023', 'aquamarine', S_W - 150, S_H - 10,)

        if key_pressed(pygame.K_SPACE):
            Sound.btn_click(self)
            self.state = 'get_ready'
        if key_pressed(pygame.K_c):
            Sound.btn_click(self)
            self.state = 'credits'
        if key_pressed(pygame.K_m):
            Sound.btn_click(self)
            self.state = 'menu'
        exit_game()

    def menu(self):
        background_image('./src/assets/images/backgrounds/bg_menu.png')
        text_creator('Press RETURN to back...', 'cornsilk', S_W - 200, S_H - 10, 24)
        if key_pressed(pygame.K_RETURN):
            self.state = 'intro'
        exit_game()

    def credits(self):
        # background_image('./src/assets/images/backgrounds/bg_EMPTY.png')
        text_creator('CREDITS', 'slateblue3', S_W // 2 - 60, 40, 40, None, None, True)
        text_creator('version: 1.0.0-beta', 'cornsilk', S_W - 130, 20, 20)

        text_creator('Free images:', 'brown', 110, 100, 35)
        text_creator('https://www.pngwing.com', 'cadetblue4', 130, 125, 30)

        text_creator('Free sounds:', 'brown', 110, 200, 35)
        text_creator('https://freesound.org/', 'cadetblue4', 130, 225, 30)

        text_creator('Platform 2D game:', 'brown', 110, S_H // 2, 34)
        text_creator('https://www.pygame.org', 'cadetblue4', 130, S_H // 2 + 24, 30)

        SCREEN.blit(pygame.image.load('./src/assets/images/title/pygame_logo.png'), (S_W // 4 - 50, S_H - 266))

        text_creator('Developer:', 'brown', 30, S_H - 60, 30)
        text_creator('by Abaddon', 'cadetblue4', 50, S_H - 40, 30)

        text_creator('Bug rapports:', 'brown', S_W // 2 - 90, S_H - 60, 30)
        text_creator('subtotal@abv.bg', 'cadetblue4', S_W // 2 - 70, S_H - 40, 30)

        text_creator('Copyright:', 'brown', S_W - 140, S_H - 60, 30)
        text_creator('© 2023', 'cadetblue4', S_W - 120, S_H - 40, 30)

        text_creator('Press RETURN to back...', 'cornsilk', S_W - 200, S_H - 10, 24)

        if key_pressed(pygame.K_RETURN):
            Sound.btn_click(self)
            self.state = 'intro'
        exit_game()

    def get_ready(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.start_timer > self.COOLDOWN:
            self.start_game_counter -= 1
            self.start_timer = time_now
        background_image('./src/assets/images/backgrounds/bg_snake.png')
        text_creator(f'START AFTER: {self.start_game_counter}', 'black', 260, S_H // 2, 50)
        # text_creator('Press RETURN to continue...', 'bisque', S_W - 280, S_H - FRAME_SIZE - 10)
        if self.start_game_counter == 0:
            self.reset_data = True
            self.state = 'game'
        exit_game()

    def start_pause(self):
        background_image('./src/assets/images/backgrounds/bg_pause.png')
        text_creator('PAUSE', 'chartreuse4', S_W - 360, S_H - FRAME_SIZE - 250, 50)
        text_creator('Press RETURN to continue...', 'bisque', S_W - 280, S_H - FRAME_SIZE - 10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                Sound.btn_click(self)
                if event.key == pygame.K_RETURN:
                    self.state = 'game'

    # ========================================= state manager ...
    def state_manager(self):
        print(self.state)
        if self.state == 'intro':
            self.intro()
        if self.state == 'game':
            self.game()
        if self.state == 'get_ready':
            self.get_ready()
        if self.state == 'menu':
            self.menu()
        if self.state == 'credits':
            self.credits()
        if self.state == 'pause':
            self.start_pause()


#  ================================ create new GameState
game_state = GameState()

# ================================================================ create top Table for: score , energy and more

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)
# ============= Starting Game loop
while True:
    SCREEN.fill(pygame.Color('black'))
    game_state.state_manager()
    pygame.display.update()
    CLOCK.tick(snake.speed)
