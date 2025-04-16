import requests
import pandas as pd
import re
import time  # For tracking the time taken by API requests

class ZipCodeLookup:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.api_key = 'ad8a8d40-1b12-11f0-a238-052639287357'  # Replace with your actual API key
        self.base_url = "https://app.zipcodebase.com/api/v1/search"

    def extract_city(self, address):
        # Try to extract city name from address using a simple rule
        try:
            parts = address.split(',')
            if len(parts) >= 2:
                return parts[-2].strip()
        except:
            pass
        return None

    def has_zip(self, address):
        # Checks if a 5-digit zip code exists in the address
        return bool(re.search(r'\b\d{5}\b', address))

    def lookup_zip_code(self, city: str):
        try:
            start_time = time.time()  # Start timer for API request
            response = requests.get(f"{self.base_url}?apikey={self.api_key}&city={city}&country=US")
            request_time = time.time() - start_time  # Calculate how long the request took
            print(f"API request for {city} took {request_time:.2f} seconds.")
            data = response.json()
            if "results" in data and city in data["results"]:
                return data["results"][city][0]  # Get first available ZIP code
        except Exception as e:
            print(f"API Error for {city}: {e}")
        return None

    def update_missing_zip_codes(self):
        updated_rows = []
        count = 0  # To track how many rows we've updated
        # Loop through the rows and find rows with missing ZIP codes
        for index, row in self.df.iterrows():
            if count >= 5:  # Stop after processing 5 rows
                break
            address = row.get('Full Address', '')
            if not self.has_zip(address):  # Check if ZIP code is missing
                city = self.extract_city(address)
                if city:
                    zip_code = self.lookup_zip_code(city)
                    if zip_code:
                        # Append zip code to the address
                        updated_address = address.strip().rstrip(',') + f" {zip_code}"
                        self.df.at[index, 'Full Address'] = updated_address
                        updated_rows.append((index, updated_address))  # Save updated row for display
                        count += 1
        return self.df, updated_rows
