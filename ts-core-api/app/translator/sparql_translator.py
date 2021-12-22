import copy
import json
import subprocess
import os

from .base_translator import BaseTranslator


class JSON_Translator(BaseTranslator):
    """
    Class containing the methods for implementing a JSON-Data based translator.
    """

    def __init__(self):
        self.translation_config = None
        self.source_data = None

    def __run_sparql_generate_jar(self, path) -> None:
        subprocess.call(['java', '-jar', 'sparql-generate-2.0.9.jar', '-q', 'query.rqg'], cwd=path)

    def __execute_config(self):
        """
        Translates the source data based on the translation rules.
        :param source_data:
        :param translation_config:
        :return:
        """
        translated_data = None
        sparql_gen_path = os.path.dirname(os.path.realpath(__file__)) + '/sparql_gen/'

        # Write translation_config as query to sparql_gen subfolder
        with open(sparql_gen_path + '/query.rqg', 'w') as query_file:
            query_file.write(self.translation_config)

        # Write source data to sparql_gen subfolder
        with open(sparql_gen_path + '/source_data.json', 'w') as data_file:
            data_file.write(json.dumps(self.source_data, indent=2))

        # Write sparql-generate-conf.json to sparql_gen subfolder
        with open(sparql_gen_path + '/sparql-generate-conf.json', 'w') as conf_file:
            conf_file.write(json.dumps({
                "output": "output",
                "documentset": [
                    {
                        "uri": "http://example.com/source.json",
                        "mediatype": "appication/json",
                        "path": "source_data.json"
                    }
                ],
                "log": "0"
            }, indent=2))

        # Execute sparql-generate
        self.__run_sparql_generate_jar(sparql_gen_path)

        # Read output.json
        with open(sparql_gen_path + 'output', 'r') as output_file:
            translated_data = output_file.read()

        # Clean up
        os.remove(sparql_gen_path + 'output')
        os.remove(sparql_gen_path + 'query.rqg')
        os.remove(sparql_gen_path + 'source_data.json')
        os.remove(sparql_gen_path + 'sparql-generate-conf.json')

        return translated_data

    def translate(self, source_data, translation_config_path):

        with open (translation_config_path, 'r') as f:
            translation_config = f.read()

        self.source_data = source_data
        self.translation_config = translation_config
        translated_data = None

        if self.source_data is not None and self.translation_config is not None:
            translated_data = self.__execute_config()
        else:
            raise Exception(
                "Source data or translation config are not defined.")

        return translated_data


translator = JSON_Translator()
