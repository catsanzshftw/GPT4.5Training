import pygame, sys, numpy as np
from pygame.locals import *

# --- Vibe Setup ---
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('NES Pong Vibes')
clock = pygame.time.Clock()
FPS = 60

# --- NES Palette ---
BLACK, WHITE, GRAY = (0, 0, 0), (248, 248, 248), (124, 124, 124)
font = pygame.font.SysFont(None, 36)

# --- Synthesized NES beep sounds ---
def beep(freq=440, duration=100):
    sample_rate = 44100
    n_samples = int(sample_rate * duration / 1000)
    wave = 4096 * np.sign(np.sin(2.0 * np.pi * freq * np.arange(n_samples) / sample_rate))
    sound = pygame.mixer.Sound(wave.astype(np.int16))
    sound.play()

# --- Paddle & Ball Setup ---
paddle_size, ball_size = (10, 60), (12, 12)
p1 = pygame.Rect(20, SCREEN_HEIGHT//2 - paddle_size[1]//2, *paddle_size)
p2 = pygame.Rect(SCREEN_WIDTH - 30, SCREEN_HEIGHT//2 - paddle_size[1]//2, *paddle_size)
ball = pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, *ball_size)
ball_speed = [4, 4]
paddle_speed = 5

# --- Score Setup ---
score_p1, score_p2 = 0, 0

# --- Game Over Logic ---
def game_over(winner):
    while True:
        screen.fill(BLACK)
        text = font.render(f"Player {winner} wins! Play Again? (Y/N)", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_y:
                    main()
                if event.key == K_n:
                    pygame.quit()
                    sys.exit()

# --- Main Game Loop ---
def main():
    global score_p1, score_p2
    score_p1, score_p2 = 0, 0
    ball.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        # Player paddle with mouse
        mouse_y = pygame.mouse.get_pos()[1]
        p1.centery = mouse_y
        if p1.top < 0: p1.top = 0
        if p1.bottom > SCREEN_HEIGHT: p1.bottom = SCREEN_HEIGHT

        # Basic AI for paddle 2
        if p2.centery < ball.centery and p2.bottom < SCREEN_HEIGHT: p2.y += paddle_speed
        if p2.centery > ball.centery and p2.top > 0: p2.y -= paddle_speed

        # Ball movement
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        # Ball collision with top/bottom walls
        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            ball_speed[1] *= -1
            beep(880)

        # Ball collision with paddles
        if ball.colliderect(p1) or ball.colliderect(p2):
            ball_speed[0] *= -1
            beep(440)

        # Ball out of bounds and scoring
        if ball.left <= 0:
            score_p2 += 1
            ball.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
            beep(220)
        if ball.right >= SCREEN_WIDTH:
            score_p1 += 1
            ball.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
            beep(220)

        if score_p1 == 5: game_over(1)
        if score_p2 == 5: game_over(2)

        # NES-style Graphics
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, p1)
        pygame.draw.rect(screen, WHITE, p2)
        pygame.draw.rect(screen, GRAY, ball)
        pygame.draw.aaline(screen, GRAY, (SCREEN_WIDTH//2, 0), (SCREEN_WIDTH//2, SCREEN_HEIGHT))

        # Score Display
        score_text = font.render(f"{score_p1} : {score_p2}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 20))

        pygame.display.flip()
        clock.tick(FPS)

main()
