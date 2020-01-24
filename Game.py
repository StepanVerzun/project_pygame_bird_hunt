import pygame
import os
import sys

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
clock = pygame.time.Clock()
FPS = 60
pygame.mouse.set_visible(0)


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
    fon = pygame.transform.scale(load_image('bg.png'), (1920, 1080))
    game_sprites = pygame.sprite.Group()
    cur = pygame.sprite.Sprite()
    cur.image = load_image("cross.png")
    cur.rect = cur.image.get_rect()
    cur.rect.x = pos[0] - 75
    cur.rect.y = pos[1] - 75
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
        game_sprites.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()


start_screen()