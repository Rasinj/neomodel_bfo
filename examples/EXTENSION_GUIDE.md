# Guide to Extending neomodel_bfo

This guide explains best practices for extending neomodel_bfo to create domain-specific ontologies while maintaining BFO compliance.

## Table of Contents

1. [Core Principles](#core-principles)
2. [Extension Patterns](#extension-patterns)
3. [Best Practices](#best-practices)
4. [Common Pitfalls](#common-pitfalls)
5. [Working with Relationships](#working-with-relationships)

---

## Core Principles

### 1. Don't Modify the Core

**Never edit `neomodel_bfo/bfo.py`** for domain-specific extensions. The BFO core should remain pure and reusable across all domains.

✅ **Good:**
```python
from neomodel_bfo import Object

class Organism(Object):
    species = StringProperty()
```

❌ **Bad:**
```python
# Don't add domain properties to bfo.py
class Object(MaterialEntity):
    species = StringProperty()  # Wrong!
```

### 2. Subclass Appropriately

Choose the correct BFO class to extend based on ontological principles:

- **Objects** → Material entities (cells, organisms, planets, chairs)
- **Processes** → Things that unfold over time (growth, chemical reactions)
- **Qualities** → Attributes that inhere in entities (color, temperature, mass)
- **Roles** → Context-dependent capacities (being a student, being a parent)
- **Functions** → Evolved or designed purposes (heart pumping, knife cutting)
- **Dispositions** → Tendencies or capabilities (fragility, solubility)

### 3. Use BFO Relationships

BFO provides standard relationships that should be used appropriately:

| Relationship | Domain | Range | Meaning |
|--------------|--------|-------|---------|
| `part_of` | Continuant/Occurrent | Continuant/Occurrent | Mereological parthood |
| `inheres_in` | SpecificallyDependentContinuant | IndependentContinuant | Quality/Role inheres in bearer |
| `participates_in` | IndependentContinuant | Process | Entity participates in process |
| `realizes` | Process | RealizableEntity | Process realizes role/function |
| `occupies_spatial_region` | Continuant | SpatialRegion | Spatial location |
| `exists_at` | Continuant | TemporalRegion | Temporal existence |
| `occurs_in` | Occurrent | TemporalRegion | Temporal occurrence |

---

## Extension Patterns

### Pattern 1: Simple Property Extension

Add domain-specific properties to BFO classes:

```python
from neomodel import StringProperty, FloatProperty
from neomodel_bfo import Object

class Star(Object):
    """A celestial star - extends BFO Object."""
    spectral_type = StringProperty()  # e.g., "G2V"
    mass_solar_masses = FloatProperty()
    temperature_kelvin = FloatProperty()
```

### Pattern 2: Domain-Specific Relationships

Add relationships specific to your domain alongside BFO relationships:

```python
from neomodel import RelationshipTo
from neomodel_bfo import Object

class Planet(Object):
    """A planet."""
    # BFO relationships are inherited:
    # - part_of (solar system)
    # - occupies_spatial_region
    # - participates_in (orbital processes)

    # Domain-specific relationships:
    orbits = RelationshipTo('Star', 'ORBITS')
    has_satellite = RelationshipFrom('Moon', 'ORBITS')
```

### Pattern 3: Abstract Domain Base Classes

Create abstract base classes for your domain that extend BFO:

```python
from neomodel_bfo import Object, Process, Quality

class BiologicalEntity(Object):
    """Abstract base for all biological entities."""
    __abstract_node__ = True
    species = StringProperty()

class Organism(BiologicalEntity):
    """A living organism."""
    age_years = IntegerProperty()

class Cell(BiologicalEntity):
    """A biological cell."""
    cell_type = StringProperty()
```

### Pattern 4: Composite Extensions

Combine multiple BFO concepts for complex domain models:

```python
from neomodel_bfo import Object, Quality, Process, Role

class Hospital(Object):
    """A hospital building."""
    capacity = IntegerProperty()

class Patient(Object):
    """A person."""
    pass

class PatientRole(Role):
    """The role of being a patient."""
    admission_date = DateTimeProperty()

class Treatment(Process):
    """Medical treatment process."""
    treatment_type = StringProperty()

# Usage:
# patient_role.inheres_in.connect(person)
# treatment.realizes.connect(patient_role)
# treatment.has_participant.connect(hospital)
```

---

## Best Practices

### 1. Maintain Ontological Coherence

**Ask yourself:** Is this entity truly an Object, or is it a Quality/Role/Process?

- ✅ `class Organism(Object)` - Yes, organisms are material objects
- ✅ `class Temperature(Quality)` - Yes, temperature is a quality
- ❌ `class Being_Red(Object)` - No, this should be a Quality
- ❌ `class Running(Object)` - No, this should be a Process

### 2. Document Your Extensions

Provide clear docstrings explaining:
- What BFO class you're extending
- Why this is the appropriate parent class
- What the entity represents in your domain
- Examples

```python
class Enzyme(Object):
    """
    A biological enzyme - extends BFO Object.

    BFO rationale: Enzymes are material entities (proteins) that
    exist in full at any time, making them Objects rather than Processes.

    The catalytic activity of an enzyme is modeled as a Function that
    inheres in the enzyme and is realized by enzymatic processes.

    Examples: DNA polymerase, amylase, lactase
    """
    enzyme_class = StringProperty()
```

### 3. Use Relationship Semantics Correctly

```python
# ✅ Correct: Quality inheres in Object
temperature = Temperature(value="37.5", unit="°C").save()
temperature.inheres_in.connect(organism)

# ✅ Correct: Object participates in Process
organism.participates_in.connect(growth_process)

# ✅ Correct: Process realizes Function
metabolism.realizes.connect(metabolic_function)

# ❌ Wrong: Don't make up relationships when BFO provides them
# Don't do: organism.has_temperature.connect(temperature)
# Use instead: temperature.inheres_in.connect(organism)
```

### 4. Leverage Graph Queries

Take advantage of Neo4j's graph traversal for powerful queries:

```python
# Find all processes an organism participates in
processes = organism.participates_in.all()

# Find all qualities of an organism
qualities = organism.bearer_of.all()

# Find all parts of an organism recursively
# (requires custom Cypher query for transitive closure)
from neomodel import db

results, meta = db.cypher_query(
    """
    MATCH (org:Organism {uid: $uid})<-[:PART_OF*]-(part)
    RETURN part
    """,
    {'uid': organism.uid}
)
```

### 5. Keep Properties Domain-Specific

Add properties that make sense for your domain, not generic BFO properties:

```python
class Gene(GenericallyDependentContinuant):
    """A gene sequence."""
    sequence = StringProperty()  # Domain-specific
    chromosome = StringProperty()  # Domain-specific
    start_position = IntegerProperty()  # Domain-specific

    # Don't add generic properties like:
    # color = StringProperty()  # Irrelevant to genes
```

---

## Common Pitfalls

### Pitfall 1: Confusing Objects with Processes

```python
# ❌ Wrong: Running is a process, not an object
class Running(Object):
    pass

# ✅ Correct:
class RunningProcess(Process):
    speed_km_per_hour = FloatProperty()
```

### Pitfall 2: Not Using Inherence for Qualities

```python
# ❌ Wrong: Don't create direct relationships for qualities
class Organism(Object):
    has_color = RelationshipTo('Color', 'HAS_COLOR')

# ✅ Correct: Qualities inhere in their bearers
class Color(Quality):
    pass  # Uses inherited inheres_in relationship

# Usage:
color = Color(value="red").save()
color.inheres_in.connect(organism)  # BFO standard
```

### Pitfall 3: Mixing Temporal Snapshots with Processes

```python
# ❌ Confused: Don't mix continuant and occurrent concepts
class OrganismAtTime(Object):
    time = DateTimeProperty()

# ✅ Correct: Use exists_at relationship
organism = Organism(...).save()
time_point = ZeroDimensionalTemporalRegion(
    temporal_start=datetime.now()
).save()
organism.exists_at.connect(time_point)
```

### Pitfall 4: Creating Too Many Relationship Types

```python
# ❌ Over-engineered: Too many custom relationships
class Person(Object):
    has_age = RelationshipTo('Age', 'HAS_AGE')
    has_height = RelationshipTo('Height', 'HAS_HEIGHT')
    has_weight = RelationshipTo('Weight', 'HAS_WEIGHT')

# ✅ Better: Use BFO bearer_of + Quality subclasses
class Age(Quality):
    pass
class Height(Quality):
    pass
class Weight(Quality):
    pass

# All use: quality.inheres_in.connect(person)
```

---

## Working with Relationships

### Bidirectional Relationships

BFO relationships are bidirectional via `RelationshipTo` and `RelationshipFrom`:

```python
# From the Continuant side
organism.part_of.connect(population)

# From the reverse side
population.has_part.all()  # Returns organism

# Both work because has_part is RelationshipFrom('Continuant', 'PART_OF')
```

### Cardinality

All BFO relationships use `ZeroOrMore` cardinality by default (no enforcement), allowing flexibility:

```python
# An organism can have multiple qualities
organism.bearer_of.all()  # Returns [color, mass, temperature, ...]

# A quality can inhere in multiple bearers (e.g., RelationalQuality)
distance_quality.inheres_in.all()  # Could return [city1, city2]
```

### Custom Relationship Properties

You can add properties to relationships if needed:

```python
from neomodel import StructuredRel

class ParticipatesInRel(StructuredRel):
    """Custom relationship with properties."""
    role_in_process = StringProperty()
    start_participation = DateTimeProperty()

class CustomProcess(Process):
    has_participant = RelationshipFrom(
        'IndependentContinuant',
        'PARTICIPATES_IN',
        model=ParticipatesInRel
    )

# Usage:
process.has_participant.connect(organism, {
    'role_in_process': 'catalyst',
    'start_participation': datetime.now()
})
```

---

## Summary

**Golden Rules:**
1. ✅ Extend BFO classes via subclassing
2. ✅ Use BFO relationships appropriately
3. ✅ Add domain properties and relationships as needed
4. ✅ Document your ontological choices
5. ❌ Never modify the core BFO classes
6. ❌ Don't create custom relationships when BFO provides them
7. ❌ Ensure ontological coherence (right entity type for the concept)

**Resources:**
- BFO 2.0 Specification: https://basic-formal-ontology.org/
- Example extensions: See `biology_example.py` and `social_ontology_example.py`
- Neomodel documentation: https://neomodel.readthedocs.io/
