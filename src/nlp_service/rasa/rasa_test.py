import os
import unittest

from rasa.rasa_classifier import RasaClassifier


class TestRasaClassifier(unittest.TestCase):
    rasaClassifier = None

    @classmethod
    def setUpClass(cls):
        cls.rasaClassifier = RasaClassifier()
        cls.rasaClassifier.train(force_train=True)

    def test_instantiate(self):
        self.assertIsNotNone(self.rasaClassifier)

    def test_classify_claimcategory(self):
        classifier_output = self.rasaClassifier.classify_problem_category("I am being kicked out.")
        self.assertIsNotNone(classifier_output)

    def test_extract_factentities(self):
        classifier_output = self.rasaClassifier.classify_fact("is_student", "I am a student.")
        self.assertIsNotNone(classifier_output)

    def test_nonexistent_factentities(self):
        classifier_output = self.rasaClassifier.classify_fact("does_not_exist", "I am a student.")
        self.assertIsNone(classifier_output)

    def test_percent_difference(self):
        intent_dict = {
            'intent_ranking': [
                {'confidence': 0.5},
                {'confidence': 0.5}
            ]
        }
        self.assertEqual(RasaClassifier.intent_percent_difference(intent_dict), 0)