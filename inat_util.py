#!/usr/bin/env python3
"""
A utility for updating iNaturalist data.
https://www.inaturalist.org/users/api_token
Once you've logged into iNat, get your API token from the link above. The token will change each time you access the page.
You can set the API token as an environment variable named 'INAT_API_TOKEN'.
If the environment variable is not set, you'll be prompted for the token when you run the script.
"""

import argparse
import os
import pandas as pd
import time
from pyinaturalist import set_observation_field


def update_vouchers(api_token, filename):
    """This function updates the observation fields in iNaturalist based on data from an Excel file.

    Parameters:
        api_token (str): The API token for the iNaturalist account.
        filename (str): The path to the Excel file to be processed.

    """

    # Load data from the Excel file into a pandas DataFrame
    df = pd.read_excel(filename)

    # Loop over each row in the DataFrame
    for _, row in df.iterrows():
        # Each row corresponds to an observation, specified by the 'iNaturalist ID' field
        observation_id = row['iNaturalist ID']
        
        # Loop over each column (observation field) in the row
        for column, value in row.items():
            # Exclude the 'iNaturalist ID' column and any NaN values
            if column != 'iNaturalist ID' and pd.notnull(value):  
                try:
                    # Update the observation field in iNaturalist with the value from the DataFrame
                    response = set_observation_field(
                        observation_id=observation_id,
                        observation_field_id=column,  # The column header is assumed to be the Observation Field ID
                        value=value,
                        access_token=api_token
                    )
                    # Check the response and print a success or failure message
                    if response:
                        print(f"Updated observation {observation_id} field {column} with value {response['value']}")
                    else:
                        print(f"Failed to update observation {observation_id} field {column}. "
                              f"Response: {response.content}")
                except Exception as e:
                    # Catch any exceptions that occur during the update process and print an error message
                    print(f"Error updating observation {observation_id} field {column} with value {value}. "
                          f"Error: {e}")
                # Sleep for 1 second to avoid hitting the API rate limit
                time.sleep(1)


def get_api_token():
    """This function gets the iNaturalist API token from an environment variable or prompts the user for it.

    Returns:
        str: The iNaturalist API token.

    """
    
    # Check if the API token is set in the environment variable
    api_token = os.getenv('INAT_API_TOKEN')

    # If not set, prompt the user for the API token
    if not api_token:
        api_token = input("Enter your iNaturalist API Token: ")

    return api_token


def main():
    """This function handles command-line arguments and calls the appropriate function."""

    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(prog='inat_update')
    subparsers = parser.add_subparsers(dest='command')

    # Define the 'update-vouchers' command and its arguments
    update_vouchers_parser = subparsers.add_parser('update-vouchers')
    update_vouchers_parser.add_argument('--file', help='the name of the Excel file to process')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Get the iNaturalist API token
    api_token = get_api_token()

    # Check which command was called and call the appropriate function
    if args.command == 'update-vouchers':
        if args.file:
            update_vouchers(api_token, args.file)
        else:
            print('You must provide a file with the --file option.')
    else:
        print(f'Unknown command: {args.command}')


if __name__ == '__main__':
    main()
