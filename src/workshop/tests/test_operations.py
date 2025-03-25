import pytest
from datetime import date
from decimal import Decimal
from fastapi import HTTPException
from ..services.operations import OperationsService
from ..models.operations import OperationCreate, OperationUpdate, OperationType
from ..tables import Operation, User

@pytest.mark.asyncio
async def test_create_operation(session, test_user):
    service = OperationsService(session)
    operation_data = OperationCreate(
        date=date(2025, 3, 3),
        operation_type=OperationType.INCOME,
        amount=Decimal("100.50"),
        description="Test income"
    )
    operation = service.create(test_user.user_id, operation_data)
    assert operation.operation_id is not None
    assert operation.amount == 100.50

@pytest.mark.asyncio
async def test_get_nonexistent_operation(session, test_user):
    service = OperationsService(session)
    with pytest.raises(HTTPException) as exc:
        service.get(test_user.user_id, 999999)
    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_update_operation(session, test_user):
    service = OperationsService(session)
    operation_data = OperationCreate(
        date=date(2025, 3, 3),
        operation_type=OperationType.INCOME,
        amount=Decimal("50.00"),
        description="Initial"
    )
    operation = service.create(test_user.user_id, operation_data)
    
    update_data = OperationUpdate(date=date(2023, 1, 1),
    operation_type=OperationType.INCOME,
    amount=Decimal("50.00"),
    description="Updated")
    updated_operation = service.update(test_user.user_id, operation.operation_id, update_data)
    assert updated_operation.description == "Updated"
@pytest.mark.asyncio
async def test_delete_operation_success(session, test_user):
    service = OperationsService(session)
    
    operation_data = OperationCreate(
        date="2025-03-03",
        operation_type="income",
        amount=100.50,
        description="Test operation"
    )
    operation = service.create(test_user.user_id, operation_data)
    
    service.delete(test_user.user_id, operation.operation_id)
    
    deleted_operation = session.query(Operation).filter_by(operation_id=operation.operation_id).first()
    assert deleted_operation is None
@pytest.mark.asyncio
async def test_delete_nonexistent_operation(session, test_user):
    service = OperationsService(session)
    non_existent_id = 99999999

    with pytest.raises(HTTPException) as exc_info:
        service.delete(test_user.user_id, non_existent_id)
    
    assert exc_info.value.status_code == 404
    assert "not found" in str(exc_info.value.detail).lower()
