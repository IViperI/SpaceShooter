#SpaceShooter
# -6.11.2025
#Settings
WIDTH = 800
HEIGHT = 600
TITLE = "SpaceShooter"
FPS_LIMIT = 75
BGVOLUME = 10
SVOLUME = 5
LIFES = 3
BULLETS_COUNT = 4
RELOADING_TIME = 3 #seconds
ENEMIES_COUNT = 4 #count
ASTEROIDS_COUNT = 3

#Sprites
asteroidImage = "asteroidMod.png"
bulletImage = "bulletMod.png"
backgroundImage = "galaxyMod.png"
rocketImage = "rocketMod.png"
ufoImage = "ufoMod.png"

#Code
import pygame as pg
from random import randint
from time import time as getTime
pg.init()

class GSprite(pg.sprite.Sprite): #GameSprite
    def __init__(self, image, position, speed, size):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(image).convert_alpha(), (size[0],size[1]))
        self.speed = speed
        self.size = size
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.mask = pg.mask.from_surface(self.image)

    def show(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class Player(GSprite):
    def update(self):
        keys = pg.key.get_pressed()
        if  keys[pg.K_a] and self.rect.x >= 5:
            self.rect.x -= self.speed
        if keys[pg.K_d] and self.rect.x <= WIDTH-self.rect.width:
            self.rect.x += self.speed

    def fire(self):
        bullets.add(Bullet(bulletImage, (self.rect.centerx-10,self.rect.top), 5, (20,40)))
        fireSound.play()

class Asteroid(GSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= HEIGHT+100:
            self.rect.y = -100
            self.rect.x = randint(0,WIDTH-80)

class Enemy(GSprite):
    def update(self):
        global missed
        self.rect.y += self.speed
        if self.rect.y >= HEIGHT+100:
            self.rect.y = -100
            self.rect.x = randint(0,WIDTH-80)
            missed += 1

class Bullet(GSprite):
    def update(self):
        if self.rect.y <= -30:
            self.kill()
        self.rect.y -= self.speed

window = pg.display.set_mode((WIDTH, HEIGHT),vsync = 1)
pg.display.set_caption(TITLE)
clock = pg.time.Clock()
bgimage = pg.transform.scale(pg.image.load(backgroundImage), (WIDTH, HEIGHT))
pg.mixer.music.load('space.ogg')
pg.mixer.music.set_volume(BGVOLUME/100)
pg.mixer.music.play()
fireSound = pg.mixer.Sound("fire.ogg")
fireSound.set_volume(SVOLUME/100)

font = pg.font.SysFont("Bahschrift", 25)
endFont = pg.font.SysFont("Bahschrift", 50)
victoryFont = endFont.render(f"VICTORY", True, (200,200,70,255))
defeatFont = endFont.render(f"DEFEAT", True, (200,70,70,255))
reloadFont = pg.font.SysFont("Bahschrift", 50).render(f"Reloading", True, (150,200,200,255))

player = Player(rocketImage, (WIDTH/2, HEIGHT-100), 5, (50,75))
bullets = pg.sprite.Group()
enemies = pg.sprite.Group()
for c in range(ENEMIES_COUNT):
    enemies.add(Enemy(ufoImage, (randint(0, WIDTH-80), randint(-100,0)), randint(1,3), (100,60)))    
asteroids = pg.sprite.Group()
for c in range(ASTEROIDS_COUNT):
    asteroids.add(Asteroid(asteroidImage, (randint(0, WIDTH-80), randint(-100,0)), randint(1,2), (50,50)))

score, missed  = 0, 0
lifes = LIFES
bulletsCount = 0
reloading = False
timeDeath = getTime()
shootTime = getTime()
game = True
finished = 0
winner = 0
while game:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game = False
        if  event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                game = False
            if event.key == pg.K_SPACE:
                if finished != 1:
                    if bulletsCount <= BULLETS_COUNT and reloading != True:
                        player.fire()
                        # shootTime = getTime()
                        bulletsCount += 1
                    if bulletsCount >= BULLETS_COUNT and reloading != True:
                        reloading = True
                        bulletsCount = 0
                        reloadTime = getTime()

            if event.key == pg.K_r:
                finished = 0
                score = 0
                missed = 0
                lifes = LIFES
                reloading = True
                reloadTime = getTime()-RELOADING_TIME
                bullets.empty()
                enemies.empty()
                asteroids.empty()
                for c in range(ENEMIES_COUNT):
                    enemies.add(Enemy(ufoImage, (randint(0,WIDTH-80),randint(-100,0)), randint(1,3), (100,60)))
                for c in range(ASTEROIDS_COUNT):
                    asteroids.add(Asteroid(asteroidImage, (randint(0, WIDTH-80), randint(-100,0)), randint(1,2), (50,50)))

    player_collide = pg.sprite.spritecollide(player, enemies, True, pg.sprite.collide_mask)
    if player_collide:
        if (getTime() - timeDeath >= 1):
            if lifes > 0:
                lifes -= 1
                timeDeath = getTime()
        enemies.add(Enemy(ufoImage, (randint(0,WIDTH-80),randint(-100,0)), randint(1,3), (100,60)))

    player_asteroids_collide = pg.sprite.spritecollide(player, asteroids, True, pg.sprite.collide_mask)
    if player_asteroids_collide:
        if (getTime() - timeDeath >= 1):
            if lifes > 0:
                lifes -= 1
                timeDeath = getTime()
        asteroids.add(Asteroid(asteroidImage, (randint(0, WIDTH-80), randint(-100,0)), randint(1,2), (50,50)))

    window.blit(bgimage,(0,0))

    if score >= 10:
        finished = 1
        winner = 1
        window.blit(victoryFont, (WIDTH/2-70,HEIGHT/2-25))

    if missed >= 3 or lifes <= 0:
        finished = 1
        winner = 0
        fontMissed = font.render(f"Missed: {missed}\\3", True, (200,200,200,255))
        window.blit(fontMissed, (10,35))
        window.blit(defeatFont, (WIDTH/2-70,HEIGHT/2-25))

    if finished != 1:
        if reloading:
            if (getTime()-reloadTime <= RELOADING_TIME):
                reloadFont = pg.font.SysFont("Bahschrift", 50).render(f"Reloading {round(RELOADING_TIME - (getTime() - reloadTime),1)}", True, (150,200,200,255))
                window.blit(reloadFont, (WIDTH/2-100,HEIGHT-50))
            else:
                bulletsCount = 0
                reloading = 0
                # reloadTime = getTime()
                
        collidesE = pg.sprite.groupcollide(enemies, bullets, True, True, pg.sprite.collide_mask)
        collidesA = pg.sprite.groupcollide(asteroids, bullets, False, True, pg.sprite.collide_mask)
        for sprite in collidesE:
            score += 1
            enemies.add(Enemy(ufoImage, (randint(0,WIDTH-80),randint(-100,0)), randint(1,3), (100,60)))
        player.update()
        bullets.update()
        enemies.update()
        asteroids.update()

    fontScore = font.render(f"Score: {score}", True, (200,200,200,255))
    fontMissed = font.render(f"Missed: {missed}\\3", True, (200,200,200,255))
    fontLifes = font.render(f"Lifes: {lifes}", True, (200,200,200,255))
    window.blit(fontScore, (10,10))
    window.blit(fontMissed, (10,35))
    window.blit(fontLifes, (10,60))

    fontRestart = font.render(f'To restart press "R"', True, (200,200,200,255))
    window.blit(fontRestart, (WIDTH-170,10))

    player.show(window)
    bullets.draw(window)
    enemies.draw(window)
    asteroids.draw(window)

    clock.tick(FPS_LIMIT)
    pg.display.update()