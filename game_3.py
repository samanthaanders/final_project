import pygame

screen = pygame.display.set_mode((1000,600), pygame.RESIZABLE)
pygame.display.set_caption("game")
white = (255,255,255)
screen.fill(white)
pygame.display.flip()

running = True
while running == True:
    screen.fill(white)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()