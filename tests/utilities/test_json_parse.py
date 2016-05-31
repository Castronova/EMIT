import json
import unittest
import os


class test_json_parse(unittest.TestCase):
    # Test each model individually
    # Test pass if the file exist and type(data: dictionary)

    def test_parse_multiplier(self):
        path = os.path.realpath("../../")
        path += "/app_data/models/multiplier/multiplier.mdl"
        self.assertTrue(os.path.exists(path), path + " does not exist")

        with open(path, "r") as f:
            data = json.load(f)
        f.close()
        self.assertIsInstance(data, dict, "data is not a dictionary")

    def test_parse_randomizer(self):
        path = os.path.realpath("../../")
        path += "/app_data/models/randomizer/randomizer.mdl"
        self.assertTrue(os.path.exists(path), path + " does not exist")

        with open(path, "r") as f:
            data = json.load(f)
        f.close()
        self.assertIsInstance(data, dict, "data is not a dictionary")

    def test_parse_slow_loading(self):
        path = os.path.realpath("../../")
        path += "/app_data/models/slow_loading/slow_loading.mdl"
        self.assertTrue(os.path.exists(path), path + " does not exist")

        with open(path, "r") as f:
            data = json.load(f)
        f.close()
        self.assertIsInstance(data, dict, "data is not a dictionary")

    def test_parse_top_model(self):
        path = os.path.realpath("../../")
        path += "/app_data/models/topmodel/topmodel.mdl"
        self.assertTrue(os.path.exists(path), path + " does not exist")

        with open(path, "r") as f:
            data = json.load(f)
        f.close()
        self.assertIsInstance(data, dict, "data is not a dictionary")

    def test_parse_ueb_model(self):
        path = os.path.realpath("../../")
        path += "/app_data/models/ueb/ueb.mdl"
        self.assertTrue(os.path.exists(path), path + " does not exist")

        with open(path, "r") as f:
            data = json.load(f)
        f.close()
        self.assertIsInstance(data, dict, "data is not a dictionary")

    def test_parse_weap_model(self):
        path = os.path.realpath("../../")
        path += "/app_data/models/weap/weap.mdl"
        self.assertTrue(os.path.exists(path), path + " does not exist")

        with open(path, "r") as f:
            data = json.load(f)
        f.close()
        self.assertIsInstance(data, dict, "data is not a dictionary")

    def test_parse_weather_model(self):
        path = os.path.realpath("../../")
        path += "/app_data/models/weather/weatherReader.mdl"
        self.assertTrue(os.path.exists(path), path + " does not exist")

        with open(path, "r") as f:
            data = json.load(f)
        f.close()
        self.assertIsInstance(data, dict, "data is not a dictionary")

    def test_unicode_to_string(self):
        """
        When converting the .mdl to .json, hidden characters were copied which caused errors when parsing the json
        This test checks the two spots where the hidden characters existed.
        :return:
        """
        path = os.path.realpath("../../")
        path += "/app_data/models/topmodel/topmodel.mdl"
        with open(path, "r") as f2:

            data = f2.read()
            json_data = json.loads(data)

            self.assertIsInstance(str(json_data["model"][0]["description"]), str, "Not a string")

        f2.close()
