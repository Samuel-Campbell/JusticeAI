import joblib
import numpy as np
from outcome_predictor.svm import LinearSVM
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


def load_data():
    """
        Loads a binarized version of our precedents
    """
    print("loading data")
    file = open('structured_precedent.bin', 'rb')
    model = joblib.load(file)
    file.close()
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


def load_new_data(data_set):
    """
        Loads a binarized version of regexed facts
        and merges it with the existing data set
        params: data_set: initial data_set
    """
    print("loading regex data")
    file = open('prec.bin', 'rb')
    prec = joblib.load(file)
    print("merging data")
    new_val = []
    for val in data_set:
        if val['name'] + '.txt' in prec.keys():
            new_val.append({'name': val['name'], 'facts_vector': np.fromiter(prec[val[
                           'name'] + '.txt'].values(), dtype=np.int32), 'decisions_vector': val['decisions_vector']})
    return new_val


if __name__ == "__main__":
    data_set = load_data()
    # Taking a subset since I don't want to wait forever
    data_set = data_set[1:10000]
    data_set = load_new_data(data_set)
    linear_svm = LinearSVM(data_set)
    linear_svm.train()
