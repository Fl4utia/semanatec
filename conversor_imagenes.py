from PIL import Image
import turtle

# Abre la imagen y la redimensiona
img1 = Image.open("sumah.gif")
img1_resized = img1.resize((180, 80))  # Cambia el tamaño a 180x80 píxeles
img1_resized.save("sumah_small.gif")  # Guarda la imagen redimensionada

win = turtle.Screen()

# Registra las imágenes redimensionadas como nuevas formas
win.addshape("sumah_small.gif")

# Crea nuevas turtles
img_turtle1 = turtle.Turtle()


# Cambia la forma de las turtles a las imágenes redimensionadas
img_turtle1.shape("sumah_small.gif")

# Mueve las turtles a posiciones específicas si es necesario
img_turtle1.goto(-100, 0)

# Mantiene abierta la ventana hasta que el usuario la cierre
turtle.done()