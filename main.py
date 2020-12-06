#IMPORT LIBRARIES
import pygame 
import random


#configs
width = 480
height = 600
fps = 45

#INITALIZE PYGAME AND CREATE WINDOW
pygame.init()
#sound
#pygame.mixer.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Qurintine Boringness")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

#Sprite Image
player1 = pygame.image.load("shipGreen_manned.png").convert()

background = pygame.image.load("space.jpg").convert()
background_rect = background.get_rect()

laser = pygame.image.load("laserBlue03.png").convert()

enemy = pygame.image.load("meteorBrown_med1.png").convert()

#colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
lightyellow = (201,246,153)
gray = (170,170,188)
yellow = (250,255,0)
purple = (148,0,255)
navy = (32,65,128)
teal = (0,113,147)
cyan = (17,214,255)
turquoise = (18,255,199)
water = (0,208,255)

#sprites
class Player(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image = player1
    self.image.set_colorkey(black)
    self.rect = self.image.get_rect()
    self.radius = 60
    #pygame.draw.circle(self.image, red, self.rect.center, self.radius)
    self.rect.centerx = width / 2
    self.rect.bottom = height - 10
    self.speedx = 0
  def update(self):
    self.speedx = 0
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_a]:
      self.speedx = -8
    if keystate[pygame.K_d]:
      self.speedx = 8
    self.rect.x += self.speedx
    if self.rect.right > width:
      self.rect.right = width
    if self.rect.left < 0:
      self.rect.left = 0

  def shoot(self):
    bullet = Bullet(self.rect.centerx , self.rect.top)
    all_sprites.add(bullet)
    bullets.add(bullet)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
      pygame.sprite.Sprite.__init__(self)
      self.image = enemy
      self.rect = self.image.get_rect()
      self.radius = int(self.rect.width * .85 / 2)
      #pygame.draw.circle(self.image, red, self.rect.center, self.radius)
      self.rect.x = random.randrange(width - self.rect.width)
      self.rect.y = random.randrange(-100,-40)
      self.speedy = random.randrange(1,8)
      self.speedx = random.randrange(-3,3)
    
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > height + 10 or self.rect.left < -25 or self.rect.right > width + 20:
          self.rect.x = random.randrange(width - self.rect.width)
          self.rect.y = random.randrange(-100,-40)
          self.speedy = random.randrange(1,8)
          self.speedx = random.randrange(-3,3)

class Bullet(pygame.sprite.Sprite):
  def __init__(self,x,y):
    pygame.sprite.Sprite.__init__(self)
    self.image = laser
    self.rect = self.image.get_rect()
    self.rect.bottom = y
    self.rect.centerx = x
    self.speedy = -12

  def update(self):
    self.rect.y += self.speedy
    if self.rect.bottom < 0:
      self.kill()
  

player = Player()
all_sprites.add(player)
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

for i in range(8):
  m = Mob()
  all_sprites.add(m)
  mobs.add(m)

# game loop
running = True 
while running:
  clock.tick(fps)
  #1. process input
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_a:
        player.speedx = -8
      if event.key == pygame.K_d:
        player.speedx = 8
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_a:
        player.speedx = 0
      if event.key == pygame.K_d:
        player.speedx = 0
    if event.type == pygame.QUIT:
        running = False 
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        player.shoot()
      
  #2. update 
  clock.tick(fps)
  all_sprites.update()

  hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
  for hit in hits:
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
  hits = pygame.sprite.spritecollide(player,mobs,False, pygame.sprite.collide_circle)
  if hits:
    running = False
  #3. draw 
  
  
  screen.fill(black)
  screen.blit(background, background_rect)
  all_sprites.draw(screen)
  pygame.display.flip()




pygame.quit
