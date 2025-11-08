# neomodel_bfo Examples

This directory contains examples demonstrating how to extend neomodel_bfo for domain-specific ontologies while maintaining BFO compliance.

## Files

### Extension Guide
- **[EXTENSION_GUIDE.md](EXTENSION_GUIDE.md)** - Comprehensive guide to extending BFO
  - Core principles for clean extensions
  - Common patterns and best practices
  - Pitfalls to avoid
  - Relationship usage guidelines

### Example Implementations

- **[biology_example.py](biology_example.py)** - Biological domain ontology
  - Models organisms, anatomical structures, cells
  - Shows biological processes, functions, and qualities
  - Demonstrates parthood, inherence, and realization relationships

- **[social_ontology_example.py](social_ontology_example.py)** - Social/institutional ontology
  - Models persons, organizations, roles
  - Shows social processes and information entities
  - Demonstrates multiple roles per person
  - Example of teaching scenario with teacher and student roles

## Quick Start

1. **Read the Extension Guide first**: [EXTENSION_GUIDE.md](EXTENSION_GUIDE.md)

2. **Study the examples**:
   - Start with `biology_example.py` for a straightforward material entity example
   - Move to `social_ontology_example.py` for more complex role-based modeling

3. **Run the examples** (requires Neo4j):
   ```python
   from neomodel import config
   from examples.biology_example import example_usage

   # Configure your Neo4j connection
   config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'

   # Run the example
   example_usage()
   ```

## Key Patterns Demonstrated

### 1. Property Extension
```python
from neomodel_bfo import Object

class Organism(Object):
    species = StringProperty()
    age_years = IntegerProperty()
```

### 2. Using BFO Relationships
```python
# Quality inheres in Object
temperature.inheres_in.connect(organism)

# Object participates in Process
organism.participates_in.connect(growth_process)

# Process realizes Function
process.realizes.connect(heart_function)
```

### 3. Domain-Specific Relationships
```python
class Person(Object):
    # BFO relationships inherited
    # Add domain-specific relationships
    employed_by = RelationshipTo('Organization', 'EMPLOYED_BY')
```

### 4. Multiple Entity Types Working Together
```python
# Create a heart (anatomical structure)
heart = AnatomicalStructure(name="Heart").save()

# Create a function that inheres in the heart
pump_function = HeartPumpingFunction(name="Pumping").save()
pump_function.inheres_in.connect(heart)

# Create a process that realizes the function
beating = BiologicalProcess(name="Beating").save()
beating.realizes.connect(pump_function)
```

## Neo4j Setup

To run these examples, you need:

1. **Neo4j installed and running**
   ```bash
   # Using Docker
   docker run -p 7474:7474 -p 7687:7687 \
     -e NEO4J_AUTH=neo4j/password \
     neo4j:latest
   ```

2. **neomodel_bfo installed**
   ```bash
   pip install -e /path/to/neomodel_bfo
   ```

3. **Configuration in your code**
   ```python
   from neomodel import config
   config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'
   ```

## Design Principles

These examples follow core BFO principles:

- **Realism**: Entities represent real-world things, not concepts or words
- **Clarity**: Clear definitions and documented ontological choices
- **Coherence**: Consistent use of BFO categories and relationships
- **Extensibility**: Core BFO remains pure; all domain specifics are subclasses

## Next Steps

After studying these examples:

1. Identify the entities in your domain
2. Map them to appropriate BFO classes
3. Define domain-specific properties
4. Use BFO relationships where appropriate
5. Add domain-specific relationships as needed
6. Document your ontological choices

## Resources

- **BFO 2.0 Specification**: https://basic-formal-ontology.org/
- **neomodel Documentation**: https://neomodel.readthedocs.io/
- **Neo4j Cypher Guide**: https://neo4j.com/docs/cypher-manual/current/
- **OBO Foundry** (BFO-based ontologies): http://www.obofoundry.org/
