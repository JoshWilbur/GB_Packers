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

    def grab_table_data(self, table, defined_headers=None):
        # Define headers to grab from table
        if defined_headers is not None:
            headers = defined_headers
        else:
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

    def fetch_website(self, url, print_html=0, output_file="output.html"):
        # Fetch website and error check
        response = requests.get(url)
        if response.status_code == 200:
            print("HTTP status code: 200")
            self.soup = BeautifulSoup(response.text, "html.parser")
        else:
            raise Exception(
                f"Failed to fetch page:" f"Status code {response.status_code}"
            )
        # Print HTML to a file for debugging, but only if needed
        if print_html == 1:
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(self.soup.prettify())
