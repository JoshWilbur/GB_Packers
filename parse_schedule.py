import csv

schedule_file = 'packers_schedule_2024.csv'

with open(schedule_file, mode='r') as file:
    # Create a CSV reader object
    csv_reader = csv.DictReader(file)

    # Iterate over the CSV file
    for row in csv_reader:
        game = row['Game']
        date = row['Date']
        time = row['Time_EST']
        opponent = row['Opponent']
        home_away = row['Home_Away']
        
        # Print the schedule as it is read in
        print(f"Week {game}: {date} at {time}, vs {opponent} ({home_away})")
