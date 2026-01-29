from enum import Enum


class ERelationshipStatus(str, Enum):
    SINGLE = "SINGLE"
    IN_RELATIONSHIP = "IN_RELATIONSHIP"
    COMPLICATED = "COMPLICATED"
