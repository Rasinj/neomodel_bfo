============
neomodel_bfo
============


.. image:: https://img.shields.io/pypi/v/neomodel_bfo.svg
        :target: https://pypi.python.org/pypi/neomodel_bfo

.. image:: https://img.shields.io/travis/rasinj/neomodel_bfo.svg
        :target: https://travis-ci.com/rasinj/neomodel_bfo

.. image:: https://readthedocs.org/projects/neomodel-bfo/badge/?version=latest
        :target: https://neomodel-bfo.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Neomodel-bfo provides a complete BFO 2.0 (Basic Formal Ontology) implementation for Neo4j graph databases using neomodel.

BFO is a top-level ontology designed to support scientific research and knowledge representation. This library lets you build BFO-compliant knowledge graphs in Neo4j, making it ideal for biomedical informatics, scientific data integration, and any domain requiring rigorous ontological modeling.

* Free software: MIT license
* Documentation: https://neomodel-bfo.readthedocs.io


Features
--------

* **Complete BFO 2.0 Class Hierarchy** - All 40+ BFO classes implemented as neomodel nodes
* **Core BFO Relationships** - Standard relationships (part_of, inheres_in, participates_in, realizes, etc.)
* **Temporal & Spatial Properties** - Built-in support for time and space modeling
* **Extensible Architecture** - Clean separation between core BFO and domain extensions
* **Comprehensive Documentation** - Detailed docstrings with BFO semantics and examples
* **Graph Database Native** - Leverages Neo4j's graph capabilities for ontological reasoning
* **Type-Safe** - Python classes provide type checking and IDE support
* **Zero Validation Overhead** - No runtime constraint enforcement for maximum flexibility

Quick Start
------------

Install the package::

    pip install neomodel-bfo

Basic usage::

    from neomodel import config, StringProperty
    from neomodel_bfo import Object, Quality, Process

    # Configure Neo4j connection
    config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'

    # Create a material object (e.g., an organism)
    organism = Object(name="E. coli K12").save()

    # Create a quality that inheres in the organism
    temp = Quality(
        name="Temperature",
        value="37.0",
        unit="°C"
    ).save()
    temp.inheres_in.connect(organism)

    # Create a process the organism participates in
    growth = Process(name="Cell division").save()
    organism.participates_in.connect(growth)

    # Query using graph relationships
    for quality in organism.bearer_of.all():
        print(f"{quality.name}: {quality.value} {quality.unit}")

Extending for Your Domain
--------------------------

Create domain-specific ontologies by subclassing BFO::

    from neomodel import StringProperty, IntegerProperty
    from neomodel_bfo import Object, Function, Process

    class Organism(Object):
        """Domain-specific organism class."""
        species = StringProperty()
        age_years = IntegerProperty()

    class MetabolicFunction(Function):
        """A biological function."""
        pathway = StringProperty()

    # Use BFO relationships
    heart = Organism(name="Heart", species="Homo sapiens").save()
    pump_function = MetabolicFunction(name="Pumping").save()
    pump_function.inheres_in.connect(heart)

See the ``examples/`` directory for complete examples in biology, social science, and more.

BFO Classes Included
--------------------

**Continuants** (entities that persist through time):

* Independent Continuants: Object, FiatObjectPart, ObjectAggregate, Site, SpatialRegion, etc.
* Dependent Continuants: Quality, Role, Disposition, Function

**Occurrents** (entities that unfold over time):

* Process, ProcessBoundary, History, ProcessProfile
* TemporalRegion, SpatioTemporalRegion

See documentation for the complete class hierarchy.

Development
-----------

Setting up a development environment::

    git clone https://github.com/rasinj/neomodel_bfo.git
    cd neomodel_bfo
    pip install -r requirements_dev.txt

Running tests::

    pytest

Running linter::

    flake8 neomodel_bfo tests examples

Project Structure
~~~~~~~~~~~~~~~~~

::

    neomodel_bfo/
    ├── neomodel_bfo/       # Main package
    │   ├── __init__.py     # Package exports
    │   └── bfo.py          # Core BFO 2.0 implementation (DO NOT MODIFY for domain work)
    ├── examples/           # Domain extension examples
    │   ├── biology_example.py
    │   ├── social_ontology_example.py
    │   └── EXTENSION_GUIDE.md
    ├── tests/              # Test suite
    │   ├── test_bfo_structure.py
    │   └── test_examples.py
    └── docs/               # Sphinx documentation

Key Principles
~~~~~~~~~~~~~~

* **Core BFO stays pure** - ``neomodel_bfo/bfo.py`` contains only BFO 2.0 standard classes
* **Extend via subclassing** - Domain-specific ontologies inherit from BFO classes
* **No validation enforcement** - Relationships are optional; ontological coherence is documentation-driven
* **Graph-first design** - Leverages Neo4j relationships for ontological reasoning

For detailed development guidelines, see ``CONTRIBUTING.rst`` and ``examples/EXTENSION_GUIDE.md``.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
