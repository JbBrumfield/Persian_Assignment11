import pandas as pd

class PepsiFilter:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def filter_pepsi(self):
        # Find rows where the 'Fuel Type' column contains 'Pepsi' and remove them
        pepsi_anomalies = self.df[self.df['Fuel Type'].str.lower() == 'pepsi']
        self.df.drop(pepsi_anomalies.index, inplace=True)
        return pepsi_anomalies

