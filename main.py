import pygame
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
SNAKE_SIZE = 20
INITIAL_SPEED = 10
ZOOM_FACTOR = 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class SnakeGame:
    def __init__(self):
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

        # Load grass background image and scale it
        self.grass_bg = pygame.image.load("grass.jpeg").convert()
        self.grass_bg = pygame.transform.scale(self.grass_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def handle_events(self):
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
            self.snake.grow()
            self.score += 1
            self.food.spawn()
            self.speed += 1

    def draw(self):
        # Draw grass background
        self.screen.blit(self.grass_bg, (0, 0))

        # Draw snake and food
        self.snake.draw(self.screen, self.direction)
        self.food.draw(self.screen)

        # Draw score
        text = self.font.render("Puntaje: " + str(self.score), True, BLACK)
        self.screen.blit(text, (10, 10))

        pygame.display.flip()

    def run(self):
        while True:
            while not self.game_over:
                self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(self.speed)

            self.screen.fill(WHITE)
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

    def reset(self):
        self.snake = Snake()
        self.food = Food()
        self.speed = INITIAL_SPEED
        self.direction = RIGHT
        self.score = 0
        self.game_over = False

class Snake:
    def __init__(self):
        self.body = [(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)]
        self.length = 1
        self.cow_img_up = pygame.image.load("cow_walk_top.png").convert_alpha()
        self.cow_img_down = pygame.image.load("cow_walk_bottom.png").convert_alpha()
        self.cow_img_left = pygame.image.load("cow_walk_left.png").convert_alpha()
        self.cow_img_right = pygame.image.load("cow_walk_right.png").convert_alpha()
        self.cow_img_size = (GRID_SIZE * ZOOM_FACTOR, GRID_SIZE * ZOOM_FACTOR)  # Zoom the image
        self.cow_img_up = pygame.transform.scale(self.cow_img_up, self.cow_img_size)
        self.cow_img_down = pygame.transform.scale(self.cow_img_down, self.cow_img_size)
        self.cow_img_left = pygame.transform.scale(self.cow_img_left, self.cow_img_size)
        self.cow_img_right = pygame.transform.scale(self.cow_img_right, self.cow_img_size)
        self.cow_img = self.cow_img_right

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

    def check_collision(self):
        head = self.body[0]
        if head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT:
            return True
        for segment in self.body[1:]:
            if head == segment:
                return True
        return False

class Food:
    def __init__(self):
        self.apple_img = pygame.image.load("apple.png").convert_alpha()
        self.apple_img = pygame.transform.scale(self.apple_img, (GRID_SIZE, GRID_SIZE))
        self.position = (random.randint(0, SCREEN_WIDTH // GRID_SIZE - 1) * GRID_SIZE,
                         random.randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE)

    def spawn(self):
        x = random.randint(1, (SCREEN_WIDTH // GRID_SIZE - 2)) * GRID_SIZE
        y = random.randint(1, (SCREEN_HEIGHT // GRID_SIZE - 2)) * GRID_SIZE
        self.position = (x, y)

    def draw(self, surface):
        surface.blit(self.apple_img, self.position)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
