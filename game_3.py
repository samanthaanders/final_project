import pygame
import random
import time
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

font = pygame.font.Font('freesansbold.ttf', 32)

screen = pygame.display.set_mode((1000,600), pygame.RESIZABLE)
pygame.display.set_caption("game!")
white = (255,255,255)

NEW_BATTLE = pygame.USEREVENT + 1 
pygame.time.set_timer(NEW_BATTLE, 1)

class player(pygame.sprite.Sprite):
    def __init__(self, name, strength, health, num, money, power):
        super(player, self).__init__()
        self.name = name
        self.strength = strength
        self.health = health
        self.num = num # used for randomizing damage dealt in attacks
        self.money = money
        self.power = power
        self.sprite = pygame.Surface((50, 50)) # create character sprite
        self.sprite.fill((0,0,0))
        self.hitbox = self.sprite.get_rect() 
        self.hitbox.center = ((screen.get_width() / 4), (screen.get_height() / 2))
        self.new_health = 0 
    def take_damage(self, num, damage, name, screen_width):
        name = str(name)
        message = name + " attacked!"
        text = font.render(message, True, (0,0,0), (150, 171, 255))
        screen.blit(text,(((screen_width / 2) - (text.get_width() / 2)),50))
        pygame.display.update()
        if (self.num == num):
            self.new_health = (self.health - damage)
            text = font.render(("the attack was very strong!"), True, (0,0,0), (150, 171, 255))
            screen.blit(text,(((screen_width / 2) - (text.get_width() / 2)),80))
            pygame.display.update()
        elif ((self.num - num == 1) or (self.num - num == -1)): # if the numbers are within 1 of eachother, 1/2 damage is dealt
            self.new_health = (self.health - (damage / 2))
            text = font.render(("the attack was strong"), True, (0,0,0), (150, 171, 255))
            screen.blit(text,(((screen_width / 2) - (text.get_width() / 2)),80))
            pygame.display.update()
        elif ((self.num - num == 2) or (self.num - num == -2)): # if the numbers are within 2 of eachother, 1/4 damage is dealt
            self.new_health = (self.health - (damage / 4))
            text = font.render(("the attack was weak"), True, (0,0,0), (150, 171, 255))
            screen.blit(text,(((screen_width / 2) - (text.get_width() / 2)),80))
            pygame.display.update()
        else:
            self.new_health = (self.health - (damage / 8))
            text = font.render(("the attack was very weak"), True, (0,0,0), (150, 171, 255))
            screen.blit(text,(((screen_width / 2) - (text.get_width() / 2)),80))
            pygame.display.update()
    def check_health(self):
        if (self.health <= 0):
            message = self.name + " lost!"
            text = font.render(message, True, (0,0,0),(150, 171, 255))
            screen.blit(text,(((screen_width / 2) - (text.get_width() / 2)),500))
            pygame.display.update()
        else:
            message = self.name + "r health is: " + str(self.health) + "  "
            text = font.render(message, True, (0,0,0),(150, 171, 255))
            screen.blit(text,(((screen_width / 2) - (text.get_width() / 2)),500))
            pygame.display.update()
    def attack(self):
        return random.randint(1,4)
    def update(self, key_pressed, screen_width, screen_height):
        if key_pressed[K_UP]:
            self.hitbox.move_ip(0, -5)
        if key_pressed[K_DOWN]:
            self.hitbox.move_ip(0, 5)
        if key_pressed[K_LEFT]:
            self.hitbox.move_ip(-5, 0)
        if key_pressed[K_RIGHT]:
            self.hitbox.move_ip(5, 0)

        if self.hitbox.left < 0:
            self.hitbox.left = 0
        if self.hitbox.right > (screen_width / 3):
            self.hitbox.right = (screen_width / 3)
        if self.hitbox.top <= 0:
            self.hitbox.top = 0
        if self.hitbox.bottom >= screen_height:
            self.hitbox.bottom = screen_height

class enemy(pygame.sprite.Sprite):
    def __init__(self, name, strength, health, max_health, num, money, reward, player):
        super(enemy, self).__init__()
        self.name = name
        self.strength = strength
        self.health = health
        self.max_health = max_health
        self.num = num
        self.money = money
        self.reward = reward
        self.agg_player = player
        self.sprite = pygame.Surface((50, 50)) # create character sprite
        self.sprite.fill((255,0,0))
        self.hitbox = self.sprite.get_rect() 
        self.hitbox.center = (((screen.get_width() / 4)* 3), (screen.get_height() / 2))
    def take_damage(self, num, damage, name, screen_width):
        message = str(name) + " attacked!"
        text = font.render(message, True, (0,0,0), (150, 171, 255))
        screen.blit(text,(((screen_width / 2) - (text.get_width() / 2)),50))
        pygame.display.update()
        if (self.num == num):
            self.health -= damage
            text = font.render("the attack was very strong!", True, (0,0,0), (150, 171, 255))
            screen.blit(text,(((screen_width / 2) - (text.get_width() / 2)),80))
            pygame.display.update()
        elif ((self.num - num == 1) or (self.num - num == -1)):
            self.health -= damage / 2
            text = font.render("the attack was strong", True, (0,0,0), (150, 171, 255))
            screen.blit(text,(((screen_width / 2) - (text.get_width() / 2)),80))
            pygame.display.update()
        elif ((self.num - num == 2) or (self.num - num == 2)):
            self.health -= damage / 4
            text = font.render("the attack was weak", True, (0,0,0), (150, 171, 255))
            screen.blit(text,(((screen_width / 2) - (text.get_width() / 2)),80))
            pygame.display.update()
        else:
            self.health -= damage / 8
            text = font.render("the attack was very weak!", True, (0,0,0), (150, 171, 255))
            screen.blit(text,(((screen_width / 2) - (text.get_width() / 2)),80))
            pygame.display.update()
    def check_health(self):
        if (self.health <= 0):
            message = self.name +  " lost!"
            text = font.render(message, True, (0,0,0),(150, 171, 255))
            screen.blit(text,(((screen_width / 2) - (text.get_width() / 2)),500))
            pygame.display.update()
        else:
            message = self.name + "'s health is: " + str(self.health) + " "
            text = font.render(message, True, (0,0,0),(150, 171, 255))
            screen.blit(text,(((screen_width / 2) - (text.get_width() / 2)),500))
            pygame.display.update()
    def attack(self):
        return self.agg_player.attack() # aggregation to reuse the player class's attack method
    
class attacks(pygame.sprite.Sprite):
    def __init__(self, colour):
        super(attacks, self).__init__()
        self.colour = colour
        self.sprite = pygame.Surface((50, 50))
        self.sprite.fill((colour))
        self.hitbox = self.sprite.get_rect()
    def attack(self, character, direction):
        if direction == ("left"):
            self.hitbox.move_ip(-5, 0)
        else:
            self.hitbox.move_ip(5, 0)

p1 = player("you", 5, 10, random.randint(1,4),0, None)

# enemy names are randomized from this list 
enemy_names = ["cave", "forest", "tree", "water", "fire"]

e1 = enemy(enemy_names[(random.randint(0,4))] + " monster", 5, 10, 10, (random.randint(1,4)), 3, 1, p1)
 
# sprite group stores all enemy attack sprites
enemy_attacks = pygame.sprite.Group() 
e_attack = attacks((255,0,0))
e_attack2 = attacks((255,0,0))
e_attack3 = attacks((255,0,0))
e_attack4 = attacks((255,0,0))
e_attack5 = attacks((255,0,0))
enemy_attacks.add(e_attack, e_attack2, e_attack3, e_attack4, e_attack5)

player_attack = attacks((0,0,0))

# creates play button
big_font = pygame.font.Font('freesansbold.ttf', 80)
start_text = font.render("Play", True, (0,0,0))
start_text_rect = start_text.get_rect()


# function used for all battles 
def battle(e, power):
    battling = True
    p1.health = 10
    e.health = e.max_health
    p1.hitbox.center = ((screen.get_width() / 4), (screen.get_height() / 2))
    e.hitbox.center = (((screen.get_width() / 4)* 3), (screen.get_height() / 2))
    while (battling == True):

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    battling = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        battling = False

        screen.blit(p1.sprite, p1.hitbox)
        screen.blit(e.sprite, e.hitbox)

        screen_width = screen.get_width()

        p1.num = (random.randint(1,4))
        p1.take_damage(e.attack(), e.strength, e.name, screen_width)
        time.sleep(1.5)

        # lets player move and creates the enemy attacks
        num = 0
        key_pressed = pygame.key.get_pressed()
        for entity in enemy_attacks:
            entity.hitbox.center = ((e.hitbox.left), (random.randint(0,(screen.get_height() - e.hitbox.height))))    
        for entity in enemy_attacks:
            entity.sprite.fill(entity.colour)
        while num <= 300:
            key_pressed = pygame.key.get_pressed()
            screen_width = screen.get_width()
            screen_height = screen.get_height()
            p1.update(key_pressed, screen_width, screen_height)
            screen.fill(white)
            for entity in enemy_attacks:
                screen.blit(entity.sprite, entity.hitbox)
            screen.blit(p1.sprite, p1.hitbox)
            screen.blit(e.sprite, e.hitbox)
            for entity in enemy_attacks:
                entity.attack(e, "left")
            clock = pygame.time.Clock()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    battling = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        battling = False
            for entity in enemy_attacks:
                if entity.hitbox.collidepoint(p1.hitbox.center):
                    entity.sprite.fill((255, 255, 255))
                    p1.health = p1.new_health
                    break
            pygame.display.flip()
            clock.tick(150)
            num += 1

        screen.blit(p1.sprite, p1.hitbox)
        p1.check_health()
        
        time.sleep(3)

        # player loses
        if ((p1.health <= 0)):
            battling = False
            break

        screen.fill(white)

        screen.blit(p1.sprite, p1.hitbox)
        screen.blit(e.sprite, e.hitbox)

        e.num = (random.randint(1,4))
        e.take_damage(p1.attack(), (p1.strength), p1.name, screen_width)

        time.sleep(1.5)

        # player attacks
        num = 0
        player_attack.hitbox.center = ((p1.hitbox.right), ((screen.get_height() / 2)))
        player_attack.sprite.fill(player_attack.colour)
        while num <= 300:
            screen.fill(white)
            screen.blit(p1.sprite, p1.hitbox)
            screen.blit(e.sprite, e.hitbox)
            screen.blit(player_attack.sprite, player_attack.hitbox)
            player_attack.attack(p1, "right")
            clock = pygame.time.Clock()
            if player_attack.hitbox.collidepoint(e.hitbox.center):
                player_attack.sprite.fill((255, 255, 255))
            pygame.display.flip()
            clock.tick(150)
            num += 1

        e.check_health()

        # enemy loses
        if ((e.health <= 0)):
            battling = False

        time.sleep(3)
        screen.fill(white)


# start screen
running = True
playing = False
while running == True:
    key_pressed = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    screen.fill(white)
    clock = pygame.time.Clock()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            

    start_text_rect.center = ((screen.get_width() / 2),(screen.get_height() / 2))
    screen.blit(start_text, start_text_rect)

    if event.type == pygame.MOUSEBUTTONDOWN:
        if start_text_rect.collidepoint(mouse_pos):
            p1.update(key_pressed, screen_width, screen_height)
            screen.blit(p1.sprite, p1.hitbox) 
            playing = True

    # game loop
    while playing == True:

        key_pressed = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        screen.fill(white)
        clock = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    playing = False

        battle(e1, p1.power)
        playing = False

        p1.update(key_pressed, screen_width, screen_height)
        screen.blit(p1.sprite, p1.hitbox)
        pygame.display.flip()
        clock.tick(150) 

    pygame.display.flip()
    clock.tick(150) 
pygame.quit()