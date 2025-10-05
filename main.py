import pygame
from constatnts import WIDTH, HEIGHT, SQUARE_SIZE, WHITE, RED, BLACK, GREEN 
from board import Board 
from piece import Piece 
from minimax import MinimaxAlgorithm

FPS = 60
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('checkers game AI')


def main():
  run = True
  clock = pygame.time.Clock()
  board = Board()
  minimax = MinimaxAlgorithm()
  board.create_all_board(WIN)
  first_left_click = True
  obj = 0

  while run:
    clock.tick(FPS)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_position = pygame.mouse.get_pos()
        if obj == 0 or len(board.possible_places_to_move) == 0 or ( obj is not isinstance(obj, int) and not obj.returnTrue(board,mouse_position)) :
          obj = board.choose_a_pown(mouse_position)
        elif len(board.possible_places_to_move) == 0:
          first_left_click = True
        else:
          first_left_click = False
        if event.button == 1:
          if first_left_click:
            #first_left_click = True
            if obj != 0:
              obj.captured_pieces.clear()
              #obj.BlueField(WIN,board) # drawing a blue fields
              obj.check_capture_recursive(board,WIN)
              #_ = obj.possible_moves(board)
          elif not first_left_click and obj is not isinstance(obj, int):
            obj.move_piece(board,WIN,mouse_position)
            first_left_click = True
            board.change_turn()
            if board.turn == WHITE:
                #board.refresh_counts()
                value, new_board, piece_ = minimax.mini_max(3, board, True)
                print(f'White left: {board.white_count}, Red left: {board.red_count}')
                print('----------')
                print(f'White kings: {board.number_of_kings_white}, Red kings: {board.number_of_kings_red}')
                board = new_board
                board.create_all_board(WIN, piece_)  # <--- to zamiast manualnego recta
                
                board.change_turn()
                print("AI made a move")
    pygame.display.update()

  pygame.quit()

main()