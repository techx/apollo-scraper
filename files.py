import csv

def read_companies_csv(input_path: str):
    """
    Reads a CSV file from the given file path and returns its contents.

    Args:
        input_path (str): The path to the CSV file.
    """
    companies = []
    try:
        with open(input_path, 'r') as file:
            csv_reader = csv.reader(file)

            next(csv_reader) 
            
            for row in csv_reader:
                companies.append(str(row[0]))
    except FileNotFoundError:
        print(f"Error: File not found at '{input_path}'")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return companies

def write_email_csv(input_path: str, output_path: str, company_info: dict):
    """
    Writes CSV file to the given file path.

    Args:
        input_path (str): The path to the input CSV file.
        output_path (str): The path to the output CSV file.
        company_info (dict): Company POC's email and name.
    """
    try:
        with open(input_path,  newline='', encoding='utf-8') as fin, \
        open(output_path, 'w', newline='', encoding='utf-8') as fout:

            reader = csv.reader(fin)
            writer = csv.writer(fout)

            header = next(reader)
            writer.writerow(header + ['Name', 'Email'])  # add new columns

            for row in reader:
                # retrieve respective company's info
                name = company_info[row[0]][0]
                email = company_info[row[0]][1]

                # append new column info
                row.append(name)
                row.append(email)

                # Write the modified row
                writer.writerow(row)
    except FileNotFoundError:
        print(f"Error: File not found at '{input_path}'")
    except Exception as e:
        print(f"An error occurred: {e}")

def write_company_csv(output_path: str, company_info: dict):
    """
    Writes CSV file to the given file path.

    Args:
        output_path (str): The path to the output CSV file.
        company_info (dict): Company POC's email and name.
    """
    with open(output_path, 'w', newline='', encoding='utf-8') as fout:
        writer = csv.writer(fout)

        writer.writerow(['Company','Name', 'Email'])  # add new columns

        for key, value in company_info.items():
            # retrieve respective company's info
            name = company_info[key][0]
            email = company_info[key][1]

            # append new column info
            row = [key, name, email]

            # Write the modified row
            writer.writerow(row)