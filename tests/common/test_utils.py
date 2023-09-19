import pandas as pd

from src.common.utils import standardize_date, drop_lines_when_empty_fields


def test_standard_date():
    date = "2020/01/01"
    expected = "2020/01/01"
    assert standardize_date(date) == expected


def test_standard_date_tiret():
    date = "2020-01-01"
    expected = "2020/01/01"
    assert standardize_date(date) == expected


def test_text_date():
    date = "1 January 2020"
    expected = "2020/01/01"
    assert standardize_date(date) == expected


def test_invalid_date():
    date = "40 juin 2026"
    expected = None
    assert standardize_date(date) == expected


def test_invalid_date():
    date = "40 juin 2026"
    expected = None
    assert standardize_date(date) == expected


def test_drop_lines_with_nan():
    data = {
        'col1': [1, 2, 3, 4],
        'col2': ['a', 'b', None, 'd']
    }
    df = pd.DataFrame(data)
    df_filtered = drop_lines_when_empty_fields(df)
    assert df_filtered.shape[0] == 3
    assert df_filtered['col2'].isnull().sum() == 0


def test_drop_lines_with_empty_string():
    data = {
        'col1': [1, 2, 3, 4],
        'col2': ['a', '   ', 'c', 'd']
    }
    df = pd.DataFrame(data)
    df_filtered = drop_lines_when_empty_fields(df)
    assert df_filtered.shape[0] == 3
    assert not df_filtered['col2'].str.isspace().any()


def test_all_valid_rows():
    data = {
        'col1': [1, 2, 3],
        'col2': ['a', 'b', 'c']
    }
    df = pd.DataFrame(data)
    df_filtered = drop_lines_when_empty_fields(df)
    assert df_filtered.shape == df.shape
