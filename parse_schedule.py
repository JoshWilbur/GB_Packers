import csv
from datetime import datetime


# This class will allow easy access to the Packers schedule
class Packers_Games:
    def __init__(self, csv_path):
        # Load in schedule file
        self.csv_path = csv_path
        self.game_schedule = self._import_schedule()

    # Load in schedule
    def _import_schedule(self):
        schedule = []
        with open(self.csv_path, mode="r") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                row["Date"] = datetime.strptime(row["Date"], "%Y-%m-%d")
                schedule.append(row)
        return schedule

    # Find the next game
    def next_game(self):
        # Obtain current time
        now = datetime.now()
        for game in self.game_schedule:
            if game["Date"] >= now:
                return game
        return None

    # Allow printing of the next game
    def print_next_game(self):
        self.closest_game = self.next_game()

        if self.closest_game is not None:
            game_date = self.closest_game["Date"].strftime("%B %d, %Y")
            print(
                f"Next Packers Game:\n"
                f"Game {self.closest_game['Game']}: {game_date}"
                f" at {self.closest_game['Time_EST']} EST\n"
                f"Opponent: {self.closest_game['Opponent']}"
            )
        else:
            print("No upcoming games found")


def main():
    schedule_file_2024 = "packers_schedule_2024.csv"
    gb_packers = Packers_Games(schedule_file_2024)
    gb_packers.print_next_game()


if __name__ == "__main__":
    main()
