from random import choice, randint

import pygame as pg

# Инициализация PyGame
pg.init()

# Константы для размеров
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP: tuple[int, int] = (0, -1)
DOWN: tuple[int, int] = (0, 1)
LEFT: tuple[int, int] = (-1, 0)
RIGHT: tuple[int, int] = (1, 0)

# Цвета фона - черный
BOARD_BACKGROUND_COLOR: tuple[int, int, int] = (0, 0, 0)

# Цвета для объектов
GREEN_COLOR: tuple[int, int, int] = (0, 255, 0)
RED_COLOR: tuple[int, int, int] = (255, 0, 0)
BROWN_COLOR: tuple[int, int, int] = (139, 69, 19)
# Скорость движения змейки
SPEED: int = 20

# Настройка игрового окна
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля
pg.display.set_caption('Изгиб Питона')

# Настройка времени
clock = pg.time.Clock()

# Тут опишите все классы игры


class GameObject():
    """Родительский класс для игровых объектов."""

    def __init__(self, body_color=None):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color
        super().__init__()

    def draw(self):
        """Абстрактный метод для наследования в дочерних классах."""
        pass


class Snake(GameObject):
    """Класс описывает змейку."""

    positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
    length = 1
    direction = RIGHT
    next_direction = None

    def __init__(self, body_color=GREEN_COLOR):
        super().__init__(body_color)
        self.last = None
        self.position = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]

    def update_direction(self):
        """Метод изменяет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self, surface):
        """Отрисовка змейки на игровом поле."""
        for position in self.positions[:-1]:
            rect = (
                pg.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pg.draw.rect(surface, self.body_color, rect)
            pg.draw.rect(surface, (0, 0, 0), rect, 1)

    # Отрисовка головы змейки
        head = self.positions[0]
        head_rect = pg.Rect((head[0], head[1]), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(surface, self.body_color, head_rect)
        pg.draw.rect(surface, (0, 0, 0), head_rect, 1)

    # Затирание последнего сегмента
        if self.last is not None:
            last_rect = pg.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def undraw(self, surface):
        """Затирание при неправильной еде."""
        rect = pg.Rect(
            (self.positions[-1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(surface, (0, 0, 0), rect)
        pg.draw.rect(surface, (0, 0, 0), rect, 1)

    def get_head_position(self):
        """Метод возвращает позицию головы змейки."""
        result = self.positions[0]
        return result

    def reset(self):
        """Возвращает змейку в исходное состояние."""
        directions = [UP, DOWN, RIGHT, LEFT]
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = choice(directions)

    def move(self):
        """Метод, позволяющий змейке двигаться по направлению"""
        current_head_position = self.get_head_position()
        new_pos = ((current_head_position[0] + self.direction[0] * GRID_SIZE),
                   current_head_position[1] + self.direction[1] * GRID_SIZE)
        if new_pos[0] > SCREEN_WIDTH - GRID_SIZE or new_pos[0] < 0:
            new_x = (new_pos[0] % SCREEN_WIDTH)
            new_y = (new_pos[1] % SCREEN_HEIGHT)
            new_pos = (new_x, new_y)
            if new_pos in self.positions:
                self.reset()
                screen.fill(BOARD_BACKGROUND_COLOR)
            else:
                self.positions.insert(0, new_pos)
                self.last = self.positions[-1]
                self.positions.pop(-1)
        elif new_pos[1] > SCREEN_HEIGHT - GRID_SIZE or new_pos[1] < 0:
            new_x = (new_pos[0] % SCREEN_WIDTH)
            new_y = (new_pos[1] % SCREEN_HEIGHT)
            new_pos = (new_x, new_y)
            if new_pos in self.positions:
                self.reset()
                screen.fill(BOARD_BACKGROUND_COLOR)
            else:
                self.positions.insert(0, new_pos)
                self.last = self.positions[-1]
                self.positions.pop(-1)
        else:
            if new_pos in self.positions:
                self.reset()
                screen.fill(BOARD_BACKGROUND_COLOR)
            else:
                self.positions.insert(0, new_pos)
                self.last = self.positions[-1]
                self.positions.pop(-1)


class Apple(GameObject):
    """Класс, описывающий еду для змейки."""

    def randomize_position(self, snake=Snake):
        """Задаёт случайные координаты для яблока."""
        self.position = ((randint(1, 31) * GRID_SIZE),
                         (randint(1, 23) * GRID_SIZE))
        if self.position in snake.positions:
            while self.position in snake.positions:
                self.position = ((randint(1, 31) * GRID_SIZE),
                                 (randint(1, 23) * GRID_SIZE))
        return self.position

    def __init__(self, snake=Snake, body_color=RED_COLOR):
        super().__init__(body_color)
        self.position = self.randomize_position(snake)
        self.snake_pos = snake.positions

    def draw(self, surface):
        """Метод для отрисовки яблока."""
        rect = pg.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(surface, self.body_color, rect)
        pg.draw.rect(surface, (0, 0, 0), rect, 1)

    def undraw(self, surface):
        """Метод для удаления яблока."""
        rect = pg.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(surface, (0, 0, 0), rect)
        pg.draw.rect(surface, (0, 0, 0), rect, 1)


class Junkfood(Apple):
    """Класс, описывающий неправильную еду."""

    def __init__(self, snake=Snake, body_color=BROWN_COLOR):
        self.body_color = body_color
        self.position = self.randomize_position(snake)


def handle_keys(game_object):
    """Обрабатывает действия пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        elif event.type == pg.KEYDOWN:
            if (event.key == pg.K_UP or event.key == pg.K_w
               and game_object.direction != DOWN):
                game_object.next_direction = UP
            elif (event.key == pg.K_DOWN or event.key == pg.K_s
                  and game_object.direction != UP):
                game_object.next_direction = DOWN
            elif (event.key == pg.K_LEFT or event.key == pg.K_a
                  and game_object.direction != RIGHT):
                game_object.next_direction = LEFT
            elif (event.key == pg.K_RIGHT or event.key == pg.K_d
                  and game_object.direction != LEFT):
                game_object.next_direction = RIGHT


def main():
    """Функция, исполняющая логику игры."""
    apple = Apple()
    snake = Snake()
    junkfood = Junkfood()
    running = True
    while running:
        clock.tick(SPEED)
        junkfood.draw(screen)
        apple.draw(screen)
        snake.draw(screen)
        snake.move()
        handle_keys(snake)
        snake.update_direction()
        if snake.positions[0] == apple.position:
            snake.positions.insert(-1, apple.position)
            apple.randomize_position(snake)
        if snake.positions[0] == junkfood.position:
            if len(snake.positions) > 1:
                junkfood.randomize_position(snake)
                snake.undraw(screen)
                snake.positions.pop(-1)
            else:
                snake.reset()
                screen.fill(BOARD_BACKGROUND_COLOR)
        pg.display.update()


if __name__ == '__main__':
    main()
