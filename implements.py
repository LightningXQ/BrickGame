import math
import random
import time
import config
import pygame
from pygame.locals import Rect, K_LEFT, K_RIGHT

class Basic:
    def __init__(self, color: tuple, speed: int = 0, pos: tuple = (0, 0), size: tuple = (0, 0)):
        self.color = color
        self.rect = Rect(pos[0], pos[1], size[0], size[1])
        self.center = (self.rect.centerx, self.rect.centery)
        self.speed = speed
        self.start_time = time.time()
        self.dir = 270

    def move(self):
        dx = math.cos(math.radians(self.dir)) * self.speed
        dy = -math.sin(math.radians(self.dir)) * self.speed
        self.rect.move_ip(dx, dy)
        self.center = (self.rect.centerx, self.rect.centery)

class Block(Basic):
    def __init__(self, pos: tuple = (0, 0), hits_required: int = 3):
        super().__init__((255, 0, 0), 0, pos, config.block_size)
        self.hits_required = hits_required
        self.max_hits = hits_required
        self.alive = hits_required > 0
        self.update_color()

    def update_color(self):
        if self.hits_required == 3:
            self.color = (255, 0, 0)
        elif self.hits_required == 2:
            self.color = (255, 165, 0)
        elif self.hits_required == 1:
            self.color = (255, 255, 0)

    def draw(self, surface) -> None:
        if self.hits_required > 0:
            pygame.draw.rect(surface, self.color, self.rect)

    def collide(self):
        if self.hits_required > 0:
            self.hits_required -= 1
            self.update_color()
            if self.hits_required == 0:
                self.alive = False

class GrayBlock(Block):
    def __init__(self, pos: tuple = (0, 0)):
        super().__init__(pos, hits_required=float('inf'))
        self.color = (128, 128, 128)

    def collide(self):
        pass

class Paddle(Basic):
    def __init__(self):
        super().__init__(config.paddle_color, 0, config.paddle_pos, config.paddle_size)
        self.start_pos = config.paddle_pos
        self.speed = config.paddle_speed
        self.cur_size = config.paddle_size

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def move_paddle(self, event: pygame.event.Event):
        if event.key == K_LEFT and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)
        elif event.key == K_RIGHT and self.rect.right < config.display_dimension[0]:
            self.rect.move_ip(self.speed, 0)

class Ball(Basic):
    def __init__(self, pos: tuple = config.ball_pos):
        super().__init__(config.ball_color, config.ball_speed, pos, config.ball_size)
        self.power = 1
        self.dir = 90 + random.randint(-45, 45)

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

    def collide_paddle(self, paddle: Paddle):
        if self.rect.colliderect(paddle.rect):
            self.dir = 360 - self.dir + random.randint(-5, 5)

    def hit_wall(self):
        if self.rect.left <= 0 or self.rect.right >= config.display_dimension[0]:
            self.dir = 180 - self.dir
        if self.rect.top <= 0:
            self.dir = 360 - self.dir

    def alive(self):
        return self.rect.bottom <= 800

class Item(Basic):
    def __init__(self, color: tuple, pos: tuple):
        super().__init__(color, config.display_dimension[1] // 100, pos, config.item_size)

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

    def move(self):
        self.rect.move_ip(0, self.speed)
