import mysql.connector
from getpass import getpass

try:
    password = getpass("MySQL құпиясөзін енгізіңіз: ")

    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="library_app",
        password=password,
        database="library_db"
    )

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Books")
    books = cursor.fetchall()

    print("\n===== КІТАПТАР ТІЗІМІ =====")

    for book in books:
        print(
            f"ID: {book[0]} | "
            f"Атауы: {book[1]} | "
            f"Автор ID: {book[2]} | "
            f"Жанр ID: {book[3]} | "
            f"Жылы: {book[4]}"
        )

    cursor.close()
    conn.close()

except mysql.connector.Error as e:
    print("Қате:", e)