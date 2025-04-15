import pandas as pd
from pepsiAnomalyPackage.pepsi_filter import PepsiFilter
from zipPackage.zip_code_lookup import ZipCodeLookup
from mainPackage.utils import write_csv

class DataCleaner:
    def __init__(self, input_file: str, output_file: str, anomaly_file: str):
        self.input_file = input_file
        self.output_file = output_file
        self.anomaly_file = anomaly_file
        self.df = pd.read_csv(self.input_file)

    def clean_data(self):
        # 1. Format Gross Price
        self.df['Gross Price'] = self.df['Gross Price'].apply(lambda x: round(x, 2))

        # 2. Remove duplicates
        self.df.drop_duplicates(inplace=True)

        # 3. Handle Pepsi anomalies
        pepsi_filter = PepsiFilter(self.df)
        pepsi_anomalies = pepsi_filter.filter_pepsi()
        write_csv(pepsi_anomalies, self.anomaly_file)

        # 4. Fix missing zip codes
        zip_code_lookup = ZipCodeLookup(self.df)
        self.df = zip_code_lookup.update_missing_zip_codes()

        # 5. Save cleaned data
        write_csv(self.df, self.output_file)

    def get_cleaned_data(self):
        return self.df