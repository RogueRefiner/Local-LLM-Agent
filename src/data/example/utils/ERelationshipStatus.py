from enum import Enum


class ERelationshipStatus(str, Enum):
    SINGLE = "SINGLE"
    IN_RELATIONSHIP = "IN RELATIONSHIP"
    COMPLICATED = "COMPLICATED"
