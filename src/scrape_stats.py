import csv
from bs4 import BeautifulSoup
import requests


# This class has the ability to scrape team stats from PFR (see README)
class Stats:
    def __init__(self, team, year):
        self.data = []
        self.team = team
        self.year = year

    def save_to_csv(self, filename):
        # Save the data to a CSV file
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.data)
        print(f"Data saved to {filename}")

    def read_csv(self, file_path):
        with open(file_path, mode="r") as file:
            reader = csv.DictReader(file)
            info = [row for row in reader]
        return info

    def fetch_website(self, url):
        # Fetch website and error check
        response = requests.get(url)
        if response.status_code == 200:
            self.soup = BeautifulSoup(response.text, "html.parser")
        else:
            raise Exception(
                f"Failed to fetch page:" f"Status code {response.status_code}"
            )

    # ETHICAL DATA SCRAPING ROBOT
    def scrape_team_data(self):
        team_data_url = (
            f"https://www.pro-football-reference.com/"
            f"teams/{self.team}/{self.year}.htm#games"  # noqa E501
        )
        self.fetch_website(team_data_url)

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

        # Save stats to csv
        self.save_to_csv("csv_files/packers_team_stats_{year}.csv")

    # This method will scrape passing states from PFR
    def scrape_passing_data(self):
        passing_data_url = (
            f"https://www.pro-football-reference.com"
            f"/teams/{self.team}/{self.year}_advanced.htm#advanced_air_yards"
        )
        self.fetch_website(passing_data_url)

        # Find table with game data
        table = self.soup.find("table", {"id": "passing"})
        if not table:
            print("Failed to find the table with id 'games'")
            return

        # Define headers to grab from passing stats table
        headers = []
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

        self.save_to_csv("csv_files/packers_passing_stats_{year}.csv")

    # This method outputs stats based on the input week
    def team_stats_on_week(self, file_path, week, printing):
        self.week = week
        games_data = self.read_csv(file_path)
        if self.week > len(games_data):
            return f"Failed to find week:{self.week}"

        game = games_data[self.week - 1]  # Account for indexing differences

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

        # Format data to allow printing to terminal
        data = {header: game[header] for header in output_headers}

        # Output basic stats such as date, result, score, etc
        if printing:
            print(
                f"\nDATA FOR WEEK {self.week} OF THE {self.year}-"
                f"{self.year+1} NFL SEASON:"
                f"\nOn {data['Date']}, {self.year} at {data['Time']}, "
                f"the Green Bay Packers ({data['Record']}) "
                f"played the {data['Opponent']}\n"
                f"Game result: {data['Tm_Score']}-"
                f"{data['Opp_Score']} {data['Result']}\n"
            )


def main():
    team = "gnb"
    year = 2023
    week = 11
    file_path = f"csv_files/packers_team_stats_{year}.csv"
    stats = Stats(team, year)
    # stats.scrape_team_data()
    # stats.team_stats_on_week(file_path, week, 1)
    stats.scrape_passing_data()


if __name__ == "__main__":
    main()
