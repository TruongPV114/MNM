import pygame, sys
from pygame.locals import *
import random
import time

WINDOWWIDTH = 800
WINDOWHEIGHT = 500

pygame.init()
w = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

ytao = 0
ycam = 0
yxoai = 0
y_b = 0

BG = pygame.image.load('bg2.jpg')
BG = pygame.transform.scale(BG, (WINDOWWIDTH, WINDOWHEIGHT))
tao = pygame.image.load('tao.png')
tao = pygame.transform.scale(tao, (40, 50))
cam = pygame.image.load('cam.png')
cam = pygame.transform.scale(cam, (40, 50))
xoai = pygame.image.load('xoai.png')
xoai = pygame.transform.scale(xoai, (40, 50))
start_button = pygame.image.load('start.png')
start_button = pygame.transform.scale(start_button, (200, 170))
level_up_image = pygame.image.load('level.jpg')
level_up_image = pygame.transform.scale(level_up_image, (WINDOWWIDTH, WINDOWHEIGHT))
continue_button = pygame.image.load('continue.png')
continue_button = pygame.transform.scale(continue_button, (200, 100))
you_lose_image = pygame.image.load('you_lose.jpg')
you_lose_image = pygame.transform.scale(you_lose_image, (WINDOWWIDTH, WINDOWHEIGHT))

FPS = 20
fpsClock = pygame.time.Clock()
clock = pygame.time.Clock()

diem = 0
toc_do_tao = 5
toc_do_cam = 7
toc_do_xoai = 9
level = 1
time_left = 30
game_started = False
show_level_up = False
show_you_lose = False


def reset_positions():
  global ytao, ycam, yxoai
  ytao = ycam = yxoai = 0


def change_x_coords():
  x_coords = [random.randint(100, 700), random.randint(100, 700), random.randint(100, 700)]
  return x_coords


tao_x, cam_x, xoai_x = change_x_coords()

time0 = time.time()

while True:
  current_time = time.time()

  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()

    if event.type == pygame.MOUSEBUTTONDOWN:
      if not game_started:
        if event.pos[0] > 300 and event.pos[0] < 500 and event.pos[1] > 200 and event.pos[1] < 300:
          game_started = True
          time_left = 30
          time0 = current_time
          reset_positions()
          diem = 0
          toc_do_tao = 5
          toc_do_cam = 7
          toc_do_xoai = 9
          level = 1
      elif show_level_up:
        # Check for continue button click during level-up screen
        if event.pos[0] > 300 and event.pos[0] < 500 and event.pos[1] > 200 and event.pos[1] < 300:
          show_level_up = False
          game_started = True  # Start the game again
          time_left = 30  # Reset time
          time0 = current_time
          level += 1  # Increase level
          toc_do_tao += 1  # Increase fruit speeds
          toc_do_cam += 1
          toc_do_xoai += 1
          tao_x, cam_x, xoai_x = change_x_coords()  # Change fruit positions
      elif event.pos[0] > tao_x and event.pos[0] < tao_x + 40 and event.pos[1] > ytao - 50 and event.pos[1] < ytao + 50:
        diem += 5
        ytao = 0
        tao_x = random.randint(100, 700)
      elif event.pos[0] > cam_x and event.pos[0] < cam_x + 40 and event.pos[1] > ycam - 50 and event.pos[1] < ycam + 50:
        diem += 5
        ycam = 0
        cam_x = random.randint(100, 700)
      elif event.pos[0] > xoai_x and event.pos[0] < xoai_x + 40 and event.pos[1] > yxoai - 50 and event.pos[
        1] < yxoai + 50:
        diem += 5
        yxoai = 0
        xoai_x = random.randint(100, 700)

  if game_started and not show_level_up and not show_you_lose:
    time1 = current_time
    time_left = 30 - int(time1 - time0)

    if time_left <= 0:
      show_you_lose = True
      time0 = current_time

    w.blit(BG, (0, y_b))
    w.blit(tao, (tao_x, ytao))
    w.blit(cam, (cam_x, ycam))
    w.blit(xoai, (xoai_x, yxoai))

    ytao += toc_do_tao
    ycam += toc_do_cam
    yxoai += toc_do_xoai

    if ytao > WINDOWHEIGHT:
      ytao = 0
      tao_x = random.randint(100, 700)
      diem -= 5
      if diem <=0: diem =0

    if ycam > WINDOWHEIGHT:
      ycam = 0
      cam_x = random.randint(100, 700)
      diem -= 5
      if diem <= 0: diem = 0

    if yxoai > WINDOWHEIGHT:
      yxoai = 0
      xoai_x = random.randint(100, 700)
      diem -= 5
      if diem <= 0: diem = 0


    if diem >= level * 100:
      show_level_up = True
      game_started = False  # Pause the game when level-up screen shows

    font = pygame.font.SysFont('Arial', 30)
    text = font.render('Tong diem: {}'.format(diem), True, (255, 0, 0))
    text1 = font.render('Thoi gian: {}'.format(time_left), True, (255, 0, 0))
    text2 = font.render('Level: {}'.format(level), True, (255, 0, 0))
    w.blit(text, (50, 50))
    w.blit(text1, (50, 80))
    w.blit(text2, (50, 110))

  elif show_level_up:
    w.blit(level_up_image, (0, 0))
    w.blit(continue_button, (300, 200))

  elif show_you_lose:
    w.blit(you_lose_image, (0, 0))
    if current_time - time0 >= 3:
      game_started = False
      show_you_lose = False

  else:
    w.blit(BG, (0, 0))
    w.blit(start_button, (300, 200))

  pygame.display.update()
  fpsClock.tick(FPS)
