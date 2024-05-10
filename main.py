import pygame
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
SNAKE_SIZE = 20
INITIAL_SPEED = 10

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
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
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.snake = Snake()
        self.food = Food()
        self.speed = INITIAL_SPEED
        self.direction = RIGHT
        self.score = 0
        self.game_over = False

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
        self.screen.fill(WHITE)
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        text = self.font.render("Score: " + str(self.score), True, BLACK)
        self.screen.blit(text, (10, 10))
        pygame.display.flip()

    def run(self):
        while not self.game_over:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.speed)
        pygame.quit()

class Snake:
    def __init__(self):
        self.body = [(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)]
        self.length = 1
        self.cow_img = pygame.image.load("vaca_1.gif").convert_alpha()
        self.cow_img = pygame.transform.scale(self.cow_img, (SNAKE_SIZE, SNAKE_SIZE))

    def move(self, direction):
        head = self.body[0]
        x, y = head
        dx, dy = direction
        new_head = (x + dx * GRID_SIZE, y + dy * GRID_SIZE)
        self.body.insert(0, new_head)
        if len(self.body) > self.length:
            self.body.pop()

    def grow(self):
        self.length += 1

    def draw(self, surface):
        for i, segment in enumerate(self.body):
            if i == 0:
                surface.blit(self.cow_img, (segment[0], segment[1]))
            else:
                surface.blit(self.cow_img, (segment[0], segment[1]))

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
        self.position = (random.randint(0, SCREEN_WIDTH // GRID_SIZE - 1) * GRID_SIZE,
                         random.randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE)

    def spawn(self):
        self.position = (random.randint(0, SCREEN_WIDTH // GRID_SIZE - 1) * GRID_SIZE,
                         random.randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
