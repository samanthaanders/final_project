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
#text_rect = text.get_rect()

screen = pygame.display.set_mode((1000,600), pygame.RESIZABLE)
pygame.display.set_caption("game!")
white = (255,255,255)

NEW_BATTLE = pygame.USEREVENT + 1 ## maybe unnecessary
pygame.time.set_timer(NEW_BATTLE, 1)


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
        self.text = font.render(" ", True, (255,255,255), (0,0,0)) ###3
        #self.text2 = font.render(" ", True, (255,255,255), (0,0,0))
        self.health_message = self.name + "r health is: " + str(self.health)
    def take_damage(self, num, damage, name):
        name = str(name)
        message = name + " attacked!"
        text = font.render(message, True, (0,0,0), (150, 171, 255))
        screen.blit(text,(100,70))
        pygame.display.update()
        if (self.num == num):
            self.health -= damage
            text = font.render(("the attack was very strong!"), True, (0,0,0), (150, 171, 255))
            screen.blit(text,(100,200))
            pygame.display.update()
        elif ((self.num - num == 1) or (self.num - num == -1)): # if the numbers are within 1 of eachother, 1/2 damage is dealt
            self.health -= damage / 2
            text = font.render(("the attack was strong"), True, (0,0,0), (150, 171, 255))
            screen.blit(text,(100,200))
            pygame.display.update()
        elif ((self.num - num == 2) or (self.num - num == -2)): # if the numbers are within 2 of eachother, 1/4 damage is dealt
            self.health -= damage / 4
            text = font.render(("the attack was weak"), True, (0,0,0), (150, 171, 255))
            screen.blit(text,(100,200))
            pygame.display.update()
        else:
            text = font.render(("the attack failed!"), True, (0,0,0), (150, 171, 255))
            screen.blit(text,(100,200))
    def check_health(self):
        if (self.health <= 0):
            message = self.name + " lost!"
            text = font.render(message, True, (0,0,0),(150, 171, 255))
            screen.blit(text,(100,100))
            pygame.display.update()
        else:
            message = self.name + "r health is: " + str(self.health) + "  "
            text = font.render(message, True, (0,0,0),(150, 171, 255))
            screen.blit(text,(100,100))
            pygame.display.update()
            #self.text2 = font.render(message, True, (150, 171, 255),(150, 171, 255))
            #screen.blit(self.text2,(100,100))
    def use_power(self, uses, amount):
        if (self.power == "strength potion"):
            if uses > 0:
                self.strength += amount
                ###print(self.name +"'s strength:", self.strength) ###
                ###print(self.power +" uses left: ",(uses - 1)) ###
            else:
                print(self.power + " has been used up") ###
        elif (self.power == "health potion"):
            if uses > 0:
                self.health += amount
                ###print(self.name +"'s health:", self.health) ###
                ###print(self.power +" uses left: ",(uses - 1)) ###
            else:
                print(self.power + " has been used up") ###
        elif (self.power == "cookie"):
            if uses > 0:
                self.health += amount
                print(self.name +"'s health:", self.health) ###
                print(self.power +" uses left: ",(uses - 1)) ###
            else:
                print(self.power + " has been used up") ###
        elif (self.power == "sword"):
            if uses > 0:
                self.strength += amount
                print(self.name +"'s strength:", self.strength) ###
                print(self.power +" uses left: ",(uses - 1)) ###
            else:
                print(self.power + " has already been equipped") ###
        elif (self.power == "health spell"):
            if uses > 0:
                self.health += amount
                print(self.name +"'s health:", self.health) ###
                print(self.power +" uses left: ",(uses - 1)) ###
            else:
                print(self.power + " has been used up") ###
        elif (self.power == "luck potion"):
            if uses > 0:
                amount = self.obj_item.rand_amount() # composition to use method of "special_item" class
                self.health += amount
                print(self.name +"'s health:", self.health) ###
                print(self.power +" uses left: ",(uses - 1)) ###
            else:
                print(self.power + " has been used up") ###
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
    def update_text(self):
        text = font.render(("the attack was very strong!"), True, (150, 171, 255), (150, 171, 255))
        screen.blit(text,(100,200))
        text = font.render(("small forest monster's heath is: 10  "), True, (150, 171, 255), (150, 171, 255))
        screen.blit(text,(100,100))


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
        self.sprite.fill((0,0,0))
        self.hitbox = self.sprite.get_rect() # hitbox = rect

    def take_damage(self, num, damage, name):
        message = str(name) + " attacked!"
        text = font.render(message, True, (0,0,0), (150, 171, 255))
        screen.blit(text,(100,70))
        pygame.display.update()
        if (self.num == num):
            self.health -= damage
            text = font.render("the attack was very strong!", True, (0,0,0), (150, 171, 255))
            screen.blit(text,(100,200))
            pygame.display.update()
            ###print("the attack was very strong!") ###
        elif ((self.num - num == 1) or (self.num - num == -1)):
            self.health -= damage / 2
            text = font.render("the attack was strong", True, (0,0,0), (150, 171, 255))
            screen.blit(text,(100,200))
            pygame.display.update()
            ###print("the attack was strong") ###
        elif ((self.num - num == 2) or (self.num - num == 2)):
            self.health -= damage / 4
            text = font.render("the attack was weak", True, (0,0,0), (150, 171, 255))
            screen.blit(text,(100,200))
            pygame.display.update()
            ###print("the attack was weak") ###
        else:
            text = font.render("the attack failed!", True, (0,0,0), (150, 171, 255))
            screen.blit(text,(100,200))
            pygame.display.update()
            ###print("the attack failed!") ##
   
    def check_health(self):
        if (self.health <= 0):
            message = self.name +  " lost!"
            text = font.render(message, True, (0,0,0),(150, 171, 255))
            screen.blit(text,(100,100))
            pygame.display.update()
            ###print(self.name,"lost!") ###
        else:
            message = self.name + "'s health is: " + str(self.health) + " "
            text = font.render(message, True, (0,0,0),(150, 171, 255))
            screen.blit(text,(100,100))
            pygame.display.update()
            ###print(self.name + "'s health is: ", self.health) ###

    def attack(self):
        return self.agg_player.attack() # aggregation to reuse the player class's attack method
    
    def update_text(self):
        return self.agg_player.update_text()

#screen.fill(white)
#pygame.display.flip()

p1 = player("you", 5, 10, random.randint(1,4),0, None)
p1_power = None #is this necessasry??

# enemy names are randomized from this list 
enemy_names = ["cave", "forest", "tree", "water", "fire"]

#create objects
strength_potion = item("strength potion", 15, 3, "increases strength by 5. Can be used 3 times.", 5)
health_potion = item("health potion", 20, 5, "increases health by 5. Can be used 5 times.", 5)
cookie = item("cookie", 2, 1, "increases health by 3. Can be used once.", 3)
sword = item("sword", 8, 1, "increases strength by 5. Can be used once.", 5)
health_spell = item("health spell", 50, 10, "increases health by 7. Can be used 10 times.", 7)
luck_potion = special_item("luck potion", 30, 10, "increases health by a random amount between 1-10. Can be used 10 times.", 1)

e1 = enemy("small " + enemy_names[(random.randint(0,4))] + " monster", 3, 5, 5, (random.randint(1,4)), 3, 1, p1)
e2 = enemy(enemy_names[(random.randint(0,4))] + " monster", 5, 5, 5, (random.randint(1,4)), 9, 3, p1)
e3 = enemy(enemy_names[(random.randint(0,4))] + " monster", 5, 10, 10, (random.randint(1,4)), 15, 5, p1)
boss = enemy("big "+ enemy_names[(random.randint(0,4))] + " monster", 8, 15, 15, (random.randint(1,4)), 30, 10, p1) 

# enemy names are randomized from this list 
enemy_names = ["cave", "forest", "tree", "water", "fire"]

big_font = pygame.font.Font('freesansbold.ttf', 80)
start_text = font.render("Play", True, (0,0,0))
start_text_rect = start_text.get_rect()
start_text_rect.center = (100,100)


# function used for all battles 
def battle(e, power):
    battling = True
    p1.health = 10
    e.health = e.max_health
    while (battling == True):


        print(battling)
        p1.take_damage(e.attack(), e.strength, e.name)
        time.sleep(1.5)

        num = 0
        key_pressed = pygame.key.get_pressed()
        while num <= 100:
            key_pressed = pygame.key.get_pressed()
            screen_width = screen.get_width()
            screen_height = screen.get_height()
            p1.update(key_pressed, screen_width, screen_height)
            screen.fill(white)
            screen.blit(p1.sprite, p1.hitbox) # sprite goes to top left corner
            clock = pygame.time.Clock()
            pygame.display.flip()
            clock.tick(150)
            num += 1

        p1.check_health()
        
        time.sleep(3)
        p1.update_text

        # player loses
        if ((p1.health <= 0)):
            battling = False
            break

        ###ans = input("What do you do? \n") ##

        """""
        ans = ""
        if (ans == p1.power):
            p1.use_power(power.uses, power.amount)
            power.uses -= 1
        elif (ans == "attack"):
            e.take_damage(p1.attack(), (p1.strength), p1.name)
            e.check_health()
        elif (ans == "quit"):
            #print("thanks for playing!")
            quit()
        else:
            print("invalid response! your turn has been skipped.") ###
        """

        screen.fill(white)

        e.take_damage(p1.attack(), (p1.strength), p1.name)
        e.check_health()
        print(e.health)

        time.sleep(3)
        e.update_text()

        if ((e.health <= 0)):
            print("in the loop!")
            battling = False
            #break

        print(battling)

        # player wins
        """""
        if ((e.health == 0) or (e.health < 0)):
            #print("Good job!")
            #p1.money += e.money
            #print("+" , e.money, "coins")
            #print(p1.name,"has", p1.money,"coins")
            #p1.strength += e.reward
            #print("+", e.reward, "strength") 
            #print(p1.name + "'s strength:",p1.strength)
            battling == False
            break
        """

def create_enemies():
    e1 = enemy("small " + enemy_names[(random.randint(0,4))] + " monster", 3, 5, (random.randint(1,4)), 3, 1, p1)
    e2 = enemy(enemy_names[(random.randint(0,4))] + " monster", 5, 5, (random.randint(1,4)), 9, 3, p1)
    e3 = enemy(enemy_names[(random.randint(0,4))] + " monster", 5, 10, (random.randint(1,4)), 15, 5, p1)
    boss = enemy("big "+ enemy_names[(random.randint(0,4))] + " monster", 8, 15, (random.randint(1,4)), 30, 10, p1) 

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
            

    screen.blit(start_text, start_text_rect)

    if  event.type == pygame.MOUSEBUTTONDOWN:
        if start_text_rect.collidepoint(mouse_pos):
            p1.update(key_pressed, screen_width, screen_height)
            screen.blit(p1.sprite, p1.hitbox) # sprite goes to top left corner
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
        #while p1.health >= 0 and e1.health >= 0: 
            #battle(e1, p1.power)

        battle(e1, p1.power)
        playing = False

        p1.update(key_pressed, screen_width, screen_height)
        screen.blit(p1.sprite, p1.hitbox)
        pygame.display.flip()
        clock.tick(150) #150

    pygame.display.flip()
    clock.tick(150) #150
pygame.quit()

"""""
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
    #while p1.health >= 0 and e1.health >= 0: 
        #battle(e1, p1.power)

    battle(e1, p1.power)
    playing = False
    """
"""""
    #clock.tick(5)
    p1.take_damage(e1.attack(), e1.strength, e1.name)
    screen.fill(white)
    #pygame.display.update()
    #clock.tick(5)
    time.sleep(0.5)
    p1.update_text()
    p1.check_health()
    time.sleep(0.5)
    """
"""""
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
    """
"""
    elif event.type == NEW_BATTLE: # this part is not working 
        create_enemies()
        while p1.health >= 0 and e1.health >= 0: 
            clock.tick(5)
            p1.take_damage(e1.num, e1.strength, e1.name)
            clock.tick(5)
            pygame.display.flip()
            p1.check_health()
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
    """
"""""
    p1.update(key_pressed, screen_width, screen_height)
    screen.blit(p1.sprite, p1.hitbox)

    pygame.display.flip()
    clock.tick(150) #150
    """
#pygame.quit()