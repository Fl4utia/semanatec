import turtle
import time
from PIL import Image
import random
running = True
win = turtle.Screen()
win.title("Snake Game")
win.bgcolor("#45C231")
win.setup(width=600, height=600)
win.tracer(0)

delay = 0.3

# Open an image file
img = Image.open('vaca.gif')
# Resize it
img = img.resize((40, 30), Image.LANCZOS)
# Save it back to disk
img.save('vaca_small.gif')

win.addshape('vaca_small.gif')

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape('vaca_small.gif')  # Change "square" to "vaca.gif"
head.color("white")
head.penup()
head.goto(0, 0)
head.direction = "Stop"

# Snake food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")  # Change this to any shape you want or an image like you did with the snake head
food.color("red")
food.penup()
food.goto(0, 100)

# Score
score = 0

# Functions to move the snake
def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

# Functions
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

# Keyboard bindings
win.listen()
win.onkeypress(go_up, "w")
win.onkeypress(go_down, "s")
win.onkeypress(go_left, "a")
win.onkeypress(go_right, "d")

def end_game():
    global running
    running = False

## Score
score = 0

# Score display
score_display = turtle.Turtle()
score_display.speed(0)
score_display.shape("square")
score_display.color("black")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)
score_display.write("Score: {}".format(score), align="center", font=("Courier", 24, "normal"))

# Main game loop
while running:
    win.update()

    # Check for a collision with the border
    if head.xcor()>290 or head.xcor()<-290 or head.ycor()>290 or head.ycor()<-290:
        head.goto(0, 0)
        head.direction = "Stop"
        # Optional: Hide the snake head when game is over
        head.hideturtle()
        end_game()

    # Check for a collision with the food
    if head.distance(food) < 20:
        # Move the food to a random spot on the screen
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)

        # Increase the score
        score += 1
        score_display.clear()
        score_display.write("Score: {}".format(score), align="center", font=("Courier", 24, "normal"))

    # Move the snake
    move()
    time.sleep(delay)

# Close the window
win.mainloop()