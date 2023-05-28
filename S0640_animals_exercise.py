"""
Opgave "Animals"

Som altid skal du læse hele øpgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Alt, hvad du har brug for at vide for at løse denne opgave, finder du i cars_oop- og rpg1-filerne.

Definer en klasse ved navn Animal.
Hvert objekt i denne klasse skal have attributterne name (str), sound (str), height (float),
weight (float), legs (int), female (bool).
I parentes står data typerne, dette attributterne typisk har.

Tilføj til klassen meningsfulde metoder __init__ og __repr__.
Kald disse metoder for at oprette objekter af klassen Animal og for at udskrive dem i hovedprogrammet.

Skriv en klassemetode ved navn make_noise, som udskriver dyrets lyd i konsollen.
Kald denne metode i hovedprogrammet.

Definer en anden klasse Dog, som arver fra Animal.
Hvert objekt af denne klasse skal have attributterne tail_length (int eller float)
og hunts_sheep (typisk bool).

Tilføj til klassen meningsfulde metoder __init__ og __repr__.
Ved skrivning af konstruktoren for Dog skal du forsøge at genbruge kode fra klassen Animal.
Kald disse metoder for at oprette objekter af klassen Hund og for at udskrive dem i hovedprogrammet.

Kald metoden make_noise på Dog-objekter i hovedprogrammet.

Skriv en klassemetode ved navn wag_tail for Dog.
Denne metode udskriver i konsollen noget i stil med
"Hunden Snoopy vifter med sin 32 cm lange hale"
Kald denne metode i hovedprogrammet.

Skriv en funktion mate(mother, father). Begge parametre er af typen Dog.
Denne funktion skal returnere et nyt objekt af typen Dog.
I denne funktion skal du lave meningsfulde regler for den nye hunds attributter.
Sørg for, at denne funktion kun accepterer hunde med det korrekte køn som argumenter.

I hovedprogrammet kalder du denne metode og udskriver den nye hund.

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Teams-meddelelse til din lærer: <filename> færdig
Fortsæt derefter med den næste fil."""

import math
import random

def get_gender_name(animal):
    return "hunkøn" if animal.female else "hankøn"

def get_half_of_string(string, which_half):
    half_length = math.floor(len(string) / 2)
    return string[:half_length] if which_half == "first" else string[half_length:]

def randbool():
    random.seed()
    return random.choice([False, True])

class Animal:
    name = ""
    sound = ""
    height = 0
    weight = 0
    legs = 0
    female = False

    def __init__(self, name, sound, height, weight, legs, female):
        self.name = name
        self.sound = sound
        self.height = height
        self.weight = weight
        self.legs = legs
        self.female = female

    def __repr__(self):
        return f"Dette dyr er en/et {get_gender_name(self)}s {self.name}. Den/det har {self.legs} ben, er {self.height}cm høj, vejer {self.weight}kg, og siger {self.sound}"

    def make_noise(self):
        print(self.sound)

class Dog(Animal):
    tail_length = ""
    hunts_sheep = False

    def __init__(self, name, sound, height, weight, legs, female, tail_length, hunts_sheep):
        super().__init__(name, sound, height, weight, legs, female)
        self.tail_length = tail_length
        self.hunts_sheep = hunts_sheep

    def wag_tail(self):
        print(f"Hunden {self.name} vifter med sin {self.tail_length}cm lange hale")

def mate(mother, father):
    if father.female or not mother.female:
        print(f"Du har enten magerne i forkert rækkefølge, eller forsøger at gennemføre homoseksuel parring. Moderens køn er {get_gender_name(mother)}, og faderens er {get_gender_name(father)}.")
    else:
        if not mother.hunts_sheep and not father.hunts_sheep:
            hunts_sheep = False
        elif mother.hunts_sheep and father.hunts_sheep:
            hunts_sheep = True
        else:
            hunts_sheep = randbool()

        return Dog(
            get_half_of_string(mother.name, "first") + get_half_of_string(father.name, "second"),
            get_half_of_string(mother.sound, "first") + get_half_of_string(father.sound, "second"),
            (mother.height + father.height) / 2,
            (mother.weight + father.weight) / 2,
            math.ceil((mother.legs + father.legs) / 2),
            randbool(),
            (mother.tail_length + father.tail_length) / 2,
            hunts_sheep
        )


mother_dog = Dog("Hund", "Vuffelivov", 50, 30, 4, True, 10, False)
father_dog = Dog("Hund", "Vov-vov", 70, 40, 4, False, 15, True)
puppy = mate(mother_dog, father_dog)
print("Hvalp født!")
print(puppy)
print(f"Hvalpen har en hale på {puppy.tail_length}cm og {'jager får' if puppy.hunts_sheep else 'jager ikke får'}.")
