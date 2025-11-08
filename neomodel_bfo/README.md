# neomodel_bfo Core Package

This directory contains the core BFO 2.0 implementation for neomodel.

## Files

### `__init__.py`
Package initialization and exports. This file:
- Imports all BFO classes from `bfo.py`
- Defines `__all__` for clean imports
- Exposes BFO classes at package level

Usage:
```python
from neomodel_bfo import Object, Quality, Process
```

### `bfo.py`
Complete BFO 2.0 class hierarchy implementation. Contains:
- All 40+ BFO classes (Entity, Continuant, Occurrent, etc.)
- Core BFO relationships (part_of, inheres_in, participates_in, realizes, etc.)
- Standard properties (temporal, spatial, descriptive)
- Comprehensive docstrings with BFO IDs

**⚠️ Important**: This file should only contain standard BFO 2.0 classes and relationships. Do NOT add domain-specific extensions here.

## Design Principles

### 1. Pure BFO Core
This package implements only standard BFO 2.0 without domain-specific additions. Domain extensions should be in separate packages or the `examples/` directory.

### 2. No Validation Enforcement
BFO relationships are defined but not enforced at runtime. This provides maximum flexibility:
- All relationships use `ZeroOrMore` cardinality
- No Python validators or save() hooks
- Ontological coherence is documentation-driven

### 3. Graph-First
Designed to leverage Neo4j's graph capabilities:
- Bidirectional relationships (e.g., `part_of` ↔ `has_part`)
- Graph traversal via neomodel
- Supports Cypher queries for complex reasoning

### 4. Extensibility via Inheritance
Proper use:
```python
# ✅ CORRECT - Extend in your own code
from neomodel_bfo import Object

class Organism(Object):
    species = StringProperty()
```

Improper use:
```python
# ❌ WRONG - Don't modify bfo.py
class Object(MaterialEntity):
    species = StringProperty()  # Don't add domain properties here!
```

## Module Structure

```
Entity (base)
├── Continuant (persists through time)
│   ├── IndependentContinuant
│   │   ├── MaterialEntity (objects with matter)
│   │   │   ├── Object
│   │   │   ├── FiatObjectPart
│   │   │   └── ObjectAggregate
│   │   └── ImmaterialEntity
│   │       ├── Site
│   │       ├── SpatialRegion
│   │       └── ContinuantFiatBoundary
│   ├── GenericallyDependentContinuant (information)
│   └── SpecificallyDependentContinuant
│       ├── Quality (attributes)
│       └── RealizableEntity
│           ├── Role
│           ├── Disposition
│           └── Function
└── Occurrent (unfolds over time)
    ├── Process
    │   ├── History
    │   └── ProcessProfile
    ├── ProcessBoundary
    ├── TemporalRegion
    └── SpatioTemporalRegion
```

## Key Relationships

| Relationship | Domain | Range | Meaning |
|-------------|--------|-------|---------|
| `part_of` | Continuant/Occurrent | Same type | Mereological parthood |
| `inheres_in` | SpecificallyDependentContinuant | IndependentContinuant | Quality/Role/Function borne by entity |
| `participates_in` | IndependentContinuant | Process | Entity participating in process |
| `realizes` | Process | RealizableEntity | Process realizing role/function |
| `exists_at` | Continuant | TemporalRegion | When entity exists |
| `occurs_in` | Occurrent | TemporalRegion | When event occurs |

See `bfo.py` docstrings for complete relationship documentation.

## Adding New BFO Classes

Only add classes that are part of BFO 2.0 specification:

1. Add class to `bfo.py` with proper docstring (include BFO ID)
2. Add to imports in `__init__.py`
3. Add to `__all__` in `__init__.py`
4. Add tests in `tests/test_bfo_structure.py`
5. Update documentation in `docs/usage.rst`

## References

- BFO 2.0 Specification: https://basic-formal-ontology.org
- BFO OWL: http://purl.obolibrary.org/obo/bfo.owl
- neomodel Documentation: https://neomodel.readthedocs.io
