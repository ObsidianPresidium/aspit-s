"""
Opgave "Morris The Miner" (denne gang objekt orienteret)

Som altid skal du læse hele øpgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Omskriv din oprindelige Morris-kode til en objektorienteret version.

Definer en klasse Miner med attributter som sleepiness, thirst osv.
og metoder som sleep, drink osv.
Opret Morris og initialiser hans attributter ved at kalde konstruktoren for Miner:
morris = Miner()

Hvis du går i stå, så spørg google, de andre elever eller læreren (i denne rækkefølge).

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Teams-meddelelse til din lærer: <filename> færdig
Fortsæt derefter med den næste fil."""

# Dette er copy-pastet fra den oprindelige opgave, da jeg mener jeg har udført den på en objektorienteret måde fra starten af

class Miner:
    sleepiness = 0
    thirst = 0
    hunger = 0
    whisky = 0
    gold = 0
    time_to_drink = False
    rounds = 0

    def sleep(self):
        self.sleepiness -= 10
        self.thirst += 1
        self.hunger += 1
        self.rounds += 1

    def mine(self):
        self.sleepiness += 5
        self.thirst += 5
        self.hunger += 5
        self.gold += 5
        self.rounds += 1

    def eat(self):
        self.sleepiness += 5
        self.thirst -= 5
        self.hunger -= 20
        self.gold -= 2
        self.rounds += 1

    def buy_whisky(self):
        self.sleepiness += 5
        self.thirst += 1
        self.hunger += 1
        self.whisky += 1
        self.gold -= 1
        self.rounds += 1

    def drink(self):
        self.sleepiness += 5
        self.thirst -= 15
        self.hunger -= 1
        self.whisky -= 1
        self.rounds += 1


morris = Miner()



while morris.rounds < 1000:
    values = [morris.sleepiness, morris.thirst, morris.hunger, morris.whisky, morris.gold]
    vitals = [morris.sleepiness, morris.thirst, morris.hunger]
    if morris.time_to_drink:
        morris.drink()
        morris.time_to_drink = False
    elif morris.sleepiness >= 95:
        morris.sleep()
    elif morris.hunger >= 95:
        morris.eat()
    elif morris.thirst >= 94:
        morris.buy_whisky()
        morris.time_to_drink = True
    else:
        morris.mine()

    for i in values:
        if i < 0:
            print("Morris has used more resources than he has, and has created an impossible situation")

    for i in enumerate(vitals):
        if i[1] > 100:
            if i[0] == 0:
                cause_of_death = "sleepiness"
            elif i[0] == 1:
                cause_of_death = "thirst"
            elif i[0] == 2:
                cause_of_death = "hunger"
            print(f"Morris has died by overworking himself. Cause of death: {cause_of_death}. His {cause_of_death} level was {i[1]}.")

print(f"Morris has finished his {morris.rounds} rounds of activity, and during it, he managed to mine {morris.gold} gold!")