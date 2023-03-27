import pygame as pg
import random

pg.init()
WIDTH = 400
HEIGHT = 300
GAME_WIDTH = int(WIDTH / 10)
GAME_HEIGHT = int(HEIGHT / 10)

screen = pg.display.set_mode((WIDTH, HEIGHT))


class Snake:
    def __init__(self, head, direction):
        self.body = [head]
        self.direction = direction

    def move(self):
        self.body.insert(0, (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1]))
        self.body.pop()

    def grow(self):
        self.body.insert(0, (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1]))

    def change_direction(self, new_direction):
        self.direction = new_direction


class Apple:
    def __init__(self):
        self.regenerate()

    def regenerate(self):
        self.position = (random.randint(0, GAME_WIDTH - 1), random.randint(0, GAME_HEIGHT - 1))


class Roadblock:
    def __init__(self):
        self.regenerate()

    def regenerate(self):
        self.position = (random.randint(0, GAME_WIDTH - 1), random.randint(0, GAME_HEIGHT - 1))


class GameBoard:
    def __init__(self):
        self.snake = Snake((0, 0), (1, 0))
        self.apple = Apple()
        self.score = 0
        self.roadblocks = []
        for i in range(10):
            self.roadblocks.append(Roadblock())

    def draw_snake(self):
        for part in self.snake.body:
            pg.draw.rect(screen, "green", ((10 * part[0], 10 * part[1]), (10, 10)))

    def draw_apple(self):
        pg.draw.rect(screen, "red", ((10 * self.apple.position[0], 10 * self.apple.position[1]), (10, 10)))

    def roadblock(self):
        for block in self.roadblocks:
            pg.draw.rect(screen, "gray", ((10 * block.position[0], 10 * block.position[1]), (10, 10)))

    def is_collision(self):
        if self.snake.body[0][0] < 0 or self.snake.body[0][0] >= GAME_WIDTH:
            return True
        if self.snake.body[0][1] < 0 or self.snake.body[0][1] >= GAME_HEIGHT:
            return True
        if self.snake.body[0] in self.snake.body[1:]:
            return True
        for block in self.roadblocks:
            if self.snake.body[0] == block.position:
                return True
        return False

    def check_collision(self):
        if self.snake.body[0] == self.apple.position:
            self.apple.regenerate()
            self.snake.grow()
            self.score += 1

    def draw_score(self):
        font = pg.font.Font(None, 36)
        score_text = font.render("Score: " + str(self.score), True, (0, 0, 0))
        screen.blit(score_text, (10, 10))


the_game = GameBoard()
apple_counter = 0

while True:
    screen.fill("white")
    the_game.draw_snake()
    the_game.draw_apple()
    the_game.roadblock()
    the_game.draw_score()
    the_game.snake.move()
    the_game.check_collision()
    apple_counter += 1

    if the_game.is_collision():
        print("GAME OVER!")
        pg.quit()
        break

    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                the_game.snake.change_direction((-1, 0))
            if event.key == pg.K_RIGHT:
                the_game.snake.change_direction((1, 0))
            if event.key == pg.K_UP:
                the_game.snake.change_direction((0, -1))
            if event.key == pg.K_DOWN:
                the_game.snake.change_direction((0, 1))

    if apple_counter % 5 == 0:
        pg.time.Clock().tick(15)
    else:
        pg.time.Clock().tick(10)

    pg.display.update()