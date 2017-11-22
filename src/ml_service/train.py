import numpy as np
from outcome_predictor.svm import LinearSVM
from ml_models.models import Load
# I ran a crude regex to see which clusters have resiliation
resiliation_custers = [1,
                       2,
                       12,
                       17,
                       23,
                       25,
                       63,
                       78,
                       84,
                       96,
                       97,
                       98,
                       119,
                       138,
                       140,
                       143,
                       190,
                       197,
                       199,
                       253,
                       284,
                       306,
                       346,
                       381,
                       384,
                       393,
                       395,
                       423,
                       442,
                       445,
                       451,
                       463,
                       468,
                       506,
                       510,
                       512,
                       543,
                       560
                       ]


def get_valid_cluster_precedent_vector():
    """
        Loads a binarized version of our precedents
    """
    print("loading data")
    model = Load.load_model_from_bin(Load.precedent_vector_from_clusters)
    for (key, val) in model.items():
        val['name'] = key
    valid_values = [precedent for precedent in model.values() if precedent[
        'facts_vector'] is not None and precedent['decisions_vector'] is not None]
    for val in valid_values:
        if 'decisions' in val.keys():
            del val['decisions']
        if 'facts' in val.keys():
            del val['facts']
        resiliation_values = [val['decisions_vector'][x]
                              for x in resiliation_custers]
        if np.sum(resiliation_values) > 0:
            val['decisions_vector'] = np.array([1])
        else:
            val['decisions_vector'] = np.array([0])
    return valid_values


def merge_regex_and_cluster_precedent_vector(data_set):
    """
        Loads a binarized version of regexed facts
        and merges it with the existing data set
        params: data_set: initial data_set
    """
    print("loading regex data")
    fact_vectors = Load.load_model_from_bin(Load.regex_vectors)
    # demand_vectors = Load.load_model_from_bin(Load.demand_vector_regex_lib)

    # # creates new fact vector where file have has facts and demands
    # new_fact_vectors = {}
    # for file_name in fact_vectors.keys():
    #     if file_name in demand_vectors:
    #         new_fact_vectors[file_name] = np.append(fact_vectors[file_name], demand_vectors[file_name], axis=0)
    print("merging data")
    new_val = []
    for val in data_set:
        if val['name'] + '.txt' in fact_vectors.keys():
            new_val.append(
                {
                    'name': val['name'],
                    'facts_vector': fact_vectors[val['name'] + '.txt']['facts_vector'],
                    'demands_vector': fact_vectors[val['name'] + '.txt']['demands_vector'],
                    'decisions_vector': val['decisions_vector']
                }
            )
    return new_val


if __name__ == "__main__":
    valid_cluster_precedent_vector = get_valid_cluster_precedent_vector()
    # Taking a subset since I don't want to wait forever
    new_precedent_vector = merge_regex_and_cluster_precedent_vector(
        valid_cluster_precedent_vector)
    linear_svm = LinearSVM(new_precedent_vector)
    linear_svm.train()
