import requests
import pandas as pd
import re

class ZipCodeLookup:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.api_key = 'YOUR_API_KEY'  # Replace this with your actual API key
        self.base_url = "https://app.zipcodebase.com/api/v1/search"

    def extract_city(self, address):
        # Try to extract city name from address using a regex or simple rule
        try:
            parts = address.split(',')
            if len(parts) >= 2:
                return parts[-2].strip()
        except:
            pass
        return None

    def has_zip(self, address):
        return bool(re.search(r'\b\d{5}\b', address))

    def lookup_zip_code(self, city: str):
        try:
            response = requests.get(f"{self.base_url}?apikey={self.api_key}&city={city}&country=US")
            data = response.json()
            if "results" in data and city in data["results"]:
                return data["results"][city][0]
        except Exception as e:
            print(f"API Error for {city}: {e}")
        return None

    def update_missing_zip_codes(self):
        for index, row in self.df.iterrows():
            address = row.get('Full Address', '')
            if not self.has_zip(address):
                city = self.extract_city(address)
                if city:
                    zip_code = self.lookup_zip_code(city)
                    if zip_code:
                        # Append zip code to the end of the address
                        updated_address = address.strip().rstrip(',') + f" {zip_code}"
                        self.df.at[index, 'Full Address'] = updated_address
        return self.df
