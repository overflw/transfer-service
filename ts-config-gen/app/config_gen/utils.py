import jsonpickle

from .glom_config_gen import GlomConfigGenerator
from app.models.configmodel import Config


def __query_for_mapping_files(url):
    """
    Query for mapping files.
    """
    # TODO: Implement in future iterations.
    pass


def __generate_graph_from_mapping_file(mapping_file):
    """
    Generate a graph from a mapping file.
    Since accessing data types for properties is facilitated by using shape graphs, 
    we suggest using RML2SHACL (see https://github.com/RMLio/RML2SHACL) like tooling to provide shape graph as well.
    The shape and data graphs could also be merged as expected in the current implementation.
    For the graph generation we suggest the SDM-RDFizer tool (see https://github.com/SDM-TIB/SDM-RDFizer).
    """
    # TODO Implement generating a template containing the of each key as its value from a mapping file in future iterations.
    
    # TODO Apply mapping file to template to generate the graph.
    


def __generate_alignment(source_graph, target_graph):
    """
    Generate an alignment from the source and target graphs.
    """
    # TODO: Implement in future iterations.
    pass


def generate_config(
    export_url=None,
    import_url=None,
    repository_url=None,
    alignment=None,
    source_mapping=None,
    target_mapping=None,
    source_graph = None,
    target_graph = None
):
    """
    Generate a config file for Glom.
    The arguments of the generator (source and target graphs, alignment and target template) must be generated from mapping files.
    These are retrieved either from the source and target controllers directly, or from a repository known to the application.
    """
    
    config: Config = {
        "exportingDataController": export_url,
        "importingDataController": import_url,
        "config": ""
    }

    if (source_graph is None) or (target_graph is None):
        # First try to query the source and target controllers directly for the mapping files
        if source_mapping is None:
            source_mapping = __query_for_mapping_files(export_url)
        if target_mapping is None:
            target_mapping = __query_for_mapping_files(import_url)

        # If arguments could not be retrieved from the controllers, query the repository
        if (source_mapping is None) or (target_mapping is None):
            source_mapping, target_mapping = __query_for_mapping_files(
                repository_url)

        if (source_mapping is None) or (target_mapping is None):
            raise Exception(
                "Could not retrieve mapping files from source and target controllers or repository.")

        # Generate the source and target graphs from the mapping files
        if source_graph is None:
            source_graph = __generate_graph_from_mapping_file(source_mapping)
        if target_graph is None:
            target_graph = __generate_graph_from_mapping_file(target_mapping)

    # If no alignment is provided, query for it or generate it from the source and target graphs
    if alignment is None:
        # TODO Query if an alignment can be provided from a repository or a Controller
        alignment = __generate_alignment(source_graph, target_graph)

    generator = GlomConfigGenerator(
        source_graph=source_graph,
        target_graph=target_graph,
        alignment=alignment,
        target_template=target_mapping
    )
    config["config"] = generator.get_config()

    # Pickle the config object so that it can be transferred as simle json to the transfer management module
    config = jsonpickle.encode(config)

    return config
