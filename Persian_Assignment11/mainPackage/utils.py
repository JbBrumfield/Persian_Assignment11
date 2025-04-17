import pandas as pd

def write_csv(df: pd.DataFrame, file_path: str):
    try:
        df.to_csv(file_path, index=False)
        print(f"Saved file to {file_path}")
    except Exception as e:
        print(f"Error saving file {file_path}: {e}")
