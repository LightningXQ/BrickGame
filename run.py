import sys
import random
from implements import Basic, Block, GrayBlock, Paddle, Ball, Item
import config

import pygame
from pygame.locals import QUIT, Rect, K_ESCAPE, K_SPACE

pygame.init()
pygame.key.set_repeat(3, 3)
surface = pygame.display.set_mode(config.display_dimension)

fps_clock = pygame.time.Clock()

paddle = Paddle()
ball1 = Ball()
BLOCKS = []
ITEMS = []
BALLS = [ball1]
life = config.life
start = False

def create_blocks():
    for i in range(config.num_blocks[0]):
        for j in range(config.num_blocks[1]):
            x = config.margin[0] + i * (config.block_size[0] + config.spacing[0])
            y = config.margin[1] + config.scoreboard_height + j * (config.block_size[1] + config.spacing[1])

            if random.random() < 0.1:  # 10% 확률로 회색 블록 생성
                block = GrayBlock((x, y))
            else:
                hits_required = random.randint(1, 3)  # 1~3번 충돌해야 깨지는 블록
                block = Block((x, y), hits_required=hits_required)

            BLOCKS.append(block)

def tick():
    global life
    global BLOCKS
    global ITEMS
    global BALLS
    global paddle
    global ball1
    global start
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:  # ESC 키가 눌렸을 때
                pygame.quit()
                sys.exit()
            if event.key == K_SPACE:  # space키가 눌려지만 start 변수가 True로 바뀌며 게임 시작
                start = True
            paddle.move_paddle(event)

    for ball in BALLS:
        if start:
            ball.move()
        else:
            ball.rect.centerx = paddle.rect.centerx
            ball.rect.bottom = paddle.rect.top

        collide_blocks = []
        for block in BLOCKS:
            if ball.rect.colliderect(block.rect):
                collide_blocks.append(block)
        
        for block in collide_blocks:
            if abs(ball.rect.bottom - block.rect.top) < abs(ball.speed) or abs(ball.rect.top - block.rect.bottom) < abs(ball.speed):
                ball.dir = 360 - ball.dir  # 위/아래 반사
            elif abs(ball.rect.right - block.rect.left) < abs(ball.speed) or abs(ball.rect.left - block.rect.right) < abs(ball.speed):
                ball.dir = 180 - ball.dir  # 좌/우 반사

            block.collide()

            if isinstance(block, GrayBlock) and block.hits_required > 0:
                continue

            if not block.alive:
                BLOCKS.remove(block)

            if random.random() < 0.2:
                color = (255, 0, 0) if random.random() < 0.5 else (0, 0, 255)
                item = Item(color, block.rect.center)
                ITEMS.append(item)

        ball.collide_paddle(paddle)
        ball.hit_wall()
        if not ball.alive():
            BALLS.remove(ball)
    
    for item in ITEMS[:]:
        item.move()
        if paddle.rect.colliderect(item.rect):
            ITEMS.remove(item)
        elif item.rect.top > config.display_dimension[1]:
            ITEMS.remove(item)

def main():
    global life
    global BLOCKS
    global ITEMS
    global BALLS
    global paddle
    global ball1
    global start
    my_font = pygame.font.SysFont(None, 50)
    mess_clear = my_font.render("Cleared!", True, config.colors[2])
    mess_over = my_font.render("Game Over!", True, config.colors[2])
    create_blocks()

    while True:
        tick()
        surface.fill((0, 0, 0))
        paddle.draw(surface)

        for block in BLOCKS:
            block.draw(surface)
        
        for item in ITEMS:
            item.draw(surface)

        cur_score = config.num_blocks[0] * config.num_blocks[1] - len(BLOCKS)

        score_txt = my_font.render(f"Score : {cur_score * 10}", True, config.colors[2])
        life_font = my_font.render(f"Life: {life}", True, config.colors[0])

        surface.blit(score_txt, config.score_pos)
        surface.blit(life_font, config.life_pos)

        if len(BALLS) == 0:
            if life > 1:
                life -= 1
                ball1 = Ball()
                BALLS = [ball1]
                start = False
            else:
                surface.blit(mess_over, (200, 300))
        elif all(isinstance(block, GrayBlock) or not block.alive for block in BLOCKS):
            surface.blit(mess_clear, (200, 400))
        else:
            for ball in BALLS:
                if start:
                    ball.move()
                ball.draw(surface)
            for block in BLOCKS:
                block.draw(surface)


        pygame.display.update()
        fps_clock.tick(config.fps)

if __name__ == "__main__":
    main()
