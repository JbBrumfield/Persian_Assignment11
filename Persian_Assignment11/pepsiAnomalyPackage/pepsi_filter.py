# File Name : pepsi_filter.py
# Student Name: Jacob Brumfield, Justin Ganduri
# email:  brumfijb@mail.uc.edu, gandurpn@mail.uc.edu
# Assignment Number: Assignment 11
# Due Date:   4/17/2025
# Course #/Section:   IS 4010 001
# Semester/Year:   Spring 2025
# Brief Description of the assignment:  The assignment removes duplicate rows, makes the price two decimal points, and selects the rows where people accidentally bought pepsi instead of fuel and creates a new csv called dataanamolies and datacleaned.

# Brief Description of what this module does. This is the python file that selects the fuel type pepsi and removes it and adds all of them to a different csv
# Citations: {"Stack Overflow" is not sufficient. Provide repeatable links, book page #, etc.}

# Anything else that's relevant:
import pandas as pd

class PepsiFilter:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def filter_pepsi(self):
        # Find rows where the 'Fuel Type' column contains 'Pepsi' and remove them
        pepsi_anomalies = self.df[self.df['Fuel Type'].str.lower() == 'pepsi']
        self.df.drop(pepsi_anomalies.index, inplace=True)
        return pepsi_anomalies
