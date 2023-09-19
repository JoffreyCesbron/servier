import pandas as pd

from src.pipeline.graph import prepare_pubmed, check_word, build_graph

data_row = pd.Series({
    'label': 'A title with diphenhydramine and tetracycline effects',
    'id': 'some_id',
    'journal': 'Journal of emergency nursing',
    'date': '2020/01/01'
})

sample_drugs = ['diphenhydramine', 'tetracycline', 'ethanol']

data_drugs = {'atccode': ['a04ad'], 'drug': ['diphenhydramine']}
data_pubmed = {'id': [1], 'title': ['A title with diphenhydramine'], 'date': "2020/01/01", 'journal': ['Journal A']}
data_clinical_trials = {'id': ['NCT01967433'], 'scientific_title': ['Some study'], 'date': "2020/01/01",
                        'journal': ['Journal B']}


def get_sample_pubmed_df() -> pd.DataFrame:
    data_pubmed = {
        'id': [1, 2, 3],
        'title': ['A title with diphenhydramine', 'Another title', 'Yet another title'],
        'journal': ['Journal of emergency nursing', 'The Journal of pediatrics', 'JOURNAL OF FOOD PROTECTION']
    }
    return pd.DataFrame(data_pubmed)


def test_adds_type_column():
    result_df = prepare_pubmed(get_sample_pubmed_df())
    assert 'type' in result_df.columns
    assert all(result_df['type'] == 'pubmed')


def test_renames_title_to_label():
    result_df = prepare_pubmed(get_sample_pubmed_df())
    assert 'label' in result_df.columns
    assert 'title' not in result_df.columns


def test_filters_columns():
    result_df = prepare_pubmed(get_sample_pubmed_df())
    assert set(result_df.columns) == {'id', 'label', 'type'}


def test_identify_drug_mention_in_label():
    matches = check_word(data_row, sample_drugs)
    assert any('diphenhydramine' in match['source'] for match in matches)
    assert any('tetracycline' in match['source'] for match in matches)
    assert not any('ethanol' in match['source'] for match in matches)


def test_returns_correct_links():
    matches = check_word(data_row, sample_drugs)
    diphenhydramine_links = [match for match in matches if match['source'] == 'diphenhydramine']
    assert any(match['target'] == 'some_id' for match in diphenhydramine_links)
    assert any(match['target'] == 'Journal of emergency nursing' for match in diphenhydramine_links)


def test_returns_empty_list_for_no_mention():
    no_drugs = []
    matches = check_word(data_row, no_drugs)
    assert not matches


def test_build_graph_output_structure():
    df_drugs = pd.DataFrame(data_drugs)
    df_pubmed = pd.DataFrame(data_pubmed)
    df_clinical_trials = pd.DataFrame(data_clinical_trials)
    result = build_graph(df_drugs, df_pubmed, df_clinical_trials)
    assert isinstance(result, list)
    assert len(result) == 2
    assert "nodes" in result[0]
    assert "edges" in result[1]


def test_drugs_node_type():
    df_drugs = pd.DataFrame(data_drugs)
    df_pubmed = pd.DataFrame(data_pubmed)
    df_clinical_trials = pd.DataFrame(data_clinical_trials)
    result = build_graph(df_drugs, df_pubmed, df_clinical_trials)
    drug_nodes = [node for node in result[0]['nodes'] if node['type'] == 'drugs']
    assert len(drug_nodes) == len(df_drugs)


def test_pubmed_and_clinical_trials_node_type():
    df_drugs = pd.DataFrame(data_drugs)
    df_pubmed = pd.DataFrame(data_pubmed)
    df_clinical_trials = pd.DataFrame(data_clinical_trials)
    result = build_graph(df_drugs, df_pubmed, df_clinical_trials)
    pubmed_nodes = [node for node in result[0]['nodes'] if node['type'] == 'pubmed']
    clinical_trials_nodes = [node for node in result[0]['nodes'] if node['type'] == 'clinical_trial']
    assert len(pubmed_nodes) == len(df_pubmed)
    assert len(clinical_trials_nodes) == len(df_clinical_trials)


def test_journal_nodes_added():
    df_drugs = pd.DataFrame(data_drugs)
    df_pubmed = pd.DataFrame(data_pubmed)
    df_clinical_trials = pd.DataFrame(data_clinical_trials)
    result = build_graph(df_drugs, df_pubmed, df_clinical_trials)
    journal_nodes = [node for node in result[0]['nodes'] if node['type'] == 'journal']
    assert len(journal_nodes) == 2


def test_edges_are_built():
    df_drugs = pd.DataFrame(data_drugs)
    df_pubmed = pd.DataFrame(data_pubmed)
    df_clinical_trials = pd.DataFrame(data_clinical_trials)
    result = build_graph(df_drugs, df_pubmed, df_clinical_trials)
    assert result[1]['edges']
