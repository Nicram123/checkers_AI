import pygame

# board dimensions 
WIDTH, HEIGHT = 700, 700 
# number of rows and columns 
ROWS, COLS = 8, 8
# size of each square 
SQUARE_SIZE = WIDTH//COLS
# picture for crown 
CROWN = pygame.transform.scale(pygame.image.load('crown2.png'), (48, 38)) # 44 , 25 
# colors definitions 
GREEN = (46, 139, 87)
GREEN = (0, 128, 0)
RED = (255, 0, 0) 
WHITE = (255, 255, 255)  
BLACK = (53, 56, 57) 
GOLDEN = (218, 165, 32)
GREY = (128, 128, 128)

