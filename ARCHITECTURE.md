# Architecture Overview

This document provides a high-level overview of neomodel_bfo's architecture and design decisions.

## Core Philosophy

neomodel_bfo implements Basic Formal Ontology (BFO) 2.0 as a clean, extensible Python library for Neo4j graph databases. The architecture follows three key principles:

1. **Separation of Concerns** - Pure BFO core separated from domain extensions
2. **Graph-Native Design** - Leverages Neo4j's relationship model for ontological reasoning
3. **Flexibility Over Enforcement** - Documentation-driven ontological coherence without runtime validation

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Applications                        │
│  (Biomedical informatics, scientific data, domain ontologies)│
└─────────────────┬───────────────────────────────────────────┘
                  │ inherits from
┌─────────────────▼───────────────────────────────────────────┐
│                  Domain Extensions                           │
│        (examples/biology_example.py, etc.)                   │
│  Classes: Organism, Cell, Person, Organization, etc.        │
└─────────────────┬───────────────────────────────────────────┘
                  │ extends
┌─────────────────▼───────────────────────────────────────────┐
│              neomodel_bfo Core Package                       │
│               (neomodel_bfo/bfo.py)                          │
│  Classes: Entity, Object, Process, Quality, etc.            │
│  Relationships: part_of, inheres_in, realizes, etc.         │
└─────────────────┬───────────────────────────────────────────┘
                  │ uses
┌─────────────────▼───────────────────────────────────────────┐
│                      neomodel OGM                            │
│  (Object-Graph Mapping for Neo4j)                           │
└─────────────────┬───────────────────────────────────────────┘
                  │ connects to
┌─────────────────▼───────────────────────────────────────────┐
│                   Neo4j Graph Database                       │
└─────────────────────────────────────────────────────────────┘
```

## Component Overview

### Core BFO Implementation (`neomodel_bfo/bfo.py`)

**Purpose**: Pure implementation of BFO 2.0 class hierarchy

**Contents**:
- 40+ BFO classes (Entity → Continuant/Occurrent → subclasses)
- Standard BFO relationships (15+ core relationships)
- Standard properties (temporal, spatial, descriptive)

**Key Design Decision**: This file contains ONLY standard BFO 2.0. No domain-specific additions.

**Why**: Ensures the core remains reusable across all domains (biology, social science, engineering, etc.)

### Package Exports (`neomodel_bfo/__init__.py`)

**Purpose**: Clean API for importing BFO classes

**Design**: Re-exports all classes from `bfo.py` at package level

**Usage**: `from neomodel_bfo import Object, Quality, Process`

### Domain Extensions (`examples/`)

**Purpose**: Demonstrate how to extend BFO for specific domains

**Pattern**: Subclass BFO classes, add domain properties/relationships

**Examples**:
- `biology_example.py` - Organisms, cells, biological processes
- `social_ontology_example.py` - People, organizations, roles

### Test Suite (`tests/`)

**Purpose**: Verify structural integrity without database dependencies

**Strategy**: Test that classes exist, have correct hierarchy, properties, and relationships - not runtime behavior

**Why**: Fast, deterministic tests that run anywhere (CI, local, etc.)

## Design Decisions

### 1. No Runtime Validation

**Decision**: BFO relationships are defined but not enforced in Python

**Rationale**:
- BFO axioms are complex (e.g., "every quality must inhere in something")
- Runtime enforcement adds overhead and reduces flexibility
- Different domains may have different validation needs
- Ontological coherence is better maintained through documentation and domain-specific validators

**Implementation**: All relationships use `ZeroOrMore` cardinality

### 2. Bidirectional Relationships

**Decision**: Relationships have both forward and inverse directions

**Example**:
```python
# Forward
part.part_of.connect(whole)

# Inverse (automatic)
whole.has_part.all()  # Returns [part]
```

**Rationale**: Enables natural graph traversal in both directions

**Implementation**: Use neomodel's `RelationshipTo` and `RelationshipFrom` on same relationship type

### 3. Abstract Base Classes

**Decision**: Some BFO classes marked as abstract (Entity, Continuant, etc.)

**Rationale**: These are ontological categories, not directly instantiated entities

**Implementation**: `__abstract_node__ = True` in class definition

### 4. Temporal and Spatial Properties

**Decision**: Include basic temporal/spatial properties in core BFO

**Properties**:
- Temporal: `start_time`, `end_time`, `temporal_start`, `temporal_end`
- Spatial: `coordinates` (JSON), `coordinate_system`

**Rationale**: BFO entities exist in time and space; provide basic support without prescribing formats

**Flexibility**: JSON for coordinates allows any coordinate system (lat/lng, x/y/z, WKT, etc.)

### 5. Graph-First vs. Object-First

**Decision**: Emphasize graph relationships over object attributes

**Example**:
```python
# ✅ Graph-first (preferred)
temp = Quality(value="37", unit="°C")
temp.inheres_in.connect(organism)

# ❌ Object-first (avoid)
organism.temperature = "37°C"  # Loses ontological structure
```

**Rationale**: BFO is fundamentally about relationships; graph databases excel at relationships

## Data Flow

### Creating Entities and Relationships

```
1. User creates BFO instance
   organism = Object(name="E. coli")

2. Save to Neo4j
   organism.save()
   [neomodel creates Node with label "Object"]

3. Create relationship
   temp.inheres_in.connect(organism)
   [neomodel creates Edge "INHERES_IN" from temp to organism]

4. Query via graph traversal
   organism.bearer_of.all()
   [neomodel traverses "INHERES_IN" edges in reverse]
```

### Extension Pattern

```
1. Domain developer extends BFO class
   class Organism(Object):
       species = StringProperty()

2. Inherits BFO relationships automatically
   - part_of, has_part
   - participates_in
   - bearer_of
   - All Entity properties

3. Uses relationships same as core BFO
   heart.part_of.connect(organism)
```

## Extensibility Points

### For Domain Ontologies

- **Subclass any BFO class** - Add properties, domain-specific relationships
- **Keep BFO relationships** - Inherit standard relationships like `part_of`, `inheres_in`
- **Add domain relationships** - Define new relationships specific to your domain

### For New BFO Classes

If BFO specification adds new classes:
1. Add to `bfo.py` with BFO ID in docstring
2. Export in `__init__.py`
3. Add tests in `test_bfo_structure.py`
4. Document in `docs/usage.rst`

## Non-Goals

What this library does NOT attempt:

- **Reasoning Engine** - No OWL reasoning, SWRL rules, or logical inference
- **Constraint Enforcement** - No runtime validation of BFO axioms
- **Data Validation** - No schema enforcement beyond neomodel's property types
- **OWL/RDF Export** - Focused on graph database use, not semantic web interchange

These capabilities can be added by users if needed, but aren't in the core library to maintain simplicity and performance.

## Performance Considerations

- **No validation overhead** - Save operations are fast (just neomodel)
- **Graph traversal** - Leverages Neo4j's optimized relationship queries
- **Lazy loading** - Relationships loaded on access, not eagerly
- **Index properties** - `uid` is indexed for fast lookups

## Future Directions

Potential enhancements (not committed, just possibilities):

- **Utility functions** - Helper methods for common graph queries (transitive closure of `part_of`, etc.)
- **Domain ontology templates** - More examples in different domains
- **Visualization tools** - Graph visualization of BFO instances
- **Import/Export** - Integration with OBO formats, OWL ontologies

## References

- BFO 2.0 Specification: https://basic-formal-ontology.org
- neomodel Documentation: https://neomodel.readthedocs.io
- Neo4j Graph Database: https://neo4j.com
- OBO Foundry: http://www.obofoundry.org (BFO-based ontologies)
