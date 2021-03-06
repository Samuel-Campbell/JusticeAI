import os
import unittest

from rasa.rasa_classifier import RasaClassifier


class TestRasaClassifier(unittest.TestCase):
    rasaClassifier = None

    @classmethod
    def setUpClass(cls):
        cls.rasaClassifier = RasaClassifier()
        cls.rasaClassifier.train(force_train=False)

    def test_instantiate(self):
        self.assertIsNotNone(self.rasaClassifier)

    def test_classify_claimcategory_tenant(self):
        classifier_output = self.rasaClassifier.classify_problem_category("i am being kicked out", "TENANT")
        self.assertIsNotNone(classifier_output)

    def test_classify_claimcategory_landlord(self):
        classifier_output = self.rasaClassifier.classify_problem_category("my tenant owes me rent money", "LANDLORD")
        self.assertIsNotNone(classifier_output)

    def test_classify_acknowledgement(self):
        classifier_output = self.rasaClassifier.classify_acknowledgement("sure")
        self.assertIsNotNone(classifier_output)

    def test_extract_factentities(self):
        classifier_output = self.rasaClassifier.classify_fact("apartment_dirty", "No")
        self.assertIsNotNone(classifier_output)

    def test_nonexistent_factentities(self):
        classifier_output = self.rasaClassifier.classify_fact("does_not_exist", "Whatever.")
        self.assertIsNone(classifier_output)
