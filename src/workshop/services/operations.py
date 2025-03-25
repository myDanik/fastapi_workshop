from typing import Optional, List

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import tables
from ..database import get_db_session
from ..models.operations import OperationCreate, OperationType, OperationUpdate


class OperationsService:
    def __init__(self, session: Session = Depends(get_db_session)):
        self.session = session

    def _get_operation_by_id(self, user_id: int, operation_id) -> tables.Operation:
        operation = self.session.query(tables.Operation).filter_by(
            operation_id=operation_id,
            user_id=user_id,
        ).first()
        if not operation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return operation

    def get_list(self, user_id: int, operation_type: Optional[OperationType] = None) -> List[tables.Operation]:
        query = self.session.query(tables.Operation).filter_by(user_id=user_id)
        if operation_type:
            query = query.filter_by(operation_type=operation_type)
        operations = query.all()
        return operations

    def get(self, user_id: int, operation_id: int) -> tables.Operation:
        return self._get_operation_by_id(user_id, operation_id)

    def create_many(self, user_id: int, operations_data: List[OperationCreate]) -> List[tables.Operation]:
        operations = [
            tables.Operation(
                **operation_data.dict(),
                user_id=user_id,
            )
            for operation_data in operations_data
        ]
        self.session.add_all(operations)
        self.session.commit()
        return operations

    def create(self, user_id: int, operation_data: OperationCreate) -> tables.Operation:
        operation = tables.Operation(
            **operation_data.dict(),
            user_id=user_id,
        )
        self.session.add(operation)
        self.session.commit()
        return operation

    def update(self, user_id: int, operation_id: int, operation_data: OperationUpdate) -> tables.Operation:
        operation = self._get_operation_by_id(user_id, operation_id)
        update_data = operation_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(operation, field, value)
        self.session.commit()
        return operation

    def delete(self, user_id: int, operation_id: int):
        operation = self._get_operation_by_id(user_id, operation_id)
        self.session.delete(operation)
        self.session.commit()
