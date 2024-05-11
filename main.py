import pygame
import random
 
 
# Initialize Pygame and set up the display
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((500, 600))
pygame.display.set_caption("SUDOKU - The Pycodes")
 
 
# Grid coordinates, dimensions, and initial user input value
x_coordinate = 0
y_coordinate = 0
cell_width = 500 / 9
user_input_value = ''
 
 
# Initialize an empty Sudoku grid and save its initial state
# Each cell now holds a tuple: (value, is_initial)
sudoku_grid = [[(0, False) for _ in range(9)] for _ in range(9)]
initial_sudoku_grid = []
 
 
# Fonts for displaying text
font_user_input = pygame.font.SysFont("arial", 25)
font_instructions = pygame.font.SysFont("arial", 20)
font_congratulations = pygame.font.SysFont("arial", 40)  # Larger font for congratulations
 
 
# Color definitions
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GREEN = (0, 255, 0)  # Green color for congratulations message
 
 
# Error message display variables
error_message = ""
display_error_until = 0
congratulations_message = ""
 
 
def get_coordinate(pos):
   global x_coordinate, y_coordinate
   x_coordinate = int(pos[0] // cell_width)
   y_coordinate = int(pos[1] // cell_width)
 
 
def draw_selection_box():
   for i in range(2):
       pygame.draw.line(screen, COLOR_RED, (x_coordinate * cell_width - 3, (y_coordinate + i) * cell_width),
                        (x_coordinate * cell_width + cell_width + 3, (y_coordinate + i) * cell_width), 7)
       pygame.draw.line(screen, COLOR_RED, ((x_coordinate + i) * cell_width, y_coordinate * cell_width),
                        ((x_coordinate + i) * cell_width, y_coordinate * cell_width + cell_width), 7)
 
 
def draw_sudoku_grid():
   for i in range(9):
       for j in range(9):
           num, is_initial = sudoku_grid[j][i]
           pygame.draw.rect(screen, COLOR_WHITE, (i * cell_width, j * cell_width, cell_width, cell_width))
           if num != 0:
               text_color = COLOR_BLUE if is_initial else COLOR_RED
               text_value = font_user_input.render(str(num), True, text_color)
               screen.blit(text_value, (i * cell_width + 15, j * cell_width + 15))
   for i in range(10):
       thick = 7 if i % 3 == 0 else 1
       pygame.draw.line(screen, COLOR_BLACK, (0, i * cell_width), (500, i * cell_width), thick)
       pygame.draw.line(screen, COLOR_BLACK, (i * cell_width, 0), (i * cell_width, 500), thick)
 
 
def display_error_message(message):
   global error_message, display_error_until
   error_message = message
   display_error_until = pygame.time.get_ticks() + 2000  # Display the message for 2 seconds
 
 
def check_error_message():
   global error_message
   if pygame.time.get_ticks() > display_error_until:
       error_message = ""
 
 
def is_valid_move(grid, i, j, val):
   val = int(val)
   for it in range(9):
       if grid[i][it][0] == val or grid[it][j][0] == val:
           return False
   subgrid_x, subgrid_y = 3 * (i // 3), 3 * (j // 3)
   for i in range(subgrid_x, subgrid_x + 3):
       for j in range(subgrid_y, subgrid_y + 3):
           if grid[i][j][0] == val:
               return False
   return True
 
 
def check_puzzle_solved(grid):
   for row in grid:
       if sorted(num for num, _ in row) != list(range(1, 10)):
           return False
   for col in range(9):
       if sorted(grid[row][col][0] for row in range(9)) != list(range(1, 10)):
           return False
   for x in range(0, 9, 3):
       for y in range(0, 9, 3):
           subgrid = [grid[y + i][x + j][0] for i in range(3) for j in range(3)]
           if sorted(subgrid) != list(range(1, 10)):
               return False
   return True
 
 
def display_instructions():
   instruction_text = font_instructions.render("PRESS R TO RESET / N FOR NEW GAME", True, COLOR_BLACK)
   screen.blit(instruction_text, (20, 520))
 
 
def generate_sudoku_puzzle():
   global sudoku_grid, initial_sudoku_grid
   sudoku_grid = [[(0, False) for _ in range(9)] for _ in range(9)]
   for _ in range(30):
       i, j = random.randint(0, 8), random.randint(0, 8)
       num = random.randint(1, 9)
       if is_valid_move(sudoku_grid, i, j, num):
           sudoku_grid[i][j] = (num, True)
   initial_sudoku_grid = [row[:] for row in sudoku_grid]
 
 
def reset_sudoku_puzzle():
   global sudoku_grid, initial_sudoku_grid
   sudoku_grid = [row[:] for row in initial_sudoku_grid]
 
 
generate_sudoku_puzzle()
 
 
# Main game loop
run = True
while run:
   screen.fill(COLOR_WHITE)
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           run = False
       if event.type == pygame.MOUSEBUTTONDOWN:
           pos = pygame.mouse.get_pos()
           get_coordinate(pos)
       if event.type == pygame.KEYDOWN:
           if pygame.K_1 <= event.key <= pygame.K_9:
               user_input_value = str(event.key - 48)  # Convert pygame key to string representation of integer
           elif event.key == pygame.K_r:
               reset_sudoku_puzzle()
           elif event.key == pygame.K_n:
               generate_sudoku_puzzle()
           elif event.key == pygame.K_UP:
               y_coordinate = (y_coordinate - 1) % 9
           elif event.key == pygame.K_DOWN:
               y_coordinate = (y_coordinate + 1) % 9
           elif event.key == pygame.K_LEFT:
               x_coordinate = (x_coordinate - 1) % 9
           elif event.key == pygame.K_RIGHT:
               x_coordinate = (x_coordinate + 1) % 9
 
 
   if user_input_value:
       num, is_initial = sudoku_grid[y_coordinate][x_coordinate]
       if not is_initial:
           if num == int(user_input_value):
               sudoku_grid[y_coordinate][x_coordinate] = (0, False)  # Clear the cell
           elif is_valid_move(sudoku_grid, y_coordinate, x_coordinate, user_input_value):
               sudoku_grid[y_coordinate][x_coordinate] = (int(user_input_value), False)  # Update with new input
               if check_puzzle_solved(sudoku_grid):
                   congratulations_message = "Congratulations! Puzzle Solved!"
           else:
               display_error_message("Invalid move!")
       user_input_value = ''
 
 
   draw_sudoku_grid()
   draw_selection_box()
   display_instructions()
 
 
   check_error_message()
   if error_message:
       error_text = font_instructions.render(error_message, True, COLOR_RED)
       screen.blit(error_text, (20, 550))
   if congratulations_message:
       congrats_text = font_congratulations.render(congratulations_message, True, COLOR_GREEN)
       text_rect = congrats_text.get_rect(center=(250, 300))
       screen.blit(congrats_text, text_rect)
 
 
   pygame.display.update()
 
 
pygame.quit()
