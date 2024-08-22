import csv
from bs4 import BeautifulSoup
import requests


# This class has the ability to scrape stats from PFR (see README)
class Packers_Stats:
    def __init__(self, url):
        self.url = url
        self.data = []

    # ETHICAL DATA SCRAPING ROBOT
    def scrape_pfr_data(self):
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
        print(f"Data successfully saved to {filename}")

    def scrape_and_save(self, filename):
        self.scrape_pfr_data()
        self.save_to_csv(filename)


def main():
    url = "https://www.pro-football-reference.com/teams/gnb/2023.htm#games"
    stats = Packers_Stats(url)
    stats.scrape_and_save("packers_team_stats_2023.csv")


if __name__ == "__main__":
    main()
