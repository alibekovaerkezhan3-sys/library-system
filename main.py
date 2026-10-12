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

    while True:
        print("\n===== КІТАПХАНА АҚПАРАТТЫҚ ЖҮЙЕСІ =====")
        print("1 - Кітаптарды көрсету")
        print("2 - Жаңа кітап қосу")
        print("3 - Кітапты онлайн брондау")
        print("4 - Брондауларды көрсету")
        print("5 - Шығу")

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

            author_id = int(input("Автор ID таңдаңыз: "))

            if author_id not in [a[0] for a in authors]:
                print("Мұндай автор жоқ!")
                continue

            cursor.execute("SELECT categoryID, name FROM Categories")
            categories = cursor.fetchall()

            print("\n===== ЖАНРЛАР =====")
            for category in categories:
                print(f"{category[0]} - {category[1]}")

            category_id = int(input("Жанр ID таңдаңыз: "))

            if category_id not in [c[0] for c in categories]:
                print("Мұндай жанр жоқ!")
                continue

            year = int(input("Шыққан жылы: "))

            cursor.execute("""
                INSERT INTO Books
                (title, authorID, categoryID, year_published)
                VALUES (%s, %s, %s, %s)
            """, (title, author_id, category_id, year))

            conn.commit()
            print("Кітап сәтті қосылды!")

        elif choice == "3":
            print("\n===== КІТАПТЫ ОНЛАЙН БРОНДАУ =====")

            cursor.execute("SELECT bookID, title FROM Books")
            books = cursor.fetchall()

            print("\nКІТАПТАР:")
            for book in books:
                print(f"{book[0]} - {book[1]}")

            book_id = int(input("\nКітап ID таңдаңыз: "))

            if book_id not in [b[0] for b in books]:
                print("Мұндай кітап жоқ!")
                continue

            cursor.execute("SELECT readerID, fullname FROM Readers")
            readers = cursor.fetchall()

            print("\nОҚЫРМАНДАР:")
            for reader in readers:
                print(f"{reader[0]} - {reader[1]}")

            reader_id = int(input("\nОқырман ID таңдаңыз: "))

            if reader_id not in [r[0] for r in readers]:
                print("Мұндай оқырман жоқ!")
                continue

            # Белсенді брондауды тексеру
            cursor.execute("""
                SELECT reservationID
                FROM Reservations
                WHERE bookID = %s
                  AND status = 'Брондалды'
                  AND expiry_date > NOW()
                LIMIT 1
            """, (book_id,))

            if cursor.fetchone():
                print("Бұл кітап қазір брондалған!")
                continue

            cursor.execute("""
                INSERT INTO Reservations
                    (bookID, readerID, expiry_date, status)
                VALUES
                    (%s, %s, DATE_ADD(NOW(), INTERVAL 24 HOUR),
                     'Брондалды')
            """, (book_id, reader_id))

            conn.commit()
            print("Кітап 24 сағатқа сәтті брондалды!")

        elif choice == "4":
            print("\n===== БРОНДАУЛАР ТІЗІМІ =====")

            cursor.execute("""
                SELECT
                    r.reservationID,
                    b.title,
                    o.fullname,
                    r.reservation_date,
                    r.expiry_date,
                    r.status
                FROM Reservations r
                JOIN Books b ON r.bookID = b.bookID
                JOIN Readers o ON r.readerID = o.readerID
                ORDER BY r.reservationID
            """)

            reservations = cursor.fetchall()

            for reservation in reservations:
                print(
                    f"Бронь ID: {reservation[0]} | "
                    f"Кітап: {reservation[1]} | "
                    f"Оқырман: {reservation[2]} | "
                    f"Брондау уақыты: {reservation[3]} | "
                    f"Мерзімі: {reservation[4]} | "
                    f"Күйі: {reservation[5]}"
                )

        elif choice == "5":
            print("Бағдарлама аяқталды.")
            break

        else:
            print("Қате таңдау!")

    cursor.close()
    conn.close()

except (mysql.connector.Error, ValueError) as e:
    print("Қате:", e)