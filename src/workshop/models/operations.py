from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class OperationType(str, Enum):
    INCOME = 'income'
    OUTCOME = 'outcome'


class OperationBase(BaseModel):
    date: date
    operation_type: OperationType
    amount: Decimal
    description: Optional[str]


class Operation(OperationBase):
    operation_id: int

    class Config:
        orm_mode = True
        from_attributes = True


class OperationCreate(OperationBase):
    pass


class OperationUpdate(OperationBase):
    pass
