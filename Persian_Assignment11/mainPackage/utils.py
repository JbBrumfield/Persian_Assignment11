# File Name : utils.py
# Student Name: Jacob Brumfield, Justin Ganduri
# email:  brumfijb@mail.uc.edu, gandurpn@mail.uc.edu
# Assignment Number: Assignment 11
# Due Date:   4/17/2025
# Course #/Section:   IS 4010 001
# Semester/Year:   Spring 2025
# Brief Description of the assignment:  The assignment removes duplicate rows, makes the price two decimal points, and selects the rows where people accidentally bought pepsi instead of fuel and creates a new csv called dataanamolies and datacleaned.


# Brief Description of what this module does. This is the file that makes the other csv files
# Citations: {"Stack Overflow" is not sufficient. Provide repeatable links, book page #, etc.}

# Anything else that's relevant:
import pandas as pd

def write_csv(df: pd.DataFrame, file_path: str):
    try:
        df.to_csv(file_path, index=False)
        print(f"Saved file to {file_path}")
    except Exception as e:
        print(f"Error saving file {file_path}: {e}")
