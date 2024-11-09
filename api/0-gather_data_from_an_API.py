#!/usr/bin/python3
"""
This script fetches data from a REST API to get the TODO list progress
of a given employee ID and displays the progress.
"""

import requests
import sys

if __name__ == "__main__":
    # Ensure the script gets an employee ID as an argument
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print("Usage: python3 0-gather_data_from_an_API.py <employee_id>")
        sys.exit(1)

    # Get the employee ID from the command line argument
    employee_id = int(sys.argv[1])

    # Define the base URL for the API
    base_url = "https://jsonplaceholder.typicode.com"

    # Fetch user data for the employee
    user_response = requests.get(f"{base_url}/users/{employee_id}")
    if user_response.status_code != 200:
        print(f"Employee with ID {employee_id} not found.")
        sys.exit(1)

    user_data = user_response.json()
    employee_name = user_data.get("name")

    # Fetch the employee's TODO list
    todos_response = requests.get(f"{base_url}/todos?userId={employee_id}")
    todos = todos_response.json()

    # Calculate the total tasks and completed tasks
    total_tasks = len(todos)
    completed_tasks = sum(1 for task in todos if task.get("completed"))

    # Print the employee's TODO list progress
    print(f"Employee {employee_name} is done with tasks({completed_tasks}/{total_tasks}):")
    
    # Print the titles of completed tasks
    for task in todos:
        if task.get("completed"):
            print(f"\t {task.get('title')}")
