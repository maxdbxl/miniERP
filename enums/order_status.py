from enum import Enum

class OrderStatus(Enum):
    DRAFT = 1
    CONFIRMED = 2
    DELIVERED = 3
    INVOICED = 4
    CANCELLED = 5