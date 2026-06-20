# Web система за публикационна активност

Курсова разработка: Web базирана информационна система за отчитане на публикационната активност на департамент.

## Технологии

- Backend: Python Flask
- Frontend: HTML, CSS, JavaScript
- База данни: MySQL
- Инструмент за БД: MySQL Workbench

## Бърз старт

1. Инсталирай Python 3.11+.
2. Отвори MySQL Workbench и изпълни:
   - `database/schema.sql`
   - `database/seed.sql`
3. Създай виртуална среда:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

4. Копирай `.env.example` като `.env` и промени MySQL паролата.
5. Стартирай:

```powershell
python run.py
```

6. Отвори `http://127.0.0.1:5000`.

## Примерни профили

Паролата за всички демонстрационни потребители е `password123`.

- `admin@department.local` - администратор
- `head@department.local` - редактор общо съдържание
- `tuparova@department.local` - личен редактор
- `ivanov@department.local` - личен редактор

## Права

- Администратор: управлява потребители и вижда всички данни.
- Ръководител департамент: редактира общото съдържание.
- Преподавател: вижда всички данни, но редактира само своите публикации.

