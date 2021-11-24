import sys
from colorit import *
import time
# only runs one time, includes the help text
def launch():

    print("Welcome to Escape The Dungeon!")
    print("Type '" + color("help", Colors.yellow) + "' at anytime to see a list of possible commands.")
    print("")
    start()

# inventory
sword_get = False
shield_get = False

# advancements
bossA_defeat = False
bossA_defeatMethod = "sword"
puzzleA_complete = False
# room to choose sword/shield
def sword_room():
   global sword_get
   global shield_get
   
   if not sword_get and not shield_get:
    print("This is a nearly empty room.")
    print("There is a " + color("SWORD", Colors.green) + " and a " + color("SHIELD", Colors.green) + " on the ground.")
    print("You can only take one.")
    while True:
       choice = input("> ").lower()
       if choice == "leave":
           start()
       elif choice == "help":
           print("'" + color("leave", Colors.yellow) + "': Leaves the room and returns to the main path.")
           print("'" + color("take sword", Colors.yellow) + "' or '" + color("sword", Colors.yellow) + "': Takes the " + color("SWORD", Colors.green) + " and puts it in your inventory, the " + color("SHIELD", Colors.green) + " will dissappear.")
           print("'" + color("take shield", Colors.yellow) + "' or '" + color("shield", Colors.yellow) + "': Takes the " + color("SHIELD", Colors.green) + " and puts it in your inventory, the " + color("SWORD", Colors.green) + " will dissappear.")
       
       # puts the sword in your inventory, leads to attacking being easier on the guardian fight
       # choosing this leads the shield to be inaccessable
       elif choice == "take sword" and not sword_get and not shield_get or choice == "sword" and not sword_get and not shield_get:
            print("You got the " + color("SWORD", Colors.green) + ".")
            print("The " + color("SHIELD", Colors.green) + " disappeared!")
            print("")
            sword_get = True
            start()
       
       # puts the shield in your inventory, leads to defending being easier on the guardian fight
       # choosing this leads the sword to be inaccessable
       elif choice == "take shield" and not sword_get and not shield_get or choice == "shield" and not sword_get and not shield_get:
            print("You got the " + color("SHIELD", Colors.green) + ".")
            print("The " + color("SWORD", Colors.green) + " disappeared!")
            print("")
            shield_get = True
            start()

       # failsafe text
       else:
            print("I got no idea what that means.")
   else:
    print("This is a empty room.")
    while True:
       choice = input("> ").lower()
       if choice == "leave":
           start()
       elif choice == "help":
           print("'leave': Leaves the room and returns to the main path.")
       
       # failsafe text
       else:
            print("I got no idea what that means.")

# guardian bossfight
def guardian_room():
    global sword_get
    global shield_get
    
    # these arent global just so they reset each time this room is loaded
    guardian_health = 100
    guardian_energy = 100
    player_health = 100
    
    print("The " + color("GUARDIAN", Colors.red) + " stands tall.")

    # events/options against the guardian if you dont have the sword/shield
    if not sword_get and not shield_get:
        print("Facing it without any equipment is a difficult, no, impossible feat.")
        print("You can back down and return to the main room while you still have a chance.")
        print("Or you can attempt to stand your ground against it in this state.")
        
        # commands
        while True:
            choice = input("> ").lower()
            if choice == "leave":
                start()
            elif choice == "help":
                print("'leave': Leaves the room and returns to the main path.")
                print("'" + color("attack", Colors.blue) + "': Attempt to " + color("ATTACK", Colors.blue) + " the " + color("GUARDIAN", Colors.red) + ". High chance that this will fail...")
                print("'" + color("defend", Colors.blue) + "': Attempt to " + color("DEFEND", Colors.blue) + " against the " + color("GUARDIAN", Colors.red) + ". High chance that this will fail...")
            
            # you die either way here because you arent equipped with anything
            elif choice == "attack":
                dead("You died whilst attempting to " + color("ATTACK", Colors.blue) + " the " + color("GUARDIAN", Colors.red) + "... There must be some way to get some equipment to stand a chance...")
            elif choice == "defend":
                dead("You died whilst attempting to " + color("DEFEND", Colors.blue) + " against the " + color("GUARDIAN", Colors.red) + "... There must be some way to get some equipment to stand a chance...")
            
            # failsafe text
            else:
                print("I got no idea what that means.")
    

    # events/options against the guardian if you have the sword/shield
    if sword_get or shield_get:
        print("It seems that you must face it in order to get out of here.")
        print("Facing it is a difficult feat.")
        print("However, you've got a better chance with your equipment.")
        while True:
            choice = input("> ").lower()
            if choice == "leave":
                start()
            elif choice == "help":
                print("'leave': Leaves the room and returns to the main path.")
                print("'" + color("attack", Colors.blue) + "': " + color("ATTACK", Colors.blue) + "s the " + color("GUARDIAN", Colors.red) + ". Reduces its HEALTH. Get it low enough and it might retreat.")
                print("'" + color("defend", Colors.blue) + "': " + color("DEFEND", Colors.blue) + " against the " + color("GUARDIAN", Colors.red) + ". Reduces its ENERGY. Get it tired enough and it might retreat.")
            
            # attack command
            elif choice == "attack":
                
                # attacking with a sword
                if sword_get and not shield_get:
                    guardian_health -= 25
                    player_health -= 5
                    print("You " + color("ATTACK", Colors.blue) + "ed the " + color("GUARDIAN", Colors.red) + " with your " + color("SWORD", Colors.green) + ".")
                    print("GUARDIAN HEALTH: " + guardian_health.__str__() + ", GUARDIAN ENERGY: " + guardian_energy.__str__() + ", PLAYER HEALTH: " + player_health.__str__())
                    
                    # checks if you are dead, and if you are then it will trigger dead()
                    if player_health <= 1:
                        dead("You died while fighting the " + color("GUARDIAN", Colors.red) + ".")
                    
                    # checks if guardian should be dead
                    if guardian_health <= 0:
                        guardian_defeat("sword")
                
                # attacking with a shield
                elif shield_get and not sword_get:
                    guardian_health -= 5
                    player_health -= 25
                    print("You tried to " + color("ATTACK", Colors.blue) + " the " + color("GUARDIAN", Colors.red) + " with your " + color("SHIELD", Colors.green) + ".")
                    print("GUARDIAN HEALTH: " + guardian_health.__str__() + ", GUARDIAN ENERGY: " + guardian_energy.__str__() + ", PLAYER HEALTH: " + player_health.__str__())
                    
                    # checks if you are dead, and if you are then it will trigger dead()
                    if player_health <= 1:
                        dead("You died while fighting the " + color("GUARDIAN", Colors.red) + ".")

                    # checks if guardian should be dead
                    if guardian_health <= 0:
                        guardian_defeat("sword")
            
            # defend command
            elif choice == "defend":
                
                # defending with a sword
                if sword_get and not shield_get:
                    guardian_energy -= 5
                    player_health -= 25
                    print("You tried to " + color("DEFEND", Colors.blue) + " against the " + color("GUARDIAN", Colors.red) + " with your " + color("SWORD", Colors.green) + ".")
                    print("GUARDIAN HEALTH: " + guardian_health.__str__() + ", GUARDIAN ENERGY: " + guardian_energy.__str__() + ", PLAYER HEALTH: " + player_health.__str__())
                    
                    # checks if you are dead, and if you are then it will trigger dead()
                    if player_health <= 1:
                        dead("You died while fighting the " + color("GUARDIAN", Colors.red) + ".")

                    # checks if guardian energy is below 0
                    if guardian_energy <= 0:
                        guardian_defeat("shield")
                
                # defending with a shield
                elif shield_get and not sword_get:
                    guardian_energy -= 25
                    player_health -= 5
                    print("You " + color("DEFEND", Colors.blue) + "ed against the " + color("GUARDIAN", Colors.red) + " with your " + color("SHIELD", Colors.green) + ".")
                    print("GUARDIAN HEALTH: " + guardian_health.__str__() + ", GUARDIAN ENERGY: " + guardian_energy.__str__() + ", PLAYER HEALTH: " + player_health.__str__())
                    
                    # checks if you are dead, and if you are then it will trigger dead()
                    if player_health <= 1:
                        dead("You died while fighting the " + color("GUARDIAN", Colors.red) + ".")
                    
                    # checks if guardian energy is below 0
                    if guardian_energy <= 0:
                        guardian_defeat("shield")
            
            # failsafe text
            else:
                print("I got no idea what that means.")

# displays why you died and ends the app
def dead(why):
    print(why, "The End.")
    input("Hit ENTER to exit...")
    exit(0)

# shows the win text and ends the app
def end_room():
    print("You escaped the dungeon!")
    print("Thank you for playing.")
    print("The End.")
    while True:
        a = input("Hit any key to exit...") 
        if not a == "Hit any key to exit...":
            exit(0)
    

# func that starts after the guardian is defeated
# var how: takes either 'shield' or 'sword' to display how the guardian was defeated
def guardian_defeat(how):
    global bossA_defeat
    global bossA_defeatMethod
    bossA_defeat = True
    bossA_defeatMethod = how
    if how == "shield":
        print()
        print("The " + color("GUARDIAN", Colors.red) + " is out of ENERGY, and it retreats deeper into the room.")
        print("You gained a key to unlock the door in the " + color("center", Colors.yellow) + " of the main room.")
        print("")
        start()
    elif how == "sword":
        print()
        print("The " + color("GUARDIAN", Colors.red) + " is dead, its corpse lays in the middle of the room.")
        print("You gained a key to unlock the door in the " + color("center", Colors.yellow) + " of the main room.")
        print("")
        start()

# main room
def start():

    # flavor text on first start
    if not sword_get and not shield_get and not bossA_defeat:
        print("You are in a dark room, and you have been left defenceless.")
        print("There is a door to your " + color("left", Colors.yellow) + " and " + color("right", Colors.yellow) + ".")
        print("A locked door stands in the " + color("center", Colors.yellow) + ".")
        print("Which one do you take?")

    # flavor text after getting the sword/shield
    if sword_get and not bossA_defeat or shield_get and not bossA_defeat:
        print("You are in a dark room, no longer defenceless.")
        print("You feel like you could take on anything.")
        print(color("Everything.", Colors.red))
        print("...")
        print("There is a door to your " + color("left", Colors.yellow) + " and " + color("right", Colors.yellow) + ".")
        print("A locked door stands in the " + color("center", Colors.yellow) + ".")
        print("Which one do you take?")

    # flavor text after defeating the guardian
    if sword_get and bossA_defeat or shield_get and bossA_defeat:
        print("...")
        print("There is a door to your " + color("left", Colors.yellow) + " and " + color("right", Colors.yellow) + ".")
        print("The " + color("center", Colors.yellow) + " door that was previously locked is now unlocked.")
        print("Which one do you take?")
    
    # commands
    while True:
        choice = input("> ").lower()
        
        # leads to the sword/shield room
        if choice == "left":
            sword_room()
        
        # help text
        elif choice == "help":
           print("'" + color("left", Colors.yellow) + "': Leaves the main room and heads into the room to the left.")
           print("'" + color("right", Colors.yellow) + "': Leaves the main room and heads into the room to the right.")
           print("'" + color("center", Colors.yellow) + "': Leaves the main room and heads into the room ahead of you.")
           print("'" + color("inv", Colors.yellow) + "' or '" + color("inventory", Colors.yellow) + "': Checks your inventory.")
        
        # leads to the guardian fight, will lock after it is defeated
        elif choice == "right":
            if bossA_defeat == False:
                guardian_room()
            elif bossA_defeat == True:
                print("It's locked.")
        
        # useless but its cool to make the game seem like it has a complex inventory
        elif choice == "inv" or choice == "inventory":
            if shield_get == True:
                print("You have a " + color("SHIELD", Colors.green) + ", and nothing else.")
            elif sword_get == True:
                print("You have a " + color("SWORD", Colors.green) + ", and nothing else.")
            else:
                print("You have nothing.")
        
        # end door, unlocks once the guardian is defeated
        elif choice == "center":
            if bossA_defeat == False:
                print("It's locked.")
            elif bossA_defeat == True:
                hallway()
        
        # failsafe text
        else:
            print("I got no idea what that means.")

def start2():

    # flavor text on first start
    print("A familiar feeling washes over you.")
    print("There is a door to your " + color("left", Colors.yellow) + " and " + color("right", Colors.yellow) + ".")
    print("The " + color("left", Colors.yellow) + " door is locked.")
    print("Seems like going to the " + color("right", Colors.yellow) + " is the only option.")
    
    
    # commands
    while True:
        choice = input("> ").lower()
        
        # leads to the sword/shield room
        if choice == "left":
            if puzzleA_complete == False:
                print("It's locked.")
        
        # help text
        elif choice == "help":
           print("'" + color("left", Colors.yellow) + "': Leaves the main room and heads into the room to the left.")
           print("'" + color("right", Colors.yellow) + "': Leaves the main room and heads into the room to the right.")
           #print("'" + color("center", Colors.yellow) + "': Leaves the main room and heads into the room ahead of you.")
           print("'" + color("inv", Colors.yellow) + "' or '" + color("inventory", Colors.yellow) + "': Checks your inventory.")
        
        # leads to the guardian fight, will lock after it is defeated
        elif choice == "right":
            puzzle_room()
        
        # useless but its cool to make the game seem like it has a complex inventory
        elif choice == "inv" or choice == "inventory":
            if shield_get == True:
                print("You have a " + color("SHIELD", Colors.green) + ", and nothing else.")
            elif sword_get == True:
                print("You have a " + color("SWORD", Colors.green) + ", and nothing else.")
            else:
                print("You have nothing.")
        
        # end door, unlocks once the guardian is defeated
        
        # failsafe text
        else:
            print("I got no idea what that means.")

def hallway():
    for char in "You walk through the center door.":
        time.sleep(.1)
        print(char, end='', flush=True)
    print("")
    time.sleep(1)
    for char in "There is a long, dark hallway.":
        time.sleep(.1)
        print(char, end='', flush=True)
    print("")
    time.sleep(1)
    for char in "You step into the hallway.":
        time.sleep(.1)
        print(char, end='', flush=True)
    print("")
    time.sleep(1)
    for char in "The door locks behind you.":
        time.sleep(.1)
        print(char, end='', flush=True)
    print("")
    time.sleep(1)
    for char in "You enter the room.":
        time.sleep(.1)
        print(char, end='', flush=True)
    print("")
    time.sleep(1)
    for char in "...":
        time.sleep(.5)
        print(char, end='', flush=True)
    print("")
    time.sleep(.5)
    print("")
    start2()
    
def puzzle_room():

    # flavor text on first start
    print("A wall is inscribed with words.")
    print("'The " + color("GUARDIAN", Colors.red) + " has been defeated.'")
    print("'How did victor conquer such a grand fighter?'")
    print("...")
    print("What did you do to finish off the " + color("GUARDIAN", Colors.red) + "?")
    
    # commands
    while True:
        choice = input("> ").lower()
        
        if choice == "attack":
            if bossA_defeatMethod == "sword":
                end_cutscene()
            elif not bossA_defeatMethod == "sword":
                print("The room shudders.")
                print("Maybe that wasn't the correct answer?")
        elif choice == "defend":
            if bossA_defeatMethod == "shield":
                end_cutscene()
            elif not bossA_defeatMethod == "shield":
                print("The room shudders.")
                print("Maybe that wasn't the correct answer?")
        # help text
        elif choice == "help":
           print("What " + color("ACTION", Colors.blue) + " did you use to either kill or make the " + color("GUARDIAN", Colors.red) + " retreat?")
        # failsafe text
        else:
            print("I got no idea what that means.")

def end_cutscene():
    for char in "You see the left room door open.":
        time.sleep(.1)
        print(char, end='', flush=True)
    print("")
    time.sleep(1)
    for char in "As you head to the left room, you feel an uneasy worry on what lies ahead.":
        time.sleep(.1)
        print(char, end='', flush=True)
    print("")
    time.sleep(1)
    for char in "In the room there is a long set of stairs going up.":
        time.sleep(.1)
        print(char, end='', flush=True)
    print("")
    time.sleep(1)
    for char in "As you reach the end of the stairs, you feel something that you thought you never would feel again.":
        time.sleep(.1)
        print(char, end='', flush=True)
    print("")
    time.sleep(1)
    for char in "Warmth.":
        time.sleep(.1)
        print(char, end='', flush=True)
    print("")
    time.sleep(1)
    for char in "The sun shines brightly over the horizon.":
        time.sleep(.1)
        print(char, end='', flush=True)
    print("")
    time.sleep(1)
    for char in "The End.":
        time.sleep(.5)
        print(char, end='', flush=True)
    time.sleep(5)
    print("")
    input("Hit ENTER to exit...")
    exit(0)
        

launch()