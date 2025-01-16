import pygame
import sys
import random


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20


BALL_RADIUS = 10


BRICK_WIDTH = 75
BRICK_HEIGHT = 30


font = pygame.font.Font(None, 36)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Breaker")


clock = pygame.time.Clock()


def draw_text(text, color, x, y, center=False):

    label = font.render(text, True, color)
    if center:
        rect = label.get_rect(center=(x, y))
        screen.blit(label, rect)
    else:
        screen.blit(label, (x, y))


def draw_button(text, x, y, width, height, inactive_color, active_color, action=None):

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))
    
    draw_text(text, WHITE, x + width // 2, y + height // 2, center=True)


def start_menu():

    menu_running = True
    while menu_running:
        screen.fill(BLACK)
        draw_text("Brick Breaker Game", WHITE, SCREEN_WIDTH // 2, 100, center=True)
        draw_button("Start Playing", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50, RED, BLUE, game_loop)
        draw_button("Quit", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70, 200, 50, RED, BLUE, quit_game)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        pygame.display.flip()
        clock.tick(60)


def quit_game():
    pygame.quit()
    sys.exit()


def game_loop():
    paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
    paddle_y = SCREEN_HEIGHT - 50
    paddle_speed = 10


    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2
    ball_dx = 4 * random.choice((-1, 1))
    ball_dy = -4


    bricks = []
    rows = 5
    cols = SCREEN_WIDTH // BRICK_WIDTH
    for row in range(rows):
        for col in range(cols):
            bricks.append(pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT))

    score = 0

    running = True
    while running:
        screen.fill(BLACK)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < SCREEN_WIDTH - PADDLE_WIDTH:
            paddle_x += paddle_speed
        

        ball_x += ball_dx
        ball_y += ball_dy
        

        if ball_x <= 0 or ball_x >= SCREEN_WIDTH - BALL_RADIUS:
            ball_dx *= -1
        if ball_y <= 0:
            ball_dy *= -1
        

        if (paddle_y <= ball_y + BALL_RADIUS <= paddle_y + PADDLE_HEIGHT and
                paddle_x <= ball_x <= paddle_x + PADDLE_WIDTH):
            ball_dy *= -1
        

        for brick in bricks[:]:
            if brick.collidepoint(ball_x, ball_y):
                bricks.remove(brick)
                ball_dy *= -1
                score += 10


        if ball_y > SCREEN_HEIGHT:
            running = False  # Game over
        

        pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))

        pygame.draw.circle(screen, RED, (ball_x, ball_y), BALL_RADIUS)
        

        for brick in bricks:
            pygame.draw.rect(screen, BLUE, brick)
        

        draw_text(f"Score: {score}", WHITE, 10, 10)
        
        pygame.display.flip()
        clock.tick(60)
    

    start_menu()


start_menu()
