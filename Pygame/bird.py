import pygame, sys
from pygame.locals import *
import random
import time

chieu_dai = 800  # Chiều dài cửa sổ
chieu_rong = 500  # Chiều cao cửa sổ
pygame.init()  # Khởi tạo game
w = pygame.display.set_mode((chieu_dai, chieu_rong))  # Tạo 1 cửa sổ game tên là w
pygame.display.set_caption('Tiêu đề của game')

# ------------- tạo nền của game là 1 ảnh -----------------
anh_nen = pygame.image.load('bg2.jpg')
anh_nen = pygame.transform.scale(anh_nen, (chieu_dai, chieu_rong))

# ----------- tạo ảnh con chim--------------
chim1 = pygame.image.load('chim1.png')
chim1 = pygame.transform.scale(chim1, (60, 50))

chim2 = pygame.image.load('chim2.png')
chim2 = pygame.transform.scale(chim2, (60, 50))

chim3 = pygame.image.load('chim3.png')
chim3 = pygame.transform.scale(chim3, (60, 50))

chim4 = pygame.image.load('chim4.png')
chim4 = pygame.transform.scale(chim4, (60, 50))

chim5 = pygame.image.load('chim5.png')
chim5 = pygame.transform.scale(chim5, (60, 50))

# ---------- tạo vị trí ban đầu--------------
x1 = 200
y1 = 200
x_b = 0
x2 = chieu_dai
y2 = random.randint(0, chieu_rong - 70)

x3 = chieu_dai + 200
y3 = random.randint(0, chieu_rong - 70)

x4 = chieu_dai + 400
y4 = random.randint(0, chieu_rong - 70)

x5 = chieu_dai + 600
y5 = random.randint(0, chieu_rong - 70)

# ---------- Khởi tạo khung thời gian --------------
FPS = 60
fpsClock = pygame.time.Clock()

time0 = time.time()

# Biến điểm số
score = 0
def check_collision(x1, y1, x2, y2, width, height):
    """Kiểm tra va chạm giữa hai con chim."""
    rect1 = pygame.Rect(x1, y1, width, height)
    rect2 = pygame.Rect(x2, y2, width, height)
    return rect1.colliderect(rect2)

def game_over():
    """Hiển thị thông báo Game Over và cho phép chơi lại."""
    font = pygame.font.SysFont('consolas', 60)
    text_surface = font.render('GAME OVER', True, (255, 0, 0))
    text_rect = text_surface.get_rect(center=(chieu_dai // 2, chieu_rong // 2))
    w.blit(text_surface, text_rect)
    pygame.display.update()

    # Vòng lặp đợi người chơi nhấn Enter hoặc Space để chơi lại
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN or event.key == K_SPACE:
                    return  # Thoát khỏi hàm để chơi lại

while True:  # tạo vòng lặp game
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_UP:
                y1 = y1 - 20
            if event.key == K_DOWN:
                y1 = y1 + 20
            if event.key == K_RIGHT:
                x1 = x1 + 20
            if event.key == K_LEFT:
                x1 = x1 - 20

    # -----vẽ ảnh nền ----------------
    w.blit(anh_nen, (x_b, 0))
    w.blit(chim1, (x1, y1))
    w.blit(chim2, (x2, y2))
    w.blit(chim3, (x3, y3))
    w.blit(chim4, (x4, y4))
    w.blit(chim5, (x5, y5))

    # Di chuyển các con chim
    x2 -= 3
    x3 -= 3
    x4 -= 3
    x5 -= 3

    # Kiểm tra nếu 2 con chim chạm nhau thì game over
    if (check_collision(x1, y1, x2, y2, 60, 50) or
        check_collision(x1, y1, x3, y3, 60, 50) or
        check_collision(x1, y1, x4, y4, 60, 50) or
        check_collision(x1, y1, x5, y5, 60, 50)):
        game_over()
        # Đặt lại vị trí ban đầu của các con chim
        x1 = 0
        y1 = 200
        x2 = chieu_dai
        x3 = chieu_dai + 200
        x4 = chieu_dai + 400
        x5 = chieu_dai + 600
        y2 = random.randint(0, chieu_rong - 70)
        y3 = random.randint(0, chieu_rong - 70)
        y4 = random.randint(0, chieu_rong - 70)
        y5 = random.randint(0, chieu_rong - 70)

    time1 = time.time()

    # Cập nhật điểm số nếu chim 2, 3, 4, hoặc 5 đi qua chim 1
    if x2 < x1 :
        score += 1

    if x3 < x1 :
        score += 1

    if x4 < x1 :
        score += 1

    if x5 < x1 :
        score += 1

    font = pygame.font.SysFont('Arial', 30)
    text1 = font.render('Thời gian: {} '.format(int(time1 - time0)), True, (255, 0, 0))  # in ra màn hình thời gian chơi
    print(time1-time0)
    text_score = font.render('Điểm: {}'.format(score), True, (255, 0, 0))  # in ra điểm số
    w.blit(text1, (50, 80))
    # w.blit(text_score, (50, 120))  # Vẽ điểm số lên màn hình
    # Điều chỉnh vị trí của chim2, chim3, chim4, chim5 khi ra khỏi màn hình và tạo chuyển động y ngẫu nhiên
    if x2 < 0:
        x2 = chieu_dai
        y2 = random.randint(0, chieu_rong - 70)

    if x3 < 0:
        x3 = chieu_dai
        y3 = random.randint(0, chieu_rong - 70)

    if x4 < 0:
        x4 = chieu_dai
        y4 = random.randint(0, chieu_rong - 70)

    if x5 < 0:
        x5 = chieu_dai
        y5 = random.randint(0, chieu_rong - 70)

    # Cập nhật màn hình
    pygame.display.update()
    fpsClock.tick(FPS)
