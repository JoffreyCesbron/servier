import pandas as pd

from src.common.logger import global_logger

DRUG_TYPE = "drugs"
PUBMED_TYPE = "pubmed"
CLINICAL_TRIAL_TYPE = "clinical_trial"
JOURNAL_TYPE = "journal"


def prepare_drug(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare the dataframe to build the graph"""

    global_logger().info("prepare drug for the graph")
    df.drop_duplicates(inplace=True)
    df.rename(columns={'atccode': 'id', 'drug': 'label'}, inplace=True)
    df['type'] = DRUG_TYPE
    return df


def prepare_pubmed(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare the dataframe to build the graph"""

    global_logger().info("prepare pubmed for the graph")
    df["type"] = PUBMED_TYPE
    df.rename(columns={'title': 'label'}, inplace=True)
    df_filtered = df[["id", "label", "type"]]
    return df_filtered


def prepare_clinical_trials(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare the dataframe to build the graph"""

    global_logger().info("prepare clinical_trials for the graph")
    df["journal"] = df["journal"].str.lower()
    df["type"] = CLINICAL_TRIAL_TYPE
    df.rename(columns={'scientific_title': 'label'}, inplace=True)
    df_filtered = df[["id", "label", "type"]]
    return df_filtered


def check_word(row: pd.Series, drugs: [str]) -> list:
    """Check if the drug exist in the row. If present, returns the link with the file (pubmed or clinical trial
     and the journal """

    matches = []
    for drug in drugs:
        if drug.lower() in row['label'].lower():
            matches.extend([
                {"source": drug, "target": row['id'], "date_mention": row['date']},
                {"source": drug, "target": row['journal'], "date_mention": row['date']}
            ])
    return matches


def get_edges(df_clinical_trials: pd.DataFrame, df_pubmed: pd.DataFrame, drugs: pd.DataFrame) -> list:
    """Get the list of edges"""
    all_matches_pubmed = df_pubmed.apply(lambda row: check_word(row, drugs), axis=1).tolist()
    all_matches_clinical_trials = df_clinical_trials.apply(lambda row: check_word(row, drugs), axis=1).tolist()
    all_matches = all_matches_pubmed + all_matches_clinical_trials
    output = [match for sublist in all_matches for match in sublist]
    return output


def build_graph(df_drugs: pd.DataFrame, df_pubmed: pd.DataFrame, df_clinical_trials: pd.DataFrame):
    """Building the json that represents the relation between the drugs, pubmed, clinical trials and journals"""

    drugs = df_drugs["drug"].tolist()
    journals = set(df_pubmed['journal'].tolist() + df_clinical_trials['journal'].tolist())
    journals_lower_case = [s.lower() for s in journals]

    df_drugs_prepared = prepare_drug(df_drugs)
    drugs_nodes = df_drugs_prepared.to_dict(orient='records')

    df_pubmed_prepared = prepare_pubmed(df_pubmed)
    pubmed_nodes = df_pubmed_prepared.to_dict(orient='records')

    df_clinical_trials_prepared = prepare_clinical_trials(df_clinical_trials)
    clinical_trials_nodes = df_clinical_trials_prepared.to_dict(orient='records')

    journals_nodes = [{'id': journal, 'label': '', 'type': JOURNAL_TYPE} for journal in journals_lower_case]

    nodes = drugs_nodes + clinical_trials_nodes + pubmed_nodes + journals_nodes
    edges = get_edges(df_clinical_trials, df_pubmed, drugs)

    output = [{"nodes": nodes}, {"edges": edges}]

    return output
