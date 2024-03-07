import mysql.connector
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="manager",
  database="LibraryManagement"
)

mycursor = mydb.cursor()

def menu():
    print("************************Menu************************")
    print("1.Add new book")
    print("2.Add new student")
    print("3.Show all books and quantity")
    print("4.Show all student")
    print("5.search book")
    print("6.Search student")
    print("7.Issue new book")
    print("8.List of student those are not return book in  15 days")
    print("9.Return book")
    print("10.Exit")
    n = int(input("Select your choice :=  "))
    print("*****************************************************")
    return n
def addBook():
    bookname = input("Enter Book name := ")
    authername = input("Enter Auther name := ")
    catogery = input("Enter category of book := ")
    quantity = int(input("Enter Quantity of books := "))

    sql = "select BooksId from Books where BookName = %s and AuthorName = %s"
    val = (bookname,authername)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchone()
    if mycursor.rowcount:
        (id,) = myresult
        sql = "UPDATE Books SET Quantity = %s + Quantity  WHERE BooksId = %s"
        val = (quantity,id)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Book is already available quantity added in inventory")
    else:
        sql = "INSERT INTO Books (BookName, AuthorName, Category, Quantity) VALUES (%s, %s, %s,%s)"
        val = (bookname, authername, catogery,quantity)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Book Added successfully")


def addStudent():
    name = input("Enter Student name := ")
    standard = int(input("Enter standard := "))
    mobileno = input("Enter mobile number := ")

    sql = "select StudentId from Student where StudentName = %s and MobileNo = %s"
    val = (name, mobileno)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchone()
    if mycursor.rowcount:
        (id,) = myresult
        print(f"Student already Exist with id : {id}")
    else:
        sql = "INSERT INTO Student (StudentName, Standard, MobileNo) VALUES (%s, %s, %s)"
        val = (name,standard,mobileno)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Student Added successfully")


def showAllBookAndQuantity():
    id_width = 5
    name_width = 30
    quantity_width = 12

    mycursor.execute("select BooksId , BookName, Quantity from Books")
    myresult = mycursor.fetchall()

    print(f"|{'ID':<{id_width}}|{'Book Name':<{name_width}}|{'Quantity':<{quantity_width}}|")
    for row in myresult:
        print(f"|{row[0]:<{id_width}}|{row[1]:<{name_width}}|{row[2]:<{quantity_width}}|")

def showAllStudent():
    id_width = 5
    name_width = 12
    standard_width = 9
    mobile_width = 12

    mycursor.execute("select * from Student")
    myresult = mycursor.fetchall()

    print(f"|{'ID':<{id_width}}|{'StudentName':<{name_width}}|{'Standard':<{standard_width}}|{'MobileNo':<{mobile_width}}|")
    for row in myresult:
        print(f"|{row[0]:<{id_width}}|{row[1]:<{name_width}}|{row[2]:<{standard_width}}|{row[3]:<{mobile_width}}|")

def searchBook():
    pattern = input("Enter name to search := ")
    sql = "select BooksId , BookName from Books where BookName like %s"
    val = "%" + pattern + "%",
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()

    id_width = 5
    name_width = 20
    print(f"|{'ID':<{id_width}}|{'BookName':<{name_width}}|")
    for row in myresult:
        print(f"|{row[0]:<{id_width}}|{row[1]:<{name_width}}|")

def searchStudent():
    print("1.Search by name")
    print("2.Search by Student id")
    n = int(input("Enter your choice := "))

    id_width = 5
    name_width = 12
    standard_width = 9
    mobile_width = 12

    if n == 1:
        name = input("Enter Student name:= ")
        sql = "select * from Student where StudentName = %s "
        val = name,
        mycursor.execute(sql,val)
        myresult = mycursor.fetchall()

        if mycursor.rowcount :
            print(f"|{'ID':<{id_width}}|{'StudentName':<{name_width}}|"
                  f"{'Standard':<{standard_width}}|{'MobileNo':<{mobile_width}}|")
            for row in myresult:
                print(f"|{row[0]:<{id_width}}|{row[1]:<{name_width}}|{row[2]:<{standard_width}}|"
                      f"{row[3]:<{mobile_width}}|")
        else:
            print(f"Student {name} is not exist")
    elif n == 2:
        id = int(input("Enter ID of student := "))
        sql = "select * from Student where StudentId = %s"
        val = id,
        mycursor.execute(sql,val)
        mysesult = mycursor.fetchone()

        if mycursor.rowcount:
            sid, name,std,mobno = mysesult
            print(f"Id = {sid}")
            print(f"Name = {name}")
            print(f"Standard = {std}")
            print(f"Mobile Number = {mobno}")
        else:
            print(f"Student with id {id} is not exist")
    else:
        print("Wrong choice")

def issueNewBook():
    bookid = int(input("Enter Book Id := "))
    studentid = int(input("Enter Student Id := "))
    sql = "select 1 from Student where StudentId = %s"
    val = studentid,
    mycursor.execute(sql, val)
    myres = mycursor.fetchall()
    if mycursor.rowcount:
        sql = "select BookName from Books where BooksId = %s and Quantity > 0"
        val = bookid,
        mycursor.execute(sql, val)
        if len(mycursor.fetchall()) > 0:
            sql = "select IssueDate from Transaction where StudentId = %s and BooksId = %s and ReturnDate is NULL "
            val = (studentid, bookid)
            mycursor.execute(sql, val)
            myresult = mycursor.fetchall()
            if len(myresult)>0:

                print(f"Student already issue book on date : {myresult}")
            else:
                sql = "INSERT INTO Transaction (StudentId, BooksId, IssueDate) VALUES (%s, %s, CURDATE())"
                val = (studentid, bookid)
                mycursor.execute(sql, val)
                mydb.commit()
                mycursor.nextset()
                print("Book Issue Successfully")

                sql = "UPDATE Books SET Quantity = Quantity - 1 WHERE BooksId = %s"
                val = bookid,
                mycursor.execute(sql, val)
                mydb.commit()
                mycursor.nextset()
        else:
            print("Sorry book is not available")
            mycursor.nextset()
    else:
        print(f"student with ID {studentid} is not available")
        mycursor.nextset()

def studentWhoNotReturnBookIn15Days():
    mycursor.execute("SELECT TransactionId,StudentId,BooksId,IssueDate FROM Transaction WHERE DATEDIFF(CURDATE(),IssueDate) > 15 and ReturnDate is  NULL")
    myresult = mycursor.fetchall()

    tid_width = 14
    sid_width = 14
    bid_width = 14
    date_width = 12

    print(f"|{'TransactionId':<{tid_width}}|{'StudentId':<{sid_width}}|{'BooksId':<{bid_width}}|{'IssueDate':<{date_width}}|")
    for row in myresult:
        print(f"|{row[0]:<{tid_width}}|{row[1]:<{sid_width}}|{row[2]:<{bid_width}}|{row[3]:<{date_width}}|")

def returnBook():
    sid = int(input("Enter Student ID := "))
    bid = int(input("Enter Book ID := "))
    sql = "select TransactionId from Transaction where StudentId = %s and BooksId = %s and ReturnDate is NULL "
    val = (sid,bid)
    mycursor.execute(sql,val)
    if len(mycursor.fetchall()) >0:
        sql = "UPDATE Transaction SET ReturnDate = CURDATE() WHERE StudentId = %s and BooksId = %s "
        val = (sid,bid)
        mycursor.execute(sql,val)
        mydb.commit()
        print("Book return Successfully")
        sql = "UPDATE Books SET Quantity = Quantity + 1 WHERE BooksId = %s"
        val = bid,
        mycursor.execute(sql,val)
        mydb.commit()
    else:
        print("Record not found ")

while (True):
    choice = menu()
    if choice == 1:
        addBook()

    elif choice == 2:
        addStudent()

    elif choice == 3:
        showAllBookAndQuantity()

    elif choice == 4:
        showAllStudent()

    elif choice == 5:
        searchBook()

    elif choice == 6:
        searchStudent()

    elif choice == 7:
        issueNewBook()

    elif choice == 8:
        studentWhoNotReturnBookIn15Days()

    elif choice == 9:
        returnBook()

    elif choice == 10:
        print("Bye Bye")
        break

    else:
        print("Invalid choice. Please enter a number between 1 and 10.")

mycursor.close()
mydb.close()