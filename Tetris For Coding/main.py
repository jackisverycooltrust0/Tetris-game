#Tetris Game - Pseudocode
#Imports
import pygame
import random
pygame.init()

# Game Settings
WIDTH, HEIGHT, FPS = 300, 500, 24
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()



# Constant Variables
CELLSIZE = 20
ROWS = (HEIGHT - 120)  // CELLSIZE
COLS = WIDTH // CELLSIZE

# Create colors
BLACK = (21, 24, 29)
WHITE = (255, 255, 255)
RED = (252, 91, 122)
BLUE = (31, 25, 76)

# Load / Store my images
ASSETS = {
    1: pygame.image.load("1.png"),
    2: pygame.image.load("2.png"),
    3: pygame.image.load("3.png"),
    4: pygame.image.load("4.png")

}
# Create fonts
style1 = pygame.font.Font(None, 50)
style2 = pygame.font.SysFont('cursive', 25)
# Classes
class TetrisShape:
    # Class Variables
    FIGURES = {
        'I': [[1, 5, 9, 13], [4, 5, 6, 7]],
        'Z': [[4, 5, 9, 10], [2, 6, 5, 9]],
        'S': [[6, 7, 9, 10], [1, 5, 6, 10]],
        'L': [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        'J': [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        'T': [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        'O': [[1, 2, 5, 6]]
    } #dictionary
    
    TYPES = ['I', 'Z', 'S', 'L', 'J', 'T', 'O'] #list

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.choice(self.TYPES)
        self.shape = self.FIGURES[self.type]
        self.color = random.randint(1,4)
        self.rotation = 0
        
    def image(self):
        """The current shape and its rotation

        Returns:
            list: A list representing the current rotation
        """
        return self.shape[self.rotation]
        
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

class Tetris:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.score = 0
        self.level = 1
        self.next = None
        self.gameover = False
        # List comprehension
        self.board = [[0 for j in range(cols)] for i in range(rows)]
        self.new_shape()
        

    def draw_grid(self):
        for i in range(self.rows + 1):
            pygame.draw.line(SCREEN, WHITE, (0, CELLSIZE*i), (WIDTH, CELLSIZE*i))
            
        for j in range(self.cols):
            pygame.draw.line(SCREEN,WHITE,(CELLSIZE*j,0),(CELLSIZE*j, HEIGHT-120))
            
    def new_shape(self):
        if not self.next:
            self.next = TetrisShape(5, 0)
        self.figure = self.next
        self.next = TetrisShape(5, 0)

    #Collision
    def collision(self) -> bool:
        for i in range(4):
            for j in range(4):
                if (i * 4 + j) in self.figure.image():
                    block_row = i + self.figure.y
                    block_col = j + self.figure.x
                    if (block_row >= self.rows or block_col >= self.cols or block_col < 0 or self.board[block_row][block_col]>0):
                        return True
        return False

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if (i*4+j) in self.figure.image():
                    self.board[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.remove_row()
        self.new_shape()
        if self.collision():
            self.gameover = True

    def move_down(self):
        self.figure.y += 1
        if self.collision():
            self.figure.y -= 1
            self.freeze()

    def move_left(self):
        self.figure.x -= 1
        if self.collision():
            self.figure.x +=1
    
    def move_right(self):
        self.figure.x += 1
        if self.collision():
            self.figure.x -=1

    def freefall(self):
        while not self.collision():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def rotate(self):
        orientation = self.figure.rotation
        self.figure.rotate()
        if self.collision():
            self.figure.rotation = orientation

    def remove_row(self):
        rerun = False

        for y in range(self.rows-1, 0, -1):
            for x in range(0, self.cols):
                if self.board[y][x] == 0: 
                    completed = False
            if completed:
                del self.board[y]
                self.board.insert(0, [0 for i in range(self.cols)])
                self.score += 1
                if self.score % 10 == 0:
                    self.level += 1
                rerun = True
        if rerun:
            self.remove_row()
        
    def end_game(self):
        popup = pygame.Rect(50, 140, WIDTH-100, HEIGHT-350)
        pygame.draw.rect(SCREEN, BLACK, popup)
        pygame.draw.rect(SCREEN, RED, popup, 2)
        game_over = style2.render("Press r to restart", True, WHITE)
        option_1 = style2.render("Press q to quit", True, WHITE)

        SCREEN.blit(game_over, (popup.centerx-game_over.get_width()/2, popup.y + 20))
        SCREEN.blit(option1, (popup.centerx-option1.get_width()/2, popup.y + 80))
        SCREEN.blit(option2, (popup.centerx-option2.get_width()/2, popup.y + 110))
        
# Main function
def main():
    counter = 0
    move = True
    space_pressed = False 

    tetris = Tetris(ROWS, COLS)
    run = True
    while run:
        SCREEN.fill(BLUE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        keys = pygame.key.get_pressed()
        if not tetris.gameover:
            if keys[pygame.K_LEFT]:
                tetris.move_left()
            elif keys[pygame.K_RIGHT]:
                tetris.move_right()
            elif keys[pygame.K_DOWN]:
                tetris.move_down()
            elif keys[pygame.K_UP]:
                tetris.rotate()
            elif keys[pygame.K_SPACE]:
                space_pressed = True



        counter += 1
        if counter >= 15000:
            counter = 0
        if move:
            if counter % ((FPS//tetris.level*2)) == 0:
                if not tetris.gameover:
                    if space_pressed:
                        tetris.freefall()
                        space_pressed = False
                    else:
                        tetris.move_down()

            
        tetris.draw_grid()
       
        for x in range(ROWS):
            for y in range(COLS):
                if tetris.board[x][y] > 0:
                    value = tetris.board[x][y]
                    image = ASSETS[value]
                    SCREEN.blit(image, (y*CELLSIZE, x*CELLSIZE))
                    pygame.draw.rect(SCREEN, WHITE, (y*CELLSIZE, x*CELLSIZE, CELLSIZE, CELLSIZE),1)

        if tetris.figure: 
            for i in range(4):
                for j in range(4):
                    if (i * 4+ j)in tetris.figure.image():
                        shape = ASSETS[tetris.figure.color]
                        x = CELLSIZE * (tetris.figure.x + j)
                        y = CELLSIZE * (tetris.figure.y + i)
                        SCREEN.blit(shape, (x,y))
                        pygame.draw.rect(SCREEN, WHITE, (x,y, CELLSIZE, CELLSIZE), 1)

        if tetris.next:
             for i in range(4):
                for j in range(4):
                    if (i * 4+ j)in tetris.next.image():
                        image = ASSETS[tetris.next.color]
                        x = CELLSIZE * (tetris.next.x +j - 4)
                        y = HEIGHT -100 + CELLSIZE *(tetris.next.y + i)
                        SCREEN.blit(image, (x,y))
        if tetris.gameover:
            #END GAME
            tetris.end_game()
            
        score_text = style1.render(f"{tetris.score}", True, WHITE)
        level_text = style2.render(f"level:{tetris.level}", True, WHITE)
        SCREEN.blit(score_text,(250-score_text.get_width()//2, HEIGHT-110))
        SCREEN.blit(level_text,(250-level_text.get_width()//2, HEIGHT-30))
                    
        
        pygame.display.update()
        clock.tick(FPS)
                        

if __name__ in "__main__":
    main()


