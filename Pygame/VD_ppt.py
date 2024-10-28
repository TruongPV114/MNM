import pygame  # gọi thư viện Game
pygame.init()   # khởi động
screen_width, screen_height = 800, 600  # Thiết lập kích thước cửa sổ
screen = pygame.display.set_mode((screen_width, screen_height))
running = True  # Vòng lặp chính của trò chơi
while running:
         for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                            running = False
         # Code vẽ và logic của trò chơi sẽ điều này
pygame.display.flip()
pygame.quit() # Kết thúc trò chơi
