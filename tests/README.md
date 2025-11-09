# Test Suite

This directory contains the test suite for neomodel_bfo. All tests are designed to run without requiring a Neo4j database connection.

## Running Tests

Run all tests:
```bash
pytest
```

Run with verbose output:
```bash
pytest -v
```

Run specific test file:
```bash
pytest tests/test_bfo_structure.py
```

Run specific test class:
```bash
pytest tests/test_bfo_structure.py::TestBFOHierarchy
```

Run with coverage:
```bash
pytest --cov=neomodel_bfo
```

## Test Files

### `test_bfo_structure.py`

Tests the core BFO implementation structure without database dependencies.

**Test Classes:**

- `TestBFOImports` - Verifies all BFO classes can be imported
- `TestBFOHierarchy` - Validates class inheritance chains (e.g., Object → MaterialEntity → IndependentContinuant)
- `TestBFOProperties` - Checks that classes have expected properties (uid, name, value, unit, coordinates, etc.)
- `TestBFORelationships` - Verifies relationship definitions exist (part_of, inheres_in, participates_in, realizes, etc.)
- `TestBFODocumentation` - Ensures docstrings exist and contain BFO IDs
- `TestBFOModuleExports` - Validates `__all__` exports

### `test_examples.py`

Tests that example code in the `examples/` directory is valid and demonstrates proper BFO usage.

**Test Classes:**

- `TestBiologyExample` - Validates biology domain extension (Organism, AnatomicalStructure, etc.)
- `TestSocialOntologyExample` - Validates social ontology extension (Person, Organization, Roles, etc.)
- `TestExamplesDocumentation` - Ensures examples have documentation

## Test Philosophy

### What We Test

✅ **Structural integrity** - Class hierarchy, properties, relationships are defined
✅ **Import functionality** - All classes can be imported and used
✅ **Documentation exists** - Classes have docstrings with BFO IDs
✅ **Examples are valid** - Extension examples can be imported

### What We Don't Test

❌ **Database operations** - No Neo4j connection required
❌ **Relationship constraints** - BFO doesn't enforce constraints in Python
❌ **Data validation** - Validation is documentation-driven, not code-enforced
❌ **Cypher queries** - Graph traversal requires database setup

This keeps tests fast, deterministic, and runnable in any environment (CI, local, etc.).

## Adding New Tests

When adding new BFO classes or relationships:

1. Add import test in `TestBFOImports`
2. Add hierarchy test in `TestBFOHierarchy` if it's a new inheritance chain
3. Add property test in `TestBFOProperties` if new properties are added
4. Add relationship test in `TestBFORelationships` if new relationships are added
5. Add documentation test in `TestBFODocumentation`

When adding new examples:

1. Add import test in the appropriate example test class
2. Add property/relationship tests to verify BFO features are inherited
3. Add documentation test

## Test Dependencies

- `pytest` - Test runner
- `neomodel` - Required for importing BFO classes (but no database needed)

See `requirements_dev.txt` for version requirements.
