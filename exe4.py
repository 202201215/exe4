import sqlite3

# 连接到数据库
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# 创建Books表
cursor.execute('''CREATE TABLE IF NOT EXISTS Books 
                  (BookID INTEGER PRIMARY KEY AUTOINCREMENT,
                   Title TEXT,
                   Author TEXT,
                   ISBN TEXT,
                   Status INTEGER)''')

# 创建Users表
cursor.execute('''CREATE TABLE IF NOT EXISTS Users
                  (UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                   Name TEXT,
                   Email TEXT)''')

# 创建Reservations表
cursor.execute('''CREATE TABLE IF NOT EXISTS Reservations
                  (ReservationID INTEGER PRIMARY KEY AUTOINCREMENT,
                   BookID INTEGER,
                   UserID INTEGER,
                   FOREIGN KEY(BookID) REFERENCES Books(BookID),
                   FOREIGN KEY(UserID) REFERENCES Users(UserID))''')

# 向数据库中添加一本新书
def add_book(title, author, isbn, status):
    cursor.execute("INSERT INTO Books (Title, Author, ISBN, Status) VALUES (?, ?, ?, ?)",
                   (title, author, isbn, status))
    conn.commit()
    print("成功添加一本新书！")

# 在BookID上查找一本书的详细信息
def find_book_details(book_id):
    cursor.execute("SELECT Books.*, Users.* FROM Books LEFT JOIN Reservations ON Books.BookID = Reservations.BookID LEFT JOIN Users ON Reservations.UserID = Users.UserID WHERE Books.BookID = ?", (book_id,))
    result = cursor.fetchone()
    if result:
        print("书的详细信息：")
        print("BookID:", result[0])
        print("Title:", result[1])
        print("Author:", result[2])
        print("ISBN:", result[3])
        print("Status:", result[4])
        print("预订状态:", "已预订" if result[5] else "未预订")
        if result[5]:
            print("用户信息：")
            print("UserID:", result[6])
            print("Name:", result[7])
            print("Email:", result[8])
    else:
        print("未找到该书的详细信息。")

# 根据BookID、Title、UserID和ReservationID查找图书的预订状态
def find_reservation_status(input_text):
    if input_text.startswith("LB ):
        book_id = input_text[2:]
        cursor.execute("SELECT Status FROM Books WHERE BookID = ?", (book_id,))
        result = cursor.fetchone()
        if result:
            print("书的预订状态：", "已预订" if result[0] else "未预订")
        else:
            print("未找到该书的预订状态。")
    elif input_text.startswith("LU"):
        user_id = input_text[2:]
        cursor.execute("SELECT Status FROM Reservations WHERE UserID = ?", (user_id,))
        result = cursor.fetchone()
        if result:
            print("该用户的预订状态：", "已预订" if result[0] else "未预订")
        else:
            print("该用户没有进行过预订。")
    elif input_text.startswith("LR"):
        reservation_id = input_text[2:]
        cursor.execute("SELECT Status FROM Reservations WHERE ReservationID = ?", (reservation_id,))
        result = cursor.fetchone()
        if result:
            print("预订状态：", "已预订" if result[0] else "未预订")
        else:
            print("未找到该预订信息。")
    else:
        title = input_text
        cursor.execute("SELECT Books.*, Users.* FROM Books LEFT JOIN Reservations ON Books.BookID = Reservations.BookID LEFT JOIN Users ON Reservations.UserID = Users.UserID WHERE Books.Title = ?", (title,))
        result = cursor.fetchall()
        if result:
            print("找到以下书的详细信息：")
            for row in result:
                print("BookID:", row[0])
                print("Title:", row[1])
                print("Author:", row[2])
                print("ISBN:", row[3])
                print("Status:", row[4])
                print("预订状态:", "已预订" if row[5] else "未预订")
                if row[5]:
                    print("用户信息：")
                    print("UserID:", row[6])
                    print("Name:", row[7])
                    print("Email:", row[8])
                    print()
        else:
            print("未找到与该标题相关的书籍。")

# 在数据库中找到所有的书
def find_all_books():
    cursor.execute("SELECT Books.*, Users.*, Reservations.ReservationID FROM Books \
                    LEFT JOIN Reservations ON Books.BookID = Reservations.BookID \
                    LEFT JOIN Users ON Reservations.UserID = Users.UserID")
    result = cursor.fetchall()
    if result:
        print("所有书的详细信息：")
        for row in result:
            print("BookID:", row[0])
            print("Title:", row[1])
            print("Author:", row[2])
            print("ISBN:", row[3])
            print("Status:", row[4])
            print("预订状态:", "已预订" if row[5] else "未预订")
            if row[5]:
                print("用户信息：")
                print("UserID:", row[6])
                print("Name:", row[7])
                print("Email:", row[8])
                print("ReservationID:", row[9])
            print()
    else:
        print("数据库中没有书籍。")

# 修改/更新图书的详细信息
def update_book_details(book_id, title=None, author=None, isbn=None, status=None):
    if title:
            cursor.execute("UPDATE Books SET Title = ? WHERE BookID = ?", (title, book_id))
        conn.commit()
    if author:
        cursor.execute("UPDATE Books SET Author = ? WHERE BookID = ?", (author, book_id))
        conn.commit()
    if isbn:
        cursor.execute("UPDATE Books SET ISBN = ? WHERE BookID = ?", (isbn, book_id))
        conn.commit()
    if status:
        cursor.execute("UPDATE Books SET Status = ? WHERE BookID = ?", (status, book_id))
        conn.commit()
    print("图书详细信息已更新。")

# 基于bookkid删除图书
def delete_book(book_id):
    cursor.execute("SELECT * FROM Reservations WHERE BookID = ?", (book_id,))
    reservation_result = cursor.fetchone()
    if reservation_result:
        cursor.execute("DELETE FROM Reservations WHERE BookID = ?", (book_id,))
        conn.commit()
    cursor.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))
    conn.commit()
    print("图书已删除。")

# 进行交互操作
while True:
    choice = input("请输入操作选项：\n1. 添加一本新书\n2. 查找一本书的详细信息\n3. 查找图书的预订状态\n4. 找到所有的书\n5. 修改/更新图书的详细信息\n6. 删除图书\n>")
    
    if choice == "1":
        title = input("请输入书名：")
        author = input("请输入作者：")
        isbn = input("请输入ISBN号��：")
        status = input("请输入预订状态（0代表未预订，1代表已预订）：")
        add_book(title, author, isbn, status)
    
    elif choice == "2":
        book_id = input("请输入BookID：")
        find_book_details(book_id)
    
    elif choice == "3":
        input_text = input("请输入BookID、UserID、ReservationID或者Title：")
        find_reservation_status(input_text)
    
    elif choice == "4":
        find_all_books()
    
    elif choice == "5":
        book_id = input("请输入要修改的图书的BookID：")
        title = input("请输入新的书名（如果不需要更新，请按回车键跳过）：")
        author = input("请输入新的作者（如果不需要更新，请按回车键跳过）：")
        isbn = input("请输入新的ISBN号码（如果不需要更新，请按回车键跳过）：")
        status = input("请输入新的预订状态（0代表未预订，1代表已预订；如果不需要更新，请按回车键跳过）：")
        update_book_details(book_id, title, author, isbn, status)
    
    elif choice == "6":
        book_id = input("请输入要删除的图书的BookID：")
        delete_book(book_id)
    
    else:
        print("无效的选择。请重新选择。")
    
    continue_ = input("是否继续操作？（输入Y继续，其他键退出）")
    if continue_.lower() != "y":
        break

# 关闭数据库连接
conn.close()