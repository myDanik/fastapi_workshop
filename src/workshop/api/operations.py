from typing import Optional

from fastapi import APIRouter, Depends, Response, status

from ..models.auth import User
from ..models.operations import (
Operation,
OperationCreate,
OperationType,
OperationUpdate
)
from ..services.auth import get_current_user
from ..services.operations import OperationsService

router = APIRouter(
    prefix='/operations',
    tags=['operations'],
)


@router.get('/', response_model=list[Operation])
def get_operations(
        operation_type: Optional[OperationType] = None,
        user: User = Depends(get_current_user),
        service: OperationsService = Depends(),
):
    return service.get_list(user_id=user.user_id, operation_type=operation_type)


@router.post('/', response_model=Operation, status_code=status.HTTP_201_CREATED)
def create_operation(
        operation_data: OperationCreate,
        user: User = Depends(get_current_user),
        service: OperationsService = Depends(),
):
    return service.create(user_id=user.user_id, operation_data=operation_data)


@router.get('/{operation_id}', response_model=Operation)
def get_operation(
        operation_id: int,
        user: User = Depends(get_current_user),
        service: OperationsService = Depends(),
):
    return service.get(user_id=user.user_id, operation_id=operation_id)


@router.put('/{operation_id}', response_model=Operation)
def update_operation(
        operation_id: int,
        operation_data: OperationUpdate,
        user: User = Depends(get_current_user),
        service: OperationsService = Depends(),
):
    return service.update(
        user_id=user.user_id,
        operation_id=operation_id,
        operation_data=operation_data,
    )


@router.delete('/{operation_id}')
def delete_operation(
        operation_id: int,
        user: User = Depends(get_current_user),
        service: OperationsService = Depends(),
):
    service.delete(user_id=user.user_id, operation_id=operation_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
