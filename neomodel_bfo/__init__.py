"""Top-level package for neomodel_bfo."""

__author__ = """Olle Nordesjo"""
__email__ = 'olle.nordesjo@gmail.com'
__version__ = '0.1.0'

# Import all BFO classes for convenient access
from neomodel_bfo.bfo import (
    # Base
    Entity,
    # Continuants
    Continuant,
    IndependentContinuant,
    MaterialEntity,
    Object,
    FiatObjectPart,
    ObjectAggregate,
    ImmaterialEntity,
    Site,
    ContinuantFiatBoundary,
    ZeroDimensionalContinuantFiatBoundary,
    OneDimensionalContinuantFiatBoundary,
    TwoDimensionalContinuantFiatBoundary,
    SpatialRegion,
    ZeroDimensionalSpatialRegion,
    OneDimensionalSpatialRegion,
    TwoDimensionalSpatialRegion,
    ThreeDimensionalSpatialRegion,
    GenericallyDependentContinuant,
    SpecificallyDependentContinuant,
    Quality,
    RelationalQuality,
    RealizableEntity,
    Role,
    Disposition,
    Function,
    # Occurrents
    Occurrent,
    Process,
    History,
    ProcessProfile,
    ProcessBoundary,
    TemporalRegion,
    ZeroDimensionalTemporalRegion,
    OneDimensionalTemporalRegion,
    SpatioTemporalRegion,
)

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
