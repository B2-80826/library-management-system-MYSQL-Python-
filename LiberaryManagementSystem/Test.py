import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="manager",
    database="LibraryManagement"
)
mycursor = mydb.cursor()


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




n = 1
while n != 0:
    issueNewBook()
    n = int(input("Final"))

mycursor.close()
mydb.close()