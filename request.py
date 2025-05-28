import os

from dotenv import load_dotenv

import requests

load_dotenv()

APOLLO_API_KEY = os.getenv("APOLLO_API_KEY")

#print(APOLLO_API_KEY)

def organization_search(organization: str):
    """
    Writes CSV file to the given file path.

    Args:
        input_path (str): The path to the input CSV file.
        output_path (str): The path to the output CSV file.
        company_info (dict): Company POC's email and name.
    """

    url = "https://api.apollo.io/api/v1/people/match?reveal_personal_emails=false&reveal_phone_number=false"

    headers = {
        "accept": "application/json",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "x-api-key": APOLLO_API_KEY
    }

    response = requests.post(url, headers=headers)

    print(response.text)

def get_emails(companies: list):
    company_info = {}
    for c in companies:
        name = " ".join([c,"name"]) # replace with function calls later
        email = " ".join([c,"email"])

        company_info[c]=[name, email]

    return company_info