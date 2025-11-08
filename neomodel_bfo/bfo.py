"""
BFO 2.0 (Basic Formal Ontology) implementation for neomodel/Neo4j.

This module provides a complete class hierarchy representing BFO 2.0 entities
with their standard relationships and properties. It is designed to be extended
by domain-specific ontologies while keeping the core BFO structure intact.

For extensibility patterns, see the examples directory.
"""

from neomodel import (
    StructuredNode,
    StringProperty,
    UniqueIdProperty,
    DateTimeProperty,
    FloatProperty,
    JSONProperty,
    RelationshipTo,
    RelationshipFrom,
    ZeroOrMore,
    ZeroOrOne
)


# =============================================================================
# BASE ENTITY
# =============================================================================

class Entity(StructuredNode):
    """
    BFO:0000001 - Entity

    The root class of all BFO entities. An entity is anything that exists or
    has existed or will exist.

    BFO distinguishes between:
    - Continuants: entities that persist through time (objects, qualities)
    - Occurrents: entities that unfold over time (processes, events)

    Properties:
        uid: Unique identifier for this entity
        name: Human-readable name/label
        description: Detailed description of this entity
        created_at: Timestamp when this entity was created in the database
        modified_at: Timestamp when this entity was last modified
    """
    __abstract_node__ = True

    uid = UniqueIdProperty()
    name = StringProperty(unique_index=False)
    description = StringProperty()
    created_at = DateTimeProperty(default_now=True)
    modified_at = DateTimeProperty(default_now=True)


# =============================================================================
# CONTINUANTS - Entities that persist through time
# =============================================================================

class Continuant(Entity):
    """
    BFO:0000002 - Continuant

    An entity that exists in full at any time in which it exists at all,
    persists through time while maintaining its identity and has no temporal
    parts.

    Examples: an organism, a molecule, a quality, a function

    BFO Relations:
        - exists_at: connects to temporal regions when this continuant exists
        - part_of: mereological parthood to another continuant
        - has_part: inverse of part_of
        - located_in: spatial location relationship
        - occupies_spatial_region: the spatial region this continuant occupies
    """
    __abstract_node__ = True

    # Temporal relationships
    exists_at = RelationshipTo('.TemporalRegion', 'EXISTS_AT', cardinality=ZeroOrMore)

    # Mereological (parthood) relationships
    part_of = RelationshipTo('Continuant', 'PART_OF', cardinality=ZeroOrMore)
    has_part = RelationshipFrom('Continuant', 'PART_OF', cardinality=ZeroOrMore)

    # Spatial relationships
    located_in = RelationshipTo('Continuant', 'LOCATED_IN', cardinality=ZeroOrMore)
    occupies_spatial_region = RelationshipTo('.SpatialRegion', 'OCCUPIES_SPATIAL_REGION',
                                             cardinality=ZeroOrMore)


class IndependentContinuant(Continuant):
    """
    BFO:0000004 - Independent Continuant

    A continuant that is a bearer of qualities and realizable entities, in
    which other entities inhere and which itself cannot inhere in anything.

    Examples: an organism, a molecule, a planet, a chair

    BFO Relations:
        - bearer_of: has qualities, roles, dispositions, or functions that inhere in it
        - participates_in: participates in processes
    """
    __abstract_node__ = True

    # Inherence relationships (has qualities, roles, dispositions)
    bearer_of = RelationshipFrom('.SpecificallyDependentContinuant', 'INHERES_IN',
                                 cardinality=ZeroOrMore)

    # Participation in processes
    participates_in = RelationshipTo('.Process', 'PARTICIPATES_IN', cardinality=ZeroOrMore)


# =============================================================================
# MATERIAL ENTITIES - Physical objects and their parts
# =============================================================================

class MaterialEntity(IndependentContinuant):
    """
    BFO:0000040 - Material Entity

    An independent continuant that has some portion of matter as proper or
    improper continuant part.

    Examples: a cell, an organism, a planet, a chair, a portion of blood

    Properties:
        mass_kg: Mass in kilograms (optional)
    """
    __abstract_node__ = True

    mass_kg = FloatProperty()


class Object(MaterialEntity):
    """
    BFO:0000030 - Object

    A material entity that is spatially extended, maximally self-connected,
    and self-contained (the parts of an object are not separated by spatial gaps).

    Examples: a cell, an organism, a planet, a chair
    """
    pass


class FiatObjectPart(MaterialEntity):
    """
    BFO:0000024 - Fiat Object Part

    A material entity that is part of an object but not demarcated by any
    physical discontinuity.

    Examples: the upper half of an apple, the North side of a building,
    the handle of a coffee mug
    """
    pass


class ObjectAggregate(MaterialEntity):
    """
    BFO:0000027 - Object Aggregate

    A material entity that is a mereological sum of separate objects and
    possesses non-connected boundaries.

    Examples: a collection of cells, a pile of rocks, a fleet of cars,
    a population of organisms
    """
    pass


# =============================================================================
# IMMATERIAL ENTITIES - Sites, boundaries, and spatial regions
# =============================================================================

class ImmaterialEntity(IndependentContinuant):
    """
    BFO:0000141 - Immaterial Entity

    An independent continuant that has no material entities as parts.

    Examples: a hole in a piece of cheese, the interior of a box, a surface,
    a spatial region
    """
    __abstract_node__ = True


class Site(ImmaterialEntity):
    """
    BFO:0000029 - Site

    An immaterial entity that is a three-dimensional immaterial part (or
    occupant) of some material entity.

    Examples: the interior of your bedroom, a hole in a piece of cheese,
    the cockpit of an aircraft
    """
    pass


class ContinuantFiatBoundary(ImmaterialEntity):
    """
    BFO:0000140 - Continuant Fiat Boundary

    An immaterial entity that is of zero, one or two dimensions and does not
    include a spatial region as part.

    Examples: the plane separating air from a water surface, the border
    between France and Belgium
    """
    __abstract_node__ = True


class ZeroDimensionalContinuantFiatBoundary(ContinuantFiatBoundary):
    """
    BFO:0000147 - Zero-Dimensional Continuant Fiat Boundary

    A continuant fiat boundary of zero dimensions (a point).

    Examples: the geographic point at the center of a city
    """
    pass


class OneDimensionalContinuantFiatBoundary(ContinuantFiatBoundary):
    """
    BFO:0000142 - One-Dimensional Continuant Fiat Boundary

    A continuant fiat boundary of one dimension (a line).

    Examples: the international date line, the edge of a table
    """
    pass


class TwoDimensionalContinuantFiatBoundary(ContinuantFiatBoundary):
    """
    BFO:0000146 - Two-Dimensional Continuant Fiat Boundary

    A continuant fiat boundary of two dimensions (a surface).

    Examples: the surface of the earth, the boundary between France and Belgium
    """
    pass


# =============================================================================
# SPATIAL REGIONS - Space itself
# =============================================================================

class SpatialRegion(ImmaterialEntity):
    """
    BFO:0000006 - Spatial Region

    An immaterial entity whose location is a space or spatial region and which
    is not a quality.

    Examples: the region of space occupied by your body, the region of space
    occupied by a particular atom

    Properties:
        coordinates: JSON structure for storing spatial data (lat/lng, x/y/z, WKT, etc.)
        coordinate_system: Description of the coordinate reference system used
    """
    __abstract_node__ = True

    coordinates = JSONProperty()
    coordinate_system = StringProperty()

    # Spatial regions can contain other spatial regions
    spatially_contains = RelationshipTo('SpatialRegion', 'SPATIALLY_CONTAINS',
                                        cardinality=ZeroOrMore)
    spatially_contained_in = RelationshipFrom('SpatialRegion', 'SPATIALLY_CONTAINS',
                                              cardinality=ZeroOrMore)


class ZeroDimensionalSpatialRegion(SpatialRegion):
    """
    BFO:0000018 - Zero-Dimensional Spatial Region

    A spatial region of zero dimensions (a point in space).

    Examples: a point in Cartesian space
    """
    pass


class OneDimensionalSpatialRegion(SpatialRegion):
    """
    BFO:0000026 - One-Dimensional Spatial Region

    A spatial region of one dimension (a line in space).

    Examples: a trajectory path
    """
    pass


class TwoDimensionalSpatialRegion(SpatialRegion):
    """
    BFO:0000009 - Two-Dimensional Spatial Region

    A spatial region of two dimensions (a surface in space).

    Examples: the spatial region on the surface of the earth
    """
    pass


class ThreeDimensionalSpatialRegion(SpatialRegion):
    """
    BFO:0000028 - Three-Dimensional Spatial Region

    A spatial region of three dimensions (a volume in space).

    Examples: the spatial region occupied by a cube of air
    """
    pass


# =============================================================================
# DEPENDENT CONTINUANTS - Entities that depend on other entities
# =============================================================================

class GenericallyDependentContinuant(Continuant):
    """
    BFO:0000031 - Generically Dependent Continuant

    A continuant that is dependent on one or more other entities but can be
    concretized in multiple bearers.

    Examples: the pattern in a coloring book, the information content of a
    gene sequence, the pdf file stored on your computer, a recipe
    """
    pass


class SpecificallyDependentContinuant(Continuant):
    """
    BFO:0000020 - Specifically Dependent Continuant

    A continuant that inheres in or is borne by other entities and cannot
    exist without its bearer.

    Examples: a particular shape, color, or temperature of an object; the
    role of being a teacher; the function of the heart

    BFO Relations:
        - inheres_in: the independent continuant this entity inheres in (its bearer)
    """
    __abstract_node__ = True

    inheres_in = RelationshipTo('.IndependentContinuant', 'INHERES_IN',
                                cardinality=ZeroOrMore)


class Quality(SpecificallyDependentContinuant):
    """
    BFO:0000019 - Quality

    A specifically dependent continuant that is exhibited if it inheres in an
    entity or entities at all.

    Examples: the color of a tomato, the ambient temperature of a room,
    the shape of your nose, the mass of a molecule

    Properties:
        value: The measured or observed value of this quality
        unit: The unit of measurement (kg, m, °C, etc.)
    """
    __abstract_node__ = True

    value = StringProperty()  # Can store numeric or categorical values
    unit = StringProperty()


class RelationalQuality(Quality):
    """
    BFO:0000145 - Relational Quality

    A quality that inheres in an entity and requires multiple entities to
    be instantiated.

    Examples: the marriage bond between two people, the distance between
    two cities, being a sibling
    """
    pass


class RealizableEntity(SpecificallyDependentContinuant):
    """
    BFO:0000017 - Realizable Entity

    A specifically dependent continuant that can be realized in a process.

    Examples: a role of being a student, a disposition to dissolve in water,
    the function of the heart to pump blood

    BFO Relations:
        - realized_by: the process that realizes this realizable entity
    """
    __abstract_node__ = True

    realized_by = RelationshipFrom('.Process', 'REALIZES', cardinality=ZeroOrMore)


class Role(RealizableEntity):
    """
    BFO:0000023 - Role

    A realizable entity that exists because the bearer is in some special
    physical, social, or institutional context.

    Examples: the role of being a student, the role of being a parent,
    the role of a chemical catalyst
    """
    pass


class Disposition(RealizableEntity):
    """
    BFO:0000016 - Disposition

    A realizable entity that is such that if it exists then it is in virtue
    of the bearer's physical make-up and this physical make-up is something
    that could exist even if it is never realized.

    Examples: the disposition of a vase to break when dropped, the disposition
    of salt to dissolve in water, the disposition of a person to bleed when cut
    """
    pass


class Function(Disposition):
    """
    BFO:0000034 - Function

    A disposition that exists in virtue of the bearer's physical make-up and
    this physical make-up is something the bearer possesses because it came
    into being through evolution (in the case of natural biological entities)
    or through intentional design (in the case of artifacts).

    Examples: the function of the heart to pump blood, the function of a knife
    to cut, the function of a gene to encode a protein
    """
    pass


# =============================================================================
# OCCURRENTS - Entities that unfold over time
# =============================================================================

class Occurrent(Entity):
    """
    BFO:0000003 - Occurrent

    An entity that has temporal parts and unfolds itself in time. Occurrents
    exist only when they are occurring.

    Examples: a process of cell division, a person's life, a temporal interval,
    a region of spacetime

    Properties:
        start_time: When this occurrent begins
        end_time: When this occurrent ends

    BFO Relations:
        - occurs_in: temporal region during which this occurs
        - part_of: temporal parthood (earlier phases are parts of later processes)
        - has_part: inverse of part_of for occurrents
    """
    __abstract_node__ = True

    start_time = DateTimeProperty()
    end_time = DateTimeProperty()

    # Temporal relationships
    occurs_in = RelationshipTo('.TemporalRegion', 'OCCURS_IN', cardinality=ZeroOrMore)

    # Mereological relationships for occurrents
    part_of = RelationshipTo('Occurrent', 'PART_OF', cardinality=ZeroOrMore)
    has_part = RelationshipFrom('Occurrent', 'PART_OF', cardinality=ZeroOrMore)


class Process(Occurrent):
    """
    BFO:0000015 - Process

    An occurrent that has some temporal proper part, has no spatial location,
    and depends on some material entity.

    Examples: cell division, a heart beating, walking to the store, the process
    of metabolism, a chemical reaction

    BFO Relations:
        - has_participant: independent continuants that participate in this process
        - realizes: realizable entities (roles, functions, dispositions) realized by this process
        - has_process_boundary: start and end boundaries of this process
        - preceded_by: temporal ordering of processes
        - precedes: inverse of preceded_by
    """
    __abstract_node__ = True

    # Participation relationships
    has_participant = RelationshipFrom('.IndependentContinuant', 'PARTICIPATES_IN',
                                       cardinality=ZeroOrMore)

    # Realization relationships
    realizes = RelationshipTo('.RealizableEntity', 'REALIZES', cardinality=ZeroOrMore)

    # Process boundaries
    has_process_boundary = RelationshipTo('.ProcessBoundary', 'HAS_PROCESS_BOUNDARY',
                                          cardinality=ZeroOrMore)

    # Temporal ordering
    preceded_by = RelationshipFrom('Process', 'PRECEDES', cardinality=ZeroOrMore)
    precedes = RelationshipTo('Process', 'PRECEDES', cardinality=ZeroOrMore)


class History(Process):
    """
    BFO:0000182 - History

    A process that is the sum of the totality of processes occurring in the
    spatiotemporal region occupied by a material entity or site.

    Examples: the life of an organism, the history of a planet, the complete
    career of a person
    """
    pass


class ProcessProfile(Process):
    """
    BFO:0000144 - Process Profile

    A process that is the answer to a 'how-question' about a process.

    Examples: the velocity of a moving object, the rate of a chemical reaction,
    the intensity of a pain over time
    """
    pass


class ProcessBoundary(Occurrent):
    """
    BFO:0000035 - Process Boundary

    A zero-dimensional temporal region that is the boundary of a process.

    Examples: the moment of birth, the moment of death, the start of a race,
    the endpoint of a chemical reaction
    """
    pass


# =============================================================================
# TEMPORAL REGIONS - Time itself
# =============================================================================

class TemporalRegion(Occurrent):
    """
    BFO:0000008 - Temporal Region

    An occurrent over which processes can unfold.

    Examples: the temporal region during WWII, the moment of the big bang,
    the temporal region occupied by your reading of this text

    Properties:
        temporal_start: Start point of this temporal region
        temporal_end: End point of this temporal region
    """
    __abstract_node__ = True

    temporal_start = DateTimeProperty()
    temporal_end = DateTimeProperty()

    # Temporal regions can contain other temporal regions
    temporally_contains = RelationshipTo('TemporalRegion', 'TEMPORALLY_CONTAINS',
                                         cardinality=ZeroOrMore)
    temporally_contained_in = RelationshipFrom('TemporalRegion', 'TEMPORALLY_CONTAINS',
                                               cardinality=ZeroOrMore)


class ZeroDimensionalTemporalRegion(TemporalRegion):
    """
    BFO:0000148 - Zero-Dimensional Temporal Region

    A temporal region that is a temporal instant (a point in time).

    Examples: the moment of your birth, the moment the light switch was flipped,
    midnight on January 1, 2000
    """
    pass


class OneDimensionalTemporalRegion(TemporalRegion):
    """
    BFO:0000038 - One-Dimensional Temporal Region

    A temporal region that is a temporal interval (has duration).

    Examples: the temporal region from 9am to 5pm, the duration of WWII,
    the first year of a person's life
    """
    pass


class SpatioTemporalRegion(Occurrent):
    """
    BFO:0000011 - Spatiotemporal Region

    An occurrent at or in which processual entities can be located.

    Examples: the spatiotemporal region occupied by a process of cellular
    meiosis, the spatiotemporal region occupied by a football match

    Properties:
        spatial_extent: JSON for storing spatial information
        temporal_extent: Description of temporal bounds
    """
    spatial_extent = JSONProperty()
    temporal_extent = StringProperty()


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    # Base
    'Entity',
    # Continuants
    'Continuant',
    'IndependentContinuant',
    'MaterialEntity',
    'Object',
    'FiatObjectPart',
    'ObjectAggregate',
    'ImmaterialEntity',
    'Site',
    'ContinuantFiatBoundary',
    'ZeroDimensionalContinuantFiatBoundary',
    'OneDimensionalContinuantFiatBoundary',
    'TwoDimensionalContinuantFiatBoundary',
    'SpatialRegion',
    'ZeroDimensionalSpatialRegion',
    'OneDimensionalSpatialRegion',
    'TwoDimensionalSpatialRegion',
    'ThreeDimensionalSpatialRegion',
    'GenericallyDependentContinuant',
    'SpecificallyDependentContinuant',
    'Quality',
    'RelationalQuality',
    'RealizableEntity',
    'Role',
    'Disposition',
    'Function',
    # Occurrents
    'Occurrent',
    'Process',
    'History',
    'ProcessProfile',
    'ProcessBoundary',
    'TemporalRegion',
    'ZeroDimensionalTemporalRegion',
    'OneDimensionalTemporalRegion',
    'SpatioTemporalRegion',
]


if __name__ == '__main__':
    pass
