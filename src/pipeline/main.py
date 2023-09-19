import json

from src.common.logger import global_logger
from src.common.utils import load_csv, save_file
from src.pipeline.graph import build_graph
from src.pipeline.transform import clean_clinical_trial, clean_drugs, clean_pubmed


def main():
    global_logger().info("starting application")

    df_drugs = load_csv("data/drugs.csv")
    df_pubmed = load_csv("data/pubmed.csv")
    df_clinical_trials = load_csv("data/clinical_trials.csv")

    df_drugs_cleaned = clean_drugs(df_drugs)
    df_pubmed_cleaned = clean_pubmed(df_pubmed)
    df_clinical_trials_cleaned = clean_clinical_trial(df_clinical_trials)

    json_file = build_graph(df_drugs_cleaned, df_pubmed_cleaned, df_clinical_trials_cleaned)

    save_file("output.json", json_file)

    global_logger().info(json.dumps(json_file, indent=4))

    global_logger().info("ending application")


if __name__ == '__main__':
    main()
