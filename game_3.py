import pygame
import random
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

class item:
    def __init__(self, name, cost, uses, desc, amount):
        self.name = name
        self.cost = cost
        self.uses = uses
        self.desc = desc
        self.amount = amount

class special_item(item): # inheritance 
    def __init__(self, name, cost, uses, desc, amount):
        super().__init__(name, cost, uses, desc, amount)
    def rand_amount(self):
        self.amount = random.randint(1,10)
        return self.amount

class player(pygame.sprite.Sprite):
    def __init__(self, name, strength, health, num, money, power):
        super(player, self).__init__()
        self.name = name
        self.strength = strength
        self.health = health
        self.num = num # used for randomizing damage dealt in attacks
        self.money = money
        self.power = power
        self.obj_item = special_item(None, 0, 0, None, 1) # composition
        self.sprite = pygame.Surface((50, 50)) # create character sprite
        self.sprite.fill((0,0,0))
        self.hitbox = self.sprite.get_rect() # hitbox = rect
    def take_damage(self, num, damage, name):
        print(name, "attacked!")
        if (self.num == num):
            self.health -= damage
            print("the attack was very strong!")
        elif ((self.num - num == 1) or (self.num - num == -1)): # if the numbers are within 1 of eachother, 1/2 damage is dealt
            self.health -= damage / 2
            print("the attack was strong")
        elif ((self.num - num == 2) or (self.num - num == -2)): # if the numbers are within 2 of eachother, 1/4 damage is dealt
            self.health -= damage / 4
            print("the attack was weak")
        else:
            print("the attack failed!")
    def check_health(self):
        if (self.health <= 0):
            print(self.name,"lost!")
        else:
            print(self.name + "'s health is: ", self.health)
    def use_power(self, uses, amount):
        if (self.power == "strength potion"):
            if uses > 0:
                self.strength += amount
                print(self.name +"'s strength:", self.strength)
                print(self.power +" uses left: ",(uses - 1))
            else:
                print(self.power + " has been used up")
        elif (self.power == "health potion"):
            if uses > 0:
                self.health += amount
                print(self.name +"'s health:", self.health)
                print(self.power +" uses left: ",(uses - 1))
            else:
                print(self.power + " has been used up")
        elif (self.power == "cookie"):
            if uses > 0:
                self.health += amount
                print(self.name +"'s health:", self.health)
                print(self.power +" uses left: ",(uses - 1))
            else:
                print(self.power + " has been used up")
        elif (self.power == "sword"):
            if uses > 0:
                self.strength += amount
                print(self.name +"'s strength:", self.strength)
                print(self.power +" uses left: ",(uses - 1))
            else:
                print(self.power + " has already been equipped")
        elif (self.power == "health spell"):
            if uses > 0:
                self.health += amount
                print(self.name +"'s health:", self.health)
                print(self.power +" uses left: ",(uses - 1))
            else:
                print(self.power + " has been used up")
        elif (self.power == "luck potion"):
            if uses > 0:
                amount = self.obj_item.rand_amount() # composition to use method of "special_item" class
                self.health += amount
                print(self.name +"'s health:", self.health)
                print(self.power +" uses left: ",(uses - 1))
            else:
                print(self.power + " has been used up")
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
        if self.hitbox.right > screen_width:
            self.hitbox.right = screen_width
        if self.hitbox.top <= 0:
            self.hitbox.top = 0
        if self.hitbox.bottom >= screen_height:
            self.hitbox.bottom = screen_height


screen = pygame.display.set_mode((1000,600), pygame.RESIZABLE)
pygame.display.set_caption("game!")
white = (255,255,255)
screen.fill(white)
pygame.display.flip()

p1 = player("name", 5, 10, random.randint(1,4),0, None)


running = True
while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
    
    key_pressed = pygame.key.get_pressed()
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    p1.update(key_pressed, screen_width, screen_height)
    screen.fill(white)
    screen.blit(p1.sprite, p1.hitbox) # sprite goes to top left corner
    pygame.display.flip()

pygame.quit()