import pandas as pd

def read_excel(file, **kwargs):
    data_dict = []
    try:
        data = pd.read_excel(file, **kwargs)
        data_dict = data.to_dict('records')
    finally:
        return data_dict
