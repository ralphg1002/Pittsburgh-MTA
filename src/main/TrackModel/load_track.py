import pandas as pd


def read_track_data(filePath):
    excelData = pd.read_excel(filePath, sheet_name="Blue Line")
    data = excelData.head(15).to_dict(orient="records")
    return data
