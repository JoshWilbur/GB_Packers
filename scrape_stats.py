import csv
from bs4 import BeautifulSoup
import requests


# This class has the ability to scrape team stats from PFR (see README)
class Stats:
    def __init__(self, team, year):
        self.url = (
            f"https://www.pro-football-reference.com/"
            f"teams/{team}/{year}.htm#games"  # noqa E501
        )
        self.data = []

    # ETHICAL DATA SCRAPING ROBOT
    def scrape_team_data(self):
        # Fetch website and error check
        response = requests.get(self.url)
        if response.status_code == 200:
            self.soup = BeautifulSoup(response.text, "html.parser")
        else:
            raise Exception(
                f"Failed to fetch page:" f"Status code {response.status_code}"
            )

        # Find table with game data
        table = self.soup.find("table", {"id": "games"})
        if not table:
            print("Failed to find the table with id 'games'")
            return

        # Define headers to grab from "Schedule & Game Results" table
        headers = [
            "Day",
            "Date",
            "Time",
            "boxscore",
            "Result",
            "OT",
            "Record",
            "Home/Away",
            "Opponent",
            "Tm_Score",
            "Opp_Score",
            "O_1stD",
            "O_TotYd",
            "O_PassY",
            "O_RushY",
            "O_TO",
            "D_1stD",
            "D_TotYd",
            "D_PassY",
            "D_RushY",
            "D_TO",
            "O_EXP",
            "D_EXP",
            "Sp_Tms",
        ]
        self.data.append(headers)

        # Extract the rows
        rows = table.find("tbody").find_all("tr")
        for row in rows:
            # Skip rows with class: thead
            if row.get("class") and "thead" in row.get("class"):
                continue

            # Extract cells from the row
            cells = row.find_all("td")
            row_data = [cell.get_text(strip=True) for cell in cells]

            # Ensure the row has the same length as the header
            if len(row_data) < len(headers):
                row_data.extend([""] * (len(headers) - len(row_data)))

            self.data.append(row_data)

    def save_to_csv(self, filename):
        # Save the data to a CSV file
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.data)
        print(f"Data saved to {filename}")

    def read_csv(self, file_path):
        with open(file_path, mode="r") as file:
            reader = csv.DictReader(file)
            games = [row for row in reader]
        return games

    # This method outputs stats based on the input week (TODO: refine more)
    def stats_on_week(self, file_path, week):
        games_data = self.read_csv(file_path)
        if week > len(games_data):
            return f"Failed to find week:{week}"

        game = games_data[week - 1]  # Account for indexing differences

        # Some headers contain irrelevant info, only include useful ones
        output_headers = [
            "Date",
            "Time",
            "Result",
            "Record",
            "Home/Away",
            "Opponent",
            "Tm_Score",
            "Opp_Score",
            "O_1stD",
            "O_TotYd",
            "O_PassY",
            "O_RushY",
            "O_TO",
            "D_1stD",
            "D_TotYd",
            "D_PassY",
            "D_RushY",
            "D_TO",
        ]

        return {header: game[header] for header in output_headers}

    # Output basic stats such as date, result, score, etc
    def output_simple_stats(self, stats_on_week):
        stats_on_week = (
            f"Date: {stats_on_week['Date']}\n"
            f"Time: {stats_on_week['Time']}\n"
            f"Result: {stats_on_week['Result']}\n"
            f"Record: {stats_on_week['Record']}\n"
            f"Home/Away: {stats_on_week['Home/Away']}\n"
            f"Opponent: {stats_on_week['Opponent']}\n"
            f"Team Score: {stats_on_week['Tm_Score']}\n"
            f"Opponent Score: {stats_on_week['Opp_Score']}\n"
        )

    def scrape_and_save(self, filename):
        self.scrape_team_data()
        self.save_to_csv(filename)


def main():
    team = "gnb"
    year = "2023"
    stats = Stats(team, year)
    file_path = f"csv_files/packers_team_stats_{year}.csv"
    stats.scrape_and_save(file_path)

    game_data = stats.stats_on_week(file_path, 1)
    print(stats.output_simple_stats(game_data))
    print(f"Data for week: {game_data}")


if __name__ == "__main__":
    main()
