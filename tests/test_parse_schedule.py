import unittest
import os
from io import StringIO
from contextlib import redirect_stdout
from datetime import datetime
from parse_schedule import Packers_Games


# This class will test each method of the Packers_Games class
class TestPackersGames(unittest.TestCase):
    def setUp(self):
        # Assign packers_game attribute to the test csv file
        test_csv_path = os.path.join(os.path.dirname(__file__), "test_schedule.csv")
        self.packers_games = Packers_Games(test_csv_path)
        self.output_file = "test_output.txt"

    # Ensure the test schedule imported correctly
    def test_import_schedule(self):
        schedule = self.packers_games._import_schedule()
        self.assertEqual(len(schedule), 3)
        self.assertEqual(schedule[0]["Opponent"], "Chicago Bears")
        self.assertIsInstance(schedule[0]["Date"], datetime)

    # Test only covers the first game, dates are set far into the future
    def test_next_game(self):
        next_game = self.packers_games.next_game()
        self.assertEqual(next_game["Game"], "1")
        self.assertEqual(next_game["Opponent"], "Chicago Bears")

    # Test if the printed output matches what is expected
    def test_print_next_game(self):
        # Redirect stdout into a StringIO object to avoid making a real file
        f = StringIO()
        with redirect_stdout(f):
            self.packers_games.print_next_game()
        output = f.getvalue().strip()
        self.assertIn("Next Packers Game:", output)
        self.assertIn("Chicago Bears", output)
