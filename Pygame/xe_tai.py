import pygame
import random
import sys

# Khởi động Pygame
pygame.init()

# Kích thước màn hình
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game Xe Tải Đi Đường Núi")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Tải hình ảnh
truck_image = pygame.image.load('car1.png')  # Thay bằng đường dẫn tới hình ảnh xe tải của bạn
truck_rect = truck_image.get_rect(center=(100, height // 2))

# Định nghĩa các quả núi
mountains = []
for i in range(3):
    mountain_x = random.randint(400, 700)
    mountain_height = random.randint(100, 300)
    mountains.append(pygame.Rect(mountain_x, height - mountain_height, 100, mountain_height))

# Tốc độ di chuyển
truck_speed = 5

# Vòng lặp trò chơi
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Điều khiển xe tải
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        truck_rect.y -= truck_speed
    if keys[pygame.K_DOWN]:
        truck_rect.y += truck_speed

    # Giới hạn di chuyển
    if truck_rect.top < 0:
        truck_rect.top = 0
    if truck_rect.bottom > height:
        truck_rect.bottom = height

    # Kiểm tra va chạm với các quả núi
    for mountain in mountains:
        if truck_rect.colliderect(mountain):
            print("Thua cuộc! Bạn đã chạm vào núi!")
            pygame.quit()
            sys.exit()

    # Vẽ mọi thứ lên màn hình
    screen.fill(WHITE)
    screen.blit(truck_image, truck_rect)
    for mountain in mountains:
        pygame.draw.rect(screen, GREEN, mountain)

    pygame.display.flip()
    clock.tick(60)
