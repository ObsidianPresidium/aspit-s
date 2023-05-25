"""
Opgave "Cars":

Som altid skal du læse hele øpgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Definer en funktion drive_car(), der udskriver en bils motorlyd (f.eks. "roooaar")

I hovedprogrammet:
    Definer variabler, som repræsenterer antallet af hjul og den maksimale hastighed for 2 forskellige biler
    Udskriv disse egenskaber for begge biler
    Kald derefter funktionen motorlyd

Hvis du ikke har nogen idé om, hvordan du skal begynde, kan du åbne S0420_cars_help.py og starte derfra.
Hvis du går i stå, kan du spørge google, de andre elever eller læreren (i denne rækkefølge).
Hvis du stadig er gået i stå, skal du åbne S0430_cars_solution.py og sammenligne den med din løsning.

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Team-besked til din lærer: <filename> færdig
Fortsæt derefter med den næste fil."""

cars = []

class Car:
    def __init__(self, wheels, top_speed):
        self.wheels = wheels
        self.top_speed = top_speed
        cars.append(self)

def drive_car():
    print("VRUM VRUM!")

car1 = Car(4, 200)
car2 = Car(3, 45)

for i in enumerate(cars):
    print(f"Bil nr. {i[0] + 1} har {i[1].wheels} dæk og en tophastighed på {i[1].top_speed} km/t")

drive_car()