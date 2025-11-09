====================
Development Guide
====================

This guide provides detailed information for developers working on neomodel_bfo.

Development Setup
=================

Clone and Install
-----------------

Clone the repository::

    git clone https://github.com/rasinj/neomodel_bfo.git
    cd neomodel_bfo

Create a virtual environment (recommended)::

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

Install development dependencies::

    pip install -r requirements_dev.txt

This installs:

- pytest (testing)
- flake8 (linting)
- neomodel (core dependency)
- Sphinx (documentation)
- Other development tools

Development Workflow
====================

Making Changes
--------------

1. **Create a feature branch**::

    git checkout -b feature/your-feature-name

2. **Make your changes** - Edit code in ``neomodel_bfo/`` or add examples

3. **Write tests** - Add tests in ``tests/`` for new functionality

4. **Run tests**::

    pytest

5. **Run linter**::

    flake8 neomodel_bfo tests examples

6. **Commit your changes**::

    git add .
    git commit -m "Description of changes"

Code Organization
=================

Core BFO Module
---------------

``neomodel_bfo/bfo.py``
    Contains the complete BFO 2.0 class hierarchy. This file should only contain
    standard BFO classes, properties, and relationships.

    **DO NOT modify this file for domain-specific work.**

``neomodel_bfo/__init__.py``
    Package initialization and exports. Updates ``__all__`` when adding new BFO classes.

Examples Directory
------------------

``examples/``
    Contains domain extension examples showing how to use neomodel_bfo.

    - ``biology_example.py`` - Biological organisms and processes
    - ``social_ontology_example.py`` - People, organizations, and roles
    - ``EXTENSION_GUIDE.md`` - Comprehensive extension patterns
    - ``README.md`` - Overview of examples

Tests Directory
---------------

``tests/``
    Test suite for BFO structure and examples.

    - ``test_bfo_structure.py`` - Tests core BFO implementation
    - ``test_examples.py`` - Tests example code
    - ``README.md`` - Test documentation

Documentation Directory
-----------------------

``docs/``
    Sphinx documentation source files.

    - ``conf.py`` - Sphinx configuration
    - ``usage.rst`` - Usage guide
    - ``development.rst`` - This file
    - Build with ``make html`` in this directory

Adding New BFO Classes
======================

If you need to add a new BFO 2.0 class (rare - BFO is stable):

1. **Add class to bfo.py**::

    class NewBFOClass(ParentClass):
        """
        BFO:XXXXXXX - New BFO Class

        Definition from BFO specification.

        Examples: list examples here
        """
        # Properties and relationships

2. **Export in __init__.py** - Add to imports and ``__all__``

3. **Add tests**::

    # In tests/test_bfo_structure.py
    def test_new_class_imports(self):
        from neomodel_bfo import NewBFOClass
        assert NewBFOClass is not None

    def test_new_class_hierarchy(self):
        assert issubclass(NewBFOClass, ParentClass)

4. **Update documentation** - Add to ``docs/usage.rst`` if it's a major class

5. **Run tests** - Ensure all tests pass

Creating Domain Extensions
==========================

Domain extensions should go in separate packages or in the ``examples/`` directory.

Example Structure
-----------------

::

    your_domain_package/
    ├── __init__.py
    ├── entities.py         # Domain objects extending BFO
    ├── qualities.py        # Domain qualities
    ├── processes.py        # Domain processes
    └── README.md           # Domain documentation

Example Code
------------

::

    # entities.py
    from neomodel import StringProperty
    from neomodel_bfo import Object

    class DomainEntity(Object):
        """Your domain-specific entity."""
        domain_property = StringProperty()

See ``examples/EXTENSION_GUIDE.md`` for detailed patterns and best practices.

Testing Guidelines
==================

Test Philosophy
---------------

- Tests should run **without a Neo4j database**
- Test structure, not behavior (class hierarchy, properties exist, etc.)
- Keep tests fast and deterministic
- Test both core BFO and examples

Writing Tests
-------------

Add tests for:

- ✅ New classes can be imported
- ✅ Inheritance hierarchy is correct
- ✅ Properties are defined
- ✅ Relationships are defined
- ✅ Documentation exists

Do not test:

- ❌ Database operations (no Neo4j required)
- ❌ Data validation (BFO doesn't enforce)
- ❌ Cypher queries (integration tests only)

Test Example::

    def test_my_new_class(self):
        """Test that MyNewClass can be imported."""
        from neomodel_bfo import MyNewClass

        assert MyNewClass is not None
        assert issubclass(MyNewClass, ExpectedParent)
        assert 'expected_property' in dir(MyNewClass)

Documentation
=============

Docstring Standards
-------------------

All BFO classes must have docstrings with:

1. **BFO ID** - e.g., "BFO:0000001"
2. **Definition** - From BFO specification
3. **Examples** - Real-world instances
4. **Properties** - Document custom properties
5. **Relationships** - Document key relationships

Example::

    class MyClass(BFOParent):
        """
        BFO:XXXXXXX - My Class

        A class that represents something in BFO.

        Examples: concrete instance, another instance

        Properties:
            my_property: Description of property

        BFO Relations:
            - relationship_name: What it connects to
        """
        my_property = StringProperty()

Building Documentation
----------------------

Build HTML documentation::

    cd docs
    make html
    open _build/html/index.html

The documentation is also built automatically on ReadTheDocs.

Code Style
==========

Linting
-------

We use flake8 for linting::

    flake8 neomodel_bfo tests examples

Configuration is in ``setup.cfg``:

- Max line length: 127
- Max complexity: 10

Formatting
----------

- Use 4 spaces for indentation
- Follow PEP 8 conventions
- Keep lines under 127 characters
- Add blank lines between class definitions
- Use descriptive variable names

Imports
-------

Order imports as::

    # Standard library
    from datetime import datetime

    # Third-party
    from neomodel import StringProperty

    # Local
    from neomodel_bfo import Object

Common Tasks
============

Running All Checks
------------------

Before committing::

    # Run tests
    pytest -v

    # Run linter
    flake8 neomodel_bfo tests examples

    # Check documentation builds
    cd docs && make html

Releasing a New Version
-----------------------

1. Update version in ``neomodel_bfo/__init__.py``
2. Update ``HISTORY.rst`` with changes
3. Commit changes
4. Tag release::

    git tag -a v0.2.0 -m "Release version 0.2.0"
    git push --tags

5. Build and upload to PyPI::

    python setup.py sdist bdist_wheel
    twine upload dist/*

Troubleshooting
===============

Tests Failing
-------------

**Import errors**::

    # Make sure you've installed dev dependencies
    pip install -r requirements_dev.txt

**Pluggy version conflict**::

    # Update pluggy
    pip install 'pluggy>=1.5.0'

Linting Errors
--------------

**Line too long**::

    # Break into multiple lines or add # noqa comment if necessary

**Undefined name**::

    # Check imports are correct
    # Ensure variable is defined before use

Neo4j Connection Issues
-----------------------

The test suite doesn't require Neo4j. If you're running integration tests:

- Ensure Neo4j is running
- Check connection URL in neomodel config
- Verify credentials

Getting Help
============

- GitHub Issues: https://github.com/rasinj/neomodel_bfo/issues
- Documentation: https://neomodel-bfo.readthedocs.io
- BFO Specification: https://basic-formal-ontology.org
- Neomodel Docs: https://neomodel.readthedocs.io
