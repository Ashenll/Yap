import pygame
from pygame.draw import *
from random import randint,choice


pygame.init()

FPS = 30
WIDTH, HEIGHT = 1200,900
screen = pygame.display.set_mode((WIDTH,HEIGHT))


RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
GREEN = (0,255,0)
MAGENTA = (255,0,255)
CYAN = (0,255,255)
BLACK = (0,0,0)
COLORS = [RED,BLUE,YELLOW,GREEN,MAGENTA,CYAN]


NUM_BALLS = 5
balls = []

font = pygame.font.SysFont('arial', 30)


score = 0

def new_ball():

    x = randint(100,1100)
    y = randint(100,900)
    r = randint(10,100)
    color = choice(COLORS)
    dx,dy = randint(-5,5),randint(-5,5)
    return [x,y,r,color,dx,dy]

def draw_ball(ball):

    circle(screen,ball[3],(ball[0],ball[1]),ball[2])

def move_ball(ball):

    ball[0] += ball[4]
    ball[1] += ball[5]
    if ball[0] - ball[2] < 0 or ball[0] + ball[2] > WIDTH:
        ball[4] = -ball[4]
    if ball[1] - ball[2] < 0 or ball[1] + ball[2] > HEIGHT:
        ball[5] = -ball[5]

def check_click(event,ball):
    distance = ((event.pos[0] - ball[0])*2 + (event.pos[1] - ball[1])*2)**0.5
    return distance < ball[2]

text_pos = (10, 10)


for _ in range(NUM_BALLS):
    balls.append(new_ball())

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for ball in balls:
                if check_click(event,ball):
                    score += 1
                    print(f"Score: {score}")
                    balls.remove(ball)
                    balls.append(new_ball())

    screen.fill(BLACK)
    for ball in balls:
        draw_ball(ball)
        move_ball(ball)

    show_score = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(show_score, text_pos)
    pygame.display.update()
    pygame.display.update()



pygame.quit()
