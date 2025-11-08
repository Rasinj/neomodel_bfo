"""
Example: Extending BFO for Biology - Modeling Organisms

This example shows how to extend neomodel_bfo to model biological organisms
with their parts, qualities, and processes while maintaining BFO compliance.

Pattern demonstrated:
- Subclassing BFO classes for domain entities
- Adding domain-specific properties
- Creating domain-specific relationships
- Using BFO relationships appropriately
"""

from neomodel import StringProperty, IntegerProperty, FloatProperty, RelationshipTo
from neomodel_bfo import (
    Object,
    FiatObjectPart,
    Quality,
    Function,
    Process,
    Role
)


# =============================================================================
# Domain Objects - Biological Entities
# =============================================================================

class Organism(Object):
    """
    A biological organism - extends BFO Object.

    Inherits from Object:
    - uid, name, description (from Entity)
    - part_of, has_part (mereology)
    - occupies_spatial_region (spatial location)
    - participates_in (process participation)
    - bearer_of (qualities and functions)

    Domain-specific additions:
    - species: taxonomic classification
    - age_years: current age
    """
    species = StringProperty(required=True)
    age_years = IntegerProperty()

    # Domain-specific relationships (in addition to BFO ones)
    offspring_of = RelationshipTo('Organism', 'OFFSPRING_OF')
    has_offspring = RelationshipFrom('Organism', 'OFFSPRING_OF')


class AnatomicalStructure(FiatObjectPart):
    """
    An anatomical part of an organism - extends BFO FiatObjectPart.

    Examples: heart, liver, brain, arm

    Inherits BFO relationships:
    - part_of (connects to Organism)
    - has_part (for sub-structures)
    - bearer_of (for functions and qualities)
    """
    anatomical_type = StringProperty()  # e.g., "organ", "tissue", "cell"

    # Domain relationship: which organism this is part of
    # (uses inherited part_of, but we can add domain-specific traversal helpers)


class Cell(Object):
    """
    A biological cell - extends BFO Object.

    Can be part of an organism or exist independently.
    """
    cell_type = StringProperty()  # e.g., "neuron", "epithelial", "muscle"


# =============================================================================
# Domain Qualities
# =============================================================================

class BodyTemperature(Quality):
    """
    Temperature of an organism - extends BFO Quality.

    Inherits:
    - inheres_in (the organism that has this temperature)
    - value, unit (from Quality)
    """
    pass  # Uses inherited value/unit properties

    # Example usage:
    # temp = BodyTemperature(
    #     name="Body temp of organism X",
    #     value="37.5",
    #     unit="°C"
    # ).save()
    # temp.inheres_in.connect(organism)


class BodyMass(Quality):
    """
    Mass of an organism - extends BFO Quality.
    """
    pass


# =============================================================================
# Domain Functions
# =============================================================================

class BiologicalFunction(Function):
    """
    A function that exists due to evolution - extends BFO Function.

    Inherits:
    - inheres_in (the anatomical structure that bears this function)
    - realized_by (the process that realizes this function)
    """
    function_category = StringProperty()  # e.g., "metabolic", "regulatory", "structural"


class HeartPumpingFunction(BiologicalFunction):
    """
    The function of the heart to pump blood.
    """
    pass


# =============================================================================
# Domain Processes
# =============================================================================

class BiologicalProcess(Process):
    """
    A biological process - extends BFO Process.

    Inherits:
    - has_participant (organisms/cells that participate)
    - realizes (functions being realized)
    - part_of (larger processes this is part of)
    - start_time, end_time
    """
    process_type = StringProperty()  # e.g., "metabolic", "developmental", "behavioral"


class CellDivision(BiologicalProcess):
    """
    Process of cell division (mitosis/meiosis).
    """
    division_type = StringProperty()  # "mitosis" or "meiosis"


class Growth(BiologicalProcess):
    """
    Process of an organism growing.
    """
    growth_rate_mm_per_day = FloatProperty()


# =============================================================================
# Domain Roles
# =============================================================================

class Predator(Role):
    """
    The role of being a predator in an ecosystem - extends BFO Role.

    Inherits:
    - inheres_in (the organism that bears this role)
    - realized_by (predation processes)
    """
    pass


class Prey(Role):
    """
    The role of being prey in an ecosystem.
    """
    pass


# =============================================================================
# Usage Example
# =============================================================================

def example_usage():
    """
    Demonstrates how to use the extended BFO classes to model a biological scenario.

    NOTE: This requires Neo4j connection to be configured via neomodel.config.
    """
    from neomodel import config

    # Configure Neo4j connection (example - adjust for your setup)
    # config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'

    # Create an organism
    mouse = Organism(
        name="Mickey Mouse",
        species="Mus musculus",
        age_years=2
    ).save()

    # Create an anatomical structure (heart)
    heart = AnatomicalStructure(
        name="Mickey's heart",
        anatomical_type="organ"
    ).save()

    # Connect: heart is part of mouse (using BFO part_of relationship)
    heart.part_of.connect(mouse)

    # Create a function that inheres in the heart
    pump_function = HeartPumpingFunction(
        name="Pumping function of Mickey's heart",
        function_category="circulatory"
    ).save()

    # Connect: function inheres in heart (using BFO inheres_in relationship)
    pump_function.inheres_in.connect(heart)

    # Create a quality of the organism
    body_temp = BodyTemperature(
        name="Mickey's body temperature",
        value="37.2",
        unit="°C"
    ).save()

    # Connect: quality inheres in organism
    body_temp.inheres_in.connect(mouse)

    # Create a process (heart beating)
    beating = BiologicalProcess(
        name="Mickey's heart beating",
        process_type="circulatory"
    ).save()

    # Connect: heart participates in the process
    heart.participates_in.connect(beating)

    # Connect: process realizes the pumping function
    beating.realizes.connect(pump_function)

    print(f"Created organism: {mouse.name}")
    print(f"  - Has part: {heart.name}")
    print(f"  - Heart has function: {pump_function.name}")
    print(f"  - Function realized by: {beating.name}")
    print(f"  - Has quality: {body_temp.name} = {body_temp.value} {body_temp.unit}")

    # Query examples
    print("\nQuery: All parts of the mouse")
    for part in mouse.has_part.all():
        print(f"  - {part.name}")

    print("\nQuery: All processes the heart participates in")
    for process in heart.participates_in.all():
        print(f"  - {process.name}")

    print("\nQuery: All functions realized by the beating process")
    for func in beating.realizes.all():
        print(f"  - {func.name}")


if __name__ == "__main__":
    # Uncomment to run (requires Neo4j setup)
    # example_usage()
    print("Biology example loaded. Configure Neo4j and call example_usage() to run.")
