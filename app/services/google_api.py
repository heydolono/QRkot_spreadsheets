from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"
SPREADSHEET_BODY = {
    'properties': {'title': 'Отчёт на временное значение', 'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'Лист1',
                               'gridProperties': {'rowCount': 100,
                                                  'columnCount': 11}}}]
}
PERMISSIONS_BODY = {'type': 'user',
                    'role': 'writer',
                    'emailAddress': settings.email}
TABLE_VALUES = [
    ['Отчёт от', 'временное значение'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
UPDATE_BODY = {
    'majorDimension': 'ROWS',
    'values': TABLE_VALUES
}


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    spreadsheet_body = SPREADSHEET_BODY.copy()
    spreadsheet_body['properties']['title'] = f'Отчёт на {now_date_time}'
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
    now_date_time = datetime.now().strftime(FORMAT)
    table_values = TABLE_VALUES.copy()
    table_values[0][1] = now_date_time
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
