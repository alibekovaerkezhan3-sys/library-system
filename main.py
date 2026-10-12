import mysql.connector
from getpass import getpass

password = getpass("MySQL құпиясөзін енгізіңіз: ")

try:
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="library_app",
        password=password,
        database="library_db"
    )

    cursor = conn.cursor()

    print("\n===== КІТАПХАНА АҚПАРАТТЫҚ ЖҮЙЕСІ =====")
    print("1 - Кітаптарды көрсету")
    print("2 - Жаңа кітап қосу")
    print("3 - Шығу")

    choice = input("\nТаңдаңыз: ")

    if choice == "1":
        cursor.execute("""
            SELECT b.bookID, b.title, a.name, c.name,
                   b.year_published
            FROM Books b
            JOIN Authors a ON b.authorID = a.authorID
            JOIN Categories c ON b.categoryID = c.categoryID
            ORDER BY b.bookID
        """)

        print("\n===== КІТАПТАР ТІЗІМІ =====")

        for book in cursor.fetchall():
            print(
                f"ID: {book[0]} | "
                f"Кітап: {book[1]} | "
                f"Автор: {book[2]} | "
                f"Жанр: {book[3]} | "
                f"Жылы: {book[4]}"
            )

    elif choice == "2":
        print("\n===== ЖАҢА КІТАП ҚОСУ =====")

        title = input("Кітап атауы: ")

        cursor.execute("SELECT authorID, name FROM Authors")
        authors = cursor.fetchall()

        print("\n===== АВТОРЛАР =====")
        for author in authors:
            print(f"{author[0]} - {author[1]}")

        author_id = int(input("\nАвтор ID таңдаңыз: "))

        if author_id not in [a[0] for a in authors]:
            print("Мұндай автор жоқ!")
        else:
            cursor.execute("SELECT categoryID, name FROM Categories")
            categories = cursor.fetchall()

            print("\n===== ЖАНРЛАР =====")
            for category in categories:
                print(f"{category[0]} - {category[1]}")

            category_id = int(input("\nЖанр ID таңдаңыз: "))

            if category_id not in [c[0] for c in categories]:
                print("Мұндай жанр жоқ!")
            else:
                year = int(input("Шыққан жылы: "))

                cursor.execute("""
                    INSERT INTO Books
                    (title, authorID, categoryID, year_published)
                    VALUES (%s, %s, %s, %s)
                """, (title, author_id, category_id, year))

                conn.commit()
                print("\nКітап сәтті қосылды!")

    elif choice == "3":
        print("Бағдарлама аяқталды.")

    else:
        print("Қате таңдау!")

    cursor.close()
    conn.close()

except (mysql.connector.Error, ValueError) as e:
    print("Қате:", e)