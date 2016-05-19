import json
import unittest
import os


class test_json_parse(unittest.TestCase):
    # Test each model individually
    # Test pass if the file exist and type(data: dictionary)

    def test_parse_multiplier(self):
        path = os.path.realpath("../../")
        path += "/app_data/models/multiplier/multiplier.json"
        self.assertTrue(os.path.exists(path), path + " does not exist")

        with open(path, "r") as f:
            data = json.load(f)
        f.close()
        self.assertIsInstance(data, dict, "data is not a dictionary")

    def test_parse_randomizer(self):
        path = os.path.realpath("../../")
        path += "/app_data/models/randomizer/randomizer.json"
        self.assertTrue(os.path.exists(path), path + " does not exist")

        with open(path, "r") as f:
            data = json.load(f)
        f.close()
        self.assertIsInstance(data, dict, "data is not a dictionary")

    def test_parse_slow_loading(self):
        path = os.path.realpath("../../")
        path += "/app_data/models/slow_loading/slow_loading.json"
        self.assertTrue(os.path.exists(path), path + " does not exist")

        with open(path, "r") as f:
            data = json.load(f)
        f.close()
        self.assertIsInstance(data, dict, "data is not a dictionary")

    def test_parse_top_model(self):
        path = os.path.realpath("../../")
        path += "/app_data/models/topmodel/topmodel.json"
        self.assertTrue(os.path.exists(path), path + " does not exist")

        with open(path, "r") as f:
            data = json.load(f)
        f.close()
        self.assertIsInstance(data, dict, "data is not a dictionary")

    def test_parse_ueb_model(self):
        path = os.path.realpath("../../")
        path += "/app_data/models/ueb/ueb.json"
        self.assertTrue(os.path.exists(path), path + " does not exist")

        with open(path, "r") as f:
            data = json.load(f)
        f.close()
        self.assertIsInstance(data, dict, "data is not a dictionary")

    def test_parse_weap_model(self):
        path = os.path.realpath("../../")
        path += "/app_data/models/weap/weap.json"
        self.assertTrue(os.path.exists(path), path + " does not exist")

        with open(path, "r") as f:
            data = json.load(f)
        f.close()
        self.assertIsInstance(data, dict, "data is not a dictionary")

    def test_parse_weather_model(self):
        path = os.path.realpath("../../")
        path += "/app_data/models/weather/weatherReader.json"
        self.assertTrue(os.path.exists(path), path + " does not exist")

        with open(path, "r") as f:
            data = json.load(f)
        f.close()
        self.assertIsInstance(data, dict, "data is not a dictionary")
