import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Thiết lập kích thước cửa sổ
width, height = 800, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cửa sổ Game")

# Tải ảnh nền
bg_image = pygame.image.load("bg3.png")
bg_image = pygame.transform.scale(bg_image, (width, height))  # Thay đổi kích thước ảnh nền

# Vòng lặp chính của game
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Vẽ ảnh nền
    screen.blit(bg_image, (0, 0))

    # Cập nhật màn hình
    pygame.display.flip()

# Thoát Pygame
pygame.quit()
sys.exit()
