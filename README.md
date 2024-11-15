# QRKot - Благотворительный фонд поддержки котиков

## Описание проекта
QRKot — это приложение для благотворительного фонда, который собирает пожертвования на проекты, направленные на поддержку кошек. Это может быть медицинское обслуживание, обустройство кошачьей колонии, закупка корма и многое другое, связанное с улучшением жизни котиков.

## Установка и запуск проекта
1. Клонируйте репозиторий:
   ```
   git clone https://github.com/heydolono/cat_charity_fund.git
   ```

2. Создайте виртуальное окружение и активируйте его:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```

4. Выполните миграции базы данных:
   ```
   alembic upgrade head
   ```

5. Запустите приложение:
   ```
   uvicorn main:app 
   ```