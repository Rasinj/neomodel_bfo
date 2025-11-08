=====
Usage
=====

Basic Usage
-----------

To use neomodel_bfo in a project::

    from neomodel import config
    from neomodel_bfo import Object, Quality, Process, Function

    # Configure Neo4j connection
    config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'

    # Create entities
    organism = Object(name="E. coli").save()
    temp = Quality(name="Temperature", value="37", unit="°C").save()

    # Connect using BFO relationships
    temp.inheres_in.connect(organism)

Understanding BFO Classes
--------------------------

BFO divides entities into two main categories:

**Continuants** - Things that persist through time:

* ``Object`` - Material things (organisms, molecules, planets)
* ``Quality`` - Attributes (color, temperature, mass)
* ``Role`` - Context-dependent capacities (being a student)
* ``Function`` - Purposes (heart pumping blood)
* ``Disposition`` - Tendencies (fragility, solubility)

**Occurrents** - Things that unfold over time:

* ``Process`` - Activities (growth, chemical reactions)
* ``TemporalRegion`` - Periods of time
* ``SpatioTemporalRegion`` - Spacetime regions

Working with Relationships
---------------------------

BFO provides standard relationships::

    # Parthood
    cell.part_of.connect(organism)
    organism.has_part.all()  # Returns all parts

    # Inherence (qualities, roles, functions)
    quality.inheres_in.connect(object)
    object.bearer_of.all()  # Returns all qualities/roles/functions

    # Participation
    organism.participates_in.connect(process)
    process.has_participant.all()  # Returns participants

    # Realization
    process.realizes.connect(function)
    function.realized_by.all()  # Returns realizing processes

    # Spatial location
    object.occupies_spatial_region.connect(spatial_region)

    # Temporal existence
    continuant.exists_at.connect(temporal_region)
    occurrent.occurs_in.connect(temporal_region)

Extending BFO for Your Domain
------------------------------

Subclass BFO classes to create domain ontologies::

    from neomodel import StringProperty, IntegerProperty
    from neomodel_bfo import Object, Function, Process

    # Create domain classes
    class Organism(Object):
        species = StringProperty()
        age_years = IntegerProperty()

    class HeartFunction(Function):
        beats_per_minute = IntegerProperty()

    class Metabolism(Process):
        rate = StringProperty()

    # Use them with BFO relationships
    mouse = Organism(species="Mus musculus", age_years=2).save()
    heart_func = HeartFunction(beats_per_minute=600).save()
    heart_func.inheres_in.connect(mouse)

    metabolic_process = Metabolism(rate="high").save()
    mouse.participates_in.connect(metabolic_process)

Complete Examples
-----------------

See the ``examples/`` directory for complete working examples:

* ``biology_example.py`` - Organisms, anatomical structures, biological processes
* ``social_ontology_example.py`` - People, organizations, roles, social processes
* ``EXTENSION_GUIDE.md`` - Comprehensive guide to extending BFO

Querying the Graph
------------------

Use neomodel's traversal methods::

    # Get all qualities of an organism
    for quality in organism.bearer_of.all():
        print(f"{quality.name}: {quality.value} {quality.unit}")

    # Get all processes an entity participates in
    for process in organism.participates_in.all():
        print(f"Process: {process.name}")

    # Get all parts of an entity
    for part in organism.has_part.all():
        print(f"Part: {part.name}")

For complex queries, use Cypher::

    from neomodel import db

    # Find all parts recursively (transitive closure)
    results, meta = db.cypher_query(
        """
        MATCH (org:Object {uid: $uid})<-[:PART_OF*]-(part)
        RETURN part.name as name
        """,
        {'uid': organism.uid}
    )

    for record in results:
        print(f"Part: {record[0]}")

Best Practices
--------------

1. **Choose the right BFO class**: Objects for material things, Processes for activities, Qualities for attributes
2. **Use BFO relationships**: Don't create custom relationships when BFO provides them
3. **Document your choices**: Explain why you chose each BFO class for your domain entities
4. **Keep core pure**: Never modify ``bfo.py``; always extend via subclassing
5. **Leverage the graph**: Use Neo4j's traversal capabilities for complex queries

For more details, see the Extension Guide in the examples directory
