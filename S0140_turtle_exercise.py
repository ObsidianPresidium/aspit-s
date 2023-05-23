"""
Opgave "Tom the Turtle":

Som altid skal du læse hele øpgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Funktionen "demo" introducerer dig til alle de kommandoer, du skal bruge for at interagere med Tom i de følgende øvelser.

Kun hvis du er nysgerrig og elsker detaljer:
    Her er den fulde dokumentation for turtle graphics:
    https://docs.python.org/3.3/library/turtle.html

Del 1:
    Skriv en funktion "square", som accepterer en parameter "length".
    Hvis denne funktion kaldes, får skildpadden til at tegne en firkant med en sidelængde på "længde" pixels.

Del 2:
     Færdiggør funktionen "visible", som skal returnere en boolsk værdi,
     der angiver, om skildpadden befinder sig i det synlige område af skærmen.
     Brug denne funktion i de følgende dele af denne øvelse
     til at få skildpadden tilbage til skærmen, når den er vandret væk.

Del 3:
    Skriv en funktion "many_squares" med en for-loop, som kalder square gentagne gange.
    Brug denne funktion til at tegne flere firkanter af forskellig størrelse i forskellige positioner.
    Funktionen skal have nogle parametre. F.eks:
        antal: hvor mange firkanter skal der tegnes?
        størrelse: hvor store er firkanterne?
        afstand: hvor langt væk fra den sidste firkant er den næste firkant placeret?

Del 4:
    Skriv en funktion, der producerer mønstre, der ligner dette:
    https://pixabay.com/vectors/spiral-square-pattern-black-white-154465/

Del 5:
    Skriv en funktion, der producerer mønstre svarende til dette:
    https://www.101computing.net/2d-shapes-using-python-turtle/star-polygons/
    Funktionen skal have en parameter, som påvirker mønsterets form.

Del 6:
    Opret din egen funktion, der producerer et sejt mønster.
    Senere, hvis du har lyst, kan du præsentere dit mønster på storskærmen for de andre.

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Teams-meddelelse til din lærer: <filename> færdig
Fortsæt derefter med den næste fil.
"""

import turtle  # this imports a library called "turtle". A library is (someone else's) python code, that you can use in your own program.
import math
from time import sleep

tom = turtle.Turtle()
# turtle.setup(800, 600)
tom.speed(1)

def visible(turtle_name):  # returns true if both the x- and y-value of the turtle's position are between -480 and 480
    # you will need this: x-value: turtle_name.position()[0]
    # and this:           y-value: turtle_name.position()[1]
    x = turtle_name.position()[0]
    y = turtle_name.position()[1]
    if x > -480 and x < 480 and y > -480 and y < 480:
        return True
    else:
        return False
    return 0


def demo():  # demonstration of basic turtle commands
    print(type(tom))
    tom.speed(1)  # fastest: 10, slowest: 1
    for x in range(8):  # do the following for x = 0, 1, 2, 3, 4, 5, 6, 7
        tom.forward(50)  # move 50 pixels
        tom.left(45)  # turn 45 degrees left
        print(f'Tom is now at {tom.position()}, x-value: {tom.position()[0]=:.2f}, y-value: {tom.position()[1]=:.2f}')
    tom.penup()  # do not draw while moving from now on
    tom.forward(100)
    tom.pendown()  # draw while moving from now on
    tom.pencolor("red")  # draw in red
    tom.right(90)  # turn 90 degrees right
    tom.forward(120)
    tom.right(-90)  # turning -90 degrees right is the same as turning +90 degrees left
    tom.forward(120)
    tom.home()  # return to the original position in the middle of the window

def square(size, forward=0):
    tom.pendown()
    for n in range(4):
        tom.forward(size)
        tom.right(90)
    tom.penup()
    tom.forward(forward)


def many_squares(num_squares, size=50, margin=4):
    for i in range(num_squares):
        square(size, size + margin)


def square_spiral(size, margin=2):
    length = size
    tom.pendown()

    while length > 0:
        tom.forward(length)
        tom.right(90)
        length -= margin

    tom.penup()


def star(size=100, num_nodes=10):
    tom.pendown()
    for i in range(num_nodes):
        tom.forward(size)
        # Hvis i er lige, drej 150 grader. Hvis ikke, drej 150 grader til venstre, minus 360 grader divideret med mængden af spidser (math.floor(num_nodes / 2)).
        tom.right(150 if i % 2 == 0 else -150 + 360 / math.floor(num_nodes / 2))
    tom.penup()


def box(size=100, rotation=[45, 30]):
    tom.penup()
    size = size / 2
    nodes = [
        [-size, -size, -size],
        [-size, -size, size],
        [-size, size, -size],
        [-size, size, size],
        [size, -size, -size],
        [size, -size, size],
        [size, size, -size],
        [size, size, size]
    ]
    edges = [
        [0, 1],
        [1, 3],
        [3, 2],
        [2, 0],
        [4, 5],
        [5, 7],
        [7, 6],
        [6, 4],
        [0, 4],
        [1, 5],
        [2, 6],
        [3, 7]
    ]

    # Rotér punkter i 3-D
    # X rotation
    sin_theta = math.sin(rotation[0])
    cos_theta = math.cos(rotation[0])
    for i in nodes:
        y = i[1]
        z = i[2]
        i[1] = y * cos_theta - z * sin_theta
        i[2] = z * cos_theta + y * sin_theta

    # Y rotation
    sin_theta = math.sin(rotation[1])
    cos_theta = math.cos(rotation[1])
    for i in nodes:
        x = i[0]
        z = i[2]
        i[0] = x * cos_theta + z * sin_theta
        i[2] = z * cos_theta - x * sin_theta

    # Z rotation
    sin_theta = math.sin(60)
    cos_theta = math.cos(60)
    for i in nodes:
        x = i[0]
        y = i[1]
        i[0] = x * cos_theta - y * sin_theta
        i[1] = y * cos_theta + x * sin_theta


    for i in edges:
        from_node = nodes[i[0]]
        to_node = nodes[i[1]]
        tom.goto(from_node[0], from_node[1])
        tom.pendown()
        tom.goto(to_node[0], to_node[1])
        tom.penup()

    tom.home()

def boxAnimation(size=100, yaw=100, step=2):
    x_rotation = 0
    while True:
        box(size, [x_rotation, yaw])
        sleep(1)
        tom.clear()
        x_rotation += step

boxAnimation()



turtle.done()