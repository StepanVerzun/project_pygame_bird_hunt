import pygame
import os
import sys

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
clock = pygame.time.Clock()
FPS = 60
pygame.mouse.set_visible(0)
shot = pygame.mixer.Sound('shot.wav')


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
    game_sprites.add(cur)
    bird = AnimatedSprite(load_image("bird-sprite.png"), 5, 3, -100, 360)
    bird_sprites.add(bird)
    game_sprites.add(cur)
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
                bird.rect.x = -100
                bird.rect.y = 360
            if event.type == pygame.MOUSEBUTTONDOWN and not bird.rect.collidepoint(event.pos):
                shot.play()
        bird_sprites.update()
        bird_sprites.draw(screen)
        game_sprites.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()


start_screen()