"""Opgave "Number pyramid"

Som altid skal du læse hele øpgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Se de første 93 sekunder af denne video: https://www.youtube.com/watch?v=NsjsLwYRW8o

Skriv en funktion "pyramid", der producerer de tal, der er vist i videoen.
Funktionen har en parameter, der definerer, hvor mange talrækker der skal produceres.
Funktionen udskriver tallene i hver række og også deres sum.

I hovedprogrammet kalder du funktionen med fx 7 som argument.

Tilføj en mere generel funktion pyramid2.
Denne funktion har som andet parameter en liste med tallene i
pyramidens øverste række.

I hovedprogrammet kalder du pyramid2 med 1, 2, 3, ..., 10 som det første argument
og en liste med tal efter eget valg som det andet argument.
Afprøv forskellige lister som andet argument.

Hvis du ikke aner, hvordan du skal begynde, kan du åbne S1620_pyramid_help.py og starte derfra

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Teams-meddelelse til din lærer: <filename> færdig
Fortsæt derefter med den næste fil."""

import math

add_if_numbers = [1, 2, 3, 4, 5, 6]

def pyramid(n_rows=1):
    pyramid_list = [[1, 1]]
    top_padding = math.floor(n_rows / 2)
    for i in range(n_rows - 1):  # - 1 because we already have 1, 1 registered
        working_pyramid_row = []
        for j in enumerate(pyramid_list[i]):
            if j[1] != len(pyramid_list[i]) - 1:
                if j[0] in add_if_numbers and pyramid_list[j[1] + 1] in add_if_numbers:
                    working_pyramid_row.append(j[0] + pyramid_list[j[1] + 1])
            else:
                pyramid_list.append(working_pyramid_row)


    for i in pyramid_list:
        final_padding = ""
        for j in range(top_padding):
            final_padding += " "
        print(f"{i}")

pyramid(2)