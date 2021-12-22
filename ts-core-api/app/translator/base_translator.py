from abc import ABC, abstractmethod


class BaseTranslator(ABC):
    """
    Base class for all translators.
    Methods
    -------
    translate(source_schema, target_schema)
        When implemented it should return a dictionary containing the translated data
    """

    @abstractmethod
    def translate(self, source_data, translation_rules_file_path):
        """
        Parameters
        ---------
        source_data: Dict
        translation_rules: Dict
        
        Returns
        -------
        dict
            A dictionary containing the translated data
        """
        raise NotImplementedError