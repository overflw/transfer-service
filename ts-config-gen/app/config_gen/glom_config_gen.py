import json
import jsonpickle
from profilehooks import profile
from rdflib import Graph, URIRef, Literal
import rdflib
from rdflib.namespace import XSD, RDF, SH
from .base_config_gen import BaseConfigGen


class GlomConfigGenerator(BaseConfigGen):
    """
    Class containing the methods for generating a translation configuration for a glom based translator.
    """

    def __init__(self, source_graph=None, target_graph=None, alignment=None, target_template=None):
        self.source_graph = source_graph
        self.target_graph = target_graph
        self.alignment = alignment
        self.target_template = target_template

    def get_config(self):

        # Apply alignment to source graph
        aligned_graph = self.__apply_alignment()

        # Resolve target template queries
        self.__resolve_template_queries(aligned_graph, self.target_template)
        config = self.target_template

        return config

    # @profile
    def __resolve_template_queries(self, graph, template):
        for key, value in template.items():
            if isinstance(value, dict):
                self.__resolve_template_queries(graph, value)
            else:
                # evaluate sparql query
                results = graph.query(value)

                # process query results and map them to template keys
                results_json = results.serialize(format="json")
                bindings = json.loads(results_json)["results"]["bindings"]
                bindings = [{k: jsonpickle.decode(v["value"]) for k, v in result.items()}
                            for result in bindings]
                if len(bindings) == 1:
                    if len(bindings[0]) == 1 and "result" in bindings[0]:
                        template[key] = bindings[0]["result"]
                    else:
                        template[key] = [{k: v}
                                         for k, v in bindings[0].items()]
                else:
                    template[key] = bindings

    def __apply_alignment(self):
        """
        Applies the alignment to the graph.
        For every node annotated by an aligned concept, try to update the node and its propertie's concept.
        """

        # Create a new graph
        aligned_graph = Graph()

        # For each aligned source class-concept, add all triples connected to this class to the aligned graph and update their concept
        for class_align in self.alignment['classes']:
            source_class = class_align[0]
            target_class = class_align[1]

            # Get all triples connected to the source class
            for s, p, o in self.source_graph.triples(
                    (None, RDF.type, URIRef(source_class))):
                # Add the triple to the aligned graph
                aligned_graph.add((s, p, URIRef(target_class)))

        for prop_align in self.alignment['properties']:
            source_prop = URIRef(prop_align[0])
            target_prop = URIRef(prop_align[1])

            # Get all triples with the source property
            for s, p, o in self.source_graph.triples((None, source_prop, None)):
                path = f"{o}"

                # Check whether the property data type should be transformed
                updated_path = self.__transform_property_data_type(
                    source_prop, target_prop, s, path)
                if updated_path:
                    path = updated_path
                o = Literal(jsonpickle.encode(path))
                # Add the triple to the aligned graph
                aligned_graph.add((s, target_prop, o))

        return aligned_graph

    def __transform_property_data_type(self, source_prop, target_prop, source_subject, source_value):
        """
        This method adds a data type conversion rule to the value of the source property based on the target property.
        First the source and target data types must be inferred from the properties and their subjects. 
        For this the corresponding SHACL shapes are evaluated.
        See https://www.w3.org/TR/shacl/
        """
        # Find the source and target property data types from the SHACL shapes graph.
        def __get_prop_data_type(prop, graph):
            # Verify that we use the shape for the correct subject.
            # Try to find the class of the properties subject
            shape_property_subject = None
            subject_class = graph.value(
                subject=source_subject, predicate=RDF.type)
            if subject_class:
                # Get the SHACL NodeShape subject for the subject class
                for s, p, o in graph.triples((None, SH.targetClass, subject_class)):
                    # Get the subjects of the NodeShape's properties named 'property'
                    for s, p, o in graph.triples((s, SH.property, None)):
                        # Verify that a sh:property matching the property in question is found
                        for s, p, o in graph.triples((o, SH.path, prop)):
                            shape_property_subject = s
            else:
                # If no subject class is found, we assume that the property is the correct one.
                shape_property_subject = graph.value(
                    predicate=SH.path,
                    object=prop
                )
            return graph.value(
                subject=shape_property_subject,
                predicate=SH.datatype
            )

        # Get the source property data type
        source_prop_data_type = __get_prop_data_type(
            source_prop, self.source_graph)
        target_prop_data_type = __get_prop_data_type(
            target_prop, self.target_graph)

        # Check whether the data type should be transformed
        if source_prop_data_type == target_prop_data_type:
            return None
        else:
            return self.__get_transform_rule(source_prop_data_type, target_prop_data_type, source_value)

    def __get_transform_rule(self, source_data_type, target_data_type, value):
        """
        Returns the transformation rule for the given data types. 
        In this prototype, value is a path and we create a glom spec transforming the output of the path to the target data type.
        """
        path_with_rules = None
        path = value
        # TODO: get the transformation rules from the repository or generate them locally

        # Dummy glom transformation rules
        if source_data_type == XSD.string:
            if target_data_type == XSD.integer:
                path_with_rules = (path, int)
            elif target_data_type == XSD.float:
                path_with_rules = (path, float)
            elif target_data_type == XSD.boolean:
                path_with_rules = (path, bool)

        return path_with_rules
