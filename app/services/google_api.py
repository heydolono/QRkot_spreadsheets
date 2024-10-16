from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"
NOW_DATE_TIME = datetime.now().strftime(FORMAT)
SPREADSHEET_BODY = {
    'properties': {'title': f'Отчёт на {NOW_DATE_TIME}',
                            'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                'sheetId': 0, 'title': 'Лист1',
                'gridProperties': {'rowCount': 100,
                                            'columnCount': 11}}}]
}
PERMISSIONS_BODY = {'type': 'user',
                    'role': 'writer',
                    'emailAddress': settings.email}
TABLE_VALUES = [
        ['Отчёт от', NOW_DATE_TIME],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
]
UPDATE_BODY = {
        'majorDimension': 'ROWS',
        'values': TABLE_VALUES
}


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=SPREADSHEET_BODY)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=PERMISSIONS_BODY,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    for project in projects:
        collection_time = project.close_date - project.create_date
        new_row = [project.name, str(collection_time), project.description]
        TABLE_VALUES.append(new_row)
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=UPDATE_BODY
        )
    )
