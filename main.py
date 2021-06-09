import pygame
import sys
from random import randrange


WIDTH, HEIGHT = 400, 700
FPS = 120
floor_height = int((112 * WIDTH) / 336)
scaled_height = int(WIDTH / 336)
scaled_width = int(WIDTH / 336)
gravity = 0.15
bird_movement = 0
jump_height = 4

# -550 lowest
# -700 Middle
# -850 highest


def ypos(oldvalue):
    oldmin = 0
    oldmax = 100
    newmin = 380
    newmax = 80
    return ((((oldvalue - oldmin) * (newmax - newmin)) / (oldmax - oldmin)) + newmin) * -1


pygame.init()
pygame.display.set_caption("Flappy Bird")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Background
bg_surface = pygame.image.load('sprites/background-day.png').convert()
bg_surface = pygame.transform.scale(bg_surface, (WIDTH, HEIGHT))

# Floor
floor_x_pos = 0
floor_surface = pygame.image.load('sprites/base.png').convert()
floor_surface = pygame.transform.scale(floor_surface, (WIDTH, floor_height))
floor_rect = floor_surface.get_rect(
    midleft=(floor_x_pos, (HEIGHT-floor_height+(int(floor_surface.get_height())/2))))
floor_rect2 = floor_surface.get_rect(
    midleft=(floor_x_pos+WIDTH, (HEIGHT-floor_height+(int(floor_surface.get_height())/2))))

# Bird
bird_surface = pygame.image.load('sprites/yellowbird-midflap.png').convert()
bird_surface = pygame.transform.scale(bird_surface, (44, 31))
bird_rect = bird_surface.get_rect(
    center=(WIDTH / 5, (HEIGHT - floor_height) / 2))


# First Pipe
pipe_y_pos1 = randrange(100)
pipe_x_pos1 = WIDTH
top_pipe_surface1 = pygame.image.load('sprites/pipe-green.png').convert()
top_pipe_surface1 = pygame.transform.rotate(top_pipe_surface1, 180)
top_pipe_surface1_rect = top_pipe_surface1.get_rect(
    center=((pipe_x_pos1, ypos(pipe_y_pos1))))
offset = 1060

bottom_pipe_surface1 = pygame.image.load('sprites/pipe-green.png').convert()
bottom_pipe_surface1_rect = bottom_pipe_surface1.get_rect(
    center=((pipe_x_pos1, ypos(pipe_y_pos1)+offset)))
pipe_height = int(top_pipe_surface1.get_height())
pipe_width = int(top_pipe_surface1.get_width())

# Second Pipe
pipe_y_pos2 = randrange(100)
pipe_x_pos2 = WIDTH + (WIDTH/2)+(pipe_width/2)

offset2 = 150
top_pipe_surface2 = pygame.image.load('sprites/pipe-green.png').convert()
top_pipe_surface2 = pygame.transform.rotate(top_pipe_surface2, 180)
top_pipe_surface2_rect = top_pipe_surface2.get_rect(
    center=((pipe_x_pos2, ypos(pipe_y_pos2))))

bottom_pipe_surface2 = pygame.image.load('sprites/pipe-green.png').convert()
bottom_pipe_surface2_rect = bottom_pipe_surface2.get_rect(
    center=((pipe_x_pos2, ypos(pipe_y_pos2)+offset)))


def draw_floor():
    screen.blit(floor_surface, floor_rect)
    screen.blit(floor_surface, floor_rect2)


def draw_pipes1():
    screen.blit(top_pipe_surface1, top_pipe_surface1_rect)
    screen.blit(bottom_pipe_surface1, bottom_pipe_surface1_rect)


def draw_pipes2():

    screen.blit(top_pipe_surface2, top_pipe_surface2_rect)
    screen.blit(bottom_pipe_surface2, bottom_pipe_surface2_rect)


running = True
while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                clicked = True
                bird_movement = 0
                bird_movement -= jump_height

    # Bird
    screen.blit(bg_surface, (0, 0))

    bird_movement += gravity
    bird_rect.centery += bird_movement

    screen.blit(bird_surface, bird_rect)

    # Pipe 1
    top_pipe_surface1_rect = top_pipe_surface1.get_rect(
        center=((pipe_x_pos1, ypos(pipe_y_pos1))))
    bottom_pipe_surface1_rect = bottom_pipe_surface1.get_rect(
        center=((pipe_x_pos1, ypos(pipe_y_pos1)+offset)))
    pipe_x_pos1 -= 1
    draw_pipes1()
    if pipe_x_pos1 <= 0-(pipe_width/2):
        pipe_x_pos1 = WIDTH+(pipe_width/2)
        pipe_y_pos1 = randrange(100)

    # Pipe 2
    top_pipe_surface2_rect = top_pipe_surface2.get_rect(
        center=((pipe_x_pos2, ypos(pipe_y_pos2))))
    bottom_pipe_surface2_rect = bottom_pipe_surface2.get_rect(
        center=((pipe_x_pos2, ypos(pipe_y_pos2)+offset)))
    pipe_x_pos2 -= 1
    draw_pipes2()
    if pipe_x_pos2 <= 0-(pipe_width/2):
        pipe_x_pos2 = WIDTH+(pipe_width/2)
        pipe_y_pos2 = randrange(100)

    # Floor
    floor_rect = floor_surface.get_rect(midleft=(
        floor_x_pos, (HEIGHT-floor_height+(int(floor_surface.get_height())/2))))
    floor_rect2 = floor_surface.get_rect(midleft=(
        floor_x_pos+WIDTH, (HEIGHT-floor_height+(int(floor_surface.get_height())/2))))
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -WIDTH:
        floor_x_pos = 0

    pipes = [top_pipe_surface1_rect, bottom_pipe_surface1_rect,
             top_pipe_surface2_rect, bottom_pipe_surface2_rect, floor_rect, floor_rect2]

    for pipe in pipes:
        if pygame.Rect.colliderect(bird_rect, pipe) == True:
            running = False

    pygame.display.update()
    clock.tick(FPS)
