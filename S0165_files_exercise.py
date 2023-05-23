"""
Opgave "Reading from a file":

Som altid skal du læse hele øpgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Opret en tekstfil med en editor efter eget valg (pycharm, notepad, notepad++ osv.)
Hver række skal bestå af en persons navn efterfulgt af et mellemrum og et tal, der repræsenterer personens alder.
gem filen i din løsningsmappe

Skriv et program, der læser filen til en liste af strings.
Derefter brug indholdet af hver string til at udskrive en række som f.eks:
    <navn> er <alder> år gammel.

Hvis du går i stå, så spørg google, de andre elever eller læreren (i denne rækkefølge).

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Teams-meddelelse til din lærer: <filename> færdig
Fortsæt derefter med den næste fil.
"""

myfile = "S0166_files_exercise_input.txt"
mercs = []
ages = []

with open(myfile) as file:
    lines = file.readlines()

for i in lines:
    i = i.strip()
    i = i.split()
    mercs.append(i[0])
    ages.append(i[1])

for i in range(len(mercs)):
    print(f"{mercs[i]} er {ages[i]} år gammel.")