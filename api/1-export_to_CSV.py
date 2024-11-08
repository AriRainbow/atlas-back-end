#!/usr/bin/python3
"""
This script exports the TODO list progress
of a given employee ID to a CSV file.
It uses the REST API at https://jsonplaceholder.typicode.com to fetch
user and task data and writes the completed and incomplete tasks to a CSV.
"""

import csv
import sys
import requests

if __name__ == "__main__":
    # Check if the script receives the employee ID as an argument
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print("Usage: python3 1-export_to_CSV.py <employee_id>")
        sys.exit(1)

    # Get the employee ID from the command line argument
    employee_id = int(sys.argv[1])

    # Define the base URL for the API
    base_url = "https://jsonplaceholder.typicode.com"

    # Fetch user data
    user_response = requests.get(f"{base_url}/users/{employee_id}")
    if user_response.status_code != 200:
        print("Employee not found")
        sys.exit(1)

    user_data = user_response.json()
    username = user_data.get("username")

    # Fetch the user's TODO list
    todos_response = requests.get(f"{base_url}/todos?userId={employee_id}")
    todos = todos_response.json()

    # Create a CSV file named after the employee ID
    csv_filename = f"{employee_id}.csv"

    # Write data to the CSV file
    with open(
        csv_filename, mode="w", newline="", encoding="utf-8"
    ) as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        for task in todos:
            writer.writerow([
                employee_id, username, task.get("completed"),
                task.get("title")
            ])

    print(
        f"Data for employee ID {employee_id} has been "
        f"exported to {csv_filename}"
    )
