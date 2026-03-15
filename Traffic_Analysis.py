# Author:C.D.N.S.Basnayake

import csv
import tkinter as tk
import os

# Task A: Input Validation
def validate_date_input():

    # validate day
    while True:
        try:
            day = int(input("Please enter the day of the survey in the format dd: "))
            if 1 <= day <= 31:
                break
            else:
                print("Out of range - values must be in the range 1 and 31.")
        except ValueError:
            print("Integer required")

    # validate month
    while True:
        try:
            month = int(input("Please enter the month of the survey in the format MM: "))
            if 1 <= month <= 12:
                break
            else:
                print("Out of range - values must be in the range 1 and 12.")
        except ValueError:
            print("Integer required")

    # validate year
    while True:
        try:
            year = int(input("Please enter the year of the survey in the format YYYY: "))
            if 2000 <= year <= 2024:
                break
            else:
                print("Out of range - values must range from 2000 and 2024.")
        except ValueError:
            print("Integer required")

    return day, month, year


def validate_continue_input() -> bool:

    while True:
        choice = (input("Do you want to select another data file for different date? (Y/N): ").strip().lower() )
        if choice == "y":
            return True
        elif choice == "n":
            print("Exiting the system.")
            return False
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")


# Task B: Processed Outcomes
def process_csv_data(file_path: str) -> dict:
    outcomes = []

    try:
        with open(file_path, mode="r") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                outcomes.append(row)
    except FileNotFoundError as e:
        print(f"Error reading the file: {e}")
        return {}
    
    #The total number of vehicles
    total_vehicles = len(outcomes)
    
    #The total number of trucks
    total_trucks = [row for row in outcomes if row["VehicleType"].strip().lower() == "truck"]
    
    #The total number of bicycles
    total_bicycles = [row for row in outcomes if row["VehicleType"].strip().lower() == "bicycle"]
    
    #The total number of electric vehicles
    total_electric_vehicles = [row for row in outcomes if row["elctricHybrid"].strip().lower() == "true"]
    
    #The total number of two wheeled vehicles
    total_two_wheeled_vehicles = [
        row
        for row in outcomes
        if row["VehicleType"].strip().lower() in {"bicycle", "motorcycle", "scooter"}
    ]
    
    #The total number of busses leaving Elm Avenue/Rabbit Road junction heading North
    total_buses_heading_north = [
        row
        for row in outcomes
        if row["JunctionName"] == "Elm Avenue/Rabbit Road"
        and row["travel_Direction_out"] == "N"
        and row["VehicleType"].strip().lower() == "buss"
    ]
    
    #The total number of vehicles passing through both junctions without turning left or right
    vehicles_without_turning = [
        row
        for row in outcomes
        if row["travel_Direction_in"] == row["travel_Direction_out"]
    ]
    
    #The percentage of total vehicles recorded that are trucks for this date 
    truck_percentage = f"{round((len(total_trucks) / total_vehicles*100) if total_vehicles else 0)}%"
    
    #The average number of Bikes per hour for this date
    hours_counted = len(set(row["timeOfDay"].split(":")[0] for row in outcomes))
    average_bicycles_per_hour = round(len(total_bicycles) / hours_counted) if hours_counted else 0
    
    #The total number of vehicles recorded as over the speed limit for this date
    over_speed_vehicles = [
        row
        for row in outcomes
        if int(row["VehicleSpeed"]) > int(row["JunctionSpeedLimit"])
    ]
    
    #The total number of vehicles recorded through Elm Avenue/Rabbit Road junction
    vehicles_elmavenue = [
        row for row in outcomes if row["JunctionName"] == "Elm Avenue/Rabbit Road"
    ]
    
    #The total number of vehicles recorded through Hanley Highway/Westway junction
    vehicles_hanley = [
        row for row in outcomes if row["JunctionName"] == "Hanley Highway/Westway"
    ]
    
    #The total of scooters that are recorded through Elm Avenue/Rabbit Road
    total_scooters = [
        row for row in outcomes if row["VehicleType"].strip().lower() == "scooter" and row["JunctionName"] == "Elm Avenue/Rabbit Road"
    ]
    
    #The highest number of vehicles in an hour on Hanley Highway/Westway
    peak_hours = {}
    for row in vehicles_hanley:
        hour = row["timeOfDay"].split(":")[0]

        if hour in peak_hours:
            peak_hours[hour] += 1
        else:
            peak_hours[hour] = 1
            
    #The most vehicles through Hanley Highway/Westway were recorded
    busiest_hour_count = max(peak_hours.values(), default=0)
    peak_times = [
        f"Between {int(hour):02d}:00 and {int(hour) + 1:02d}:00"
        for hour, count in peak_hours.items()
        if count == busiest_hour_count
    ]
    
    #The number of hours of rain for this date
    rainy_hours = [
        row['timeOfDay'].split(':')[0]
        for row in outcomes
        if row.get('Weather_Conditions', '').strip().lower() in {'light rain', 'heavy rain'}
    ]
    count_rainy_hours = len(set(rainy_hours))

    # Constructing the results dictionary
    return {
        "data file selected is": file_path,
        "The total number of vehicles recorded for this date is": total_vehicles,
        "The total number of trucks recorded for this date is": len(total_trucks),
        "The total number of electric vehicles for this date is":len(total_electric_vehicles),
        "The total number of two-wheeled vehicles for this date is": len(total_two_wheeled_vehicles),
        "The total number of Busses leaving Elm Avenue/Rabbit Road heading North is":len(total_buses_heading_north),
        "The total number of Vehicles through both junctions not turning left or right is": len(vehicles_without_turning),
        "The percentage of total vehicles recorded that are trucks for this date is": truck_percentage,
        "The average number of Bikes per hour for this date is": average_bicycles_per_hour,
        "The total number of vehicles recorded as over the speed limit for this date is": len(over_speed_vehicles),
        "The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is": len(vehicles_elmavenue),
        "The total number of vehicles recorded through Hanley Highway/Westway junction is": len(vehicles_hanley),
        "The percentage of scooters that are recorded through Elm Avenue/Rabbit Road is": (
            f"{round(len(total_scooters) / len(vehicles_elmavenue) * 100)}%"
            if vehicles_elmavenue
            else "0%"
        ),
        "The highest number of vehicles in an hour on Hanley Highway/Westway is":busiest_hour_count,
        "The most vehicles through Hanley Highway/Westway were recorded": peak_times,
        "The number of hours of rain for this date is":count_rainy_hours ,
    }


def display_outcomes(outcomes: dict):
    print("\n************************************************")
    for key, value in outcomes.items():
        print(f"{key}: {value}")
    print()


# Task C: Save Results to Text File
def save_results_to_file(outcomes: dict, file_name="results.txt"):
    """Save results to a text file."""
    with open(file_name, "a") as file:
        for key, value in outcomes.items():
            file.write(f"{key}: {value}\n")
        file.write("\n********************\n\n")
        

#Task D: Histogram Display
class HistogramApp:
    def __init__(self, traffic_data, date):
        self.traffic_data = traffic_data
        self.date = date
        self.root = tk.Tk()
        self.root.title(f"Histogram of Vehicle Frequency per Hour ({self.date})")
        self.canvas = tk.Canvas(self.root, width=1500, height=700, bg="lightgrey")
        self.canvas.pack()

    def setup_window(self):
        self.canvas.create_text(700, 650, text="Hours 00:00 to 24:00", font=("Arial", 14))
        self.canvas.create_text(600, 30, text=f"Histogram of Vehicle Frequency per Hour ({self.date})", font=("Arial", 14))

    def draw_histogram(self):
        bar_width = 20
        colors = ["purple", "orange"]  # Colors for each junction
        junctions = list(self.traffic_data.keys())
        max_height = 500  # Maximum height of bars
        max_vehicles = max(max(hourly_data.values()) for hourly_data in self.traffic_data.values())

        for hour in range(24):
            x0_base = 90 + (hour * 52)
            for i, junction in enumerate(junctions):
                count = self.traffic_data[junction][hour]
                bar_height = (count / max_vehicles) * max_height
                x0 = x0_base + (i * bar_width)
                y0 = 600 - bar_height
                x1 = x0 + bar_width
                y1 = 600

                self.canvas.create_rectangle(x0, y0, x1, y1, fill=colors[i], outline="black")
                self.canvas.create_text(x0 + bar_width / 2, y0 - 10, text=str(count), font=("Arial", 10), fill="black")

            self.canvas.create_text(x0_base + bar_width / 2, 620, text=f"{hour:02d}", font=("Arial", 10))

    def add_legend(self):
        self.canvas.create_rectangle(1050, 20, 1070, 40, fill="purple")
        self.canvas.create_text(1080, 30, text="Elm Avenue/Rabbit Road", anchor="w", font=("Arial", 10))
        self.canvas.create_rectangle(1050, 50, 1070, 70, fill="orange")
        self.canvas.create_text(1080, 60, text="Hanley Highway/Westway", anchor="w", font=("Arial", 10))

    def run(self):
        self.setup_window()
        self.draw_histogram()
        self.add_legend()
        self.root.mainloop()

# Task E: Code Loops to Handle Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):
        self.current_data = None

    def load_csv_file(self, file_path):
        traffic_data = {
            "Elm Avenue/Rabbit Road": {hour: 0 for hour in range(24)},
            "Hanley Highway/Westway": {hour: 0 for hour in range(24)}
        }

        with open(file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                hour = int(row['timeOfDay'].split(":")[0])
                junction = row['JunctionName']
                if junction in traffic_data:
                    traffic_data[junction][hour] += 1

        return traffic_data

    def clear_previous_data(self):
        self.current_data = None


def main():
    processor = MultiCSVProcessor()

    while True:
        date = validate_date_input()
        file_name = f"traffic_data{date[0]:02d}{date[1]:02d}{date[2]}.csv"
        date_str = f"{date[0]:02d}-{date[1]:02d}-{date[2]}"

        try:
            data = process_csv_data(file_name)
            if data:  # Ensure data is not empty before displaying or saving
                display_outcomes(data)
                save_results_to_file(data)

                # Load data for histogram and run the app
                traffic_data = processor.load_csv_file(file_name)
                app = HistogramApp(traffic_data, date_str)
                app.run()

        except FileNotFoundError:
            print(f"Error: File {file_name} not found")
        except Exception as e:
            print("Unexpected error: ", e)

        if not validate_continue_input():
            break


if __name__ == "__main__":
    main()
 
 