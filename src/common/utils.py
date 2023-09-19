import json
from datetime import datetime

import pandas as pd

from src.common.logger import global_logger


def standardize_date(date: str) -> str:
    """Convert date like 1 January 2020 to the format YYYY-MM-DD"""

    formats = ["%d %B %Y", "%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y"]

    for fmt in formats:
        try:
            date = datetime.strptime(date, fmt)
            return date.strftime("%Y/%m/%d")
        except ValueError:
            pass
    global_logger().info("date is invalid")

    return None


def load_csv(path: str) -> pd.DataFrame:
    global_logger().info(f"loading df with the file <{path}>")
    df = pd.read_csv(path)
    global_logger().info(f"number of lines <{df.shape[0]}>, number of columns <{df.shape[1]}>")
    return df


def drop_lines_when_empty_fields(df: pd.DataFrame) -> pd.DataFrame:
    """If one field contains an empty value or Nan then we drop the lines"""

    global_logger().info(f"nb of lines before dropping {df.shape[0]}")
    df = df.replace(r'^\s*$', float('nan'), regex=True)
    df_filtered = df.dropna()
    global_logger().info(f"nb of lines after dropping {df_filtered.shape[0]}")
    return df_filtered


def save_file(file_name: str, json_output: dict) -> None:
    global_logger().info(f"saving file <{file_name}>")
    with open(file_name, "w") as f:
        json.dump(json_output, f, indent=4)
