"""
Tests for BFO class hierarchy and structure.

These tests verify the class hierarchy, properties, and relationships
are correctly defined without requiring a Neo4j connection.
"""

import pytest
from neomodel_bfo import (
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
    SpatialRegion,
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
    SpatioTemporalRegion,
)


class TestBFOImports:
    """Test that all BFO classes can be imported."""

    def test_entity_import(self):
        """Test Entity class is importable."""
        assert Entity is not None

    def test_continuant_imports(self):
        """Test all Continuant classes are importable."""
        assert Continuant is not None
        assert IndependentContinuant is not None
        assert MaterialEntity is not None
        assert Object is not None

    def test_occurrent_imports(self):
        """Test all Occurrent classes are importable."""
        assert Occurrent is not None
        assert Process is not None
        assert TemporalRegion is not None


class TestBFOHierarchy:
    """Test the BFO class hierarchy is correct."""

    def test_continuant_hierarchy(self):
        """Test Continuant inheritance chain."""
        assert issubclass(Continuant, Entity)
        assert issubclass(IndependentContinuant, Continuant)
        assert issubclass(MaterialEntity, IndependentContinuant)
        assert issubclass(Object, MaterialEntity)

    def test_quality_hierarchy(self):
        """Test Quality inheritance chain."""
        assert issubclass(SpecificallyDependentContinuant, Continuant)
        assert issubclass(Quality, SpecificallyDependentContinuant)
        assert issubclass(RelationalQuality, Quality)

    def test_realizable_entity_hierarchy(self):
        """Test RealizableEntity inheritance chain."""
        assert issubclass(RealizableEntity, SpecificallyDependentContinuant)
        assert issubclass(Role, RealizableEntity)
        assert issubclass(Disposition, RealizableEntity)
        assert issubclass(Function, Disposition)

    def test_occurrent_hierarchy(self):
        """Test Occurrent inheritance chain."""
        assert issubclass(Occurrent, Entity)
        assert issubclass(Process, Occurrent)
        assert issubclass(History, Process)
        assert issubclass(TemporalRegion, Occurrent)

    def test_spatial_region_hierarchy(self):
        """Test SpatialRegion inheritance chain."""
        assert issubclass(ImmaterialEntity, IndependentContinuant)
        assert issubclass(SpatialRegion, ImmaterialEntity)


class TestBFOProperties:
    """Test that BFO classes have expected properties."""

    def test_entity_has_base_properties(self):
        """Test Entity has uid, name, description properties."""
        entity_properties = dir(Entity)
        assert 'uid' in entity_properties
        assert 'name' in entity_properties
        assert 'description' in entity_properties
        assert 'created_at' in entity_properties
        assert 'modified_at' in entity_properties

    def test_quality_has_value_properties(self):
        """Test Quality has value and unit properties."""
        quality_properties = dir(Quality)
        assert 'value' in quality_properties
        assert 'unit' in quality_properties

    def test_occurrent_has_temporal_properties(self):
        """Test Occurrent has temporal properties."""
        occurrent_properties = dir(Occurrent)
        assert 'start_time' in occurrent_properties
        assert 'end_time' in occurrent_properties

    def test_spatial_region_has_coordinate_properties(self):
        """Test SpatialRegion has coordinate properties."""
        spatial_properties = dir(SpatialRegion)
        assert 'coordinates' in spatial_properties
        assert 'coordinate_system' in spatial_properties


class TestBFORelationships:
    """Test that BFO classes have expected relationships."""

    def test_continuant_has_parthood_relationships(self):
        """Test Continuant has part_of and has_part relationships."""
        continuant_relationships = dir(Continuant)
        assert 'part_of' in continuant_relationships
        assert 'has_part' in continuant_relationships

    def test_continuant_has_temporal_relationships(self):
        """Test Continuant has exists_at relationship."""
        continuant_relationships = dir(Continuant)
        assert 'exists_at' in continuant_relationships

    def test_continuant_has_spatial_relationships(self):
        """Test Continuant has spatial relationships."""
        continuant_relationships = dir(Continuant)
        assert 'located_in' in continuant_relationships
        assert 'occupies_spatial_region' in continuant_relationships

    def test_independent_continuant_has_inherence_relationships(self):
        """Test IndependentContinuant has bearer_of relationship."""
        ic_relationships = dir(IndependentContinuant)
        assert 'bearer_of' in ic_relationships
        assert 'participates_in' in ic_relationships

    def test_specifically_dependent_continuant_has_inheres_in(self):
        """Test SpecificallyDependentContinuant has inheres_in relationship."""
        sdc_relationships = dir(SpecificallyDependentContinuant)
        assert 'inheres_in' in sdc_relationships

    def test_realizable_entity_has_realized_by(self):
        """Test RealizableEntity has realized_by relationship."""
        re_relationships = dir(RealizableEntity)
        assert 'realized_by' in re_relationships

    def test_process_has_participation_relationships(self):
        """Test Process has participant relationships."""
        process_relationships = dir(Process)
        assert 'has_participant' in process_relationships
        assert 'realizes' in process_relationships

    def test_process_has_temporal_ordering(self):
        """Test Process has precedes/preceded_by relationships."""
        process_relationships = dir(Process)
        assert 'precedes' in process_relationships
        assert 'preceded_by' in process_relationships

    def test_occurrent_has_parthood_relationships(self):
        """Test Occurrent has part_of and has_part relationships."""
        occurrent_relationships = dir(Occurrent)
        assert 'part_of' in occurrent_relationships
        assert 'has_part' in occurrent_relationships
        assert 'occurs_in' in occurrent_relationships


class TestBFODocumentation:
    """Test that BFO classes have documentation."""

    def test_entity_has_docstring(self):
        """Test Entity has a docstring."""
        assert Entity.__doc__ is not None
        assert 'BFO:0000001' in Entity.__doc__

    def test_continuant_has_docstring(self):
        """Test Continuant has a docstring."""
        assert Continuant.__doc__ is not None
        assert 'BFO:0000002' in Continuant.__doc__

    def test_object_has_docstring(self):
        """Test Object has a docstring."""
        assert Object.__doc__ is not None
        assert 'BFO:0000030' in Object.__doc__

    def test_process_has_docstring(self):
        """Test Process has a docstring."""
        assert Process.__doc__ is not None
        assert 'BFO:0000015' in Process.__doc__

    def test_quality_has_docstring(self):
        """Test Quality has a docstring."""
        assert Quality.__doc__ is not None
        assert 'BFO:0000019' in Quality.__doc__


class TestBFOModuleExports:
    """Test that __all__ exports are correct."""

    def test_all_exports_exist(self):
        """Test that all exported names exist in the module."""
        from neomodel_bfo import bfo

        for name in bfo.__all__:
            assert hasattr(bfo, name), f"{name} in __all__ but not defined"

    def test_major_classes_exported(self):
        """Test that major BFO classes are in __all__."""
        from neomodel_bfo import bfo

        major_classes = [
            'Entity', 'Continuant', 'Object', 'Process',
            'Quality', 'Role', 'Function', 'Disposition'
        ]

        for cls in major_classes:
            assert cls in bfo.__all__, f"{cls} not exported in __all__"
