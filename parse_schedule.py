import csv
from datetime import datetime

# Load in schedule file
schedule_file = 'packers_schedule_2024.csv'


# Function to obtain the closest game based off system time
def find_next_game(csv_path):
    next_game = None

    # Obtain current time
    now = datetime.now()

    # Open csv with read permission
    with open(csv_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            game_date = datetime.strptime(row['Date'], "%Y-%m-%d")

            # Return game if one is found, else return none
            if game_date >= now:
                next_game = row
                return next_game
    return None


def main():
    nearest_game = find_next_game(schedule_file)
    print(nearest_game)


if __name__ == "__main__":
    main()
