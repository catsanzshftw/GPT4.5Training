import pygame, sys, random, numpy as np
from pygame.locals import *

# Pygame setup
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Breakout - PS3 Vibes Edition')
clock = pygame.time.Clock()
FPS = 60

# Colors
BLACK, WHITE, NEON = (10, 10, 10), (230, 230, 230), (0, 255, 170)

# Synthesized beep sounds
def beep(freq, duration=100):
    sample_rate = 44100
    n_samples = int(sample_rate * duration / 1000)
    buf = np.array([4096 * np.sin(2.0 * np.pi * freq * x / sample_rate) for x in range(n_samples)]).astype(np.int16)
    sound = pygame.mixer.Sound(buffer=buf)
    sound.play()

# Paddle setup
paddle = pygame.Rect(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT - 50, 120, 15)

# Ball setup
ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 15, 15)
ball_speed = [5, -5]

# Bricks setup
bricks = []
rows, cols = 6, 10
brick_width, brick_height = 75, 25
for row in range(rows):
    for col in range(cols):
        brick = pygame.Rect(col * (brick_width + 5) + 35, row * (brick_height + 5) + 35, brick_width, brick_height)
        bricks.append(brick)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    paddle.x += (keys[K_RIGHT] - keys[K_LEFT]) * 8
    paddle.x = max(0, min(SCREEN_WIDTH - paddle.width, paddle.x))

    ball.left += ball_speed[0]
    ball.top += ball_speed[1]

    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        ball_speed[0] *= -1
        beep(600)
    if ball.top <= 0:
        ball_speed[1] *= -1
        beep(600)

    if ball.colliderect(paddle):
        ball_speed[1] *= -1
        beep(800)

    for brick in bricks[:]:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed[1] *= -1
            beep(1200)

    if ball.bottom >= SCREEN_HEIGHT:
        beep(300, 400)
        ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        ball_speed = [random.choice([-5, 5]), -5]

    screen.fill(BLACK)

    pygame.draw.rect(screen, NEON, paddle, border_radius=10)
    pygame.draw.ellipse(screen, WHITE, ball)

    for brick in bricks:
        pygame.draw.rect(screen, (random.randint(0,255), random.randint(0,255), random.randint(0,255)), brick, border_radius=8)

    pygame.display.flip()
    clock.tick(FPS)

    if not bricks:
        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 74)
        text = font.render('YOU WIN! Play Again? Y/N', True, NEON)
        screen.blit(text, (60, SCREEN_HEIGHT // 2 - 50))
        pygame.display.flip()
        pygame.mixer.Sound.play
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_y:
                        bricks = [pygame.Rect(col * (brick_width + 5) + 35, row * (brick_height + 5) + 35, brick_width, brick_height) for row in range(rows) for col in range(cols)]
                        ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                        ball_speed = [5, -5]
                        waiting = False
                    elif event.key == K_n:
                        pygame.quit()
                        sys.exit()
