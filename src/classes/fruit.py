from src.settings import *


class Fruit(pygame.sprite.Sprite):
    fruits_list = list(sorted(Path('./src/assets/images/fruits/').glob('*.png')))

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, )
        self.image = pygame.image.load('./src/assets/images/fruits/a_100_cherry.png')
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect = self.image.get_rect()
        self.x_pos = randint(0, CELL_NUMBER - 1) * BLOCK_SIZE - self.image.get_width() // 2
        self.y_pos = randint(0, CELL_NUMBER - 10) * BLOCK_SIZE - self.image.get_height() // 2
        self.rect.center = (self.x_pos, self.y_pos)
        self.pos = vec(self.rect.center)
        self.is_fruit = False

    def create_random_fruit(self):
        random_weight_fruit = choices(self.fruits_list, weights=[10, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1])[0]
        self.image = pygame.image.load(random_weight_fruit)

    def update(self):
        self.create_random_fruit()
        print(self.fruits_list[0])

