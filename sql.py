import sqlite3 as sl

# Создаём соединение с базой данных
con = sl.connect('durka.db')

# Создаем таблицы в базе данных
tables = {
    "CLIENTS": """
        CREATE TABLE IF NOT EXISTS CLIENTS (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date_of_birth INTEGER,
            information TEXT,
            tel TEXT UNIQUE
        );
    """,
    "EMPLOYEES": """
        CREATE TABLE IF NOT EXISTS EMPLOYEES (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date_of_birth INTEGER,
            position TEXT,
            tel TEXT UNIQUE
        );
    """,
    "SERVICES": """
        CREATE TABLE IF NOT EXISTS SERVICES (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price INTEGER,
            time TEXT,
            position INTEGER
        );
    """,
    "EVENTS": """
        CREATE TABLE IF NOT EXISTS EVENTS (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            client INTEGER,
            employee INTEGER,
            service INTEGER
        );
    """,
    "POSITIONS": """
        CREATE TABLE IF NOT EXISTS POSITIONS (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            salary INTEGER,
            cab TEXT
        );
    """
}

with con:
    for table, sql in tables.items():
        con.execute(sql)

# Вставляем данные в таблицу SERVICES
sql_insert = "INSERT OR IGNORE INTO SERVICES (id, name, price, time, position) values(?, ?, ?, ?, ?)"
with con:
    con.execute(sql_insert, [1, "Операция", 500, "04:00", 2])
    con.execute(sql_insert, [2, "Диагностика", 50, "00:30", 1])

# Получаем и выводим данные из таблицы SERVICES
with con:
    data = con.execute("SELECT * FROM SERVICES").fetchall()
    print(data)
