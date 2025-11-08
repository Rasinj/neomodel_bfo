"""
Tests for example code.

These tests verify that example code can be imported and has the expected
structure without requiring a Neo4j connection.
"""

import pytest


class TestBiologyExample:
    """Test the biology example can be imported."""

    def test_biology_example_imports(self):
        """Test that biology example classes can be imported."""
        from examples.biology_example import (
            Organism,
            AnatomicalStructure,
            Cell,
            BodyTemperature,
            BiologicalFunction,
            BiologicalProcess,
        )

        assert Organism is not None
        assert AnatomicalStructure is not None
        assert Cell is not None
        assert BodyTemperature is not None
        assert BiologicalFunction is not None
        assert BiologicalProcess is not None

    def test_organism_has_domain_properties(self):
        """Test Organism class has expected domain properties."""
        from examples.biology_example import Organism

        organism_props = dir(Organism)
        assert 'species' in organism_props
        assert 'age_years' in organism_props

    def test_organism_inherits_bfo_relationships(self):
        """Test Organism inherits BFO relationships from Object."""
        from examples.biology_example import Organism

        organism_rels = dir(Organism)
        # Should have BFO relationships from Object
        assert 'part_of' in organism_rels
        assert 'has_part' in organism_rels
        assert 'participates_in' in organism_rels
        assert 'bearer_of' in organism_rels


class TestSocialOntologyExample:
    """Test the social ontology example can be imported."""

    def test_social_example_imports(self):
        """Test that social ontology example classes can be imported."""
        from examples.social_ontology_example import (
            Person,
            Organization,
            SocialRole,
            EmployeeRole,
            StudentRole,
            Teaching,
        )

        assert Person is not None
        assert Organization is not None
        assert SocialRole is not None
        assert EmployeeRole is not None
        assert StudentRole is not None
        assert Teaching is not None

    def test_person_has_domain_properties(self):
        """Test Person class has expected domain properties."""
        from examples.social_ontology_example import Person

        person_props = dir(Person)
        assert 'date_of_birth' in person_props
        assert 'nationality' in person_props

    def test_social_role_has_domain_properties(self):
        """Test SocialRole class has expected domain properties."""
        from examples.social_ontology_example import SocialRole

        role_props = dir(SocialRole)
        assert 'role_type' in role_props

    def test_person_inherits_bfo_relationships(self):
        """Test Person inherits BFO relationships from Object."""
        from examples.social_ontology_example import Person

        person_rels = dir(Person)
        # Should have BFO relationships from Object
        assert 'part_of' in person_rels
        assert 'participates_in' in person_rels
        assert 'bearer_of' in person_rels


class TestExamplesDocumentation:
    """Test that examples have proper documentation."""

    def test_biology_example_has_docstrings(self):
        """Test biology example classes have docstrings."""
        from examples.biology_example import Organism, BiologicalFunction

        assert Organism.__doc__ is not None
        assert BiologicalFunction.__doc__ is not None

    def test_social_example_has_docstrings(self):
        """Test social ontology example classes have docstrings."""
        from examples.social_ontology_example import Person, SocialRole

        assert Person.__doc__ is not None
        assert SocialRole.__doc__ is not None
