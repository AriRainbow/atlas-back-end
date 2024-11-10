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


def fetch_data(url):
    """Helper function to fetch data from the API and handle errors."""
    try:
        response = requests.get(url)
        # Raise HTTPError for bad responses (4xx, 5xx)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Error fetching data from {url}: {err}")
        sys.exit(1)


def export_all_employees_tasks():
    """Fetches and exports the tasks of all employees to a JSON file."""
    # Define the base URL for the API
    base_url = "https://jsonplaceholder.typicode.com"

    # Fetch all users
    users = fetch_data(f"{base_url}/users")

    # Dictionary to hold all tasks for each user
    all_tasks = {}

    # Loop through each user and fetch their tasks
    for user in users:
        user_id = user['id']
        username = user['username']
        tasks = fetch_data(f"{base_url}/todos?userId={user_id}")

        # Create a list of tasks for the user in the required format
        task_list = [
            {
                "username": username,
                "task": task.get("title"),
                "completed": task.get("completed")
            }
            for task in tasks
        ]

        # Add the user's tasks to the all_tasks dictionary
        all_tasks[user_id] = task_list

    # Write the data to todo_all_employees.json
    with open("todo_all_employees.json", "w", encoding="utf-8") as json_file:
        json.dump(all_tasks, json_file, indent=4)

    print("Data for all employees has been exported to todo_all_employees.json")


if __name__ == "__main__":
   export_all_employees_tasks()
