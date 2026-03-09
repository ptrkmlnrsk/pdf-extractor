from re import findall
import pandas as pd

def extract_data_from_string(string: str) -> list:
    extracted_data = findall(r"(INV\d{3})[\s\S]*?(\d+\.\d{2})", string)
    return extracted_data

def transform_data_to_df(extracted_data: list) -> pd.DataFrame:
    df = pd.DataFrame(extracted_data, columns=['invoice_id', 'amount'])
    df['invoice_id'] = df['invoice_id'].astype(float)
    return df