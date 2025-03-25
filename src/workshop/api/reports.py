from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks
from fastapi.responses import StreamingResponse

from ..models.auth import User
from ..services.auth import get_current_user
from ..services.reports import ReportsService

router = APIRouter(
    prefix='/reports',
    tags=['reports'],
)


@router.post('/import')
def import_operations_from_csv(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        user: User = Depends(get_current_user),
        report_service: ReportsService = Depends(),
):
    background_tasks.add_task(
        report_service.import_operations_from_csv,
        user.user_id,
        file.file
    )


@router.get('/export')
def export_operations_to_csv(
        user: User = Depends(get_current_user),
        report_service: ReportsService = Depends(),
):
    report = report_service.export_operations_to_csv(user.user_id)
    return StreamingResponse(
        report,
        media_type='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename=report.csv'
        },
    )
