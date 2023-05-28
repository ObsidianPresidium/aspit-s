"""opgave: Objektorienteret rollespil, del 2 :

Som altid skal du læse hele øvelsesbeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Byg videre på din løsning af del 1.

Opfind to nye klasser, som arver fra klassen Character. For eksempel Hunter og Magician.
Dine nye klasser skal have deres egne ekstra metoder og/eller attributter. Måske overskriver de også metoder eller attributter fra klassen Character.

Lad i hovedprogrammet objekter af dine nye klasser (dvs. rollespilfigurer) kæmpe mod hinanden,
indtil den ene figur er død. Udskriv, hvad der sker under kampen.

I hver omgang bruger en figur en af sine evner (metoder). Derefter er det den anden figurs tur.
Det er op til dig, hvordan dit program i hver tur beslutter, hvilken evne der skal bruges.
Beslutningen kan f.eks. være baseret på tilfældighed eller på en smart strategi

Opgradering 1:
Hver gang en figur bruger en af sine evner, skal du tilføje noget tilfældighed til den anvendte evne.

Opgradering 2:
Lad dine figurer kæmpe mod hinanden 100 gange.
Hold styr på resultaterne.
Prøv at afbalancere dine figurers evner på en sådan måde, at hver figur vinder ca. halvdelen af kampene.

Hvis du går i stå, kan du spørge google, de andre elever eller læreren (i denne rækkefølge).

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Teams-besked til din lærer: <filename> done
Fortsæt derefter med den næste fil."""

import random
import time

# Indstillinger, som kan ændres
arrow_damage = 70
mana_gain = 5
turn_speed_multiplier = 1  # Set this to 0 to disable waiting for turns to finish!
interactive = False  # Hvis denne slås til, får du ved hver turs slutning en konsol, hvor man bl.a. kan inspicere figurer og evaluere hurtig Python-kode.
hundred_turns_mode = True  # 100 ture i alt, som Opgradering 2 forudsætter.
hundred_turns_wave_size = 4

# Globale variabler

characters = []
turn = 1
turn_speed = 0 if turn_speed_multiplier == 0 else 1 / turn_speed_multiplier

def roll(n_or_above): # Terninge-kaster. Kaster en terning på 6 sider
    random.seed()
    return True if n_or_above - 1 >= random.random() * 5 else False


class Character:
    def __init__(self, name, max_health, attackpower):
        self.name = name
        self.max_health = max_health
        self._current_health = max_health
        self.attackpower = attackpower
        self.is_dead = False
        characters.append(self)

    def __repr__(self):
        return f"Navn: {self.name}\n" \
               f"HP: {self._current_health}/{self.max_health}\n" \
               f"AP: {self.attackpower}"

    def get_target(self):
        if not hasattr(self, "target"):
            self.target = targeting(self)
            self.target.targeted_by = self
        else:
            if hasattr(self, "targeted_by"):
                self.target = self.targeted_by
            if self.target.is_dead:
                self.target = targeting(self)

    def get_hit(self, damage):
        self._current_health -= damage
        if self._current_health <= 0:
            print(f"{self.name} døde!")
            self._current_health = 0
            self.is_dead = True
            for i in enumerate(characters):
                if i[1] == self:
                    characters.pop(i[0])
                if hasattr(i[1], "targeted_by"):
                    if i[1].targeted_by == self:
                        del i[1].targeted_by

    def end_turn(self):
        pass

    def hit(self, victim, damage):
        victim.get_hit(damage)

    def type(self):
        return self.__class__.__name__


    def melee(self, victim):
        print(f"{self.name} sloges med {victim.name} i CQC for {self.attackpower} HP!")
        self.hit(victim, self.attackpower)

    def attack(self):
        self.melee(self.target)

class Hunter(Character):
    def __init__(self, name, max_health, attackpower, arrows, skill):
        super().__init__(name, max_health, attackpower)
        self.arrows = arrows
        self.skill = skill

    def shoot(self, victim):
        if self.arrows > 0:
            if roll(self.skill):
                print(f"{self.name} skød en pil på {victim.name}, og skadede dem {arrow_damage} HP!")
                self.hit(victim, arrow_damage)
            else:
                print(f"{self.name} skød en pil på {victim.name}, men missede!")
            self.arrows -= 1
        else:
            print(f"{self.name} forsøgte at skyde, men er løbet tør for pile!")

    def attack(self):
        if self.arrows > 0:
            self.shoot(self.target)
        else:
            self.melee(self.target)

class Magician(Character):
    def __init__(self, name, max_health, attackpower, max_mana, spell):
        super().__init__(name, max_health, attackpower)
        self.max_mana = max_mana
        self._current_mana = max_mana
        self.spell = spell

    def cast_spell(self, victim):
        if self._current_mana >= self.spell["mana_cost"]:
            random.seed()
            variance = round((self.spell["max_damage"] - self.spell["min_damage"]) * random.random())
            damage_to_deal = self.spell["min_damage"] + variance
            victim.get_hit(damage_to_deal)
            print(f"{self.name} tryllede et angreb frem på {victim.name}, som skadede dem {damage_to_deal} HP!")
            self._current_mana -= self.spell["mana_cost"]
        else:
            print(f"{self.name} forsøgte at trylle, men er løbet tør for mana!")

    def end_turn(self):
        self._current_mana += mana_gain

    def attack(self):
        if self._current_mana >= self.spell["mana_cost"]:
            self.cast_spell(self.target)
        else:
            self.melee(self.target)


class Zombie(Character):
    def __init__(self, name, max_health, attackpower):
        super().__init__(name, max_health, attackpower)

    def get_target(self):
        if characters[0].type() != "Zombie":
            self.target = characters[0]
            characters[0].targeted_by = self
        else:
            Character.get_target(self)

    def melee(self, victim):
        print(f"{self.name} åd en del af {victim.name}, og skadede dem for {self.attackpower}!")
        self.hit(victim, self.attackpower)


def targeting(perp):
    # De næste to linjer sikrer, at target ikke er den samme som perp.
    perp_target = perp
    while perp_target == perp:
        random.seed()
        index = random.random() * len(characters) - 1
        # ceil funktion
        rest = index % 1
        if rest < 0.5:
            index += 0.5
        index = round(index)

        perp_target = characters[index]
    return perp_target

def inspect():
    exit_inspect = False
    if turn == 1:
        print("\nAvailable commands:\n"
              "check {CHARACTER.name} - prints __repr__ for character\n"
              "kill {CHARACTER.name}  - kills a character\n"
              "exec {COMMAND}         - evaluates a Python expression\n"
              "endturn                - ends the turn\n"
              "exit                   - disables the interactive mode")
    command = input(f"Turn {turn}$ ")
    command = command.split()

    def get_character_by_command_and_name(input_command):
        command_copy = input_command.copy()
        command_copy.pop(0)
        target_name = " ".join(command_copy)
        for i in characters:
            if i.name == target_name:
                return i

    if command[0] == "check":
        print(get_character_by_command_and_name(command))
    elif command[0] == "kill":
        get_character_by_command_and_name(command).get_hit(999999999)
    elif command[0] == "exec":
        if len(command) != 1:
            command.pop(0)
            try:
                print(eval(" ".join(command)))
            except AttributeError:
                print("An attribute error occured. Are you sure the attribute you are trying to access exists?")
            except NameError:
                print("A name error occured. Are you that the object you are trying to access exists?")
            except:
                print("An error occured.")
        else:
            print("exec needs a parameter")
    elif command[0] == "endturn":
        exit_inspect = True
    elif command[0] == "exit":
        global interactive
        interactive = False
        exit_inspect = True
    else:
        print("Command not found.")

    if not exit_inspect:
        inspect()

def game_loop():
    global turn
    while len(characters) > 1:
        if turn != 1:
            time.sleep(turn_speed * 2)
        print(f"\nTur nr. {turn}:")
        for character in characters:
            print(f"{character.name}s tur!")
            character.get_target()
            time.sleep(turn_speed)
            character.attack()
            time.sleep(turn_speed)

        if interactive:
            inspect()
        turn += 1


# Figurer, som skal kæmpe mod hinanden
emil = Character("Emil", 50, 10)
gandalf = Magician("Gandalf", 100, 10, 90, {"min_damage": 10, "max_damage": 20, "mana_cost": 15})
ashe = Hunter("Ashe", 200, 10, 6, 2)
arnie = Character("Arnie", 125, 30)


print("Velkommen til arenaen!")
game_loop()

if len(characters) == 0:
    print(f"Alle er døde..?")
    exit(0)
last_man_standing = characters[0]
print(f"\n\nEfter i alt {turn - 1} ture, er {last_man_standing.name} den sidste mand på skansen!")
if hundred_turns_mode and turn < 100:
    print(f"Men er det virkelig slutningen på det hele?\n"
          f"Pludseligt spotter {last_man_standing.name} nemlig adskillige zombier langsomt rejse sig fra jorden!\n"
          f"Til angreb!")

    total_zombies = 0
    while turn < 100:
        for i in range(hundred_turns_wave_size):
            total_zombies += 1
            zombie = Zombie(f"Zombie #{total_zombies}", 25, 5)
        game_loop()
    if characters[0].type() == "Zombie":
        print("Med ingen levende figurer tilbage i arenaen, er zombieapokalypsen fuldendt.")
    else:
        print(f"{last_man_standing.name} overlevede zombieapokalypsen!")
