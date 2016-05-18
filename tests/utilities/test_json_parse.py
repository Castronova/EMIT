import json
import unittest
import os


class test_json_parse(unittest.TestCase):

    def test_parse_multiplier_json(self):
        path = os.path.realpath("../../")
        path += "/app_data/models/multiplier/multiplier.json"
        self.assertTrue(os.path.exists(path), path + " does not exist")

        with open(path, "r") as f:
            data = json.load(f)
        f.close()
        self.assertIsInstance(data, dict, "data is not a dictionary")
