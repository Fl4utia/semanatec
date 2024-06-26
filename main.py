import pygame
import random

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
SNAKE_SIZE = 20
INITIAL_SPEED = 10
ZOOM_FACTOR = 3

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Direcciones
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Preguntas disponibles
MATH_QUESTIONS = [
    ("1 + 1", 2, [1, 2, 3, 4]),
    ("3 - 1", 2, [1, 2, 3, 4]),
    ("2 + 3", 5, [3, 4, 5, 6]),
    ("4 - 2", 2, [1, 2, 3, 4]),
    ("5 + 1", 6, [4, 5, 6, 7]),
    ("6 - 3", 3, [1, 2, 3, 4]),
    ("4 + 2", 6, [5, 6, 7, 8]),
    ("7 - 4", 3, [1, 2, 3, 4]),
    ("5 + 3", 8, [6, 7, 8, 9]),
    ("8 - 5", 3, [1, 2, 3, 4]),
    ("2 + 1", 3, [2, 3, 4, 5]),
    ("3 - 2", 1, [0, 1, 2, 3]),
    ("4 + 1", 5, [3, 4, 5, 6]),
    ("5 - 3", 2, [1, 2, 3, 4]),
    ("6 + 1", 7, [5, 6, 7, 8]),
    ("7 - 5", 2, [1, 2, 3, 4]),
    ("8 + 2", 10, [7, 8, 9, 10]),
    ("9 - 3", 6, [4, 5, 6, 7]),
    ("10 + 1", 11, [9, 10, 11, 12]),
    ("10 - 8", 2, [0, 1, 2, 3])
]

# Clase del juego
class SnakeGame:
    def __init__(self):
        # Configuracion inicial / constructor
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("CowQuest")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.snake = Snake()
        self.food = Food()
        self.speed = INITIAL_SPEED
        self.direction = RIGHT
        self.score = 0
        self.game_over = False
        self.answered_correctly = False

        # Imagen de fondo
        self.grass_bg = pygame.image.load("grass.jpeg").convert()
        self.grass_bg = pygame.transform.scale(self.grass_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def handle_events(self):
        # Manejar las teclas
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.direction = RIGHT

    def update(self):
        self.snake.move(self.direction)
        if self.snake.check_collision():
            self.game_over = True
        if self.snake.body[0] == self.food.position:
            question, answer, options = random.choice(MATH_QUESTIONS)
            self.display_question(question, answer, options)
            
        if self.snake.body[0] == self.food.position and self.answered_correctly:
            self.snake.grow()
            self.food.spawn()
            self.speed += 1
            self.answered_correctly = False

    # Desplegar preguntas
    def display_question(self, question, answer, options):
        answered = False
        apple_img = pygame.image.load("apple.png").convert_alpha()
        apple_img = pygame.transform.scale(apple_img, (GRID_SIZE, GRID_SIZE))
        option_rects = []
        answer_index = options.index(answer)

        # Habilitar click para contestar pregunta
        while not answered:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, option_rect in enumerate(option_rects):
                        if option_rect.collidepoint(mouse_pos):
                            if i == answer_index:
                                self.score += 1
                                self.answered_correctly = True
                            answered = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        answered = True
                
            self.screen.blit(self.grass_bg, (0, 0))
            question_text = self.font.render(question, True, BLACK)
            self.screen.blit(question_text, (SCREEN_WIDTH / 2 - question_text.get_width() / 2, SCREEN_HEIGHT / 2 - 50))
            
            for i, option in enumerate(options):
                apple_count = option
                x_offset = SCREEN_WIDTH / 2 - (GRID_SIZE + 5) * apple_count / 2
                for j in range(apple_count):
                    self.screen.blit(apple_img, (x_offset + j * (GRID_SIZE + 5), SCREEN_HEIGHT / 2 + i * 30))
                option_rect = pygame.Rect(x_offset, SCREEN_HEIGHT / 2 + i * 30, (GRID_SIZE + 5) * apple_count, GRID_SIZE)
                option_rects.append(option_rect)
            
            pygame.display.flip()
    
    # Dibujar el contenido
    def draw(self):
        self.screen.blit(self.grass_bg, (0, 0))

        self.snake.draw(self.screen, self.direction)
        self.food.draw(self.screen)

        text = self.font.render("Puntaje: " + str(self.score), True, BLACK)
        self.screen.blit(text, (10, 10))

        pygame.display.flip()

    # Ejecutar código
    def run(self):
        while True:
            # Llevar a cabo el juego
            while not self.game_over:
                self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(self.speed)
            # Desplegar menu final
            self.screen.blit(self.grass_bg, (0, 0))
            game_over_text = self.font.render("Perdiste!", True, BLACK)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
            self.screen.blit(game_over_text, game_over_rect)

            score_text = self.font.render("Puntaje: " + str(self.score), True, BLACK)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            self.screen.blit(score_text, score_rect)

            play_again_text = self.font.render("Presiona V para volver a jugar | Presiona S para salir", True, BLACK)
            play_again_rect = play_again_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
            self.screen.blit(play_again_text, play_again_rect)

            pygame.display.flip()

            while self.game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_s:
                            pygame.quit()
                            return
                        elif event.key == pygame.K_v:
                            self.reset()
                            self.game_over = False
    # reiniciar variables
    def reset(self):
        self.snake = Snake()
        self.food = Food()
        self.speed = INITIAL_SPEED
        self.direction = RIGHT
        self.score = 0
        self.game_over = False
        self.answered_correctly = False

class Snake:
    def __init__(self):
        # Datos de las vacas
        self.body = [(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)]
        self.length = 1
        self.cow_img_up = pygame.image.load("cow_walk_top.png").convert_alpha()
        self.cow_img_down = pygame.image.load("cow_walk_bottom.png").convert_alpha()
        self.cow_img_left = pygame.image.load("cow_walk_left.png").convert_alpha()
        self.cow_img_right = pygame.image.load("cow_walk_right.png").convert_alpha()
        self.cow_img_size = (GRID_SIZE * ZOOM_FACTOR, GRID_SIZE * ZOOM_FACTOR)
        self.cow_img_up = pygame.transform.scale(self.cow_img_up, self.cow_img_size)
        self.cow_img_down = pygame.transform.scale(self.cow_img_down, self.cow_img_size)
        self.cow_img_left = pygame.transform.scale(self.cow_img_left, self.cow_img_size)
        self.cow_img_right = pygame.transform.scale(self.cow_img_right, self.cow_img_size)
        self.cow_img = self.cow_img_right

    # Cambiar posicion, sprite al mover
    def move(self, direction):
        head = self.body[0]
        x, y = head
        dx, dy = direction
        new_head = (x + dx * GRID_SIZE, y + dy * GRID_SIZE)
        self.body.insert(0, new_head)
        if len(self.body) > self.length:
            self.body.pop()
        if direction == UP:
            self.cow_img = self.cow_img_up
        elif direction == DOWN:
            self.cow_img = self.cow_img_down
        elif direction == LEFT:
            self.cow_img = self.cow_img_left
        elif direction == RIGHT:
            self.cow_img = self.cow_img_right

    def grow(self):
        self.length += 1
    
    # Actualizar vaca
    def draw(self, surface, direction):
        for i, segment in enumerate(self.body):
            if direction == UP:
                adjusted_pos = (segment[0], segment[1] + i * (GRID_SIZE // 2))
            elif direction == DOWN:
                adjusted_pos = (segment[0], segment[1] - i * (GRID_SIZE // 2))
            elif direction == LEFT:
                adjusted_pos = (segment[0] + i * (GRID_SIZE), segment[1])
            elif direction == RIGHT:
                adjusted_pos = (segment[0] - i * (GRID_SIZE), segment[1])
            zoomed_segment = (adjusted_pos[0] - GRID_SIZE * (ZOOM_FACTOR - 1) / 2, adjusted_pos[1] - GRID_SIZE * (ZOOM_FACTOR - 1) / 2)
            surface.blit(self.cow_img, zoomed_segment)
    # Checar si la vaca intersecta
    def check_collision(self):
        head = self.body[0]
        if head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT:
            return True
        for segment in self.body[1:]:
            if head == segment:
                return True
        return False

class Food:
    # Manzana
    def __init__(self):
        self.apple_img = pygame.image.load("apple.png").convert_alpha()
        self.apple_img = pygame.transform.scale(self.apple_img, (GRID_SIZE, GRID_SIZE))
        self.position = (random.randint(0, SCREEN_WIDTH // GRID_SIZE - 1) * GRID_SIZE,
                         random.randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE)
    # Desplegar manzana en el mapa
    def spawn(self):
        center_range_x = (SCREEN_WIDTH // 2 - 100, SCREEN_WIDTH // 2 + 100)
        center_range_y = (SCREEN_HEIGHT // 2 - 100, SCREEN_HEIGHT // 2 + 100)
        
        x = random.randint(center_range_x[0] // GRID_SIZE, center_range_x[1] // GRID_SIZE) * GRID_SIZE
        y = random.randint(center_range_y[0] // GRID_SIZE, center_range_y[1] // GRID_SIZE) * GRID_SIZE
        
        self.position = (x, y)

    def draw(self, surface):
        surface.blit(self.apple_img, self.position)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
