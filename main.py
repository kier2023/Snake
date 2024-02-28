import pygame, sys, math
import random
from pygame.math import Vector2
import asyncio

class SNAKE:
    def __init__(self):
        self.body =[Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

        self.head_up = pygame.image.load('graphics/head up.png').convert_alpha()
        self.head_down = pygame.image.load('graphics/head down.png').convert_alpha()
        self.head_right = pygame.image.load('graphics/head right.png').convert_alpha()
        self.head_left = pygame.image.load('graphics/head left.png').convert_alpha()

        self.tail_up = pygame.image.load('graphics/tail up.png').convert_alpha()
        self.tail_down = pygame.image.load('graphics/tail down.png').convert_alpha()
        self.tail_right = pygame.image.load('graphics/tail right.png').convert_alpha()
        self.tail_left = pygame.image.load('graphics/tail left.png').convert_alpha()

        self.body_vertical = pygame.image.load('graphics/body vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('graphics/body horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('graphics/body tr.png').convert_alpha()
        self.body_tl = pygame.image.load('graphics/body tl.png').convert_alpha()
        self.body_br = pygame.image.load('graphics/body br.png').convert_alpha()
        self.body_bl = pygame.image.load('graphics/body bl.png').convert_alpha()

        self.crunc_sound = pygame.mixer.Sound('sounds/eating-sound-effect-36186.wav')

    def draw_snake(self):
        head_image = self.update_head_graphics()
        tail_image = self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)

            if index == 0:
                SCREEN.blit(pygame.transform.scale(head_image, (CELL_SIZE, CELL_SIZE)), block_rect)
            elif index == len(self.body) - 1:
                SCREEN.blit(pygame.transform.scale(tail_image, (CELL_SIZE, CELL_SIZE)), block_rect)
            
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index -1] - block
                if previous_block.x == next_block.x:
                    SCREEN.blit(pygame.transform.scale(self.body_horizontal, (CELL_SIZE, CELL_SIZE)), block_rect)
                elif previous_block.y == next_block.y:
                    SCREEN.blit(pygame.transform.scale(self.body_vertical, (CELL_SIZE, CELL_SIZE)), block_rect)
            
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        SCREEN.blit(pygame.transform.scale(self.body_tl, (CELL_SIZE, CELL_SIZE)), block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        SCREEN.blit(pygame.transform.scale(self.body_tr, (CELL_SIZE, CELL_SIZE)), block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        SCREEN.blit(pygame.transform.scale(self.body_br, (CELL_SIZE, CELL_SIZE)), block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        SCREEN.blit(pygame.transform.scale(self.body_bl, (CELL_SIZE, CELL_SIZE)), block_rect)
        
    def update_head_graphics(self):
        current_direction = self.body[1] - self.body[0]
        if current_direction == Vector2(1, 0): return self.head_left
        elif current_direction == Vector2(-1, 0): return self.head_right
        elif current_direction == Vector2(0, 1): return self.head_up
        elif current_direction == Vector2(0, -1): return self.head_down
        else:
            return self.head_right
    
    def update_tail_graphics(self):
        current_direction = self.body[-2] - self.body[-1]
        if current_direction == Vector2(1, 0): return self.tail_left
        elif current_direction == Vector2(-1, 0): return self.tail_right
        elif current_direction == Vector2(0, 1): return self.tail_up
        elif current_direction == Vector2(0, -1): return self.tail_down
        else:
            return self.tail_right

        
    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False

        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
    
    def add_block(self):
        self.new_block = True
    
    def play_crunch(self):
        self.crunc_sound.play()

class FRUIT:
    def __init__(self):
        self.randomize()
    
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        resized_apple = pygame.transform.scale(APPLE, (CELL_SIZE, CELL_SIZE))
        SCREEN.blit(resized_apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = pygame.math.Vector2(self.x, self.y)

class MAIN:
    def __init__(self):
        self.state = "main menu"
        self.snake = SNAKE()
        self.fruit = FRUIT()
    
    def playing(self):
        self.state = "playing"

    def main_menu(self):
        pass

    def update(self):
        if self.state == "playing":
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()

        elif self.state == "main menu":
            self.handle_menu_input()
    
    def handle_menu_input(self, event):
        if event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.playing()
    
    def draw_elements(self):
        if self.state == "playing":
            self.draw_grass()
            self.snake.draw_snake()
            self.fruit.draw_fruit()
            self.draw_Score()

        elif self.state == "main menu":
            self.draw_main_menu()
    
    def draw_main_menu(self):
        centre_x = SCREEN.get_width() // 2
        centre_y = SCREEN.get_height() // 2
        TEXT = "PRESS ENTER TO START!"
        DEV_TEXT = "© BLUGAME DEVELOPMENT"
        pulsing_factor = 0.5 + 0.5 * math.sin(pygame.time.get_ticks() / 300) 
        menu_text = GAME_FONT.render(TEXT, True, (255, 255, 255))
        alpha_value = int(255 * pulsing_factor)
        pulsing_text = menu_text.copy()
        pulsing_text.set_alpha(alpha_value)
        text_rect = pulsing_text.get_rect(center=(centre_x - 100, centre_y + 45)) 
        menu_text2 = pygame.font.Font(None, 15).render(DEV_TEXT, True, (56, 74, 12)) 

        SCREEN.blit(MAIN_MENU, (-50, -100))
        SCREEN.blit(pulsing_text, text_rect)
        
        # Position the developer text at the bottom right
        dev_text_rect = menu_text2.get_rect(bottomright=(SCREEN.get_width() - 10, SCREEN.get_height() - 10))
        SCREEN.blit(menu_text2, dev_text_rect)
    
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch()
        
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
    
    def check_fail(self):
        if not 0 <= self.snake.body[0].x < CELL_NUMBER or not 0 <= self.snake.body[0].y < CELL_NUMBER:
            self.state = "main menu"
            self.snake = SNAKE()
            self.fruit = FRUIT()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.state = "main menu"
                self.snake = SNAKE()
                self.fruit = FRUIT()

    def game_over(self):
        pygame.quit()
        sys.exit()
    
    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(CELL_NUMBER):
            if row % 2 == 0:
                for col in range(CELL_NUMBER):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(SCREEN, grass_color, grass_rect)
            else:
                for col in range(CELL_NUMBER):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(SCREEN, grass_color, grass_rect)

    def draw_Score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = GAME_FONT.render(score_text, True, (56, 74, 12))
        score_rect = score_surface.get_rect()
        score_rect.topleft = (CELL_SIZE * CELL_NUMBER - 100, CELL_SIZE * CELL_NUMBER - 50) 

        apple_size = 30
        apple_rect = APPLE.get_rect(topleft=(score_rect.right + 10, score_rect.y + (score_rect.height - apple_size) // 2))
        apple_rect.size = (apple_size, apple_size) 

        bg_rect = pygame.Rect(score_rect.left -15, score_rect.top, score_rect.width + apple_rect.width + 40, score_rect.height)
        pygame.draw.rect(SCREEN, (167,209,61), bg_rect)

        SCREEN.blit(score_surface, score_rect)
        SCREEN.blit(pygame.transform.scale(APPLE, (apple_size, apple_size)), apple_rect)
        pygame.draw.rect(SCREEN, (56, 74, 12), bg_rect, 2)

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
CELL_SIZE = 40
CELL_NUMBER = 20
SCREEN = pygame.display.set_mode((CELL_NUMBER * CELL_SIZE,CELL_NUMBER * CELL_SIZE))
CLOCK = pygame.time.Clock()
APPLE = pygame.image.load('graphics/apple.png').convert_alpha()
MAIN_MENU = pygame.image.load('graphics/main_menu.png').convert_alpha()
GAME_FONT = pygame.font.Font('font/Kids Magazine.ttf', 25)

main_game = MAIN()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

async def main_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE and main_game.state == "playing":
                main_game.update()

            if event.type == pygame.KEYDOWN and main_game.state == "playing":
                if event.key == pygame.K_w:  # up
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_s:  # down
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, +1)
                if event.key == pygame.K_a:  # left
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_d:  # right
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(+1, 0)
            elif event.type == pygame.KEYDOWN and main_game.state == "main menu":
                if event.key == pygame.K_RETURN:
                    main_game.playing()

        SCREEN.fill((175, 215, 70))
        if main_game.state == "playing":
            main_game.draw_elements()
        elif main_game.state == "main menu":
            main_game.draw_elements()
        pygame.display.update()
        CLOCK.tick(60)
        await asyncio.sleep(0) 

if __name__ == "__main__":
    asyncio.run(main_loop())