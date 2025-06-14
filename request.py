import os

from dotenv import load_dotenv

import requests
import main

load_dotenv()

def get_companies(APOLLO_API_KEY: str, industry: str):
    url = "https://api.apollo.io/api/v1/mixed_companies/search?q_organization_keyword_tags[]="+industry

    headers = {
        "accept": "application/json",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "x-api-key": APOLLO_API_KEY
    }

    try:
        companies = []

        response = requests.post(url, headers=headers)
        response.raise_for_status()

        for comp in response.json().get("organizations", []):
            companies.append([comp['name'],comp['id']])
        
        return companies
    except requests.exceptions.HTTPError as e:
        print("API request failed:", e)



# Flow: company name -> organization search -> organization id
# organization id -> people search -> person id + name
# person id -> people enrish -> person email

def organization_search(APOLLO_API_KEY: str, organization: str):
    org = "%20".join(organization.split(" "))

    url = "".join(["https://api.apollo.io/api/v1/mixed_companies/search?q_organization_name=",org])
    
    headers = {
        "accept": "application/json",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "x-api-key": APOLLO_API_KEY
    }
    
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()

        for comp in response.json().get("organizations", []):
            # only accept exact name matches
            if comp['name'].lower() == organization.lower():
                return comp['id']
        return None
    except requests.exceptions.HTTPError as e:
        print("API request failed:", e)



def people_search(APOLLO_API_KEY: str, org_id: str):
    url = "https://api.apollo.io/api/v1/mixed_people/search?" + "contact_email_status[]=verified&" + "organization_ids[]=" + org_id + "&"

    titles = ["talent","universtiy","recruitment"]
    titles = "&".join(["person_titles[]="+t for t in titles])
    url1 = url + titles

    headers = {
        "accept": "application/json",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "x-api-key": APOLLO_API_KEY
    }
    
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()

        for person in response.json().get("people", []):
            return [person['name'], person['id']]
    except requests.exceptions.HTTPError as e:
        print("API request failed:", e)


    # HR people
    titles = ["HR"]
    titles = "&".join(["person_titles[]="+t for t in titles])
    url2 = url + titles

    headers = {
        "accept": "application/json",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "x-api-key": APOLLO_API_KEY
    }
    
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()

        for person in response.json().get("people", []):
            return [person['name'], person['id']]
    except requests.exceptions.HTTPError as e:
        print("API request failed:", e)
    

    titles = ["founder","ceo", "cto", "owner", "csuite", "cfo", "director", "manager"]
    titles = "&".join(["person_titles[]="+t for t in titles])
    url3 = url + titles

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()

        for person in response.json().get("people", []):
            return [person['name'], person['id']]
        return None
    except requests.exceptions.HTTPError as e:
        print("API request failed:", e)



def people_enrich(APOLLO_API_KEY: str, id: str):
    url = "https://api.apollo.io/api/v1/people/match?id=" + id + "&reveal_personal_emails=true&reveal_phone_number=false"

    headers = {
        "accept": "application/json",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "x-api-key": APOLLO_API_KEY
    }
    
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()

        p = response.json().get("person", [])
        return p["email"]
    except requests.exceptions.HTTPError as e:
        print("API request failed:", e)



def get_emails(APOLLO_API_KEY: str, companies: list):
    company_info = {}
    for c in companies:
        org_id = organization_search(APOLLO_API_KEY, c) # done

        poc = people_search(APOLLO_API_KEY, org_id) if org_id != None else None
        name = poc[0] if poc != None else None
        id = poc[1] if poc != None else None

        email = people_enrich(APOLLO_API_KEY, id) if id != None else None
        #name = " ".join([c,"name"]) # replace with function calls later
        #email = " ".join([c,"email"])

        company_info[c]=[name, email]

    return company_info

def get_emails_from_id(APOLLO_API_KEY: str, ids: list):
    company_info = {}
    
    if ids != None:
        for company in ids:
            c = company[0]
            org_id = company[1]

            poc = people_search(APOLLO_API_KEY, org_id) if org_id != None else None
            name = poc[0] if poc != None else None
            id = poc[1] if poc != None else None

            email = people_enrich(APOLLO_API_KEY, id) if id != None else None
            #name = " ".join([c,"name"]) # replace with function calls later
            #email = " ".join([c,"email"])

            company_info[c]=[name, email]

    return company_info