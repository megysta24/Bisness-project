# Как да стартираш проекта

## 1. Инсталирай нужните програми

Трябват ти:

- MySQL Server и MySQL Workbench
- Python 3.11 или по-нова версия

Ако имаш само MySQL Workbench, инсталирай и MySQL Server, защото Workbench е само инструмент за управление.

## 2. Създай базата

В MySQL Workbench отвори и изпълни последователно:

1. `database/schema.sql`
2. `database/seed.sql`

Това създава база `publication_activity` и зарежда демонстрационни данни.

## 3. Настрой Python проекта

Отвори PowerShell в папката `publication_activity_system` и изпълни:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 4. Настрой връзката към MySQL

Копирай `.env.example` като `.env` и попълни:

```text
MYSQL_USER=root
MYSQL_PASSWORD=твоята_mysql_парола
MYSQL_DATABASE=publication_activity
```

## 5. Стартирай приложението

```powershell
python run.py
```

Отвори:

```text
http://127.0.0.1:5000
```

## 6. Вход

Парола за всички демо потребители:

```text
password123
```

Потребители:

- `admin@department.local`
- `head@department.local`
- `tuparova@department.local`
- `ivanov@department.local`

