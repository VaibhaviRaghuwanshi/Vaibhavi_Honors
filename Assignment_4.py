import sqlite3

con = sqlite3.connect("employee.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS employee(
    id INTEGER PRIMARY KEY,
    name TEXT,
    salary REAL,
    department TEXT
)
""")

con.commit()

while True:

    print("\n===== EMPLOYEE MENU =====")
    print("1. Insert Employee")
    print("2. Display Employees")
    print("3. Search Employee")
    print("4. Update Employee")
    print("5. Delete Employee")
    print("6. Exit")

    choice = input("Enter choice: ")

    if choice == "1":

        id = int(input("Enter id: "))
        name = input("Enter name: ")
        salary = float(input("Enter salary: "))
        department = input("Enter department: ")

        cur.execute(
            "INSERT INTO employee VALUES (?, ?, ?, ?)",
            (id, name, salary, department)
        )

        con.commit()
        print("Record inserted.")

    elif choice == "2":

        cur.execute("SELECT * FROM employee")
        data = cur.fetchall()

        if data:
            for row in data:
                print(row)
        else:
            print("No records found.")

    elif choice == "3":

        id = int(input("Enter id to search: "))

        cur.execute(
            "SELECT * FROM employee WHERE id = ?",
            (id,)
        )

        data = cur.fetchone()

        if data:
            print(data)
        else:
            print("Employee not found.")

    elif choice == "4":

        id = int(input("Enter id to update: "))

        name = input("Enter new name: ")
        salary = float(input("Enter new salary: "))
        department = input("Enter new department: ")

        cur.execute("""
        UPDATE employee
        SET name = ?, salary = ?, department = ?
        WHERE id = ?
        """, (name, salary, department, id))

        con.commit()

        if cur.rowcount > 0:
            print("Record updated.")
        else:
            print("Employee not found.")

    elif choice == "5":

        id = int(input("Enter id to delete: "))

        cur.execute(
            "DELETE FROM employee WHERE id = ?",
            (id,)
        )

        con.commit()

        if cur.rowcount > 0:
            print("Record deleted.")
        else:
            print("Employee not found.")

    elif choice == "6":

        print("Thank you!")
        break

    else:
        print("Wrong choice.")

con.close()