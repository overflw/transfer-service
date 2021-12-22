import os
import json
import importlib.util


# Load data for tests
test_dir = os.path.dirname(__file__)

json_sparql_source_path = os.path.join(test_dir, 'data', 'sparql_translator', 'sparql_source.json')
json_sparql_query_path = os.path.join(test_dir, 'data', 'sparql_translator','json_sparql_query.rql')

glom_source_data_path = os.path.join(test_dir, 'data', 'glom_translator', 'source_data.json')
glom_translation_config_path = os.path.join(test_dir, 'data', 'glom_translator', 'translation_config.py')

json_sparql_source = json.load(open(json_sparql_source_path))

json_glom_source = json.load(open(glom_source_data_path))