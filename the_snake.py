from random import choice, randint

import pygame

# Инициализация PyGame
pygame.init()

# Константы для размеров
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета фона - черный
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Скорость движения змейки
SPEED = 10

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля
pygame.display.set_caption('Изгиб Питона')

# Настройка времени
clock = pygame.time.Clock()

# Тут опишите все классы игры


class GameObject():
    """Родительский класс для игровых объектов."""

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Абстрактный метод для наследования в дочерних классах."""
        pass


class Apple(GameObject):
    """Класс, описывающий еду для змейки."""

    def randomize_position(self):
        """Задаёт случайные координаты для яблока."""
        self.position = ((randint(1, 31) * GRID_SIZE),
                         (randint(1, 23) * GRID_SIZE))
        return self.position

    def __init__(self):
        self.position = self.randomize_position()
        self.body_color = (255, 0, 0)

    def draw(self, surface):
        """Метод для отрисовки яблока."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, (93, 216, 228), rect, 1)

    def undraw(self, surface):
        """Метод для отрисовки яблока."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, (0, 0, 0), rect)
        pygame.draw.rect(surface, (93, 216, 228), rect, 1)


class Snake(GameObject):
    """Класс описывает змейку."""

    positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
    length = 1
    direction = RIGHT
    next_direction = None
    body_color = (0, 255, 0)

    def __init__(self):
        self.last = None

    def update_direction(self):
        """Метод изменяет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self, surface):
        """Отрисовка змейки на игровом поле."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (93, 216, 228), rect, 1)

    # Отрисовка головы змейки
        head = self.positions[0]
        head_rect = pygame.Rect((head[0], head[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, (93, 216, 228), head_rect, 1)

    # Затирание последнего сегмента
        if self.last is not None:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

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
        screen.fill(BOARD_BACKGROUND_COLOR)

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
            else:
                self.positions.insert(0, new_pos)
                self.last = self.positions[-1]
                self.positions.pop(-1)
        else:
            if new_pos in self.positions:
                self.reset()
            else:
                self.positions.insert(0, new_pos)
                self.last = self.positions[-1]
                self.positions.pop(-1)


def handle_keys(game_object):
    """Обрабатывает действия пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Функция, исполняющая логику игры."""
    apple = Apple()
    snake = Snake()
    running = True
    while running:
        clock.tick(SPEED)
        apple.draw(screen)
        snake.draw(screen)
        snake.move()
        handle_keys(snake)
        snake.update_direction()
        if snake.positions[0] == apple.position:
            snake.positions.insert(-1, apple.position)
            apple.randomize_position()
        pygame.display.update()


if __name__ == '__main__':
    main()
