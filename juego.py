import turtle
import time
from PIL import Image
import random
from tkinter import messagebox

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
# Create several images of different sizes
for i in range(1, 11):
    img = Image.open('vaca.gif')
    img = img.resize((40 * i, 30 * i), Image.LANCZOS)
    img.save(f'vaca_{i}.gif')
    win.addshape(f'vaca_{i}.gif')
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
win.onkeypress(go_up, "Up")
win.onkeypress(go_down, "Down")
win.onkeypress(go_left, "Left")
win.onkeypress(go_right, "Right")

def end_game():
    global running
    running = False
    turtle.bye()


## Score
score = 0
size = 1
# Score display
score_display = turtle.Turtle()
score_display.speed(0)
score_display.shape("square")
score_display.color("black")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)
score_display.write("Score: {}".format(score), align="center", font=("Courier", 24, "normal"))

paused = False
def toggle_pause():
    global paused
    paused = not paused

# Keyboard binding for pausing and resuming the game
win.onkeypress(toggle_pause, "p")

# Snake body
segments = []

def on_respuesta1_click(x, y):
    # Aquí es donde pones el código que quieres que se ejecute cuando se hace clic en "respuesta1"
    global paused
    paused = False
    img_turtle_suma.hideturtle()
    img_turtle_respuesta1.hideturtle()
    img_turtle_respuesta2.hideturtle()
    img_turtle_suma.clear()
    img_turtle_resta.clear()
    img_turtle_resta.hideturtle()
    img_turtle_respuesta1.clear()
    img_turtle_respuesta2.clear()


def on_respuesta2_click(x, y):
    # Aquí es donde pones el código que quieres que se ejecute cuando se hace clic en "respuesta2"
    end_game()
    turtle.bye()


# Main game loop
while running:
    while paused:
        time.sleep(0.1)
        win.update()

    win.update()

    # Check for a collision with the border
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        head.goto(0, 0)
        head.direction = "Stop"
        # Optional: Hide the snake head when game is over
        head.hideturtle()
        end_game()

    # Check for a collision with the food
    if head.distance(food) < 20:
        # Switch to a larger image
        size += 1
        head.shape(f'vaca_{size}.gif')

        # Increase the score
        score += 1
        score_display.clear()
        score_display.write("Score: {}".format(score), align="center", font=("Courier", 24, "normal"))
        # Pause the game
        paused = True

        # Move the food to a random spot on the screen
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)
        
        if score == 1:
        # Display image options
            win.addshape("suma6_small.gif")
            win.addshape("suma4_small.gif")
            win.addshape("suma5_small.gif")

            # Create turtles for image options
            img_turtle_suma = turtle.Turtle()
            img_turtle_respuesta1 = turtle.Turtle()
            img_turtle_respuesta2 = turtle.Turtle()

            # Set shapes for turtles
            img_turtle_suma.shape("suma4_small.gif")
            img_turtle_respuesta1.shape("suma5_small.gif")
            img_turtle_respuesta2.shape("suma6_small.gif")



            # Set positions for turtles
            img_turtle_respuesta1.goto(0, -100)
            img_turtle_respuesta2.goto(0, -200)

            img_turtle_respuesta1.onclick(on_respuesta1_click)
            img_turtle_respuesta2.onclick(on_respuesta2_click)

            while paused:
                time.sleep(0.1)
                win.update()

        if score == 3:
            win.addshape("resta2_small.gif")
            win.addshape("suma5_small.gif")
            win.addshape("resta_small.gif")

            img_turtle_resta = turtle.Turtle()
            img_turtle_respuesta1 = turtle.Turtle()
            img_turtle_respuesta2 = turtle.Turtle()

            img_turtle_resta.shape("resta2_small.gif")
            img_turtle_respuesta1.shape("suma5_small.gif")
            img_turtle_respuesta2.shape("resta_small.gif")

            img_turtle_respuesta1.goto(0, -100)
            img_turtle_respuesta2.goto(0, -200)

            img_turtle_respuesta1.onclick(on_respuesta1_click)
            img_turtle_respuesta2.onclick(on_respuesta2_click)

            while paused:
                time.sleep(0.1)
                win.update()

        if score == 4:
            win.addshape("sumah_small.gif")
            win.addshape("resta_small.gif")
            win.addshape("suma5_small.gif")

            img_turtle_suma = turtle.Turtle()
            img_turtle_respuesta1 = turtle.Turtle()
            img_turtle_respuesta2 = turtle.Turtle()

            img_turtle_suma.shape("sumah_small.gif")
            img_turtle_respuesta1.shape("resta_small.gif")
            img_turtle_respuesta2.shape("suma5_small.gif")

            img_turtle_respuesta1.goto(0, -100)
            img_turtle_respuesta2.goto(0, -200)

            img_turtle_respuesta1.onclick(on_respuesta1_click)
            img_turtle_respuesta2.onclick(on_respuesta2_click)

            while paused:
                time.sleep(0.1)
                win.update()

        if score == 8:
            win.addshape("sumacinco_small.gif")
            win.addshape("cinco_small.gif")
            win.addshape("suma6_small.gif")

            img_turtle_suma = turtle.Turtle()
            img_turtle_respuesta1 = turtle.Turtle()
            img_turtle_respuesta2 = turtle.Turtle()

            img_turtle_suma.shape("sumacinco_small.gif")
            img_turtle_respuesta1.shape("cinco_small.gif")
            img_turtle_respuesta2.shape("suma6_small.gif")

            img_turtle_respuesta1.goto(0, -100)
            img_turtle_respuesta2.goto(0, -200)

            img_turtle_respuesta1.onclick(on_respuesta1_click)
            img_turtle_respuesta2.onclick(on_respuesta2_click)

            while paused:
                time.sleep(0.1)
                win.update()

        # Resume the game
        paused = False
    # Move the snake
    move()
    time.sleep(delay)

# Close the window
win.mainloop()