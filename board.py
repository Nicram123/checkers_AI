import pygame
from constatnts import BLACK, ROWS, COLS, RED, SQUARE_SIZE, WHITE, GREEN
from piece import Piece
import math as m

class Board:
  PADDING = 10
  def __init__(self):
    self.board = []
    self.possible_places_to_move = []
    self.selected_piece = None  
    self.red_count = 12
    self.white_count = 12
    self.number_of_kings_red = 0
    self.number_of_kings_white = 0
    self.turn = RED
    self.king_piece = [] 
    self.create_board()
     
   
  # Min i max evaluation function
  def score(self): 
    return self.white_count - self.red_count  + (self.number_of_kings_white * 0.5 - self.number_of_kings_red * 0.5)
   
  # usuwa pionki z planszy (listy list - zastepuje objekty Piece na 0) i zmnia licznik pionkow 
  def remove(self, pieces):
    for piece in pieces:
       if piece.king and piece in self.king_piece:
           self.king_piece.remove(piece)
           if piece.color == RED:
               self.number_of_kings_red -= 1
           else:
               self.number_of_kings_white -= 1
    
    for piece in pieces:
        self.board[piece.row][piece.col] = 0
        if piece.color == RED:
            self.red_count -= 1
        else:
            self.white_count -= 1
       
    
  # przsuwa pionek na nowe miejsce na plaszy (aktualizuje x i y czyli srodki pola i wiersz - row i kolumne - col) i zmienia board (liste list)          
  def move(self, piece, row, col):
    # aktualizuje liste list board czyli plansze w dawna pozycje pionka wstawia 0 a w nowe miejsce wstawia obiekt Piece
    self.board[piece.row][piece.col], self.board[row][col] = 0, piece
    # row i col aktualizuje czyli wiersz i kolumne danego pionka
    piece.row, piece.col = row, col  
    # x i y aktualizuje czyli srodek planszy 
    piece.set_xy()
    # czy damka jesli tak to ustaw flage king dla danego pionka na True 
    piece.ifKing()
    # ewentualnie obsługa damki

  # zwraca wszystkie pionki danego koloru na planszy ktore jeszcze istnieją 
  def list_pieces(self, color):
    return [obj for row in self.board for obj in row if obj != 0 and obj.color == color]
 
      
  # sprawdza czy ktos wygral gre jesli ktos ma 0 pionkow to przegrywa
  def if_win_the_game(self):
    if self.red_count <= 0:
        return WHITE
    elif self.white_count <= 0:
        return RED
    return None
   
  # wypelnianie planszy board (listy list) pionkami lub 0 na poczatku gry 
  def create_board(self):
    self.board = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            if self.piece_expected(r, c):
                color = WHITE if r < 3 else RED if r > 4 else None
                row.append(Piece(r, c, color) if color else 0)
            else:
                row.append(0)
        self.board.append(row)
  
   
  # sprawdza czy na danym polu powinnien byc pionek (czarne pola i odpowiednie rzędy)
  def piece_expected(self, r: int, c: int) -> bool:
    # na czarnych polach postawione pionki , fausz wywrocone dla zielonych pól 
    if (r + c) % 2 == 0:
        return False
    # białe pionki w pierwszych 3 rzędach
    if r < 3:
        return True
    # czerwone pionki w ostatnich 3 rzędach
    if r > ROWS - 4:  # np. przy ROWS = 8 => r > 4
        return True
    return False

  # rysowanie planszy i pionków na niej 
  def create_all_board(self, win, selected_piece=None):
    self.create_squares(win)
    for r, row in enumerate(self.board):
        for c, cell in enumerate(row):
            if cell != 0:
                cell.create_piece(win)
    if selected_piece is not None:
        selected_piece.setPicture(win, self)

  # metoda do rysowania zielonych kwadratów planszy w odpowiednich miejscach
  def create_squares(self, win):
    win.fill(BLACK)
    for r in range(ROWS):
        for c in range(COLS):
            if (r + c) % 2 == 0:
                rect = self.get_rect(r, c)   
                pygame.draw.rect(win, GREEN, rect)
                
                
  # Zwraca prostokąt (pygame.Rect) odpowiadający polu na planszy dla wiersza r i kolumny c.            
  def get_rect(self, r: int, c: int) -> pygame.Rect:
    return pygame.Rect(r * SQUARE_SIZE, c * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)


  # uzytkownik wybiera pionek klikajac na niego i wtedy zwraca obiekt pionka 
  def choose_a_pown(self,pos):
     for n in range(ROWS):
        for x in range(COLS):
           if ( n * SQUARE_SIZE <= pos[1] and pos[1] <= n * SQUARE_SIZE + SQUARE_SIZE ) and ( x * SQUARE_SIZE <= pos[0] and pos[0] <= x * SQUARE_SIZE + SQUARE_SIZE ):
              if self.board[n][x] != 0:
                 middleX, middleY = self.board[n][x].middleY, self.board[n][x].middleX
                 radius = SQUARE_SIZE//2 - self.PADDING 
                 d = m.sqrt((pos[1] - middleX)**2 + (pos[0] - middleY)**2)
                 if radius >= d:
                    return self.board[n][x]
     return 0
  
  # Zmiana tury przy kazdym ruchu (na zmiane player - RED, AI - WHITE) 
  def change_turn(self):
    self.turn = RED if self.turn == WHITE else WHITE
  
  
  
  
              
              