import unittest
from src.room import Room
from src.items import Item

class TestRoom(unittest.TestCase):

    def setUp(self):
        """
            Runs prior to unit test
        """
        self.room1 = Room("room1")
        self.room2 = Room("room2")
        self.room3 = Room("room3")

        self.item1 = Item("card", "does something")
        self.item2 = Item("card2", "does something")
        self.item3 = Item("card3", "does something")

    def tearDown(self):
        """
            Clear the variables for the next test
        """

        self.room1 = None
        self.room2 = None
        self.room3 = None

        self.item1 = None
        self.item2 = None
        self.item3 = None

    def test_1(self):
        ##Test add exits to rooms
        self.assertTrue(self.room1.set_exit("north", self.room2))
        self.assertTrue(self.room2.set_exit("south", self.room3))
        self.assertEqual(self.room2.get_number_of_exits(), 1)

        ##Test add items to rooms
        self.assertTrue(self.room2.add_item_to_room(self.item1))
        self.assertEqual(self.room2.get_number_of_room_items(), 1)

    def test_2(self):
        ##Test remove items to rooms
        self.room2.add_item_to_room(self.item2)
        self.room2.add_item_to_room(self.item3)
        ##Check the number of items
        self.assertEqual(self.room2.get_number_of_room_items(), 2)
        ##Remove item3
        self.room2.remove_item_to_room(self.item3.item_name)
        ##Check the number of items after remove item3
        self.assertEqual(self.room2.get_number_of_room_items(), 1)