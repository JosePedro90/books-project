from enum import Enum


class ReservationStatus(Enum):
    RESERVED = "reserved"
    RETURNED = "returned"
    CANCELED = "canceled"

    @classmethod
    def choices(cls):
        return [(member.value, member.name) for member in cls]
