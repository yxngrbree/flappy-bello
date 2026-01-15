import pygame
import sys
import random
from pygame import image

pygame.init()

WIDTH, HEIGHT = 1200, 600
BIRD_SIZE = 100
BACKGROUND_IMAGE_PATH = "b4.png"
BG = (34, 139, 34)
GROUND_COLOR = (34, 139, 34)
GRAVITY = 1
JUMP_VELOCITY = -10

pygame.mixer.music.load("gs.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

coin_sound = pygame.mixer.Sound("coin.mp3")
game_over_sound = pygame.mixer.Sound("go.mp3")

pixel_font = pygame.font.Font("PressStart2P.ttf", 16)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FlappyBello")

bird_options = [
    {"name": "", "image_path": ""}, # insert your own images to play
    {"name": "", "image_path": ""},
    {"name": "", "image_path": ""},
    {"name": "", "image_path": ""},
    {"name": "", "image_path": ""},
    {"name": "", "image_path": ""},
]

selected_bird = None

COIN_IMAGE_PATH = "coinn.png"

coin_image = pygame.image.load(COIN_IMAGE_PATH).convert_alpha()
coin_image = pygame.transform.scale(coin_image, (30, 30))

coin = {"x": 0, "y": 0, "visible": True}

def show_start_menu():
    font_large = pygame.font.Font("PressStart2P.ttf", 20)
    font_small = pygame.font.Font("PressStart2P.ttf", 30)

    start_image = pygame.image.load("start.png").convert_alpha()
    start_image = pygame.transform.scale(start_image, (WIDTH, HEIGHT))
    
    screen.blit(start_image, (0, 0))
    
    pygame.display.flip()

    start_text_shown = False
    clock = pygame.time.Clock()

    blink_timer = 0
    blink_interval = 30  
    
    while not start_text_shown:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_text_shown = True

        if not start_text_shown:
            text_small = font_small.render("Click to Start", True, (0, 0, 0))
            
            blink_timer += 1
            if blink_timer >= blink_interval:
                text_small = font_small.render("Click to Start", True, (255, 0, 0))  
                blink_timer = 0

            text_rect = text_small.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            screen.blit(text_small, text_rect)

        pygame.display.flip()
        clock.tick(30)

    return True

def choose_bird():
    global selected_bird
    font = pygame.font.Font("PressStart2P.ttf", 30)
    selected_text_color = (255, 0, 0)
    regular_text_color = (0, 0, 0)

    title_text = font.render("Zgjidhni 1 zog nga koteci:", True, regular_text_color)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title_text, title_rect)

    for i, bird in enumerate(bird_options):
        text = font.render(f"{i + 1}. {bird['name']}", True, regular_text_color)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 4 + (i + 1) * 40))
        screen.blit(text, text_rect)

    pygame.display.flip()

    selected_bird = None
    while selected_bird is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, bird in enumerate(bird_options):
                    option_rect = pygame.Rect(WIDTH // 4, HEIGHT // 4 + (i + 1) * 40, WIDTH // 2, 40)
                    if option_rect.collidepoint(mouse_x, mouse_y):
                        selected_bird = bird
                        return

    pygame.display.flip()

def draw_bird(x, y):
    bird_image = pygame.image.load(selected_bird["image_path"]).convert_alpha()
    bird_image = pygame.transform.scale(bird_image, (BIRD_SIZE, BIRD_SIZE))
    screen.blit(bird_image, (x, y))

def draw_pipe(pipe):
    pipe_image = image.load("art.png").convert_alpha()
    pipe_image = pygame.transform.scale(pipe_image, (pipe[2], pipe[3]))
    
    if pipe[1] == 0:
        pipe_image = pygame.transform.flip(pipe_image, False, True)  
        screen.blit(pipe_image, (pipe[0], 0))
    else:
        screen.blit(pipe_image, (pipe[0], pipe[1]))

def game_over():
    font = pygame.font.Font("PressStart2P.ttf", 18)
    text = font.render("Game Over,", True, (255, 0, 0))
    restart_text = font.render("Click to Restart", True, (0, 0, 0))

    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))

    screen.blit(text, text_rect)
    screen.blit(restart_text, (restart_rect.x, restart_rect.y + 20))

    pygame.display.flip()
    pygame.mixer.music.stop()
    game_over_sound.play()

   
    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting_for_restart = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting_for_restart = False

        pygame.time.Clock().tick(30)

 
    reset_game_state()

def reset_game_state():
    global bird_y, bird_velocity, pipes
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = []
    pygame.mixer.music.play(-1)

def draw_clouds():
    for _ in range(3):
        cloud_x = random.randint(0, WIDTH)
        cloud_y = random.randint(20, HEIGHT // 2)
      

background_image = pygame.image.load(BACKGROUND_IMAGE_PATH).convert_alpha()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

start_clicked = False
bird_options_displayed = False

while not start_clicked:
    start_clicked = show_start_menu()
    
    screen.blit(background_image, (0, 0))
    draw_clouds()
    pygame.display.flip()

    if start_clicked:
        bird_options_displayed = True

    while bird_options_displayed:
        choose_bird()
        bird_options_displayed = False

clock = pygame.time.Clock()

bird_y = HEIGHT // 2
bird_velocity = 0
pipes = []


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird_velocity = JUMP_VELOCITY

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        bird_velocity = JUMP_VELOCITY

    bird_y += bird_velocity
    bird_velocity += GRAVITY

    if len(pipes) == 0 or pipes[-1][0] < WIDTH - 300:
        pipe_height = random.randint(50, HEIGHT - 300)
        pipes.append([WIDTH, 0, 100, pipe_height])
        pipes.append([WIDTH, pipe_height + 300, 100, HEIGHT - pipe_height - 300])

    bird_rect = pygame.Rect(WIDTH // 3, bird_y, BIRD_SIZE, BIRD_SIZE)


    if not coin["visible"] and random.randint(0, 100) < 2:
        coin["visible"] = True
        coin["x"] = WIDTH
        coin["y"] = random.randint(50, HEIGHT - 100)

    if coin["visible"]:
        coin["x"] -= 5
        coin["y"] += random.choice([-1, 1]) * random.randint(1, 5)

        if WIDTH // 3 < coin["x"] < WIDTH // 3 + BIRD_SIZE and bird_y < coin["y"] < bird_y + BIRD_SIZE:
            coin["visible"] = False
            coin_sound.play()

        if coin["x"] < -30:
            coin["visible"] = False

        screen.blit(coin_image, (coin["x"], coin["y"]))

    for pipe in pipes:
        pipe[0] -= 5
        pipe_rect = pygame.Rect(pipe[0], pipe[1], pipe[2], pipe[3])
        if bird_rect.colliderect(pipe_rect):
            game_over()

    pipes = [pipe for pipe in pipes if pipe[0] + pipe[2] > 0]

    if bird_y < 0 or bird_y + BIRD_SIZE > HEIGHT:
        game_over()

    screen.blit(background_image, (0, 0))

    draw_clouds()
    for pipe in pipes:
        draw_pipe(pipe)
    pygame.draw.rect(screen, GROUND_COLOR, (0, HEIGHT - 20, WIDTH, 20))
    draw_bird(WIDTH // 3, bird_y)
    pygame.display.flip()
    clock.tick(30)
