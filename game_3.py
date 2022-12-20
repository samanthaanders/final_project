import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
pygame.init()

screen = pygame.display.set_mode((1000,600), pygame.RESIZABLE)
pygame.display.set_caption("game")
white = (255,255,255)
screen.fill(white)
p1_sprite = surf = pygame.Surface((50, 50))
p1_sprite.fill((0,0,0))
pygame.display.flip()

running = True
while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
    screen.fill(white)
    p1_sprite_center = (((screen.get_width() - p1_sprite.get_width()) / 2), (screen.get_height() - p1_sprite.get_height()) / 2)
    screen.blit(p1_sprite, p1_sprite_center)
    pygame.display.flip()

pygame.quit()