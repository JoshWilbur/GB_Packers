import unittest
import os
from datetime import datetime
from parse_schedule import Packers_Games


# This class will test each method of the Packers_Games class
class TestPackersGames(unittest.TestCase):
    def setUp(self):
        # Assign packers_game attribute to the test csv file
        test_csv_path = os.path.join(os.path.dirname(__file__), "test_schedule.csv")
        self.packers_games = Packers_Games(test_csv_path)

    def test_import_schedule(self):
        # Ensure the test schedule imported correctly
        schedule = self.packers_games._import_schedule()
        self.assertEqual(len(schedule), 3)
        self.assertEqual(schedule[0]["Opponent"], "Chicago Bears")
        self.assertIsInstance(schedule[0]["Date"], datetime)

    def test_next_game(self):
        # Test for the first game, this test may need to be more robust in the future
        self.packers_games.game_schedule[0]["Date"] = datetime(2024, 9, 1)
        next_game = self.packers_games.next_game()
        self.assertEqual(next_game["Game"], "1")
        self.assertEqual(next_game["Opponent"], "Chicago Bears")

    # def test_print_next_game(self):
    # TODO: add testing for this method
