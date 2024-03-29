import jsonpickle

from tests import json_sparql_source, json_sparql_query_path 
from tests import json_glom_source, glom_translation_config_string

from app.translator.glom_translator import translator as glom_translator
from app.translator.sparql_translator import translator as sparql_translator

def test_sparql_translator():
    
    output = sparql_translator.translate(json_sparql_source, json_sparql_query_path)
    assert output != None
    
def test_glom_translator():

    config = jsonpickle.decode(glom_translation_config_string)["config"]

    output = glom_translator.translate(json_glom_source, config)
    assert output == {
        "name": "Jane Doe",
        "email": "mailto:jane-doe@xyz.edu"    
    }