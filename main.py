# Standard python libraries
from tkinter import *
from random import randint
import os
import sys


class Snake:
    def __init__(self):
        self.body_size = BODY_SIZE
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_SIZE):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tags="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        x = randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tags="food")


def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text=f"score: {score}")
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_game_over(snake):
        game_over()
    else:
        window.after(SLOWNESS, next_turn, snake, food)


def change_direction(new_dir):
    global direction

    if new_dir == "left":
        if direction != "right":
            direction = new_dir

    if new_dir == "right":
        if direction != "left":
            direction = new_dir

    if new_dir == "up":
        if direction != "down":
            direction = new_dir

    if new_dir == "down":
        if direction != "up":
            direction = new_dir


def check_game_over(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x > GAME_WIDTH:
        return True

    if y < 0 or y > GAME_HEIGHT:
        return True

    for sq in snake.coordinates[1:]:
        if x == sq[0] and y == sq[1]:
            return True

    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font=("Terminal", 50), text="GAME OVER!", fill="red", tags="game_over")


def restart_program():
    path = sys.executable
    os.execl(path, path, *sys.argv)


# Variables
GAME_WIDTH = 600
GAME_HEIGHT = 600
SPACE_SIZE = 25
SLOWNESS = 200
BODY_SIZE = 2
SNAKE_COLOR = "blue"
FOOD_COLOR = "red"
BG_COLOR = "black"
score = 0
direction = "down"

# Creating an object for window from Tkinter
window = Tk()
window.title("SNAKE GAME")
window.resizable(False, False)

# Creating an object for Label from Tkinter
label = (Label(window, text=f"Score: {score}", font=("Arial", 20)))
label.pack()

# Creating game board
canvas = Canvas(window, bg=BG_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Creating restart button
restart = Button(window, text="RESTART", fg="red", font=("Arial", 12), command=restart_program)
restart.pack()

window.update()

# Window sizes
window_width = window.winfo_width()
window_height = window.winfo_height()

# Screen sizes
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

# Window position
window.geometry(f"{window_width}x{window_height}+{x}+{y-40}")

# Directions
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

snake = Snake()
food = Food()
next_turn(snake, food)

window.mainloop()
