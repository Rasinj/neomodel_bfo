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

📚 **Read the Beautiful Documentation**: https://neomodel-bfo.readthedocs.io

* Free software: MIT license
* Repository: https://github.com/rasinj/neomodel_bfo
* Documentation setup: See ``DOCS_HOSTING.md``


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

Documentation & Resources
--------------------------

This repository contains extensive documentation for different audiences:

For Users
~~~~~~~~~

**Getting Started:**

* **Installation Guide** - ``docs/installation.md`` - Setup and requirements
* **Usage Guide** - ``docs/usage.md`` - Comprehensive usage examples with all BFO relationships
* **Online Documentation** - https://neomodel-bfo.readthedocs.io - Full documentation with API reference (MyST-MD format)

**Working with BFO:**

* All BFO classes have detailed docstrings including BFO IDs, definitions, and examples
* Use your IDE's autocomplete to explore available classes, properties, and relationships
* Example: ``Object?`` in IPython shows full BFO:0000030 documentation

For Domain Developers
~~~~~~~~~~~~~~~~~~~~~~

**Creating Extensions:**

* **Extension Guide** - ``examples/EXTENSION_GUIDE.md`` - Complete patterns and best practices for extending BFO
* **Biology Example** - ``examples/biology_example.py`` - Organisms, anatomical structures, biological processes
* **Social Ontology Example** - ``examples/social_ontology_example.py`` - People, organizations, roles, social processes
* **Examples README** - ``examples/README.md`` - Overview of extension patterns

**Key Patterns:**

* Subclass BFO classes for domain entities (``class Organism(Object)``)
* Use inherited BFO relationships (``part_of``, ``inheres_in``, ``participates_in``)
* Add domain-specific properties and relationships
* Never modify ``neomodel_bfo/bfo.py`` - extend in your own code

For Contributors
~~~~~~~~~~~~~~~~

**Development Guides:**

* **Contributing Guide** - ``CONTRIBUTING.rst`` - How to contribute, PR guidelines, BFO-specific rules
* **Development Guide** - ``docs/development_old.rst`` - Detailed development workflow, code organization, testing
* **Architecture Overview** - ``ARCHITECTURE.md`` - System design, design decisions, extensibility patterns
* **Documentation Hosting** - ``DOCS_HOSTING.md`` - How to view and deploy documentation online

**Code Organization:**

* **Core Package README** - ``neomodel_bfo/README.md`` - Core module structure and principles
* **Test Suite README** - ``tests/README.md`` - Testing philosophy and how to run tests
* **Source Code** - ``neomodel_bfo/bfo.py`` - BFO 2.0 implementation (600+ lines with full documentation)

**Quick Commands:**

::

    # Setup
    pip install -r requirements_dev.txt

    # Test
    pytest                           # Run all tests
    pytest -v                        # Verbose output
    pytest tests/test_bfo_structure.py  # Specific file

    # Lint
    flake8 neomodel_bfo tests examples

    # Documentation
    cd docs && make html

Repository Navigation
~~~~~~~~~~~~~~~~~~~~~

::

    neomodel_bfo/
    ├── neomodel_bfo/           # Core BFO package
    │   ├── bfo.py              # BFO 2.0 classes (Entity, Object, Process, Quality, etc.)
    │   ├── __init__.py         # Package exports
    │   └── README.md           # Core package documentation
    │
    ├── examples/               # Domain extension examples
    │   ├── biology_example.py  # Biological organisms and processes
    │   ├── social_ontology_example.py  # People, organizations, roles
    │   ├── EXTENSION_GUIDE.md  # Complete extension patterns (⭐ START HERE for domain work)
    │   └── README.md           # Examples overview
    │
    ├── tests/                  # Test suite (no Neo4j required)
    │   ├── test_bfo_structure.py  # Core BFO tests (28 tests)
    │   ├── test_examples.py   # Example code tests (9 tests)
    │   └── README.md           # Testing documentation
    │
    ├── docs/                   # Sphinx documentation (MyST-MD format)
    │   ├── index.md            # Documentation landing page
    │   ├── usage.md            # Usage guide with relationships
    │   ├── installation.md     # Installation guide
    │   ├── DEPLOYMENT.md       # Documentation deployment guide
    │   ├── development_old.rst # Development workflow (RST)
    │   └── ...                 # Other documentation
    │
    ├── .readthedocs.yaml       # ReadTheDocs configuration
    ├── .github/workflows/docs.yml  # GitHub Pages deployment
    ├── ARCHITECTURE.md         # System architecture and design decisions
    ├── CONTRIBUTING.rst        # Contribution guidelines (⭐ READ BEFORE CONTRIBUTING)
    ├── DOCS_HOSTING.md         # Documentation hosting guide (⭐ VIEW DOCS ONLINE)
    ├── README.rst              # This file
    └── HISTORY.rst             # Version history and changelog

Finding What You Need
~~~~~~~~~~~~~~~~~~~~~

**"I want to use BFO in my application"**
  → Start with Quick Start above, then read ``docs/usage.md`` or visit https://neomodel-bfo.readthedocs.io

**"I want to create a domain ontology"**
  → Read ``examples/EXTENSION_GUIDE.md``, review ``examples/biology_example.py``

**"I want to understand the architecture"**
  → Read ``ARCHITECTURE.md``

**"I want to contribute code"**
  → Read ``CONTRIBUTING.rst``, then ``docs/development_old.rst``

**"I want to view documentation online"**
  → Visit https://neomodel-bfo.readthedocs.io or see ``DOCS_HOSTING.md`` for setup

**"I want to understand a BFO class"**
  → Read docstrings in ``neomodel_bfo/bfo.py`` or use IDE autocomplete

**"I want to see what relationships are available"**
  → Check ``docs/usage.md`` "Working with Relationships" or online docs

**"I need help or found a bug"**
  → Open an issue at https://github.com/rasinj/neomodel_bfo/issues

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

Learning BFO
------------

If you're new to Basic Formal Ontology:

**Official BFO Resources:**

* BFO 2.0 Specification: https://basic-formal-ontology.org
* BFO OWL Ontology: http://purl.obolibrary.org/obo/bfo.owl
* BFO Documentation: https://github.com/BFO-ontology/BFO/wiki

**BFO in Practice:**

* OBO Foundry (BFO-based ontologies): http://www.obofoundry.org
* Gene Ontology (uses BFO): http://geneontology.org
* Common Core Ontologies (extends BFO): https://github.com/CommonCoreOntology/CommonCoreOntologies

**Key BFO Concepts:**

* **Continuants** persist through time (objects, qualities)
* **Occurrents** unfold over time (processes, events)
* **Mereology** (parthood): ``part_of``, ``has_part``
* **Inherence**: qualities/roles/functions inhere in bearers
* **Participation**: objects participate in processes
* **Realization**: processes realize functions and roles

See ``docs/usage.rst`` for how these concepts map to neomodel_bfo classes and relationships.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
