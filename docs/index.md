# neomodel_bfo Documentation

```{toctree}
:maxdepth: 2
:hidden:
:caption: Getting Started

installation
usage
```

```{toctree}
:maxdepth: 2
:hidden:
:caption: Development

development
contributing
```

```{toctree}
:maxdepth: 1
:hidden:
:caption: Reference

modules
authors
history
```

::::{grid} 1 1 2 3
:gutter: 4
:class-container: full-width

:::{grid-item-card} 🚀 Quick Start
:link: installation
:link-type: doc

Install neomodel_bfo and get started in minutes
:::

:::{grid-item-card} 📖 Usage Guide
:link: usage
:link-type: doc

Learn how to use BFO classes and relationships
:::

:::{grid-item-card} 🧬 Examples
:link: https://github.com/rasinj/neomodel_bfo/tree/master/examples
:link-type: url

Explore biology and social ontology examples
:::

:::{grid-item-card} 🏗️ Architecture
:link: https://github.com/rasinj/neomodel_bfo/blob/master/ARCHITECTURE.md
:link-type: url

Understand the system design
:::

:::{grid-item-card} 🤝 Contributing
:link: contributing
:link-type: doc

Help improve neomodel_bfo
:::

:::{grid-item-card} 📚 API Reference
:link: modules
:link-type: doc

Browse the complete API
:::

::::

## What is neomodel_bfo?

**neomodel_bfo** provides a complete BFO 2.0 (Basic Formal Ontology) implementation for Neo4j graph databases using neomodel.

```{admonition} What is BFO?
:class: info

Basic Formal Ontology (BFO) is a top-level ontology designed to support scientific research and knowledge representation. It provides a rigorous framework for organizing entities based on whether they persist through time (Continuants) or unfold over time (Occurrents).
```

## Why neomodel_bfo?

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} 🎯 Complete BFO 2.0
All 40+ BFO classes with standard relationships
:::

:::{grid-item-card} 🔗 Graph Native
Leverages Neo4j's relationship model
:::

:::{grid-item-card} 🎨 Extensible
Clean separation of core BFO and domain extensions
:::

:::{grid-item-card} 🚄 Fast & Flexible
No runtime validation overhead
:::

::::

## Quick Example

:::::{tab-set}

::::{tab-item} Basic Usage

```python
from neomodel import config
from neomodel_bfo import Object, Quality, Process

# Configure Neo4j
config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'

# Create entities
organism = Object(name="E. coli K12").save()

# Add quality
temp = Quality(name="Temperature", value="37", unit="°C").save()
temp.inheres_in.connect(organism)

# Create process
growth = Process(name="Cell division").save()
organism.participates_in.connect(growth)

# Query
for quality in organism.bearer_of.all():
    print(f"{quality.name}: {quality.value} {quality.unit}")
```

::::

::::{tab-item} Domain Extension

```python
from neomodel import StringProperty, IntegerProperty
from neomodel_bfo import Object, Function

# Extend BFO classes
class Organism(Object):
    species = StringProperty()
    age_years = IntegerProperty()

class MetabolicFunction(Function):
    pathway = StringProperty()

# Use with BFO relationships
organism = Organism(species="E. coli", age_years=2).save()
function = MetabolicFunction(pathway="glycolysis").save()
function.inheres_in.connect(organism)
```

::::

::::{tab-item} Advanced Queries

```python
from neomodel import db

# Cypher query for transitive parthood
results, meta = db.cypher_query(
    """
    MATCH (org:Object {uid: $uid})<-[:PART_OF*]-(part)
    RETURN part.name as name, part.uid as uid
    """,
    {'uid': organism.uid}
)

for name, uid in results:
    print(f"Part: {name} ({uid})")
```

::::

:::::

## Features

```{list-table}
:header-rows: 1
:widths: 30 70

* - Feature
  - Description
* - 🏗️ Complete BFO 2.0
  - All 40+ BFO classes (Entity, Object, Process, Quality, etc.)
* - 🔗 Core Relationships
  - part_of, inheres_in, participates_in, realizes, and more
* - ⏱️ Temporal & Spatial
  - Built-in support for time and space modeling
* - 🎨 Extensible
  - Clean separation between core BFO and domain extensions
* - 📖 Well Documented
  - Detailed docstrings with BFO IDs and examples
* - 🧪 Type Safe
  - Python classes provide type checking and IDE support
* - 🚀 Zero Overhead
  - No runtime constraint enforcement
```

## BFO Class Hierarchy

::::{dropdown} View Complete Hierarchy
:open:

**Continuants** (persist through time)

```
Entity
└── Continuant
    ├── IndependentContinuant
    │   ├── MaterialEntity
    │   │   ├── Object
    │   │   ├── FiatObjectPart
    │   │   └── ObjectAggregate
    │   └── ImmaterialEntity
    │       ├── Site
    │       ├── SpatialRegion
    │       │   ├── ZeroDimensionalSpatialRegion
    │       │   ├── OneDimensionalSpatialRegion
    │       │   ├── TwoDimensionalSpatialRegion
    │       │   └── ThreeDimensionalSpatialRegion
    │       └── ContinuantFiatBoundary
    │           ├── ZeroDimensionalContinuantFiatBoundary
    │           ├── OneDimensionalContinuantFiatBoundary
    │           └── TwoDimensionalContinuantFiatBoundary
    ├── GenericallyDependentContinuant
    └── SpecificallyDependentContinuant
        ├── Quality
        │   └── RelationalQuality
        └── RealizableEntity
            ├── Role
            ├── Disposition
            └── Function
```

**Occurrents** (unfold over time)

```
Entity
└── Occurrent
    ├── Process
    │   ├── History
    │   └── ProcessProfile
    ├── ProcessBoundary
    ├── TemporalRegion
    │   ├── ZeroDimensionalTemporalRegion
    │   └── OneDimensionalTemporalRegion
    └── SpatioTemporalRegion
```

::::

## Getting Help

```{admonition} Resources
:class: tip

- 📚 **Documentation**: You're reading it!
- 💬 **Issues**: [GitHub Issues](https://github.com/rasinj/neomodel_bfo/issues)
- 🌐 **BFO Specification**: [basic-formal-ontology.org](https://basic-formal-ontology.org)
- 🔧 **neomodel Docs**: [neomodel.readthedocs.io](https://neomodel.readthedocs.io)
```

## License

neomodel_bfo is released under the [MIT License](https://github.com/rasinj/neomodel_bfo/blob/master/LICENSE).

---

```{admonition} Ready to get started?
:class: seealso

Check out the {doc}`installation` guide and {doc}`usage` examples!
```
