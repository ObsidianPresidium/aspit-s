"""
Opgave "Morris the Miner":

Som altid skal du læse hele øpgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Udgangssituation:
Morris har egenskaberne sleepiness, thirst, hunger, whisky, gold.
Alle attributter har startværdien 0.

Regler:
Hvis sleepiness, thirst eller hunger kommer over 100, dør Morris.
Morris kan ikke opbevare mere end 10 flasker whisky.
Ingen attribut kan gå under 0.

Ved hver omgang kan Morris udføre præcis én af disse aktiviteter:
sleep:      sleepiness-=10, thirst+=1,  hunger+=1,  whisky+=0, gold+=0
mine:       sleepiness+=5,  thirst+=5,  hunger+=5,  whisky+=0, gold+=5
eat:        sleepiness+=5,  thirst-=5,  hunger-=20, whisky+=0, gold-=2
buy_whisky: sleepiness+=5,  thirst+=1,  hunger+=1,  whisky+=1, gold-=1
drink:      sleepiness+=5,  thirst-=15, hunger-=1,  whisky-=1, gold+=0

Din opgave:
Skriv et program, der giver Morris så meget guld som muligt på 1000 omgange.

Hvis du ikke har nogen idé om hvordan du skal begynde, så åbn S0185_morris_help.py og start derfra.
Hvis du går i stå, så spørg google, de andre elever eller læreren (i denne rækkefølge).

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Teams-meddelelse til din lærer: <filename> færdig
Fortsæt derefter med den næste fil.
"""


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