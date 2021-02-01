from bs4 import BeautifulSoup
import requests

CURRENT_YEAR = 2021

for year in range(CURRENT_YEAR - 20, CURRENT_YEAR + 1):
    print(f"Fetching data for {year}")
    players = []

    # Fetch driving stats table for the current year
    response = requests.get(url=f"https://www.pgatour.com/stats/stat.101.y{year}.html")
    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find("table", {"id": "statsTable"}).find_all("tr")

    # Extract details for each player in the driving stats table
    for row in rows[1:]:
        details = row.find_all("td")
        position = details[0].getText().strip()
        name = details[2].getText().strip()
        avg_dist = details[4].getText().strip()
        players.append(f"{position},{name},{avg_dist}")

    # Find tour avg for the year
    tour_average = soup.select_one(selector=".tour-average").find("span").getText().strip()

    # Write to csv file
    with open(f"driving_stats/stats_{year}_avg_{tour_average}.csv", "w") as csv_file:
        for player in players:
            csv_file.write(player)
            csv_file.write("\n")

