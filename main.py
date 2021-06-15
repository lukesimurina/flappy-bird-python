import pygame
import sys
import time
from random import randrange

def ypos(oldvalue):
    oldmin = 0
    oldmax = 100
    newmin = 380
    newmax = 80
    return ((((oldvalue - oldmin) * (newmax - newmin)) / (oldmax - oldmin)) + newmin) * -1

def game():
    WIDTH, HEIGHT = 400, 700
    FPS = 120
    floor_height = int((112 * WIDTH) / 336)
    scaled_height = int(WIDTH / 336)
    scaled_width = int(WIDTH / 336)
    gravity = 0
    bird_movement = 0 
    jump_height = 4
    clicked = False
    score = 0

    pygame.init()

    # SOUNDS
    flap = pygame.mixer.Sound("audio/wing.wav")
    flap.set_volume(0.1)
    hit = pygame.mixer.Sound("audio/hit.wav")
    hit.set_volume(0.1)

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
    floor_rect = floor_surface.get_rect(midleft=(floor_x_pos, (HEIGHT-floor_height+(int(floor_surface.get_height())/2))))
    floor_rect2 = floor_surface.get_rect(midleft=(floor_x_pos+WIDTH, (HEIGHT-floor_height+(int(floor_surface.get_height())/2))))

    # Bird
    bird_surface = pygame.image.load('sprites/yellowbird-midflap.png').convert()
    bird_surface = pygame.transform.scale(bird_surface, (44, 31))
    bird_rect = bird_surface.get_rect(center=(WIDTH / 2, 2*(HEIGHT - floor_height) / 3))

    message_surface = pygame.image.load('sprites/message.png')
    message_surface = pygame.transform.scale(message_surface, (int(message_surface.get_width()*1.4),int(message_surface.get_height()*1.4)))
    message_rect = message_surface.get_rect(center=(WIDTH/2, (HEIGHT/3)+80))

    # First Pipe
    top_pipe_surface1 = pygame.image.load('sprites/pipe-green.png').convert()
    top_pipe_surface1 = pygame.transform.rotate(top_pipe_surface1, 180)

    pipe_height = int(top_pipe_surface1.get_height())
    pipe_width = int(top_pipe_surface1.get_width())

    pipe_y_pos1 = randrange(100)
    pipe_x_pos1 = WIDTH + (pipe_width/2)

    top_pipe_surface1_rect = top_pipe_surface1.get_rect(center=((pipe_x_pos1, ypos(pipe_y_pos1))))
    offset = 1060

    bottom_pipe_surface1 = pygame.image.load('sprites/pipe-green.png').convert()
    bottom_pipe_surface1_rect = bottom_pipe_surface1.get_rect(center=((pipe_x_pos1, ypos(pipe_y_pos1)+offset)))


    # Second Pipe
    pipe_y_pos2 = randrange(100)
    pipe_x_pos2 = WIDTH + (WIDTH/2)+(pipe_width)

    offset2 = 150
    top_pipe_surface2 = pygame.image.load('sprites/pipe-green.png').convert()
    top_pipe_surface2 = pygame.transform.rotate(top_pipe_surface2, 180)
    top_pipe_surface2_rect = top_pipe_surface2.get_rect(center=((pipe_x_pos2, ypos(pipe_y_pos2))))

    bottom_pipe_surface2 = pygame.image.load('sprites/pipe-green.png').convert()
    bottom_pipe_surface2_rect = bottom_pipe_surface2.get_rect(center=((pipe_x_pos2, ypos(pipe_y_pos2)+offset)))


    def draw_floor():
        screen.blit(floor_surface, floor_rect)
        screen.blit(floor_surface, floor_rect2)


    def draw_pipes1():
        screen.blit(top_pipe_surface1, top_pipe_surface1_rect)
        screen.blit(bottom_pipe_surface1, bottom_pipe_surface1_rect)


    def draw_pipes2():

        screen.blit(top_pipe_surface2, top_pipe_surface2_rect)
        screen.blit(bottom_pipe_surface2, bottom_pipe_surface2_rect)

    def reset_game():
            clicked = False
            pipe_y_pos1 = randrange(100)
            pipe_x_pos1 = WIDTH + (pipe_width/2)
            
            top_pipe_surface1_rect = top_pipe_surface1.get_rect(center=((pipe_x_pos1, ypos(pipe_y_pos1))))
            bottom_pipe_surface1_rect = bottom_pipe_surface1.get_rect(center=((pipe_x_pos1, ypos(pipe_y_pos1)+offset)))
            
            draw_pipes1()

            pipe_y_pos2 = randrange(100)
            pipe_x_pos2 = WIDTH + (WIDTH/2)+(pipe_width)
            top_pipe_surface2_rect = top_pipe_surface2.get_rect(center=((pipe_x_pos2, ypos(pipe_y_pos2))))
            bottom_pipe_surface2_rect = bottom_pipe_surface2.get_rect(center=((pipe_x_pos2, ypos(pipe_y_pos2)+offset)))
            
            draw_pipes2()


    running = True
    while running == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gravity = 0.2
                    clicked = True
                    pygame.mixer.Sound.play(flap)
                    pygame.mixer.music.stop()
                    bird_movement = 0
                    bird_movement -= jump_height

        # Bird
        screen.blit(bg_surface, (0, 0))

        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird_surface, bird_rect)
        if clicked == True:
            pipe_x_pos1 -= 1
            pipe_x_pos2 -= 1
            # Pipe 1
            top_pipe_surface1_rect = top_pipe_surface1.get_rect(center=((pipe_x_pos1, ypos(pipe_y_pos1))))
            bottom_pipe_surface1_rect = bottom_pipe_surface1.get_rect(center=((pipe_x_pos1, ypos(pipe_y_pos1)+offset)))
            
            draw_pipes1()
            if pipe_x_pos1 <= 0-(pipe_width/2):
                pipe_x_pos1 = WIDTH+(pipe_width/2)
                pipe_y_pos1 = randrange(100)
            
            # Pipe 2
            top_pipe_surface2_rect = top_pipe_surface2.get_rect(center=((pipe_x_pos2, ypos(pipe_y_pos2))))
            bottom_pipe_surface2_rect = bottom_pipe_surface2.get_rect(center=((pipe_x_pos2, ypos(pipe_y_pos2)+offset)))
            
            draw_pipes2()
            if pipe_x_pos2 <= 0-(pipe_width/2):
                pipe_x_pos2 = WIDTH+(pipe_width/2)
                pipe_y_pos2 = randrange(100)

        if clicked != True:
            screen.blit(message_surface, message_rect)


        # Floor
        floor_rect = floor_surface.get_rect(midleft=(floor_x_pos, (HEIGHT-floor_height+(int(floor_surface.get_height())/2))))
        floor_rect2 = floor_surface.get_rect(midleft=(floor_x_pos+WIDTH, (HEIGHT-floor_height+(int(floor_surface.get_height())/2))))
        floor_x_pos -= 1
        draw_floor()
        if floor_x_pos <= -WIDTH:
            floor_x_pos = 0

        if pipe_x_pos1 == (WIDTH / 2) or pipe_x_pos2 == (WIDTH / 2):
            score += 1

        def digit1(score):
            if score < 10:
                return '0'
            else: return (str(score))[0]
        
        def digit2(score):
            if score < 10:
                return str(score)
            else: return (str(score))[1]

        digit_one = pygame.image.load('sprites/'+digit1(score)+'.png')
        digit_two = pygame.image.load('sprites/'+digit2(score)+'.png')


        score_width = int(digit_one.get_width())
        offset1 = WIDTH/2 - score_width - 2
        offset2 = WIDTH/2 + 2

        screen.blit(digit_one, (offset1, 20))
        screen.blit(digit_two, (offset2, 20))
        pipes = [top_pipe_surface1_rect, bottom_pipe_surface1_rect, top_pipe_surface2_rect, bottom_pipe_surface2_rect, floor_rect, floor_rect2]
        
        for pipe in pipes:
            if pygame.Rect.colliderect(bird_rect, pipe) == True:
                pygame.mixer.Sound.play(hit)
                pygame.mixer.music.stop()
                time.sleep(1)
                game()

        pygame.display.update()
        clock.tick(FPS)

game()