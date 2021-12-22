import jsonpickle
from glom import glom


from .base_translator import BaseTranslator


class GlomTranslator(BaseTranslator):
    """
    Class containing the methods for implementing a glom based translator.
    """

    def __init__(self):
        pass

    def translate(self, source_data, translation_config):

        # extract the translation config
        spec = jsonpickle.decode(translation_config)["config"]

        if source_data is not None and translation_config is not None:
            return glom(source_data, translation_config)
        else:
            raise Exception(
                "Source data or translation config are not defined.")

translator = GlomTranslator()