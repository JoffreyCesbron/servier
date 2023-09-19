import pandas as pd

from src.common.logger import global_logger
from src.common.utils import standardize_date, drop_lines_when_empty_fields


def clean_clinical_trial(df: pd.DataFrame) -> pd.DataFrame:
    """clean the file for better usability (Nan, uniformized date and wrong chars in the string)"""

    global_logger().info("cleaning clinical trial df")
    df = drop_lines_when_empty_fields(df)
    df["date"] = df["date"].apply(standardize_date)
    df["journal"].replace(r'\\[a-zA-Z0-9]+\\[a-zA-Z0-9]+', '', inplace=True, regex=True)
    df['journal'] = df['journal'].str.lower()
    return df


def clean_drugs(df: pd.DataFrame) -> pd.DataFrame:
    """clean the file for better usability"""

    global_logger().info("cleaning drug df")
    df = drop_lines_when_empty_fields(df)
    df['atccode'] = df['atccode'].str.lower()
    df['drug'] = df['drug'].str.lower()
    return df


def clean_pubmed(df: pd.DataFrame) -> pd.DataFrame:
    """clean the file for better usability (standardized the date)"""

    global_logger().info("cleaning pubmed")
    df = drop_lines_when_empty_fields(df)
    df['date'] = df['date'].apply(standardize_date)
    df['journal'] = df['journal'].str.lower()
    return df
