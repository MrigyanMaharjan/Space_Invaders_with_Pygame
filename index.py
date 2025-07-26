import pygame
import random

from random import uniform
width = 1200
height = 700
pygame.init()
pygame

meteor=pygame.image.load("PNG/Meteors/meteorBrown_big2.png")
meteor=pygame.transform.scale(meteor,(100,100))
laser_image=pygame.image.load("PNG/Lasers/laserGreen06.png");
font=pygame.font.Font("Bonus/kenvector_future.ttf")
life=pygame.image.load("PNG/UI/playerLife1_red.png")
life=pygame.transform.scale(life,(30,30))

def displayscore():
    currentscore=pygame.time.get_ticks()//100
    font_surface=font.render(str(currentscore),True,"white")
    font_rect=font_surface.get_frect(midbottom=(width/2,50))
    display_surface.blit(font_surface,font_rect)

def displaylives(lives):
    lives_count="X"+str(lives)
    lives_text=font.render(lives_count,True,"White")
    display_surface.blit(life,(20,15))
    display_surface.blit(lives_text,(60,20))
    if lives<=0:
        pygame.quit()

class Plane(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load("PNG/playerShip2_blue.png").convert_alpha()
        self.rect = self.image.get_frect(center=(600, 600))
        self.speed = 400 
        self.direction = pygame.math.Vector2(0, 0)
        self.canshoot=True
        self.shottime=pygame.time.get_ticks()
        self.shotdelay=400
        self.health=5
        self.mask=pygame.mask.from_surface(self.image)

    def update(self, dt):
        keys = pygame.key.get_pressed()

        self.direction.x = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.direction.y = (keys[pygame.K_DOWN]  or keys[pygame.K_s]) - (keys[pygame.K_UP]   or keys[pygame.K_w])


        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()
            self.rect.centerx += self.direction.x * self.speed * dt
            self.rect.centery += self.direction.y * self.speed * dt

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        current_time = pygame.time.get_ticks()
        keys_just_pressed = pygame.key.get_just_pressed()

        if keys_just_pressed[pygame.K_SPACE] and (current_time - self.shottime > self.shotdelay):
            Laser(sprites, self.rect.centerx, self.rect.top, laser_image)
            self.shottime = current_time 


class Meteor(pygame.sprite.Sprite):

    def __init__(self, groups,image):
        super().__init__(groups)
        self.image=image
        self.rect = self.image.get_frect(center=(random.randint(0,width), -100))
        self.speed=400;
        self.direction=pygame.Vector2(uniform(-0.5,0.5),1)
    def update(self,dt):
        self.rect.center+=self.direction*self.speed*dt
        if self.rect.centery>=height+20:
            self.kill()
                
class Laser(pygame.sprite.Sprite):
    def __init__(self, groups,x,y,laser_image):
        super().__init__(groups)
        self.image=laser_image
        self.rect=self.image.get_frect(center=(x,y))
        self.speed=600

    def update(self,dt):
        self.rect.centery-=self.speed*dt
        if self.rect.centery<-10:
            self.kill()




display_surface = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders")

background = pygame.image.load("./Backgrounds/black.png").convert()
background = pygame.transform.scale(background, (width, height))

sprites = pygame.sprite.Group()
plane = Plane(sprites)
meteor_sprites=pygame.sprite.Group();
laser_sprites=pygame.sprite.Group();



meteor_event=pygame.event.custom_type()
pygame.time.set_timer(meteor_event,500)

clock = pygame.time.Clock()
FPS = 60
running = True

while running:
    dt = clock.tick(FPS) / 1000  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type==meteor_event:
            Meteor((sprites,meteor_sprites),meteor)
    sprites.update(dt)

    hit_player=pygame.sprite.spritecollide(plane,meteor_sprites,True,pygame.sprite.collide_mask)
    if hit_player:
        plane.health=plane.health-1
        print(plane.health)
        if plane.health<=0:
            print("game over")

    for laser in laser_sprites:
        collided_meteor=pygame.sprite.spritecollide(laser,meteor_sprites,True)
        if collided_meteor:
            laser.kill()
    display_surface.blit(background, (0, 0))
    displayscore()
    displaylives(plane.health)
    sprites.draw(display_surface)
   
    pygame.display.update()

pygame.quit()
