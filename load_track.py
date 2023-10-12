import pandas as pd

def read_track_data(file_path):
    excelData = pd.read_excel(file_path, sheet_name="Blue Line")
    data = excelData.head(15).to_dict(orient="records")
    return data