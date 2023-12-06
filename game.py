"""
This class is the main class of the "Trapped" application.
"Trapped" is a scape room, text based adventure game. Users can walk
around some scenery, pick items, use items and work out how to escape!


This main class creates and initialises all the others: it creates all rooms,
items and creates the parser and starts the game. It also evaluates and executes the
commands that the parser returns.

This game is adapted from the 'World of Zuul' by Michael Kolling and 
David J. Barnes. The original was written in Java and has been simplified and
converted to Python by Kingsley Sage.

The extention of the game developed by:
Andres Sebastian Salazar Alturo
Candidate number: 276209

As part of course work for Programming through python 2023 :D
"""

#Set the path to other directories
import sys
import os

## Get the current working directory
current_dir = os.getcwd()
## Append the cwd
sys.path.append(current_dir)
from src.room import Room
from src.text_ui import TextUI
from src.items import Item
from src.backpack import Backpack
from src.player import Player

class Game:

    def __init__(self):
        """
        Initialises the game.
        """
        ##Dictionary with all rooms, key as string name and value as object
        self.game_rooms = {}
        ##Create the player object
        self.my_player = Player()
        ##Set up all rooms and objects
        self.game_set_up()
        ##Initial position - Can be change to test features in other rooms
        self.my_player.current_room = self.first_room
        ##Text to UI object
        self.textUI = TextUI()

    def game_set_up(self):
        """
            Sets up all game. Create:
            Player
            Rooms
            Items
            Backpack
        :return: None
        """
        #########################################
        ######Now create the room objects########
        #########################################

        ##Initialise all the rooms in the map
        self.first_room = Room("your Initial location")

        ##Intialize corridor1
        self.corridor1 = Room("in a corridor1")

        ##Rooms option to corridor1
        self.cleaning_room = Room("in the cleaning room")
        self.security_room = Room("in the security room", password='1234')

        ##Initialize corridor2
        self.corridor2 = Room("in a corridor2", locked="card")

        ##Rooms option to corridor2
        self.lab = Room("in a computing lab", password="4321")
        self.office = Room("in the computing admin office", locked="card2")
        self.kitchen = Room("in the kitchen", locked = "statue")

        ##Kitchen options
        self.stairs = Room("You are in the stairs")
        self.garden = Room("in the garden", password="123456")
        self.dining_room = Room("in the dining room", locked = True)

        ##Stairs options
        self.basement = Room("You are in the basement")

        ##Basement options
        self.laundry_room = Room("You are in the laundry room")
        self.storage = Room("You are in the storage", password="1221")

        ##Dungeon options
        self.dungeon = Room("You are in the dangeon, just can go out using the stone!! Guess the word to get the key!!")

        ##Exit!!
        self.exit = Room("exit", locked = "key")

        #########################################
        ####Now create the exits for each room###
        #########################################

        ##First room posibilities
        """Empty room, nothing to look for"""
        self.first_room.set_exit("north", self.corridor1)

        ##Corridor1 posibilities
        self.corridor1.set_exit("west", self.cleaning_room)
        self.corridor1.set_exit("east", self.security_room)
        self.corridor1.set_exit("north", self.corridor2)
        self.corridor1.set_exit("south", self.first_room)

        ##Cleaning room posibilites
        """Could find a hint to solve a puzzle"""
        self.cleaning_room.set_exit("east", self.corridor1)

        ##Security room posibilities
        """Could find the key to go into the kitchen"""
        self.security_room.set_exit("west", self.corridor1)

        ##Corridor2 posibilities
        self.corridor2.set_exit("west", self.lab)
        self.corridor2.set_exit("east", self.office)
        self.corridor2.set_exit("north", self.kitchen)
        self.corridor2.set_exit("south", self.corridor1)

        ##Lab posibilities
        self.lab.set_exit("east", self.corridor2)
        
        ##Office posibilities
        self.office.set_exit("west", self.corridor2)

        ##Kitchen posibilities
        self.kitchen.set_exit("west", self.garden)
        self.kitchen.set_exit("east", self.dining_room)
        self.kitchen.set_exit("north", self.stairs)
        self.kitchen.set_exit("south", self.corridor2)

        ##stairs posibilities
        self.stairs.set_exit("north", self.basement)
        self.stairs.set_exit("south", self.kitchen)

        ##Garden posibilities
        self.garden.set_exit("east", self.kitchen)

        ##Dining room posibilities
        self.dining_room.set_exit("west", self.kitchen)
        self.dining_room.set_exit("east", self.exit)

        ##Basement posibilities
        self.basement.set_exit("west", self.storage)
        self.basement.set_exit("east", self.laundry_room)
        self.basement.set_exit("south", self.stairs)

        ##Storage posibilities
        self.storage.set_exit("east", self.basement)

        ##Laundry room posibilities
        self.laundry_room.set_exit("west", self.basement)

        ##Exit
        self.exit.set_exit("west", self.dining_room)

        ###############################
        #####Initialize the objects####
        ###############################

        # Create items for cleaning room
        self.card2 = Item("card2", "Could open another door")
        self.code = Item("code", "Could work as password for security room, 1234")

        ## Create items for security room
        self.card = Item("card", "Could open a door, keep it in backpack")

        ##Create items for lab
        self.pocket = Item("pocket", 3)
        self.statue = Item("statue", "To press the button in the office that opens the kitchen door")
        self.puzzle = Item("puzzle", "Guess the number puzzle")
        self.document1 = Item("document1", """

        A lab with some computers, no computer is working, all are modern but with lots of dust and broken
        someone with no patience may tried to make them work.

        To use the pocket, pick it up and use the command 'use' + 'pocket' and increse your backpack capacity. 
        You should pick the pocket and use it before pick another items, your backpack capacity is just 3!.
        
        Tip: To use interact with the puzzle pick it up and use the command 'use' + 'puzzle'
        Tip: Remember you can remove items from your backpack with the command 'remove' + 'object_to_remove'
        Tip: Keep in mind that your initial backpack capacity is 3 items. Remove objects that you are not going
        to need later as documents, try not to remove cards, keys or codes. You may find a pocket in other room
        that item could help you to increase you backpack capacity!
                              """)
        self.document2 = Item("document2", "The key could be in the basement")

        ##Create items for office
        self.button = Item("button", "Keep it press to access the kitchen")
        self.document3 = Item("document3", """

        Office room - silence, all broken, dirty and lots of desks cluttered in the middle.

        The laboratory password is 4321. To use the statue and press the button 
        use the command 'use' + 'statue'
                              """)

        ##Create items for kitchen
        self.document4 = Item("document4", "The stairs lead to the basement")

        ##Create items for garden
        self.stone = Item("stone", "Allow teleport")
        self.document8 = Item("document8", """

        The garden is everything but a beautiful garden, looks like a junkyard there are lots of old clothes
        all around the place. The plants look strange too, like angry and dark green, they do not have
        eyes but you can feel that they look at you and laugh...
        
        In the middle there is a stone, look like a diamond, seems to be the object that could help you to escape.

        Tip: To use the stone, use the command 'use' + 'stone', then type the room you want to go. E.g. 'dungeon'.
        """)

        ##Create items for dining room
        self.operation_game = Item("operation_game", "Use it and solve the operations to get an item!")

        ##Create items for basement
        self.document10 = Item("document10", """

        Some filthy and full of spiderwebs. Maybe no one have been here in a lot of time...

        Tip: At east is the laundry room and at west is the storage room, you should chech both.

        """)

        ##Create items for laundry room
        self.mini_game = Item("mini_game", "Organise the figures mini_game, solve it and get an item!")
        self.storage_password = Item("storage_password", "The storage password is 1221")
        self.document5 = Item("document5", """
        
        To interact with the mini_game. Pick it up and use command 'use' + 'mini_game'
        
        Tip: To pick the mini_game remember to use the command 'pick' + 'mini_game'.
                              """)

        ##Create items for storage room
        self.garden_password = Item("garden_password", "The garden password is 123456")
        self.document6 = Item("document6", """
        
        To interact with the operation_game. Pick it up and use command 'use' + 'operation_game'
                              """)

        ##Create items for dungeon
        self.key = Item("key", "Use the key to open the final door and escape")
        self.hungman_game = Item("hangman_game", "Play the game to get the final key!")
        self.document9 = Item("document9", """

        You are in a strange place, is like jail, is all wet and smells like sulfur, the walls are made of some type of rock. 
        In one corner there is a skeleton handcuffed and tied to a chain in the ceiling.
        There is an item in the room, some game, you should pick it up and play it, could help you to not end like our friend
        in the corner.

        Tip: Guess the word to win the key and escape! You can type any letter and if you know the answer type the full word.

        Tip: To use the hangman_game, pick it using command 'pick' + 'hangman_game' and use the command 'use' + 'hangman_game'.
                              """)

        ##Create items for dining_room
        self.document7 = Item("document7", """

        Use the stone, go to the dungeon, win the game and get the key to escape!!
        The stone is in the garden.
        And look the exit is on the east side!! We are really close! Just get the key!
        
        Tip: To use the stone, use the command 'use' + 'stone', then type the room you want to go. E.g. 'dungeon'
                              """)

        # Add items to cleaning room
        self.cleaning_room.add_item_to_room(self.code)
        self.cleaning_room.add_item_to_room(self.card2)

        # Add items to security room
        self.security_room.add_item_to_room(self.card)

        ##Add item to lab
        self.lab.add_item_to_room(self.statue)
        self.lab.add_item_to_room(self.puzzle)
        self.lab.add_item_to_room(self.pocket)
        self.lab.add_item_to_room(self.document1)
        ##Add hidden document to lab
        self.lab.add_hidden_item_to_room(self.document2)

        ##Add item to office
        self.office.add_item_to_room(self.button)
        self.office.add_item_to_room(self.document3)

        ##Add item to kitchen
        self.kitchen.add_item_to_room(self.document4)

        ##Add item to garden
        self.garden.add_item_to_room(self.stone)
        self.garden.add_item_to_room(self.document8)

        ##Add item to basemen
        self.basement.add_item_to_room(self.document10)

        ##Add items to laundry room
        self.laundry_room.add_item_to_room(self.mini_game)
        self.laundry_room.add_item_to_room(self.document5)
        self.laundry_room.add_hidden_item_to_room(self.storage_password)

        ##Add items to storage room
        self.storage.add_item_to_room(self.operation_game)
        self.storage.add_item_to_room(self.garden_password)
        self.storage.add_item_to_room(self.document6)

        ##Add item to dining_room
        self.dining_room.add_item_to_room(self.document7)

        ##Add items to dungeon
        self.dungeon.add_hidden_item_to_room(self.key)
        self.dungeon.add_item_to_room(self.hungman_game)
        self.dungeon.add_item_to_room(self.document9)

        ################################
        #####Initialize the backpack####
        ################################

        ##Create the backpack
        self.backpack = Backpack(3)

        ##Assign backpack to player
        self.my_player.backpack = self.backpack

        ##Create a dictionary with all positions
        self.game_rooms = {"first_room":self.first_room, "corridor1":self.corridor1, "cleaning_room":self.cleaning_room,"security_room":self.security_room,
                           "corridor2":self.corridor2, "computing_lab":self.lab, "office":self.office, "kitchen":self.kitchen,
                           "stairs":self.stairs, "garden":self.garden, "dining_room":self.dining_room,
                           "basement":self.basement, "storage_room":self.storage, "laundry_room":self.laundry_room,
                           "dungeon":self.dungeon}

    def play(self):
        """
            The main play loop.
            asks for the players name and add the attribute to the players object, then the game's main loop 
            keep asking for command until the player use the command 'quit' or finish the game.
        :return: None
        """
        ##Print the welcome message
        self.textUI.print_welcome()

        ##Set player's name
        self.textUI.print_to_textUI("Type your name/nickname: ")
        player_name, second_word = self.textUI.get_command()     ##Returns a 2-tuple
        self.my_player.name = player_name
        self.textUI.print_lines()
        self.textUI.print_to_textUI(f"Nice to meet you {self.my_player.name}, let's start!!")
        self.textUI.print_lines()

        finished = False
        while not finished:
            self.textUI.print_to_textUI(f'command words: {self.textUI.show_command_words()}')
            self.textUI.print_lines()
            self.textUI.print_to_textUI(f'possible movements: {self.textUI.show_posible_movements()}')
            self.textUI.print_lines()
            command = self.textUI.get_command()  # Returns a 2-tuple
            finished = self.process_command(command)
            if self.my_player.current_room == self.exit:
                self.textUI.final_context()
                finished = True
        self.textUI.print_to_textUI("Thank you for playing!")

    def process_command(self, command):
        """
            Process a command from the TextUI.
            Gets the user input and depending on the first word selects the command and does what user 
            specifies with the second word.
        :param command: a 2-tuple of the form (command_word, second_word)
        :return: True if player typed quit.
        """
        command_word, second_word = command
        if command_word != None:
            command_word = command_word.upper()
            if second_word == "room":
                second_word = second_word.upper()

        want_to_quit = False
        if command_word == "HELP":
            ##Show useful information about the game and commands
            self.textUI.print_help()

        elif command_word == "GO":
            ##Direction is the second word
            self.do_go_command(second_word)
            self.textUI.print_lines()

        elif command_word == "CURRENT" and second_word == "ROOM":
            ##Display current room info
            self.textUI.print_to_textUI(self.my_player.current_room.get_short_description())

        elif command_word == "EXPLORE":
            ##Show the available items in the room
            self.my_player.current_room.get_room_items()
            self.textUI.print_lines()

        elif command_word == "PICK":
            ##Item to pick is the second word
            self.do_pick_command(second_word)
            self.textUI.print_lines()
        
        elif command_word == 'ITEMS':
            ##Show the items in the backpack
            self.my_player.backpack.show_all_items()
            self.textUI.print_lines()

        elif command_word == "USE":
            ##Use one item in the backpack
            self.do_use_command(second_word)

        elif command_word == 'REMOVE':
            ##Item to delete is second word
            self.do_remove_command(second_word)
            self.textUI.print_lines()

        elif command_word == "QUIT":
            ##Close the game
            want_to_quit = True

        else:
            # Unknown command...
            self.textUI.print_to_textUI("Don't know what you mean.")

        return want_to_quit
    
    def do_use_command(self, second_word):
        """
            Process when the player wants to use an item. The player can just use some items, like 
            the games, the stone, and the statue to press the button.
            :param second_word: Players second word, must be a item that can be use. If can't be use
            or not in the bag pack ask for a command again.
            :return: None
        """

        if second_word == None:
            # Missing second word...
            self.textUI.print_to_textUI("use what item?")
            return
        
        ##Use the stone to teleport
        if second_word == "stone":
            room_response = self.my_player.current_room.allow_teleport(self.my_player.backpack, self.game_rooms)
            self.textUI.print_lines()
            if room_response == False:
                self.textUI.print_to_textUI("You do not have the stone to teleport")
            elif room_response == None:
                return
            else:
                self.my_player.current_room = room_response
                self.textUI.print_to_textUI(self.my_player.current_room.get_long_description())

        ##Use the puzzle
        elif second_word == "puzzle":
            ## If puzzle is not in the backpack or in the room, si not possible to do it
            if (second_word not in self.my_player.backpack.contents):
                self.textUI.print_to_textUI("The puzzle is not in the room or your backpack")
            else:
                self.textUI.guess_puzzle_info()
                quit_puzzle = False
                while not quit_puzzle:
                    self.textUI.print_to_textUI("Solve the puzzle to continue")
                    self.textUI.print_to_textUI("Type 'back' to try the puzzle later")
                    try:
                        guess, word2 = self.textUI.get_command()                         # Returns a 2-tuple
                        if guess == 'back':
                            quit_puzzle = True
                        if self.my_player.backpack.solve_puzzle(int(guess), self.my_player.current_room.hidden_items):
                            ##Delete the pocket from the backpack
                            self.my_player.backpack.remove_item(second_word)
                            quit_puzzle = True
                    except ValueError:
                        print("Do not know what you mean")

        elif second_word == "mini_game":
            ## If mini_game is not in the backpack, not possible to do it
            if (second_word not in self.my_player.backpack.contents):
                self.textUI.print_to_textUI("The mini_game is not in your backpack")
            else:
                quit_mini_game = False
                self.textUI.mini_game_info()
                while not quit_mini_game:
                    if self.my_player.backpack.process_mini_game(self.my_player.current_room.hidden_items):
                        self.textUI.print_to_textUI("Type 'back' to try the puzzle later\n Press any key to continue")
                        keep_playing, word2 = self.textUI.get_command()
                        if keep_playing == 'back':
                            quit_mini_game = True
                    else: 
                        self.textUI.print_to_textUI("The storage room password is in you backpack")
                        self.textUI.print_lines()
                        ##Remove the mini_game from the backpack
                        self.my_player.backpack.remove_item(second_word)
                        quit_mini_game = True

        elif second_word == "hangman_game":
            ## If mini_game is not in the backpack or in the room, si not possible to do it
            if (second_word not in self.my_player.backpack.contents):
                self.textUI.print_to_textUI("The hangman_game is not in your backpack")
            else:
                if self.my_player.backpack.process_hangman_game(self.my_player.current_room.hidden_items):
                    ##Remove the hangman_game from the backpack
                    self.my_player.backpack.remove_item(second_word)

        ##Use operation item
        elif second_word == "operation_game":
            ## If mini_game is not in the backpack or in the room, si not possible to do it
            if (second_word not in self.my_player.backpack.contents):
                self.textUI.print_to_textUI("The operation_game is not in your backpack")
            else:
                ##Operation_game context
                self.textUI.operation_game_info()
                start_game, word2 = self.textUI.get_command()
                if start_game == 'start':
                    if self.my_player.backpack.process_operation_game(self.game_rooms):
                        self.textUI.print_lines()
                        ##Remove the operation_game from the backpack
                        self.my_player.backpack.remove_item(second_word)
                    else:
                        ##When the player lose by time
                        print("Try to the game again!")
                else:
                    self.textUI.print_to_textUI("Remember to solve the operation_game to open the dining_room door")
                    self.textUI.print_lines()

        ##Use pocket to increase backpack capacity
        elif second_word == "pocket":
            if self.my_player.backpack.increase_backpack_capacity(second_word):
                ##Delete the pocket from the backpack
                self.my_player.backpack.remove_item(second_word)
            else:
                self.textUI.print_to_textUI(f'{second_word} not in backpack')

        ##Use statue to press the button
        elif second_word == "statue":
            if self.my_player.backpack.check_item(second_word):
                statue_object = self.my_player.backpack.contents[second_word]
                if self.my_player.current_room != self.game_rooms["office"]:
                    self.textUI.print_to_textUI(f"the {second_word} is in the floor")
                    self.my_player.current_room.add_item_to_room(statue_object)
                    ##Remove the statue from the backpack
                    self.my_player.backpack.remove_item(second_word)
                    return
                else:
                    self.my_player.current_room.add_item_to_room(statue_object)
                    ##Remove the statue from the backpack
                    self.my_player.backpack.remove_item(second_word)
                    self.textUI.print_to_textUI(f"the {second_word} is pressing the button")
                    ##Add statue to lab again in case the user use the statue in the wrong room
                    self.lab.add_item_to_room(self.statue)

            else:
                self.textUI.print_to_textUI(f"{second_word} not in backpack")

        else: 
            self.textUI.print_to_textUI("The object is not in the backpack")


    def do_remove_command(self, second_word):
        """
            Removes the item from the player's backpack and adds the item to 
            the current room, like dropping the item, the player can pick the 
            item again if the backpack is not full.
        :param second_word: the item the player wants to remove from backpack
        :return: None
        """

        if second_word == None:
            # Missing second word...
            self.textUI.print_to_textUI("Remove what item?")
            return
        
        try:
            ##Get the potential deleted object
            object_to_remove = self.my_player.backpack.contents[second_word]
        except KeyError:
            object_to_remove = None

        if self.my_player.backpack.remove_item(second_word) == True:
            self.textUI.print_to_textUI(f"{second_word} was remove from your backpack")
            ##Add the remove item to the current room
            self.my_player.current_room.add_item_to_room(object_to_remove)

    def do_pick_command(self, second_word):
        """
            Allows players to pick an item and add it to the backpack, 
            when the player adds the item to the backpack, it disappears 
            from the room and is now available just in the backpack.
        :param second_word: the item the player wants to add to backpack
        :return: None
        """
        if second_word == None:
            # Missing second word...
            self.textUI.print_to_textUI("Pick what item?")
            return
        
        if self.my_player.backpack.check_item(second_word):
            self.textUI.print_to_textUI("Item already in the backpack")
        else:
            try:
                if (self.my_player.backpack.add_item(self.my_player.current_room.room_items[second_word])):
                    self.textUI.print_to_textUI(f"{second_word} has been added to you back pack")
                    ##Delete the picked item from room_items
                    self.my_player.current_room.remove_item_to_room(second_word)
                else:
                    self.textUI.print_to_textUI("Try to remove an item")
            except KeyError:
                print("Item not in the room")

    def do_go_command(self, second_word):
        """
            Allows the player to move through the rooms, nonetheless, 
            some rooms are locked by password, cards, or key. 
        :param second_word: the direction the player wishes to travel in
        :return: None
        """
        if second_word == None:
            # Missing second word...
            self.textUI.print_to_textUI("Go where?")
            return

        ## get_exit return the room object
        next_room = self.my_player.current_room.get_exit(second_word)
        if next_room == None:
            self.textUI.print_to_textUI("There is no door!")

        else:
            ## Check if the room has password
            if next_room.password is not None:
                self.textUI.print_to_textUI("Type the password")
                password, second_word = self.textUI.get_command()
                if next_room.can_enter(self.my_player.backpack, password=password):
                    ##Enter the room
                    self.my_player.current_room = next_room
                    self.textUI.print_to_textUI(self.my_player.current_room.get_long_description())
                    return
                else:
                    self.textUI.print_to_textUI(self.my_player.current_room.get_long_description())
                    return
            
            ## Check if the room is locked
            if next_room.locked is not None:
                ## Go inside the room if does not require card, password and it was typed properly
                if next_room.can_enter(self.my_player.backpack, game_rooms = self.game_rooms, next_room = next_room, dining_room_lock = self.game_rooms):
                    self.my_player.current_room = next_room
                    self.textUI.print_to_textUI(self.my_player.current_room.get_long_description())
                    return
                else:
                ## If the card is not in the backpack, stay in the current room, not access allowed
                    self.textUI.print_to_textUI(self.my_player.current_room.get_long_description())
                    return
            ## If the rooms does not have key or password just go in
            self.my_player.current_room = next_room
            self.textUI.print_to_textUI(self.my_player.current_room.get_long_description())

def main():
    game = Game()
    game.play()

if __name__ == "__main__":
    main()
