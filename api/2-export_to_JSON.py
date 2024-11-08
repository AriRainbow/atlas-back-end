#!/usr/bin/python3
"""
This script exports the TODO list progress
of a given employee ID to a JSON file.
It uses the REST API at https://jsonplaceholder.typicode.com to fetch
user and task data and writes it in JSON format.
"""

import json
import requests
import sys


if __name__ == "__main__":
    # Check if the script receives the employee ID as an argument
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print("Usage: python3 2-export_to_JSON.py <employee_id>")
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

    # Prepare the data in the desired JSON format
    json_data = {
        str(employee_id): [
            {
                "task": task.get("title"),
                "completed": task.get("completed"),
                "username": username
            }
            for task in todos
        ]
    }

    # Create a JSON file named after the employee ID
    json_filename = f"{employee_id}.json"

    # Write data to the JSON file
    with open(json_filename, mode="w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file)

    print(
        f"Data for employee ID {employee_id} has been "
        f"exported to {json_filename}"
    )
