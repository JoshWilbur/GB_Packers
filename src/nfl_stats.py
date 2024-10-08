from scrape_stats import Stats


# This class obtains NFL stats and inherits the Stats class
class NFL_Stats(Stats):
    def __init__(self, team, year):
        super().__init__(team, year)

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
        self.grab_table_data(table, headers)

    # This method will scrape passing stats from PFR
    def scrape_passing_data(self):
        passing_data_url = (
            f"https://www.pro-football-reference.com"
            f"/teams/{self.team}/{self.year}_advanced.htm#advanced_air_yards"
        )
        self.fetch_website(passing_data_url, 1)

        # Find table with game data
        table = self.soup.find("table", {"id": "advanced_air_yards"})
        if not table:
            print("Failed to find the table with id 'advanced_air_yards'")
            return
        self.grab_table_data(table)

        # Save stats to csv
        path = f"csv_files/packers_passing_stats_{self.year}.csv"
        self.save_to_csv(path)

    # This method will scrape rushing stats from PFR
    def scrape_rushing_data(self):
        rushing_data_url = (
            f"https://www.pro-football-reference.com"
            f"/teams/{self.team}/{self.year}_advanced.htm#advanced_rushing"
        )
        self.fetch_website(rushing_data_url, 1)

        # Find table with rushing data
        table = self.soup.find("table", {"id": "advanced_rushing"})
        if not table:
            print("Failed to find the table with id 'advanced_rushing'")
            return
        self.grab_table_data(table)

        # Save stats to csv
        path = f"csv_files/packers_rushing_stats_{self.year}.csv"
        self.save_to_csv(path)

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
    week = 1
    file_path = f"csv_files/packers_team_stats_{year}.csv"
    stats = NFL_Stats(team, year)
    stats.scrape_team_data()
    stats.team_stats_on_week(file_path, week, 1)
    stats.scrape_passing_data()
    # stats.scrape_rushing_data()


if __name__ == "__main__":
    main()
