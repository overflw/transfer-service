import jsonpickle
import rdflib
import json

from app.config_gen.glom_config_gen import GlomConfigGenerator
from app.config_gen.utils import generate_config


def config_gen_setup(
    alignment,
    source_data_json_ld,
    target_data_json_ld,
    target_template,
    source_shapes_json_ld=None,
    target_shapes_json_ld=None
):
    def __graph_from_json_ld(json_ld):
        json_ld = json.dumps(json_ld)
        graph = rdflib.Graph()
        graph.parse(
            data=json_ld,
            format='json-ld'
        )
        return graph

    source_graph = __graph_from_json_ld(source_data_json_ld)
    target_graph = __graph_from_json_ld(target_data_json_ld)
    if source_shapes_json_ld is not None:
        source_shape_graph = __graph_from_json_ld(source_shapes_json_ld)
        source_graph += source_shape_graph

    if target_shapes_json_ld is not None:
        target_shape_graph = __graph_from_json_ld(target_shapes_json_ld)
        target_graph += target_shape_graph

    config = generate_config(
        alignment=alignment,
        source_graph=source_graph,
        target_graph=target_graph,
        target_mapping=target_template)

    config = jsonpickle.decode(config)
    config = config["config"]

    return config


def test_glom_config_gen_type_conversion_1():

    alignment = {
        "classes": [
            ['http://www.w3.org/2002/12/cal/ical#Vevent', 'http://schema.org/Event']
        ],
        "properties": [
            ['http://www.w3.org/2002/12/cal/ical#dtstart',
                'http://schema.org/startDate'],
        ]
    }
    source_data_graph_json_ld = {
        "@context": {
            "ical": "http://www.w3.org/2002/12/cal/ical#",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "ical:dtstart": {
                    "@type": "xsd:string",
            }
        },
        "@type": "ical:Vevent",
        "ical:dtstart": "concert.start"
    }
    source_shapes_graph_json_ld = {
        "@context": {
            "ex": "http://example.com",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "ical": "http://www.w3.org/2002/12/cal/ical#",
            "sh": "http://www.w3.org/ns/shacl#",
            "schema": "http://schema.org/"
        },
        "@id": "ex:EventShape",
        "@type": "sh:NodeShape",
        "sh:targetClass": {"@id":"ical:Vevent"},
        "sh:property": [
            {
                "sh:path": {"@id": "ical:dtstart"},
                "sh:maxCount": 1,
                "sh:datatype": {"@id": "xsd:string"}
            }
        ],
        "closed": True
    }
    target_data_graph_json_ld = {
        "@context": {
            "ical": "http://www.w3.org/2002/12/cal/ical#",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "schema": "http://schema.org/",
            "schema:startDate": {
                "@type": "xsd:float"
            }
        }
    }
    target_shapes_graph_json_ld = {
        "@context": {
            "ex": "http://example.com",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "ical": "http://www.w3.org/2002/12/cal/ical#",
            "sh": "http://www.w3.org/ns/shacl#",
            "schema": "http://schema.org/"
        },
        "@id": "ex:SchemaEventShape",
        "@type": "sh:NodeShape",
        "sh:targetClass": {"@id":"schema:Event"},
        "sh:property": [
            {
                "sh:path": {"@id": "schema:startDate"},
                "sh:maxCount": 1,
                "sh:datatype": {"@id": "xsd:float"}
            }
        ],
        "closed": True
    }

    target_template = {
        "start": """PREFIX schema:   <http://schema.org/>
        SELECT DISTINCT ?result
        WHERE {
            ?a schema:startDate ?result .
        }"""
    }

    config = config_gen_setup(
        alignment=alignment,
        source_data_json_ld=source_data_graph_json_ld,
        target_data_json_ld=target_data_graph_json_ld,
        target_template=target_template,
        target_shapes_json_ld=target_shapes_graph_json_ld,
        source_shapes_json_ld=source_shapes_graph_json_ld,
    )

    assert config == {
        "start": ('concert.start', float)
    }


def test_glom_config_gen_type_conversion_3():

    alignment = {
        "classes": [
        ],
        "properties": [
            ['http://www.w3.org/2002/12/cal/ical#dtstart',
                'http://schema.org/startDate'],
            ['http://www.w3.org/2002/12/cal/ical#location',
                'http://schema.org/location'],
            ['http://www.w3.org/2002/12/cal/ical#summary',
                'http://www.w3.org/2002/12/cal/ical#summary'],
        ]
    }
    source_data_graph_json_ld = {
        "@context": {
            "ical": "http://www.w3.org/2002/12/cal/ical#",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "ical:dtstart": {
                    "@type": "xsd:string",
            }
        },
        "ical:summary": "concert.summary",
        "ical:location": "concert.location",
        "ical:dtstart": "concert.start"
    }
    source_shapes_graph_json_ld = {
        "@context": {
            "ex": "http://example.com",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "ical": "http://www.w3.org/2002/12/cal/ical#",
            "sh": "http://www.w3.org/ns/shacl#",
            "schema": "http://schema.org/"
        },
        "@id": "ex:PersonShape",
        "@type": "sh:NodeShape",
        "sh:targetClass": "schema:Person",
        "sh:property": [
            {
                "sh:path": {"@id": "ical:dtstart"},
                "sh:maxCount": 1,
                "sh:datatype": {"@id": "xsd:string"}
            }
        ],
        "closed": True
    }

    target_data_graph_json_ld = {
        "@context": {
            "ical": "http://www.w3.org/2002/12/cal/ical#",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "schema": "http://schema.org/",
            "schema:startDate": {
                "@type": "xsd:float"
            }
        },
    }
    target_shapes_graph_json_ld = {
        "@context": {
            "ex": "http://example.com",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "ical": "http://www.w3.org/2002/12/cal/ical#",
            "sh": "http://www.w3.org/ns/shacl#",
            "schema": "http://schema.org/"
        },
        "@id": "ex:PersonShape",
        "@type": "sh:NodeShape",
        "sh:targetClass": "schema:Person",
        "sh:property": [
            {
                "sh:path": {"@id": "schema:startDate"},
                "sh:maxCount": 1,
                "sh:datatype": {"@id": "xsd:float"}
            }
        ],
        "closed": True
    }

    target_template = {
        "summary": """PREFIX ical:   <http://www.w3.org/2002/12/cal/ical#>
        SELECT DISTINCT ?result
        WHERE {
            ?a ical:summary ?result .
        }""",
        "location": """PREFIX schema:   <http://schema.org/>
        SELECT DISTINCT ?result
        WHERE {
            ?a schema:location ?result .
        }""",
        "start": """PREFIX schema:   <http://schema.org/>
        SELECT DISTINCT ?result
        WHERE {
            ?a schema:startDate ?result .
        }"""
    }

    config = config_gen_setup(
        alignment=alignment,
        source_data_json_ld=source_data_graph_json_ld,
        target_data_json_ld=target_data_graph_json_ld,
        target_template=target_template,
        target_shapes_json_ld=target_shapes_graph_json_ld,
        source_shapes_json_ld=source_shapes_graph_json_ld,
    )

    assert config == {
        "summary": 'concert.summary',
        "location": 'concert.location',
        "start": ('concert.start', float)
    }


def test_config_gen_4():
    alignment = {
        "classes": [
            ['http://schema.org/Person', 'http://schema.org/Person']
        ],
        "properties": [
            ['http://schema.org/name', 'http://schema.org/name'],
            ['http://schema.org/birthDate', 'http://schema.org/birthDate'],
            ['http://schema.org/jobTitle', 'http://schema.org/jobTitle'],
            ['http://schema.org/telephone', 'http://schema.org/telephone'],
            ['http://schema.org/email', 'http://schema.org/email']
        ]
    }

    source_graph_json_ld = {
        "@context": "https://schema.org/docs/jsonldcontext.json",
        "@type": "Person",
        "name": "user.name",
        "birthDate": "user.birthDate",
        "jobTitle": "user.jobTitle",
        "telephone": "user.telephone",
        "email": "user.email"
    }
    target_graph_json_ld = {
        "@context": "https://schema.org/docs/jsonldcontext.json",
        "@type": "Person"
    }
    target_template = {
        "fullName": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?result
            WHERE {
                ?a schema:name ?result .
            }""",
        "title": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?result
            WHERE {
                ?a schema:jobTitle ?result .
            }""",
        "birthDate": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?result
            WHERE {
                ?a schema:birthDate ?result .
            }""",
        "contactPoints": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?telephone ?email
            WHERE {
                ?a schema:telephone ?telephone .
                ?a schema:email ?email .
            }"""
    }

    config = config_gen_setup(
        alignment=alignment,
        source_data_json_ld=source_graph_json_ld,
        target_data_json_ld=target_graph_json_ld,
        target_template=target_template
    )

    assert config == {
        "fullName": "user.name",
        "title": "user.jobTitle",
        "birthDate": "user.birthDate",
        "contactPoints": [{"email": "user.email"},
                          {"telephone": "user.telephone"}]
    }


def test_config_gen_4_direct():
    alignment = {
        "classes": [
            ['http://schema.org/Person', 'http://schema.org/Person']
        ],
        "properties": [
            ['http://schema.org/name', 'http://schema.org/name'],
            ['http://schema.org/birthDate', 'http://schema.org/birthDate'],
            ['http://schema.org/jobTitle', 'http://schema.org/jobTitle'],
            ['http://schema.org/telephone', 'http://schema.org/telephone'],
            ['http://schema.org/email', 'http://schema.org/email']
        ]
    }

    source_graph_json_ld = {
        "@context": {"@vocab": "http://schema.org/"},
        "@type": "Person",
        "name": "user.name",
        "birthDate": "user.birthDate",
        "jobTitle": "user.jobTitle",
        "telephone": "user.telephone",
        "email": "user.email"
    }
    target_graph_json_ld = {
        "@context": {"@vocab": "http://schema.org/"},
        "@type": "Person"
    }
    target_template = {
        "fullName": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?result
            WHERE {
                ?a schema:name ?result .
            }""",
        "title": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?result
            WHERE {
                ?a schema:jobTitle ?result .
            }""",
        "birthDate": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?result
            WHERE {
                ?a schema:birthDate ?result .
            }""",
        "contactPoints": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?telephone ?email
            WHERE {
                ?a schema:telephone ?telephone .
                ?a schema:email ?email .
            }"""
    }

    config = config_gen_setup(
        alignment=alignment,
        source_data_json_ld=source_graph_json_ld,
        target_data_json_ld=target_graph_json_ld,
        target_template=target_template
    )

    assert config == {
        "fullName": "user.name",
        "title": "user.jobTitle",
        "birthDate": "user.birthDate",
        "contactPoints": [{"email": "user.email"},
                          {"telephone": "user.telephone"}]
    }


def test_config_gen_8():
    alignment = {
        "classes": [
            ['http://schema.org/Person', 'http://schema.org/Person']
        ],
        "properties": [
            ['http://schema.org/name', 'http://schema.org/name'],
            ['http://schema.org/familyName', 'http://schema.org/familyName'],
            ['http://schema.org/address', 'http://schema.org/address'],
            ['http://schema.org/birthDate', 'http://schema.org/birthDate'],
            ['http://schema.org/deathDate', 'http://schema.org/deathDate'],
            ['http://schema.org/gender', 'http://schema.org/gender'],
            ['http://schema.org/jobTitle', 'http://schema.org/jobTitle'],
            ['http://schema.org/telephone', 'http://schema.org/telephone'],
            ['http://schema.org/email', 'http://schema.org/email']
        ]
    }

    source_graph_json_ld = {
        "@context": "https://schema.org/docs/jsonldcontext.json",
        "@type": "Person",
        "name": "user.name",
        "familyName": "user.familyName",
        "address": "user.address",
        "deathDate": "user.deathDate",
        "birthDate": "user.birthDate",
        "gender": "user.gender",
        "jobTitle": "user.jobTitle",
        "telephone": "user.telephone",
        "email": "user.email"
    }
    target_graph_json_ld = {
        "@context": "https://schema.org/docs/jsonldcontext.json",
        "@type": "Person"
    }
    target_template = {
        "fullName": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?result
            WHERE {
                ?a schema:name ?result .
            }""",
        "title": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?result
            WHERE {
                ?a schema:jobTitle ?result .
            }""",
        "address": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?result
            WHERE {
                ?a schema:address ?result .
            }""",
        "gender": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?result
            WHERE {
                ?a schema:gender ?result .
            }""",
        "birthDate": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?result
            WHERE {
                ?a schema:birthDate ?result .
            }""",
        "deathDate": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?result
            WHERE {
                ?a schema:deathDate ?result .
            }""",
        "familyName": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?result
            WHERE {
                ?a schema:familyName ?result .
            }""",
        "contactPoints": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?telephone ?email
            WHERE {
                ?a schema:telephone ?telephone .
                ?a schema:email ?email .
            }"""
    }

    config = config_gen_setup(
        alignment=alignment,
        source_data_json_ld=source_graph_json_ld,
        target_data_json_ld=target_graph_json_ld,
        target_template=target_template
    )

    assert config == {
        "fullName": "user.name",
        "title": "user.jobTitle",
        "birthDate": "user.birthDate",
        "deathDate": "user.deathDate",
        "familyName": "user.familyName",
        "address": "user.address",
        "gender": "user.gender",
        "contactPoints": [{"email": "user.email"},
                          {"telephone": "user.telephone"}]
    }


def test_config_gen_8_direct():
    alignment = {
        "classes": [
            ['http://schema.org/Person', 'http://schema.org/Person']
        ],
        "properties": [
            ['http://schema.org/name', 'http://schema.org/name'],
            ['http://schema.org/familyName', 'http://schema.org/familyName'],
            ['http://schema.org/address', 'http://schema.org/address'],
            ['http://schema.org/birthDate', 'http://schema.org/birthDate'],
            ['http://schema.org/deathDate', 'http://schema.org/deathDate'],
            ['http://schema.org/gender', 'http://schema.org/gender'],
            ['http://schema.org/jobTitle', 'http://schema.org/jobTitle'],
            ['http://schema.org/telephone', 'http://schema.org/telephone'],
            ['http://schema.org/email', 'http://schema.org/email']
        ]
    }

    source_graph_json_ld = {
        "@context": {"@vocab": "http://schema.org/"},
        "@type": "Person",
        "name": "user.name",
        "familyName": "user.familyName",
        "address": "user.address",
        "deathDate": "user.deathDate",
        "birthDate": "user.birthDate",
        "gender": "user.gender",
        "jobTitle": "user.jobTitle",
        "telephone": "user.telephone",
        "email": "user.email"
    }
    target_graph_json_ld = {
        "@context": {"@vocab": "http://schema.org/"},
        "@type": "Person"
    }
    target_template = {
        "fullName": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?result
            WHERE {
                ?a schema:name ?result .
            }""",
        "title": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?result
            WHERE {
                ?a schema:jobTitle ?result .
            }""",
        "address": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?result
            WHERE {
                ?a schema:address ?result .
            }""",
        "gender": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?result
            WHERE {
                ?a schema:gender ?result .
            }""",
        "birthDate": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?result
            WHERE {
                ?a schema:birthDate ?result .
            }""",
        "deathDate": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?result
            WHERE {
                ?a schema:deathDate ?result .
            }""",
        "familyName": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?result
            WHERE {
                ?a schema:familyName ?result .
            }""",
        "contactPoints": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?telephone ?email
            WHERE {
                ?a schema:telephone ?telephone .
                ?a schema:email ?email .
            }"""
    }

    config = config_gen_setup(
        alignment=alignment,
        source_data_json_ld=source_graph_json_ld,
        target_data_json_ld=target_graph_json_ld,
        target_template=target_template
    )

    assert config == {
        "fullName": "user.name",
        "title": "user.jobTitle",
        "birthDate": "user.birthDate",
        "deathDate": "user.deathDate",
        "familyName": "user.familyName",
        "address": "user.address",
        "gender": "user.gender",
        "contactPoints": [{"email": "user.email"},
                          {"telephone": "user.telephone"}]
    }


def test_config_gen_3():
    alignment = {
        "classes": [
        ],
        "properties": [
            ['http://schema.org/name', 'http://schema.org/name'],
            ['http://schema.org/telephone', 'http://schema.org/telephone'],
            ['http://schema.org/email', 'http://schema.org/email']
        ]
    }

    source_graph_json_ld = {
        "@context": "https://schema.org/docs/jsonldcontext.json",
        "@type": "Person",
        "name": "user.name",
        "telephone": "user.telephone",
        "email": "user.email"
    }
    target_graph_json_ld = {
        "@context": "https://schema.org/docs/jsonldcontext.json",
        "@type": "Person"
    }
    target_template = {
        "fullName": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?result
            WHERE {
                ?a schema:name ?result .
            }""",
        "contactPoints": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?telephone ?email
            WHERE {
                ?a schema:telephone ?telephone .
                ?a schema:email ?email .
            }"""
    }

    config = config_gen_setup(
        alignment=alignment,
        source_data_json_ld=source_graph_json_ld,
        target_data_json_ld=target_graph_json_ld,
        target_template=target_template
    )

    assert config == {
        "fullName": "user.name",
        "contactPoints": [{"email": "user.email"},
                          {"telephone": "user.telephone"}]
    }


def test_config_gen_3_direct():
    alignment = {
        "classes": [
        ],
        "properties": [
            ['http://schema.org/name', 'http://schema.org/name'],
            ['http://schema.org/telephone', 'http://schema.org/telephone'],
            ['http://schema.org/email', 'http://schema.org/email']
        ]
    }

    source_graph_json_ld = {
        "@context": {"@vocab": "http://schema.org/"},
        "@type": "Person",
        "name": "user.name",
        "telephone": "user.telephone",
        "email": "user.email"
    }
    target_graph_json_ld = {
        "@context": {"@vocab": "http://schema.org/"},
        "@type": "Person"
    }
    target_template = {
        "fullName": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?result
            WHERE {
                ?a schema:name ?result .
            }""",
        "contactPoints": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?telephone ?email
            WHERE {
                ?a schema:telephone ?telephone .
                ?a schema:email ?email .
            }"""
    }

    config = config_gen_setup(
        alignment=alignment,
        source_data_json_ld=source_graph_json_ld,
        target_data_json_ld=target_graph_json_ld,
        target_template=target_template
    )

    assert config == {
        "fullName": "user.name",
        "contactPoints": [{"email": "user.email"},
                          {"telephone": "user.telephone"}]
    }


def test_config_gen_2():
    alignment = {
        "classes": [
            ['http://schema.org/Person', 'http://schema.org/Person']
        ],
        "properties": [
            ['http://schema.org/name', 'http://schema.org/name'],
            ['http://schema.org/email', 'http://schema.org/email']
        ]
    }

    source_graph_json_ld = {
        "@context": "https://schema.org/docs/jsonldcontext.json",
        "@type": "Person",
        "name": "user.name",
        "email": "user.email"
    }
    target_graph_json_ld = {
        "@context": "https://schema.org/docs/jsonldcontext.json",
        "@type": "Person"
    }
    target_template = {
        "fullName": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?result
            WHERE {
                ?a schema:name ?result .
            }""",
        "email": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?result
            WHERE {
                ?a schema:email ?result .
            }"""
    }

    config = config_gen_setup(
        alignment=alignment,
        source_data_json_ld=source_graph_json_ld,
        target_data_json_ld=target_graph_json_ld,
        target_template=target_template
    )

    assert config == {
        "fullName": "user.name",
        "email": "user.email"
    }


def test_config_gen_2_direct():
    alignment = {
        "classes": [
        ],
        "properties": [
            ['http://schema.org/name', 'http://schema.org/name'],
            ['http://schema.org/email', 'http://schema.org/email']
        ]
    }

    source_graph_json_ld = {
        "@context": {
            "@vocab": "http://schema.org/",
        },
        "@type": "Person",
        "name": "user.name",
        "email": "user.email"
    }
    target_graph_json_ld = {
        "@context": {
            "@vocab": "http://schema.org/",
        },
        "@type": "Person"
    }
    target_template = {
        "fullName": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?result
            WHERE {
                ?a schema:name ?result .
            }""",
        "email": """
            PREFIX schema:   <http://schema.org/>
            SELECT DISTINCT ?result
            WHERE {
                ?a schema:email ?result .
            }"""
    }

    config = config_gen_setup(
        alignment=alignment,
        source_data_json_ld=source_graph_json_ld,
        target_data_json_ld=target_graph_json_ld,
        target_template=target_template
    )

    assert config == {
        "fullName": "user.name",
        "email": "user.email"
    }


def test_bm_confgen_2_entries(benchmark):
    benchmark(test_config_gen_2)


def test_bm_confgen_3_entries(benchmark):
    benchmark(test_config_gen_3)


def test_bm_confgen_4_entries(benchmark):
    benchmark(test_config_gen_4)


def test_bm_confgen_8_entries(benchmark):
    benchmark(test_config_gen_8)


def test_bm_confgen_2_entries_direct(benchmark):
    benchmark(test_config_gen_2_direct)


def test_bm_confgen_3_entries_direct(benchmark):
    benchmark(test_config_gen_3_direct)


def test_bm_confgen_4_entries_direct(benchmark):
    benchmark(test_config_gen_4_direct)


def test_bm_confgen_8_entries_direct(benchmark):
    benchmark(test_config_gen_8_direct)


def test_bm_confgen_1_entries_type_con(benchmark):
    benchmark(test_glom_config_gen_type_conversion_1)


def test_bm_confgen_3_entries_type_con(benchmark):
    benchmark(test_glom_config_gen_type_conversion_3)
