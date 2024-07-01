import requests
from bs4 import BeautifulSoup
import csv

# Function to fetch and parse HTML for a given state code
def fetch_state_data(state_code):
    url = f"https://results.eci.gov.in/PcResultGenJune2024/partywiseresult-{state_code}.htm"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch page for state code {state_code}: {response.status_code}")

# Function to parse the election results HTML
def parse_election_results(html, state_name):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.select_one('.rslt-table table')
    data = []
    headers = []

    if table:
        # Extract headers
        headers = [header.text.strip() for header in table.select('thead th')]
        headers.append("State")  # Add state column to headers

        # Extract rows
        for row in table.select('tbody tr'):
            cols = [col.text.strip() for col in row.select('td')]
            if cols:
                cols.append(state_name)  # Add state name to the row
                data.append(cols)
    return headers, data

# Function to save data to CSV
def save_to_csv(headers, data, filename='election_results.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)
    print(f"Data has been saved to {filename}")

# Dictionary of state codes and names
states = {
    "U01": "Andaman & Nicobar Islands",
    "S01": "Andhra Pradesh",
    "S02": "Arunachal Pradesh",
    "S03": "Assam",
    "S04": "Bihar",
    "U02": "Chandigarh",
    "S26": "Chhattisgarh",
    "U03": "Dadra & Nagar Haveli and Daman & Diu",
    "S05": "Goa",
    "S06": "Gujarat",
    "S07": "Haryana",
    "S08": "Himachal Pradesh",
    "U08": "Jammu and Kashmir",
    "S27": "Jharkhand",
    "S10": "Karnataka",
    "S11": "Kerala",
    "U09": "Ladakh",
    "U06": "Lakshadweep",
    "S12": "Madhya Pradesh",
    "S13": "Maharashtra",
    "S14": "Manipur",
    "S15": "Meghalaya",
    "S16": "Mizoram",
    "S17": "Nagaland",
    "U05": "NCT OF Delhi",
    "S18": "Odisha",
    "U07": "Puducherry",
    "S19": "Punjab",
    "S20": "Rajasthan",
    "S21": "Sikkim",
    "S22": "Tamil Nadu",
    "S29": "Telangana",
    "S23": "Tripura",
    "S24": "Uttar Pradesh",
    "S28": "Uttarakhand",
    "S25": "West Bengal"
}

# Fetch and parse data for all states
all_data = []
all_headers = []

for state_code, state_name in states.items():
    try:
        html = fetch_state_data(state_code)
        headers, state_data = parse_election_results(html, state_name)
        if not all_headers:
            all_headers = headers  # Use the headers from the first table
        all_data.extend(state_data)
    except Exception as e:
        print(f"An error occurred while processing state {state_name}: {e}")

# Save all data to CSV
save_to_csv(all_headers, all_data)
