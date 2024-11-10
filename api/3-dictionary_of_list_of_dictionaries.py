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
        response = requests.get(url, timeout=10)  # Set tineout for the request
        # Raise HTTPError for bad responses (4xx, 5xx)
        response.raise_for_status()

        # Check if the response is empty
        if not response.text.strip():
            raise ValueError("Empty response from the API")

        # Attempt to decode the JSON response
        try:
            return response.json()
        except json.JSONDecodeError:
            # Print the first 100 characters of the response
            print(f"Failed to decode JSON from the response: "
                  f"{response.text[:100]}")
            print(f"Full response: {response.text}")  # Full response for debug
            sys.exit(1)

    except requests.exceptions.RequestException as err:
        # Add debugging info for the request error
        print(f"Request error: {err}")
        sys.exit(1)  # Exit silently in case of error

    except ValueError as err:
        # Handle empty response or non-JSON content
        print(f"Value error: {err}")
        sys.exit(1)  # Exit silently in case of error

    except json.JSONDecodeError:
        print("Failed to decode JSON. The response is not valid JSON.")
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

        # Skip empty responses
        if not tasks:
            print(f"No tasks found for user {username} (ID: {user_id})")
            continue

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
        json.dump(
            all_tasks,
            json_file,
            indent=4
        )


if __name__ == "__main__":
    export_all_employees_tasks()
