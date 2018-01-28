import os
import timeit

from rasa_nlu.components import ComponentBuilder
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.converters import load_data
from rasa_nlu.model import Trainer, Interpreter


# Class which will hold all the Rasa logic from training to parsing
class RasaClassifier:
    # Directories & Files
    config_file = "rasa/config/config_spacy_duckling.json"
    model_dir = "rasa/projects/justiceai/"
    fact_data_dir = "rasa/data/fact/"
    category_data_dir = "rasa/data/category/"

    # Dicts
    problem_category_interpreters = {}
    fact_interpreters = {}

    # RASA Caching
    builder = ComponentBuilder(use_cache=True)

    def __init__(self):
        self.rasa_config = RasaNLUConfig(self.config_file)
        self.trainer = Trainer(self.rasa_config, self.builder)

    def train(self, force_train=False, initialize_interpreters=True):

        """
        Trains the data sets from facts and problem categories separately
        :param force_train: If False will use saved models
        :param initialize_interpreters: If True the interpreters get initialized with models already present
        """

        # Train fact classifier
        self.__train_interpreter(self.fact_data_dir, self.fact_interpreters, force_train=force_train,
                                 initialize_interpreters=initialize_interpreters)

        # Train problem category classifier
        self.__train_interpreter(self.category_data_dir, self.problem_category_interpreters, force_train=force_train,
                                 initialize_interpreters=initialize_interpreters)

    def classify_problem_category(self, message):
        """
        Classifies a claim category based on a message
        :param message: Message received from user
        :return: The classified claim category dict from RASA
        """

        return self.problem_category_interpreters['claim_category'].parse(message.lower())

    def classify_fact(self, fact_name, message):
        """
        Classifies a fact based on a message
        :param fact_name: Name of the fact being classified i.e. tenant_owes_rent
        :param message: Message received from user
        :return: The classified fact dict from RASA
        """

        if fact_name in self.fact_interpreters:
            return self.fact_interpreters[fact_name].parse(message.lower())
        return None

    def __train_interpreter(self, training_data_dir, interpreter_dict, force_train, initialize_interpreters):
        """
        Trains the interpreters for fact and claim category classification
        :param training_data_dir: Directory where data is stores
        :param interpreter_dict: Dictionary will contain the interpreters
        :param force_train: If True will retrain model data
        :param initialize_interpreters: If True will initialize the interpreters
        """

        print("~~Starting training with data directory {}~~".format(training_data_dir))
        if force_train is False:
            print("->No force train, using saved models.".format(training_data_dir))

        if initialize_interpreters is False:
            print("->No interpreter initialization. Will only create model data.".format(training_data_dir))

        training_start = timeit.default_timer()

        fact_files = os.listdir(training_data_dir)
        for filename in fact_files:
            fact_key = os.path.splitext(filename)[0]

            if force_train:
                training_data = load_data(training_data_dir + filename)
                self.trainer.train(training_data)
                model_directory = self.trainer.persist(path=self.model_dir, fixed_model_name=fact_key)
            else:
                model_directory = self.model_dir + "default/" + fact_key

            print("Model data directory for fact {}: {}".format(fact_key, model_directory))
            if initialize_interpreters:
                interpreter_dict[fact_key] = Interpreter.load(model_directory, self.rasa_config, self.builder)

        training_end = timeit.default_timer()
        total_training_time = round(training_end - training_start, 2)

        print("~~Training Finished. Took {}s for {} facts ~".format(total_training_time, len(fact_files)))
