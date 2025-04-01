import pygame
import sys
import random

pygame.init()
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Pong Game")
clock = pygame.time.Clock()
ball = pygame.Rect(0, 0, 30, 30)
ball.center = (screen_width / 2, screen_height / 2)
cpu_paddle = pygame.Rect(0, 0, 20, 100)
cpu_paddle.centery = screen_height / 2
player_paddle = pygame.Rect(0, 0, 20, 100)
player_paddle.midright = (screen_width, screen_height / 2)
ball_speed_x = 6
ball_speed_y = 6
player_paddle_speed = 0
cpu_paddle_speed = 0
cpu_points, player_points = 0, 0
score_font = pygame.font.Font(None, 100)


def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.x = screen_width / 2
    ball.y = random.randint(10, 100)
    ball_speed_x *= random.choice([-1, 1])
    ball_speed_y *= random.choice([-1, 1])

def point_won(winner):
    global cpu_points, player_points
    if winner == "cpu":
        cpu_points += 1
    if winner == "player":
        player_points += 1

    reset_ball()

def animate_ball():
    global ball_speed_x, ball_speed_y
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.bottom >= screen_height or ball.top <= 0:
        ball_speed_y *= -1

    if ball.right >= screen_width:
        point_won("cpu")
    elif ball.left <= 0:
        point_won("player")

    if ball.colliderect(player_paddle) or ball.colliderect(cpu_paddle):
        ball_speed_x *= -1

def animate_player_paddle():
    player_paddle.y += player_paddle_speed
    if player_paddle.top <= 0:
        player_paddle.top = 0
    if player_paddle.bottom >= screen_height:
        player_paddle.bottom = screen_height

def animate_cpu_paddle():
    global cpu_paddle_speed
    cpu_paddle.y += cpu_paddle_speed
    if cpu_paddle.centery <= ball.centery:
        cpu_paddle_speed += 6
    if cpu_paddle.centery >= ball.centery:
        cpu_paddle_speed -= 6
    
    if cpu_paddle.top <= 0: 
        cpu_paddle.top = 0
    if cpu_paddle.bottom >= screen_height:
        cpu_paddle.bottom = screen_height

while True: 
    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_paddle_speed -= 6
            if event.key == pygame.K_DOWN:
                player_paddle_speed += 6
        
        if event.type == pygame.KEYUP:
            player_paddle_speed = 0


    # change the position of game objects
    animate_ball()
    animate_player_paddle()
    animate_cpu_paddle()

    # draw game objects
    screen.fill('black')
    cpu_score_surface = score_font.render(str(cpu_points), True, 'white')
    player_score_surface = score_font.render(str(player_points), True, 'white')
    screen.blit(cpu_score_surface, (screen_width / 4, 20))
    screen.blit(player_score_surface, (screen_width * 3 / 4, 20))
    pygame.draw.aaline(screen, 'white', (screen_width / 2, 0), (screen_width / 2, screen_height))
    pygame.draw.ellipse(screen, 'white', ball)
    pygame.draw.rect(screen, 'white', cpu_paddle)
    pygame.draw.rect(screen, 'white', player_paddle)

    # update the display
    pygame.display.update()
    clock.tick(60)