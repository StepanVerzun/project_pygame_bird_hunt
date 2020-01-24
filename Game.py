import random

import pygame
import os
import sys

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
clock = pygame.time.Clock()
FPS = 60
pygame.mouse.set_visible(0)
shot = pygame.mixer.Sound('shot.wav')
death = pygame.mixer.Sound('death.wav')
GRAVITY = 0.1
screen_rect = (0, 0, 1920, 1080)
feathers = pygame.sprite.Group()

def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('startscreen.jpg'), (1920, 1080))
    start_sprites = pygame.sprite.Group()
    playbut = pygame.sprite.Sprite()
    playbut.image = load_image('play.png')
    playbut.rect = playbut.image.get_rect()
    playbut.rect.x = 650
    playbut.rect.y = 480
    start_sprites.add(playbut)
    exitbut = pygame.sprite.Sprite()
    exitbut.image = load_image('exit.png')
    exitbut.rect = exitbut.image.get_rect()
    exitbut.rect.x = 650
    exitbut.rect.y = 700
    start_sprites.add(exitbut)
    cur = pygame.sprite.Sprite()
    cur.image = load_image("cross.png")
    cur.rect = cur.image.get_rect()
    start_sprites.add(cur)
    while True:
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                cur.rect.center = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN and playbut.rect.collidepoint(event.pos):
                game(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN and exitbut.rect.collidepoint(event.pos):
                terminate()
        start_sprites.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()


def game(pos):
    class AnimatedSprite(pygame.sprite.Sprite):
        def __init__(self, sheet, columns, rows, x, y):
            super().__init__(bird_sprites)
            self.frames = []
            self.cut_sheet(sheet, columns, rows)
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
            self.rect = self.rect.move(x, y)
            self.vx = 5
            self.vy = -10

        def cut_sheet(self, sheet, columns, rows):
            self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                    sheet.get_height() // rows)
            for j in range(rows):
                for i in range(columns):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames.append(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)))

        def update(self):
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.rect = self.rect.move(self.vx, self.vy)
            if self.rect.x == 2100:
                self.rect.x = -100
                self.rect.y = 360
            if self.rect.y == 100:
                self.vy = 10
            if self.rect.y == 800:
                self.vy = -10

    fon = pygame.transform.scale(load_image('bg.png'), (1920, 1080))
    game_sprites = pygame.sprite.Group()
    bird_sprites = pygame.sprite.Group()
    cur = pygame.sprite.Sprite()
    cur.image = load_image("cross.png")
    cur.rect = cur.image.get_rect()
    cur.rect.x = pos[0] - 75
    cur.rect.y = pos[1] - 75
    score = pygame.sprite.Sprite()
    score.image = load_image("score.png")
    score.rect = cur.image.get_rect()
    score.rect.x = 50
    score.rect.y = 900
    game_sprites.add(score)
    bullets = pygame.sprite.Sprite()
    bullets.image = load_image("bullets.png")
    bullets.rect = cur.image.get_rect()
    bullets.rect.x = 50
    bullets.rect.y = 1000
    game_sprites.add(bullets)
    bird = AnimatedSprite(load_image("bird-sprite.png"), 5, 3, -100, 360)
    bird_sprites.add(bird)
    game_sprites.add(cur)
    counter, text = 0, 'charged'.rjust(3)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('Consolas', 100)
    while True:
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                cur.rect.center = event.pos
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                start_screen()
            if event.type == pygame.MOUSEBUTTONDOWN and bird.rect.collidepoint(event.pos):
                if counter == 0:
                    death.play()
                    shot.set_volume(0.5)
                    counter = 3
                    shot.play()
                    bird.rect.x = -100
                    bird.rect.y = 360
                    create_particles(pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONDOWN and not bird.rect.collidepoint(event.pos):
                if counter == 0:
                    shot.set_volume(0.5)
                    counter = 3
                    shot.play()
            if event.type == pygame.USEREVENT:
                if counter != 0:
                    counter -= 1
                    text = 'reload' + str(counter).rjust(3) if counter > 0 else 'charged'
        feathers.update()
        screen.blit(fon, (0, 0))
        feathers.draw(screen)
        bird_sprites.update()
        bird_sprites.draw(screen)
        game_sprites.draw(screen)
        clock.tick(FPS)
        screen.blit(font.render(text, True, (255, 0, 0)), (500, 500))
        pygame.display.flip()


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("feathers.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(feathers)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    particle_count = 20
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


start_screen()
