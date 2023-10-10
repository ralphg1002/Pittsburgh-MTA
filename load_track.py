import pandas as pd
import numpy as np

def read_track_data(file_path):
    excelData = pd.read_excel(file_path, sheet_name="Blue Line")
    data = excelData.to_numpy()
    return data