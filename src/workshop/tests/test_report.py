import pytest
from io import BytesIO
from datetime import date
from decimal import Decimal
from ..services.reports import ReportsService
from ..services.operations import OperationsService
from ..models.operations import OperationCreate, OperationType
@pytest.mark.asyncio
async def test_import_operation_from_csv(session, test_user):
    csv_data = (
        "date,operation_type,amount,description\n"
        "2025-03-03,income,100.50,Test Income\n"
        "2025-03-04,outcome,50.00,Test Outcome\n"
    )
    csv_file = BytesIO(csv_data.encode('utf-8'))
    operations_service = OperationsService(session)
    reports_service = ReportsService(operations_service)

    reports_service.import_operations_from_csv(test_user.user_id, csv_file)

    operations = operations_service.get_list(test_user.user_id)
    assert len(operations) == 2
    assert operations[0].amount == 100.50
    assert operations[1].operation_type == 'outcome'
@pytest.mark.asyncio
async def test_export_operation_to_csv(session, test_user):
    operations_service = OperationsService(session)
    reports_service = ReportsService(operations_service)
    
    operation_data = OperationCreate(
        date=date(2025, 3, 3),
        operation_type=OperationType.INCOME,
        amount=Decimal("200.00"),
        description="Test Export"
    )
    operations_service.create(test_user.user_id, operation_data)

    csv_stream = reports_service.export_operations_to_csv(test_user.user_id)

    content = csv_stream.getvalue()
    assert "date,operation_type,amount,description" in content
    assert "2025-03-03,income,200.00,Test Export" in content