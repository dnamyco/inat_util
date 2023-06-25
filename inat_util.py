#!/usr/bin/env python3
"""
A utility for updating iNaturalist data.
https://www.inaturalist.org/users/api_token
Once you've logged into iNat, get your API token from the link above.
You can set the API token as an environment variable named 'INAT_API_TOKEN'.
If the environment variable is not set, you'll be prompted for the token when you run the script.
"""
import argparse
import os
import pandas as pd
from pyinaturalist import set_observation_field


def update_vouchers(api_token, filename):
    df = pd.read_excel(filename)

    for _, row in df.iterrows():
        observation_id = row['iNaturalist ID']
        for column, value in row.items():
            if column != 'iNaturalist ID':
                response = set_observation_field(
                    observation_id=observation_id,
                    observation_field_id=column,  # Assuming the column header is the Observation Field ID
                    value=value,
                    access_token=api_token
                )
                if response:
                    print(f"Updated observation {observation_id} field {column} with value {response['value']}")
                else:
                    print(f"Failed to update observation {observation_id} field {column}. "
                          f"Response: {response.content}")


def get_api_token():
    # Check if the API token is set in the environment variable
    api_token = os.getenv('INAT_API_TOKEN')

    # If not set, prompt the user for the API token
    if not api_token:
        api_token = input("Enter your iNaturalist API Token: ")

    return api_token


def main():
    parser = argparse.ArgumentParser(prog='inat_update')
    subparsers = parser.add_subparsers(dest='command')

    update_vouchers_parser = subparsers.add_parser('update-vouchers')
    update_vouchers_parser.add_argument('--file', help='the name of the Excel file to process')

    args = parser.parse_args()

    api_token = get_api_token()

    if args.command == 'update-vouchers':
        if args.file:
            update_vouchers(api_token, args.file)
        else:
            print('You must provide a file with the --file option.')
    else:
        print(f'Unknown command: {args.command}')


if __name__ == '__main__':
    main()
