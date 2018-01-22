from model_training.svm.linear_svc import LinearSVC
from model_training.similar_finder.similar_finder import SimilarFinder
from util.file import Load
from util.log import Log


def __dictionary_to_list():
    """

    Converts the binarize structured_data_dict to a list format

    structured_data_dict:{
        filename:{
            name: 'AZ-XXXXXXX.txt',
            demands_vector: [...],
            facts_vector: [...],
            outcomes_vector: [...]
        }
    }

    :return: data_list: [{
        name: 'AZ-XXXXXXX.txt',
        demands_vector: [...],
        facts_vector: [...],
        outcomes_vector: [...]
    },
    {
        ...
    }]
    """
    precedent_vector = Load.load_binary("precedent_vectors.bin")
    Log.write("Formatting data")
    data_list = []
    for precedent_file in precedent_vector:
        data_list.append(precedent_vector[precedent_file])
    return data_list


class CommandEnum:
    SVM = "--svm"
    SIMILARITY_FINDER = "--sf"
    command_list = [SVM, SIMILARITY_FINDER]


def run(command_list):
    """
    1) Converts dictionary a precedent vectors to a list of dictionaries
    2) Train the support vector machine model
    3) train the similarity finder model

    :param command_list: List of command line arguments. Not used yet since there is only 1 training technique
    :return: boolean
    """
    Log.write("Executing train model.")

    for command in command_list:
        if '--' == command[:2]:
            if command not in CommandEnum.command_list:
                Log.write(command + " not recognized")
                return False

    try:
        data_size = command_list[-1]
        precedent_vector = __dictionary_to_list()[:int(data_size)]

    except IndexError:
        precedent_vector = __dictionary_to_list()

    if CommandEnum.SVM in command_list:
        linear_svm = LinearSVC(precedent_vector)
        linear_svm.train()

    if CommandEnum.SIMILARITY_FINDER in command_list:
        SimilarFinder(train=True, dataset=precedent_vector)

    precedent_vector = None # deallocate memory

    return True
