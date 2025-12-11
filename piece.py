import pygame 
from constatnts import RED, WHITE, SQUARE_SIZE, GREY, GOLDEN, ROWS, COLS, BLACK , CROWN
import math as m

class Piece:
  PADDING = 8
  captured_pieces = {} #[]
  def __init__(self,row,col,color):
    self.king = False 
    self.color = color
    self.row = row
    self.col = col
    if self.color == RED:
      self.direction = -1
    else:
      self.direction = 1
    self.middleY = 0
    self.middleX = 0
    self.set_xy()
    
  # czy pionek moze sie ruszyc na dane pole (tj. czy pole jest puste) 
  def IfCollision(self,obj,row,col):  # 
    # jest puste bo jest 0 
    if ( obj.board[row][col] == 0):
      return True
    # nie jest puste bo jest tam pionek
    else:
      return False
  
  # sprawdza czy klikniety obszar jest w polu mozliwosci ruchu (possible_places_to_move)  
  def returnTrue(self,board,mouse_position):
    for x in range(len(board.possible_places_to_move)):
      if ( board.possible_places_to_move[x].row * SQUARE_SIZE <= mouse_position[1] <=  board.possible_places_to_move[x].row * SQUARE_SIZE + SQUARE_SIZE and
      board.possible_places_to_move[x].col * SQUARE_SIZE <= mouse_position[0] <=  board.possible_places_to_move[x].col * SQUARE_SIZE + SQUARE_SIZE ):
        return True 
    return False
  
  # przesuwa pionka na nowe miejsce na plaszy przy robieniu potrzebnych aktualizacji 
  def upgrate(self,board,win,ix):  # 
      pygame.draw.rect(win,BLACK,(self.col*SQUARE_SIZE,self.row*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
      #vi = board.board[self.row][self.col] #
      #board.board[self.row][self.col] = 0  #
      #self.row = board.possible_places_to_move[ix].row #
      #self.col = board.possible_places_to_move[ix].col # 
      #board.board[self.row][self.col] = vi # 
      
      # przesuwa pionek na nowe miejsce w planszy 
      board.move(self, board.possible_places_to_move[ix].row, board.possible_places_to_move[ix].col)
      # rysuje czarne pola na miejscach gdzie byly mozliwe ruchy
      self.drawBlackSquare(win,board)
      # czysci liste mozliwych miejsc do ruchu
      board.possible_places_to_move.clear()
      # ustawia srodek tego pionka na nowej pozycji 
      self.set_xy()
      # rysuje pionka na planszy ale na nowej pozycji 
      self.create_piece(win)

  # to jest funkcja napisana dla pionkow RED czyli playera  
  def move_piece(self,board,win,mouse_position): # 
    for x in range(len(board.possible_places_to_move)):
      # czy klikniety obszar jest w polu mozliwosci ruchu (possible_places_to_move)
      if ( board.possible_places_to_move[x].row * SQUARE_SIZE <= mouse_position[1] <=  board.possible_places_to_move[x].row * SQUARE_SIZE + SQUARE_SIZE and
      board.possible_places_to_move[x].col * SQUARE_SIZE <= mouse_position[0] <=  board.possible_places_to_move[x].col * SQUARE_SIZE + SQUARE_SIZE ):
        moves = self.possible_moves(board)
        self.upgrate(board,win,x)
        self.remove_piece(mouse_position[1],mouse_position[0],win,board, moves)
        self.ifKing()
        self.setPicture(win, board)
        break
      
  # oblicza srodek pola na ktorym stoi pionek 
  def set_xy(self):  # 
    self.middleX = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
    self.middleY = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

  # rysuje pionka na planszy jako circle o promieniu radius i srodku w (self.middleX,self.middleY) 
  def create_piece(self, win): # 
    radius = SQUARE_SIZE//2 - self.PADDING 
    pygame.draw.circle(win, self.color, (self.middleX,self.middleY), radius)
    
  # tylko dla pionkow RED (playera) tworzy liste mozliwych ruchow pionka (bić i nie bić)
  def check_capture_recursive(self, board, win): # 
    self.drawBlackSquare(win, board)
    board.possible_places_to_move.clear()
    # zwraca slownik { (row,col) : [list_of_captured_pieces] } (mozliwe ruchy - bicia i nie bicia dla pionka) 
    moves = self.possible_moves(board) 
    for x in moves.items():
      # x = ( (row,col) : [list_of_captured_pieces] )
      r = x[0][0] # row 
      c = x[0][1] # col 
      obj = Piece(r, c, self.color)
      obj.row, obj.col = r, c
      obj.set_xy()
      board.possible_places_to_move.append(obj)
      obj.drawFieldForPossibleMove(win)
    #self.captured_pieces.clear() 
      
  # tylko dla pionkow RED (playera) usuwa zbite pionki z planszy i aktualizuje liczniki pionkow
  def remove_piece(self, finalX, finalY, win, board, moves): # 
    piece_list = [] 
    for x in moves.items(): 
        tuple_ = x[0] # (row,col)
        piece_list_temp = x[1] # [list_of_captured_pieces]
        if ((tuple_[0] * SQUARE_SIZE <= finalX <= tuple_[0] * SQUARE_SIZE + SQUARE_SIZE) and 
            (tuple_[1] * SQUARE_SIZE <= finalY <= tuple_[1] * SQUARE_SIZE + SQUARE_SIZE)):
            piece_list = piece_list_temp 
            break
    for x in range(len(piece_list)):
        pygame.draw.rect(win, BLACK, (piece_list[x].col * SQUARE_SIZE, piece_list[x].row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        board.board[piece_list[x].row][piece_list[x].col] = 0
        if piece_list[x].color == WHITE: # RED 
            board.white_count -= 1
            if piece_list[x].king:
                board.number_of_kings_white -= 1 
                board.king_piece.remove(piece_list[x]) 
        #else:
        #    board.white_count -= 1 
        #    if piece_list[x].king:
        #        board.number_of_kings_white -= 1 
        #        board.king_piece.remove(piece_list[x]) 
       
        #if not self.ClumpingLimit(finalX, finalY, piece_list[x]):
        #    continue
        #else:
        #    break
        
    #self.captured_pieces.clear()        
    
  # rysuje zloty krazek na polu gdzie pionek moze sie ruszyc
  def drawFieldForPossibleMove(self, win): # 
    radius = SQUARE_SIZE//2 - self.PADDING * 4
    pygame.draw.circle(win, GOLDEN, (self.middleX,self.middleY), radius)
    
  # rysuje czarne pola na miejscach gdzie byly mozliwe ruchy 
  def drawBlackSquare(self,win,board): # 
    for x in range(len(board.possible_places_to_move)):
      pygame.draw.rect(win,BLACK,(board.possible_places_to_move[x].col*SQUARE_SIZE,board.possible_places_to_move[x].row*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
  

  # ustaiwia flage king na True (dla danego pionka) jezeli pionek dotarl do ostatniego rzedu 
  def ifKing(self):  # 
    if self.color == RED:
      if self.row == 0:
        self.king = True
    else:
      if self.row == ROWS - 1:
        self.king = True
       
  # zwiększa licznik królów i dodaje do listy king_piece 
  def setPictureFirstTime(self, board): # 
    if self.king == True and self not in board.king_piece: 
      board.king_piece.append(self)
      if self.color == RED: 
        board.number_of_kings_red += 1
      else:
        board.number_of_kings_white += 1
    
        
  # rysuje korone na pionku jezeli jest on krolowa (tj. self.king == True)
  def setPicture(self,win, board): # 
    self.setPictureFirstTime(board)
    # rysujemy korone na wszystkich pionkach z listy king_piece 
    for piece in board.king_piece:
        win.blit(CROWN, (piece.middleX - CROWN.get_width()//2, piece.middleY - CROWN.get_height()//2))
         
  
  # przekazujemy obiekt board zeby zbadac mozliwe ruchy na pionku ktory ta funkcja wywoluje (bicia i nie bicia), jezeli nie ma mozliwych bić to zwraca pusta liste
  def possible_moves(self, board): # 
    moves = {}
    directions = [(1, -1), (-1, -1), (1, 1), (-1, 1)] if self.king else [(-1, -1), (-1, 1)] if self.color == RED else [(1, -1), (1, 1)]
    def explore(row, col, captured):
        # znaleziono bicie lub nie 
        found_capture = False
        for dr, dc in directions:
            # pozycja pionka do bicia 
            r1, c1 = row + dr, col + dc
            # pozycja docelowa po biciu 
            r2, c2 = row + 2 * dr, col + 2 * dc
            # Sprawdzenie granic dla r1, c1 i r2, c2
            if (0 <= r1 < len(board.board) and 0 <= c1 < len(board.board[0]) and
                0 <= r2 < len(board.board) and 0 <= c2 < len(board.board[0])):
                # Sprawdzenie warunków bicia czyli inny kolor, puste pole za pionkiem, nie bicie tego samego pionka
                if (board.board[r1][c1] != 0 and self.color != board.board[r1][c1].color and
                    board.board[r2][c2] == 0 and board.board[r1][c1] not in captured):
                    # znaleziono bicie 
                    found_capture = True
                    new_captured = captured + [board.board[r1][c1]]
                    moves[(r2, c2)] = new_captured
                    explore(r2, c2, new_captured)
                    
        # nie jesteśmy w trakcie sekwencji bicia czyli szuka ruchow bez bicia 
        if not captured: # not found_capture and  
            for dr, dc in directions:
                # pozycja docelowa bez bicia 
                r, c = row + dr, col + dc
                if 0 <= r < len(board.board) and 0 <= c < len(board.board[0]) and board.board[r][c] == 0:
                    moves[(r, c)] = []

    explore(self.row, self.col, []) 
    #self.captured_pieces = moves
    return moves
   
  
        
  
  # 
  #def check_capture_recursive(self, board, win, captured_pieces_list=None, flag = False, max_depth=20):
    #if captured_pieces_list is None:
    #    captured_pieces_list = []
    #    
    #directions = []
    #directions = [(1, -1), (-1, -1), (1, 1), (-1, 1)] if self.king or flag else [(-1, -1), (-1, 1)] if self.color == RED else [(1, -1), (1, 1)]
    #flag = True if self.king or flag else False

    #for dr, dc in directions:
    #    r, c = self.row + dr, self.col + dc
    #    if 0 <= r < len(board.board) and 0 <= c < len(board.board[0]) and board.board[r][c] != 0 and self.color != board.board[r][c].color:
    #        r, c = r + dr, c + dc
    #        if 0 <= r < len(board.board) and 0 <= c < len(board.board[0]) and board.board[r][c] == 0:
    #            if 0 <= r < len(board.board) and 0 <= c < len(board.board[0]) and board.board[r][c] == 0:
    #                if board.board[r-dr][c-dc] not in captured_pieces_list:
    #                    captured_pieces_list.append(board.board[r-dr][c-dc])
    #                else:
    #                    break
    #            obj = Piece(r, c, self.color)
    #            obj.row, obj.col = r, c
    #            board.possible_places_to_move.append(obj)
    #            obj.set_xy()
    #            obj.drawFieldForPossibleMove(win)
    #            if max_depth > 0:
    #                obj.check_capture_recursive(board, win, captured_pieces_list, flag, max_depth - 1)

    #self.captured_pieces.append(captured_pieces_list[:])
    #if len(captured_pieces_list) != 0:
    #  captured_pieces_list.pop()      

  #def BlueField(self, win, board):
  #  self.drawBlackSquare(win, board)
  #  board.possible_places_to_move.clear()
  #  
  #  newX1 = self.col - 1
  #  newX2 = self.col + 1
  #  
  #  if self.king:
  #      newY1 = self.row - 1
  #      newY2 = self.row + 1
  #         
  #      for newX, newY in [(newX1, newY2), (newX2, newY2), (newX1, newY1), (newX2, newY1)]:
  #          if 0 <= newX < COLS and 0 <= newY < ROWS and self.IfCollision(board, newY, newX):
  #              obj = Piece(newY, newX, self.color)
  #              board.possible_places_to_move.append(obj)
  #              obj.drawFieldForPossibleMove(win)
  #  
  #  elif self.color == WHITE:
  #      newY = self.row + 1
  #      
  #      for newX in [newX1, newX2]:
  #          if 0 <= newX < COLS and 0 <= newY < ROWS and self.IfCollision(board, newY, newX):
  #              obj = Piece(newY, newX, self.color)
  #              board.possible_places_to_move.append(obj)
  #              obj.drawFieldForPossibleMove(win)
  #              
  #  elif self.color == RED:
  #      newY = self.row - 1
  #      
  #      for newX in [newX1, newX2]:
  #          if 0 <= newX < COLS and 0 <= newY < ROWS and self.IfCollision(board, newY, newX):
  #              obj = Piece(newY, newX, self.color)
  #              board.possible_places_to_move.append(obj)
  #              obj.drawFieldForPossibleMove(win)

  
  #def remove(self, finalX, finalY, win, board):
  #  piece_list = []
  #  for x in range(len(self.captured_pieces)):
  #      for y in range(len(self.captured_pieces[x])):
  #          if self.color == RED or self.king == True:
  #              if ((self.captured_pieces[x][y].row - 1) * SQUARE_SIZE <= finalX <= (self.captured_pieces[x][y].row - 1) * SQUARE_SIZE + SQUARE_SIZE and 
  #                  (self.captured_pieces[x][y].col - 1) * SQUARE_SIZE <= finalY <= (self.captured_pieces[x][y].col - 1) * SQUARE_SIZE + SQUARE_SIZE or 
  #                  (self.captured_pieces[x][y].row - 1) * SQUARE_SIZE <= finalX <= (self.captured_pieces[x][y].row - 1) * SQUARE_SIZE + SQUARE_SIZE and 
  #                  (self.captured_pieces[x][y].col + 1) * SQUARE_SIZE <= finalY <= (self.captured_pieces[x][y].col + 1) * SQUARE_SIZE + SQUARE_SIZE):
  #                  piece_list = self.captured_pieces[x]
  #                  
  #          if self.color == WHITE or self.king == True:
  #              if ((self.captured_pieces[x][y].row + 1) * SQUARE_SIZE <= finalX <= (self.captured_pieces[x][y].row + 1) * SQUARE_SIZE + SQUARE_SIZE and 
  #                  (self.captured_pieces[x][y].col - 1) * SQUARE_SIZE <= finalY <= (self.captured_pieces[x][y].col - 1) * SQUARE_SIZE + SQUARE_SIZE or 
  #                  (self.captured_pieces[x][y].row + 1) * SQUARE_SIZE <= finalX <= (self.captured_pieces[x][y].row + 1) * SQUARE_SIZE + SQUARE_SIZE and 
  #                  (self.captured_pieces[x][y].col + 1) * SQUARE_SIZE <= finalY <= (self.captured_pieces[x][y].col + 1) * SQUARE_SIZE + SQUARE_SIZE):
  #                  piece_list = self.captured_pieces[x]
  #                  
  #  for x in range(len(piece_list)):
  #      pygame.draw.rect(win, BLACK, (piece_list[x].col * SQUARE_SIZE, piece_list[x].row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
  #      board.board[piece_list[x].row][piece_list[x].col] = 0
  #              
  #      if piece_list[x].color == RED:
  #          board.red_count -= 1
  #      else:
  #          board.white_count -= 1
  #          
  #      if not self.ClumpingLimit(finalX, finalY, piece_list[x]):
  #          continue
  #      else:
  #          break

  #  self.captured_pieces.clear()

        
      
  #def ClumpingLimit(self, finalX, finalY, obj):
  #  if self.color == RED or self.king:
  #      return ((obj.row - 1) * SQUARE_SIZE <= finalX <= (obj.row - 1) * SQUARE_SIZE + SQUARE_SIZE and
  #              ((obj.col - 1) * SQUARE_SIZE <= finalY <= (obj.col - 1) * SQUARE_SIZE + SQUARE_SIZE or
  #               (obj.col + 1) * SQUARE_SIZE <= finalY <= (obj.col + 1) * SQUARE_SIZE + SQUARE_SIZE))
  #  if self.color == WHITE or self.king:
  #      return ((obj.row + 1) * SQUARE_SIZE <= finalX <= (obj.row + 1) * SQUARE_SIZE + SQUARE_SIZE and
  #              ((obj.col - 1) * SQUARE_SIZE <= finalY <= (obj.col - 1) * SQUARE_SIZE + SQUARE_SIZE or
  #               (obj.col + 1) * SQUARE_SIZE <= finalY <= (obj.col + 1) * SQUARE_SIZE + SQUARE_SIZE))
  #  return False   



  