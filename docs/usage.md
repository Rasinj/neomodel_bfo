# Usage Guide

```{contents} On this page
:local:
:depth: 2
```

## Quick Start

:::::{grid} 1 1 2 2
:gutter: 3

::::{grid-item-card} Install
:class-header: sd-bg-primary sd-text-white

```bash
pip install neomodel-bfo
```
::::

::::{grid-item-card} Configure
:class-header: sd-bg-primary sd-text-white

```python
from neomodel import config
config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'
```
::::

:::::

## Understanding BFO Classes

Basic Formal Ontology divides all entities into two fundamental categories:

::::{tab-set}

:::{tab-item} Continuants
Entities that **persist through time** and exist fully at any moment.

**Categories:**
- 🔷 **Object** - Material things (organisms, molecules, planets)
- 🎨 **Quality** - Attributes (color, temperature, mass)
- 🎭 **Role** - Context-dependent capacities (being a student)
- ⚙️ **Function** - Purposes (heart pumping blood)
- 💫 **Disposition** - Tendencies (fragility, solubility)

**Example:**
```python
from neomodel_bfo import Object, Quality

organism = Object(name="E. coli").save()
temp = Quality(name="Temperature", value="37", unit="°C").save()
```
:::

:::{tab-item} Occurrents
Entities that **unfold over time** and have temporal parts.

**Categories:**
- 🔄 **Process** - Activities (growth, chemical reactions)
- ⏱️ **TemporalRegion** - Periods of time
- 🌐 **SpatioTemporalRegion** - Spacetime regions

**Example:**
```python
from neomodel_bfo import Process

growth = Process(
    name="Cell division",
    start_time=datetime.now()
).save()
```
:::

::::

## Working with Relationships

BFO's power lies in its formal relationships between entities.

### Core BFO Relationships

::::{grid} 1 1 2 3
:gutter: 2

:::{grid-item-card} Parthood
:class-header: sd-bg-info sd-text-white

**Mereological relationships**

```python
# cell is part of organism
cell.part_of.connect(organism)

# Query all parts
for part in organism.has_part.all():
    print(part.name)
```
:::

:::{grid-item-card} Inherence
:class-header: sd-bg-success sd-text-white

**Qualities depend on bearers**

```python
# Quality inheres in object
temp.inheres_in.connect(organism)

# Query qualities
for quality in organism.bearer_of.all():
    print(f"{quality.value} {quality.unit}")
```
:::

:::{grid-item-card} Participation
:class-header: sd-bg-warning sd-text-white

**Objects participate in processes**

```python
# Organism participates in growth
organism.participates_in.connect(growth)

# Query participants
for participant in growth.has_participant.all():
    print(participant.name)
```
:::

::::

### Relationship Reference

```{list-table}
:header-rows: 1
:widths: 20 25 25 30

* - Relationship
  - Domain
  - Range
  - Meaning
* - `part_of`
  - Continuant/Occurrent
  - Same type
  - Mereological parthood
* - `inheres_in`
  - SpecificallyDependentContinuant
  - IndependentContinuant
  - Quality/Role inheres in bearer
* - `participates_in`
  - IndependentContinuant
  - Process
  - Entity participates in process
* - `realizes`
  - Process
  - RealizableEntity
  - Process realizes role/function
* - `exists_at`
  - Continuant
  - TemporalRegion
  - When entity exists
* - `occurs_in`
  - Occurrent
  - TemporalRegion
  - When event occurs
```

## Complete Examples

### Example 1: Biological Organism

```{admonition} Model an organism with parts, qualities, and processes
:class: tip

```python
from neomodel_bfo import Object, Quality, Process

# Create organism
organism = Object(name="E. coli K12").save()

# Add quality
temp = Quality(name="Temperature", value="37.0", unit="°C").save()
temp.inheres_in.connect(organism)

# Create process
growth = Process(name="Cell division").save()
organism.participates_in.connect(growth)

# Query: What are the organism's qualities?
for q in organism.bearer_of.all():
    print(f"{q.name}: {q.value} {q.unit}")
# Output: Temperature: 37.0 °C

# Query: What processes does the organism participate in?
for p in organism.participates_in.all():
    print(f"Process: {p.name}")
# Output: Process: Cell division
```
````

### Example 2: Function Realization

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} Step 1: Create entities
```python
from neomodel_bfo import Object, Function, Process

# Heart (object with function)
heart = Object(name="Heart").save()

# Pumping function
pump = Function(
    name="Pumping function"
).save()
```
:::

:::{grid-item-card} Step 2: Connect relationships
```python
# Function inheres in heart
pump.inheres_in.connect(heart)

# Beating process realizes function
beating = Process(name="Heartbeat").save()
beating.realizes.connect(pump)

# Heart participates in process
heart.participates_in.connect(beating)
```
:::

::::

```{seealso}
For domain-specific examples, see the [examples directory](https://github.com/rasinj/neomodel_bfo/tree/master/examples)
```

## Extending BFO for Your Domain

```{warning}
**Never modify `neomodel_bfo/bfo.py`** - Always extend via subclassing
```

### Creating Domain Classes

:::::{tab-set}

::::{tab-item} Simple Extension
Add domain-specific properties:

```python
from neomodel import StringProperty, IntegerProperty
from neomodel_bfo import Object

class Organism(Object):
    """Domain-specific organism."""
    species = StringProperty()
    age_years = IntegerProperty()

# Use with inherited BFO relationships
organism = Organism(species="E. coli", age_years=2).save()
```
::::

::::{tab-item} With Domain Relationships
Add both properties and relationships:

```python
from neomodel import RelationshipTo
from neomodel_bfo import Object

class Planet(Object):
    mass = FloatProperty()

    # BFO relationships inherited
    # Domain-specific relationship
    orbits = RelationshipTo('Star', 'ORBITS')

planet = Planet(name="Earth", mass=5.972e24).save()
planet.orbits.connect(sun)
```
::::

::::{tab-item} Multi-level Hierarchy
Create domain-specific hierarchies:

```python
class BiologicalEntity(Object):
    """Abstract base for biology."""
    __abstract_node__ = True
    species = StringProperty()

class Organism(BiologicalEntity):
    age_years = IntegerProperty()

class Cell(BiologicalEntity):
    cell_type = StringProperty()

# Both inherit BFO relationships + species property
```
::::

:::::

## Querying the Graph

### Basic Traversal

```python
# Get all qualities of an organism
for quality in organism.bearer_of.all():
    print(f"{quality.name}: {quality.value} {quality.unit}")

# Get all processes an entity participates in
for process in organism.participates_in.all():
    print(f"Process: {process.name}")

# Get all parts of an entity
for part in organism.has_part.all():
    print(f"Part: {part.name}")
```

### Advanced Queries with Cypher

For complex queries, use Cypher directly:

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} Transitive Parthood
:class-header: sd-bg-primary sd-text-white

Find all parts recursively (transitive closure):

```python
from neomodel import db

results, meta = db.cypher_query(
    """
    MATCH (org:Object {uid: $uid})<-[:PART_OF*]-(part)
    RETURN part.name as name
    """,
    {'uid': organism.uid}
)

for record in results:
    print(f"Part: {record[0]}")
```
:::

:::{grid-item-card} Path Queries
:class-header: sd-bg-primary sd-text-white

Find paths between entities:

```python
results, meta = db.cypher_query(
    """
    MATCH path = (start:Object {uid: $start_uid})
                 -[*..5]-
                 (end:Process {uid: $end_uid})
    RETURN path
    LIMIT 1
    """,
    {'start_uid': obj1.uid, 'end_uid': proc1.uid}
)
```
:::

::::

```{note}
Neo4j's graph algorithms can compute centrality, community detection, and other graph metrics on your BFO knowledge graph.
```

## Best Practices

::::{dropdown} ✅ Choose the Right BFO Class
:open:

Ask yourself:
- **Does it persist through time?** → Continuant
- **Does it unfold over time?** → Occurrent
- **Is it material?** → Object, MaterialEntity
- **Is it an attribute?** → Quality
- **Is it context-dependent?** → Role
- **Is it an evolved/designed purpose?** → Function
::::

::::{dropdown} ✅ Use BFO Relationships
Don't create custom relationships when BFO provides them:

```python
# ❌ Don't do this
organism.has_temperature.connect(temp)

# ✅ Do this instead
temp.inheres_in.connect(organism)
```
::::

::::{dropdown} ✅ Document Your Ontological Choices
Explain why you chose each BFO class:

```python
class Enzyme(Object):
    """
    A biological enzyme - extends BFO Object.

    BFO rationale: Enzymes are material entities (proteins)
    that exist in full at any time, making them Objects
    rather than Processes. The catalytic activity is
    modeled as a Function.
    """
    enzyme_class = StringProperty()
```
::::

## Next Steps

```{seealso}
**For Domain Developers:**
- 📖 [Extension Guide](https://github.com/rasinj/neomodel_bfo/blob/master/examples/EXTENSION_GUIDE.md) - Comprehensive patterns
- 🧬 [Biology Example](https://github.com/rasinj/neomodel_bfo/blob/master/examples/biology_example.py) - Organisms and processes
- 👥 [Social Ontology Example](https://github.com/rasinj/neomodel_bfo/blob/master/examples/social_ontology_example.py) - People and roles

**For Understanding BFO:**
- 📚 [BFO Specification](https://basic-formal-ontology.org)
- 🌐 [OBO Foundry](http://www.obofoundry.org) - BFO-based ontologies
```
