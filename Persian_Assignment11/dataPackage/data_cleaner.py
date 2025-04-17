# File Name : data_cleaner.py
# Student Name: Jacob Brumfield, Justin Ganduri
# email:  brumfijb@mail.uc.edu, gandurpn@mail.uc.edu
# Assignment Number: Assignment 11
# Due Date:   4/17/2025
# Course #/Section:   IS 4010 001
# Semester/Year:   Spring 2025
# Brief Description of the assignment:  The assignment removes duplicate rows, makes the price two decimal points, and selects the rows where people accidentally bought pepsi instead of fuel and creates a new csv called dataanamolies and datacleaned.


# Brief Description of what this module does. Cleans the data and shows what steps are taken for each step of cleaning
# Citations: {"Stack Overflow" is not sufficient. Provide repeatable links, book page #, etc.}

# Anything else that's relevant:
import pandas as pd
from pepsiAnomalyPackage.pepsi_filter import PepsiFilter
from zipPackage.zip_code_lookup import ZipCodeLookup
from mainPackage.utils import write_csv

class DataCleaner:
    def __init__(self, input_file: str, output_file: str, anomaly_file: str):
        self.input_file = input_file
        self.output_file = output_file
        self.anomaly_file = anomaly_file
        self.df = pd.read_csv(self.input_file, dtype={0: str})

    def clean_data(self):
        # 1. Format Gross Price to 2 decimal places
        self.df['Gross Price'] = self.df['Gross Price'].apply(lambda x: round(x, 2))

        # 2. Remove duplicate rows and print message
        initial_row_count = len(self.df)
        self.df.drop_duplicates(inplace=True)
        final_row_count = len(self.df)
        print(f"Deleted {initial_row_count - final_row_count} duplicate rows.")

        # 3. Handle Pepsi anomalies
        pepsi_filter = PepsiFilter(self.df)
        pepsi_anomalies = pepsi_filter.filter_pepsi()
        write_csv(pepsi_anomalies, self.anomaly_file)
        print(f"Successfully created {self.anomaly_file}")

        # 4. Handle missing ZIP codes
        zip_code_lookup = ZipCodeLookup(self.df)
        missing_zip_count = self.df[self.df['Full Address'].str.contains(r'\b\d{5}\b', na=False) == False].shape[0]
        print(f"Found {missing_zip_count} rows with missing ZIP codes.")
        self.df, updated_rows = zip_code_lookup.update_missing_zip_codes()
        self.updated_zip_rows = updated_rows  # Store updated rows for later display
        print(f"Updated the following rows with missing ZIP codes: {self.updated_zip_rows}")

        # 5. Save the cleaned data
        write_csv(self.df, self.output_file)
        print(f"Data cleaned and saved to {self.output_file}")
