import pygame as pg
from settings import *
from os import path
from random import choice, randrange, uniform
vec = pg.math.Vector2

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
        # self.mob = pg.image.load()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT - 100)
        self.pos = vec(40, HEIGHT - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        self.standing_frames = [pg.image.load(path.join(img_dir, STAND))]
        for frame in self.standing_frames:
            frame.set_colorkey(WHITE)
        self.walk_frames_r = [pg.image.load(path.join(img_dir, STAND)),
                              pg.image.load(path.join(img_dir, RIGHT))]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(WHITE)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        for frame in self.walk_frames_l:
            frame.set_colorkey(WHITE)
        self.jump_frame = pg.image.load(path.join(img_dir, JUMP))
        self.jump_frame.set_colorkey(WHITE)

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def jump(self):
        # jump only if standing on a platform
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP
            self.image = self.jump_frame
            self.rect = self.image.get_rect()

    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        # show walk animation
        if self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                # self.image = self.jump_frame
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        self.mask = pg.mask.from_surface(self.image)

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [pg.image.load(path.join(img_dir, LARGE)), #ground
                  pg.image.load(path.join(img_dir, SMALL))] #ground_small
        self.image = choice(images)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if randrange(100) < POW_SPAWN_PCT:
            Pow(self.game, self)

class Pow(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = POW_LAYER
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = choice(['boost'])
        self.image = self.game.spritesheet.get_image(820, 1805, 71, 70)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()

class Mob(pg.sprite.Sprite):
    def __init__(self, game):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.enemy_r = pg.image.load(path.join(img_dir, ENEMY))
        self.enemy_r.set_colorkey(WHITE)
        self.enemy_l = pg.transform.flip(self.enemy_r, True, False)
        self.enemy_l.set_colorkey(WHITE)
        # self.image_up = self.game.spritesheet.get_image(566, 510, 122, 139)
        # self.image_up.set_colorkey(BLACK)
        # self.image_down = self.game.spritesheet.get_image(568, 1534, 122, 135)
        # self.image_down.set_colorkey(BLACK)
        self.image = self.enemy_r
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100])
        self.vx = randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = randrange(HEIGHT / 2)
        self.vy = 0
        self.dy = 0.5

    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.image = self.enemy_r
        else:
            self.image = self.enemy_l
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = center
        self.rect.y += self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()

class GameOver(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = COIN_LAYER
        self.groups = game.all_sprites, game.coin
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_gold = self.game.spritesheet.get_image(244, 1981, 61, 61)
        self.image_gold.set_colorkey(BLACK)
        self.image_silver = self.game.spritesheet.get_image(307, 1981, 61,61)
        self.image_silver.set_colorkey(BLACK)
        self.image_bronze = self.game.spritesheet.get_image(329, 1390, 60, 61)
        self.image_bronze.set_colorkey(BLACK)
        self.rect = self.image_gold.get_rect()
        self.rect = self.image_silver.get_rect()
        self.rect = self.image_bronze.get_rect()
        
