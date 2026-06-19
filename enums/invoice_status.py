from enum import Enum

class InvoiceStatus(Enum):
    DRAFT = 1
    ISSUED = 2
    PAID = 3
    CANCELLED = 4