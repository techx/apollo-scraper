import argparse

import files
import request

import os
from dotenv import load_dotenv

load_dotenv()

# APOLLO_API_KEY = os.getenv("APOLLO_API_KEY")
global APOLLO_API_KEY

def people_search():
    INPUT_PATH = input("Enter .csv file path: ")
    # file_name = input("Enter .csv file name (e.g. testing.csv): ")
    
    # INPUT_PATH = input_path + "\\" + file_name

    parsed_path = INPUT_PATH.split("\\")[:-1]
    parsed_path.append("emails.csv")
    OUTPUT_PATH = "\\".join(parsed_path)

    companies = files.read_companies_csv(INPUT_PATH) # read in companies
    company_info = request.get_emails(companies) # find name and email through apollo

    files.write_email_csv(INPUT_PATH, OUTPUT_PATH, company_info) # write to csv file

    input_path="\\".join(INPUT_PATH.split("\\")[:-1])
    print(f"Results printed to emails.csv file in {str(input_path)}.")

def company_search():
    OUTPUT_PATH = input("Enter output file path: ")
    OUTPUT_PATH += "\\emails.csv"

    industries = input("Enter a comma and space separated list of industries (e.g. mining, sales strategy, consulting): ")
    industries = industries.split(", ")
    
    company_info = {}
    for industry in industries:
        company_ids = request.get_companies(industry) # find companies by industry
        company_info.update(request.get_emails_from_id(company_ids)) # find POC

    files.write_company_csv(OUTPUT_PATH, company_info) # write to csv file

    print(f"Results printed to emails.csv file in {str(OUTPUT_PATH)}.")

if __name__ == "__main__":
    APOLLO_API_KEY = input("Please enter you Apollo API key: ")

    parser = argparse.ArgumentParser(description="Run functions from command line")
    parser.add_argument("function", help="Function to run")

    args = parser.parse_args()

    if args.function == "people_search":
        people_search()
    elif args.function == "company_search":
        company_search()
    else:
        print("Invalid function name")