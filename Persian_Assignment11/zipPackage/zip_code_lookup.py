import requests
import pandas as pd
import re
import time

class ZipCodeLookup:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.api_key = 'ad8a8d40-1b12-11f0-a238-052639287357'  # Replace with your actual API key
        self.base_url = "https://app.zipcodebase.com/api/v1/code/city"

    def extract_city_state(self, address):
        try:
            parts = [p.strip() for p in address.split(',')]
            if len(parts) >= 3:
                city = parts[-2]
                state = parts[-1].split()[0]  # Handles ZIP if present
                return city, state
        except:
            pass
        return None, None

    def has_zip(self, address):
        return bool(re.search(r'\b\d{5}\b', address))

    def lookup_zip_code(self, city: str, state: str):
        try:
            url = f"{self.base_url}?apikey={self.api_key}&city={city}&state_code={state}&country=US"
            response = requests.get(url)
            data = response.json()

            if "results" in data and isinstance(data["results"], list) and data["results"]:
                return data["results"][0]  # Return first ZIP as string
            else:
                print(f"⚠️ Skipped '{city}, {state}' — ZIP not found.")
        except Exception as e:
            print(f"⚠️ Skipped '{city}, {state}' — API error: {e}")
        return None

    def update_missing_zip_codes(self):
        updated_rows = []

        missing_count = self.df[self.df['Full Address'].str.contains(r'\b\d{5}\b', na=False) == False].shape[0]
        print(f"Found {missing_count} rows with missing ZIP codes.")
        print("Starting ZIP code lookup for missing entries...\n")

        missing_zip_indices = [
            idx for idx in self.df.index
            if not self.has_zip(self.df.at[idx, 'Full Address'])
        ]

        to_update = missing_zip_indices[:5]

        for index in to_update:
            address = self.df.at[index, 'Full Address']
            city, state = self.extract_city_state(address)

            if city and state:
                zip_code = self.lookup_zip_code(city, state)
                if zip_code:
                    updated_address = address.strip().rstrip(',') + f" {zip_code}"
                    self.df.at[index, 'Full Address'] = updated_address
                    updated_rows.append((index, updated_address))
                    print(f"Added ZIP code '{zip_code}' to address at row {index}")

        print(f"\n Completed ZIP code updates. {len(updated_rows)} missing ZIP(s) added.")
        return self.df, updated_rows
