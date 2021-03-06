import pygame
import random
import os

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
player_img = pygame.image.load(os.path.join(img_folder,'blockerMad.png'))
enemy_img = pygame.image.load(os.path.join(img_folder,'1B.png'))
bullet_img = pygame.image.load(os.path.join(img_folder,'hill_small.png'))
background = pygame.image.load(os.path.join(img_folder, 'eye.jpg'))
background_rect = background.get_rect()

WIDTH = 1000
HEIGHT = 800
FPS = 60
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Window")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.bottom = HEIGHT -10
        self.speedx = 0
    
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a] or keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_d] or keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x +=self.speedx
        
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
            
    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)     

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.image.set_colorkey(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -30) 
        self.speedy = random.randrange(1,10)
        self.speedx = random.randrange(-3,3)
        
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -30) 
            self.speedy = random.randrange(1,5)

class Bullet(pygame.sprite.Sprite):
     def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x 
        self.speedy = -10
        
     def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for i in range (10):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)



run = True
while run:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            
    all_sprites.update()
    
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        run = False
    
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    
    screen.fill(RED)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    pygame.display.flip()
    
pygame.quit()
    
    
    
    