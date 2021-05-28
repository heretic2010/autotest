import sqlite3

try:
    sqlite_connection = sqlite3.connect('app.db')
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")

    sqlite_insert_query = """INSERT INTO emp
                          (id, username, email, department, date_joined)
                          VALUES
                          (4, 'Badjaj Aqumba', 'aqumba@gmail.com','sales', '1950-05-01 09:25:10' );"""
    count = cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    print("Запись успешно вставлена ​​ в таблицу app ", cursor.rowcount)
    cursor.close()

except sqlite3.Error as error:
    print("Ошибка при работе с SQLite", error)
finally:
    if sqlite_connection:
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")