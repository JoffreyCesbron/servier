import json

import pandas as pd

from src.common.logger import global_logger


def main():
    global_logger().info("starting analyses")

    with open('output.json', 'r') as file:
        data = json.load(file)
    nodes = data[0]['nodes']

    journal_nodes = [node['id'] for node in nodes if node['type'] == "journal"]
    edges = data[1]['edges']
    edges_with_journal = [edge for edge in edges if edge['target'] in journal_nodes]
    df = pd.DataFrame(edges_with_journal)
    df_filtered = df[["source", "target"]]
    unique_sources_count = df_filtered.groupby('target')['source'].nunique()

    max_unique_sources = unique_sources_count.max()
    top_targets = unique_sources_count[unique_sources_count == max_unique_sources]

    global_logger().info(top_targets)
    global_logger().info("ending analyses")


if __name__ == '__main__':
    main()
