"""
Opgave "double_this":

Som altid skal du læse hele øpgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Alt, hvad du har brug for at vide om funktioner for at løse denne øvelse, finder du i jupiter-notesbogen S0040_basics.ipynb.

Skriv en funktion med navnet "double_this".
Scroll ned for at finde det sted i denne fil, hvor du skal skrive funktionen ind.

Funktionen double_this skal ...
    have én parameter ved navn "number".
    beregne det dobbelte af værdien af denne parameter og gemme resultatet i en variabel ved navn double_number.
    returnere resultatet.

Der er allerede én kodelinje i hovedprogrammet, der kalder denne funktion med argumentet 3.

Kør programmet. Tallet 6 bør udskrives i konsollen,
efterfulgt af "Process finished with exit code 0".
Det betyder, at programmet sluttede uden en fejlmeddelelse.

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Teams-meddelelse til din lærer: <filename> færdig
Fortsæt derefter med den næste fil.
"""

#  Write your function below this line.

def double_this(myNumber):
    double_number = myNumber * 2
    return double_number

# Here starts the main program. From the main program you can call your functions.
print(double_this(3))