import pygame
import asyncio

# Initialize Pygame
pygame.init()

# Window dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basic Pong Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle properties
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 5

# Ball properties
BALL_RADIUS = 10
BALL_SPEED_X = 4
BALL_SPEED_Y = 4

# Paddle class
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 0

    def move(self):
        self.rect.y += self.speed
        # Keep paddle on screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

# Ball class
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS*2, BALL_RADIUS*2)
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off top and bottom
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y = -self.speed_y

    def draw(self):
        pygame.draw.ellipse(screen, WHITE, self.rect)

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = -self.speed_x  # Change direction

# Create objects
left_paddle = Paddle(20, HEIGHT//2 - PADDLE_HEIGHT//2)
right_paddle = Paddle(WIDTH - 30, HEIGHT//2 - PADDLE_HEIGHT//2)
ball = Ball()

# Clock and frame rate
clock = pygame.time.Clock()
FPS = 60

# Async main function for pygbag compatibility
async def main():
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Key down events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    left_paddle.speed = -PADDLE_SPEED
                if event.key == pygame.K_s:
                    left_paddle.speed = PADDLE_SPEED
                if event.key == pygame.K_UP:
                    right_paddle.speed = -PADDLE_SPEED
                if event.key == pygame.K_DOWN:
                    right_paddle.speed = PADDLE_SPEED

            # Key up events
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    left_paddle.speed = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    right_paddle.speed = 0

        # Move paddles and ball
        left_paddle.move()
        right_paddle.move()
        ball.move()

        # Ball collision with paddles
        if ball.rect.colliderect(left_paddle.rect) and ball.speed_x < 0:
            ball.speed_x = -ball.speed_x
        if ball.rect.colliderect(right_paddle.rect) and ball.speed_x > 0:
            ball.speed_x = -ball.speed_x

        # Ball goes out of bounds (left or right)
        if ball.rect.left <= 0 or ball.rect.right >= WIDTH:
            ball.reset()

        # Draw everything
        screen.fill(BLACK)
        left_paddle.draw()
        right_paddle.draw()
        ball.draw()

        pygame.display.flip()
        clock.tick(FPS)

        # Yield control for pygbag async
        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())