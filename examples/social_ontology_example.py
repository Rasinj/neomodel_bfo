"""
Example: Extending BFO for Social Ontology - Modeling People and Organizations

This example demonstrates how to extend neomodel_bfo for social entities,
showing how roles, organizations, and social processes work within BFO.

Pattern demonstrated:
- Modeling persons and organizations as Objects
- Using Roles for social positions
- Processes for social activities
- Multiple roles for the same person
"""

from neomodel import StringProperty, IntegerProperty, DateProperty, RelationshipTo, RelationshipFrom, ZeroOrMore
from neomodel_bfo import (
    Object,
    Role,
    Process,
    Quality,
    GenericallyDependentContinuant
)


# =============================================================================
# Domain Objects - Social Entities
# =============================================================================

class Person(Object):
    """
    A human person - extends BFO Object.

    BFO perspective: A person is a material entity (object) that can bear
    various roles (student, employee, parent) and participate in social processes.
    """
    date_of_birth = DateProperty()
    nationality = StringProperty()

    # Social relationships (domain-specific)
    employed_by = RelationshipTo('Organization', 'EMPLOYED_BY')
    member_of = RelationshipTo('Organization', 'MEMBER_OF')


class Organization(Object):
    """
    A social organization - extends BFO Object.

    BFO perspective: Organizations are material entities (collections of people
    and assets) that can participate in processes and bear roles.
    """
    founded_date = DateProperty()
    organization_type = StringProperty()  # e.g., "university", "corporation", "NGO"

    # Organizational relationships
    part_of_org = RelationshipTo('Organization', 'PART_OF_ORG')
    has_member = RelationshipFrom('Person', 'MEMBER_OF')
    employs = RelationshipFrom('Person', 'EMPLOYED_BY')


# =============================================================================
# Domain Roles - Social Positions
# =============================================================================

class SocialRole(Role):
    """
    Base class for social roles - extends BFO Role.

    BFO perspective: A role exists because the bearer is in a special social
    or institutional context. The same person can have multiple roles.

    Inherits:
    - inheres_in (the person who has this role)
    - realized_by (social processes that realize this role)
    """
    role_type = StringProperty()
    active_since = DateProperty()
    active_until = DateProperty()


class EmployeeRole(SocialRole):
    """
    The role of being an employee.
    """
    job_title = StringProperty()
    department = StringProperty()


class StudentRole(SocialRole):
    """
    The role of being a student.
    """
    student_id = StringProperty()
    program = StringProperty()
    enrollment_year = IntegerProperty()


class ParentRole(SocialRole):
    """
    The role of being a parent.
    """
    pass


class TeacherRole(SocialRole):
    """
    The role of being a teacher.
    """
    subject_area = StringProperty()


# =============================================================================
# Domain Processes - Social Activities
# =============================================================================

class SocialProcess(Process):
    """
    A social process - extends BFO Process.

    BFO perspective: Social processes are occurrents that unfold over time
    and involve people (participants) realizing their roles.
    """
    process_category = StringProperty()


class Teaching(SocialProcess):
    """
    Process of teaching - realizes TeacherRole and StudentRole.
    """
    course_name = StringProperty()


class Employment(SocialProcess):
    """
    Process of being employed - realizes EmployeeRole.
    """
    pass


class Meeting(SocialProcess):
    """
    A meeting - a social process with multiple participants.
    """
    meeting_type = StringProperty()
    location = StringProperty()


# =============================================================================
# Domain Information Entities
# =============================================================================

class InformationContentEntity(GenericallyDependentContinuant):
    """
    Information that can be encoded in multiple physical bearers.

    BFO perspective: Information is generically dependent - the same
    information can exist in a book, computer file, or person's memory.
    """
    content_type = StringProperty()


class Document(InformationContentEntity):
    """
    A document containing information.
    """
    document_type = StringProperty()  # e.g., "contract", "report", "email"
    author = RelationshipTo('Person', 'AUTHORED_BY')


# =============================================================================
# Domain Qualities - Social Attributes
# =============================================================================

class Reputation(Quality):
    """
    The reputation of a person or organization - extends BFO Quality.

    BFO perspective: A quality that inheres in a person/organization
    and can change over time.
    """
    reputation_score = StringProperty()  # e.g., "excellent", "good", "poor"


# =============================================================================
# Usage Example
# =============================================================================

def example_usage():
    """
    Demonstrates modeling a university scenario with people, roles, and processes.
    """
    from neomodel import config
    from datetime import datetime

    # Configure Neo4j connection (example)
    # config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'

    # Create a university
    university = Organization(
        name="Example University",
        organization_type="university",
        founded_date=datetime(1890, 1, 1).date()
    ).save()

    # Create a person
    alice = Person(
        name="Alice Smith",
        date_of_birth=datetime(1985, 5, 15).date(),
        nationality="USA"
    ).save()

    # Create another person
    bob = Person(
        name="Bob Johnson",
        date_of_birth=datetime(2000, 3, 20).date(),
        nationality="Canada"
    ).save()

    # Alice is employed by the university
    alice.employed_by.connect(university)

    # Create Alice's teacher role (a role that inheres in Alice)
    teacher_role = TeacherRole(
        name="Alice's teacher role",
        role_type="professor",
        subject_area="Computer Science",
        active_since=datetime(2010, 9, 1).date()
    ).save()

    # Connect: role inheres in Alice (using BFO inheres_in)
    teacher_role.inheres_in.connect(alice)

    # Create Bob's student role
    student_role = StudentRole(
        name="Bob's student role",
        role_type="graduate student",
        student_id="123456",
        program="Computer Science MS",
        enrollment_year=2022
    ).save()

    # Connect: role inheres in Bob
    student_role.inheres_in.connect(bob)

    # Create a teaching process
    teaching = Teaching(
        name="CS101 Fall 2024",
        process_category="education",
        course_name="Introduction to Programming",
        start_time=datetime(2024, 9, 1, 9, 0),
        end_time=datetime(2024, 12, 15, 17, 0)
    ).save()

    # Connect: Alice and Bob participate in the teaching process
    alice.participates_in.connect(teaching)
    bob.participates_in.connect(teaching)

    # Connect: teaching process realizes the roles
    teaching.realizes.connect(teacher_role)
    teaching.realizes.connect(student_role)

    # Create a quality (Alice's reputation)
    reputation = Reputation(
        name="Alice's academic reputation",
        value="excellent",
        unit="categorical"
    ).save()
    reputation.inheres_in.connect(alice)

    print(f"Created organization: {university.name}")
    print(f"\nCreated person: {alice.name}")
    print(f"  - Works at: {list(alice.employed_by.all())[0].name}")
    print(f"  - Has role: {teacher_role.role_type} in {teacher_role.subject_area}")
    print(f"  - Reputation: {reputation.value}")

    print(f"\nCreated person: {bob.name}")
    print(f"  - Has role: {student_role.role_type}")
    print(f"  - Program: {student_role.program}")

    print(f"\nCreated process: {teaching.name}")
    print(f"  - Participants:")
    for participant in teaching.has_participant.all():
        print(f"    - {participant.name}")
    print(f"  - Realizes roles:")
    for role in teaching.realizes.all():
        print(f"    - {role.name}")

    # Complex query: Find all processes a person participates in
    print(f"\nAll processes {alice.name} participates in:")
    for process in alice.participates_in.all():
        print(f"  - {process.name} ({process.process_category})")

    # Query: Find all roles a person has
    print(f"\nAll roles that inhere in {alice.name}:")
    for role in alice.bearer_of.all():
        if isinstance(role, SocialRole):
            print(f"  - {role.role_type}")


if __name__ == "__main__":
    # Uncomment to run (requires Neo4j setup)
    # example_usage()
    print("Social ontology example loaded. Configure Neo4j and call example_usage() to run.")
