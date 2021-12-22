from abc import ABC, abstractmethod


class BaseConfigGen(ABC):
    """
    Methods
    -------
    __init__(source_graph, alignment, target_template)
        Initializes the class with the source graph, alignment and target template.
    generate_config()
        When implemented it should return a configuartion object for a translator to transform source data to target data.
    """

    @abstractmethod
    def __init__(self, source_graph, alignment, target_template):
        """
        Parameters
        ---------
        source_graph: RDF-Graph
            The source graph to be aligned with the target graph.
        alignment: Alignment-File
            A list of alignments in the (very much simpified) format [source_concept, target_concept]
        target_template: Template for the source data.
        
        Returns
        -------
        None
        """
        raise NotImplementedError

    @abstractmethod
    def get_config(self):
        """
        Returns
        -------
        config: dict
            A dictionary containing the configuration for the translator.
        """
        raise NotImplementedError