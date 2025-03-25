from fastapi import FastAPI

from .api import api_router

TAGS_METADATA = [
    {
        'name': 'auth',
        'description': 'Авторизация',
    },
    {
        'name': 'operations',
        'description': 'Работа с операциями',
    },
    {
        'name': 'reports',
        'description': 'Импорт и экспорт отчетов',
    }
]
app = FastAPI(
    title='Workshop',
    description='Сервис учета личных расходов и доходов.',
    version='1.0.0',
    openapi_tags=TAGS_METADATA,
)
app.include_router(router)
