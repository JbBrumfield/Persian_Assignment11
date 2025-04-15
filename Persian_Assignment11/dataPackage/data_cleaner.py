import pandas as pd
from pepsiAnomalyPackage.pepsi_filter import *
from zipPackage.zip_code_lookup import *
from mainPackage.utils import *


class DataCleaner:
    def __init__(self, input_file: str, output_file: str, anomaly_file: str):
        self.input_file = input_file
        self.output_file = output_file
        self.anomaly_file = anomaly_file
        self.df = pd.read_csv(self.input_file)

    def clean_data(self):
        # 1. Clean the 'Gross Price' column to have exactly 2 decimal places
        self.df['Gross Price'] = self.df['Gross Price'].apply(lambda x: round(x, 2))

        # 2. Remove duplicate rows
        self.df.drop_duplicates(inplace=True)

        # 3. Handle anomalies (Pepsi purchases)
        pepsi_filter = PepsiFilter(self.df)
        pepsi_anomalies = pepsi_filter.filter_pepsi()
        write_csv(pepsi_anomalies, self.anomaly_file)

        # 4. Handle missing zip codes using ZipCodeLookup API
        zip_code_lookup = ZipCodeLookup(self.df)
        self.df = zip_code_lookup.update_missing_zip_codes()

        # 5. Write cleaned data to a new CSV file
        write_csv(self.df, self.output_file)

    def get_cleaned_data(self):
        return self.df

