import csv
from io import StringIO
from typing import Any

from fastapi import Depends

from ..models.operations import OperationCreate, Operation
from .operations import OperationsService


class ReportsService:
    def __init__(self, operations_service: OperationsService):
        self.operations_service = operations_service

    def import_operations_from_csv(self, user_id: int, file: Any):
        try:
            reader = csv.DictReader(
                (line.decode('utf-8') for line in file),
                fieldnames=[
                    'date',
                    'operation_type',
                    'amount',
                    'description',
                ]
            )
            operations = []
            next(reader)
            for row in reader:
                operation_data = OperationCreate.parse_obj(row)
                if not operation_data.description:
                    operation_data.description = None
                operations.append(operation_data)

            self.operations_service.create_many(user_id, operations)
        except csv.Error as e:
            raise HTTPException(status_code=400, detail=f"CSV parsing error: {e}")

    def export_operations_to_csv(self, user_id: int) -> Any:
        output = StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=[
                'date',
                'operation_type',
                'amount',
                'description',
            ],
            extrasaction='ignore',

        )
        operations = self.operations_service.get_list(user_id)

        writer.writeheader()
        for operation in operations:
            operation_data = Operation.from_orm(operation)
            writer.writerow(operation_data.dict())

        output.seek(0)
        return output


