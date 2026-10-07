import sqlite3

class Employee:
    def __init__(self):
        self.con = sqlite3.connect("employee.db")
        self.cur = self.con.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS employee(
            id INTEGER PRIMARY KEY,
            name TEXT,
            salary REAL,
            department TEXT
        )
        """)

        self.con.commit()

    def add_employee(self):
        emp_id = int(input("Enter employee id: "))
        name = input("Enter employee name: ")
        salary = float(input("Enter salary: "))
        department = input("Enter department: ")

        self.cur.execute(
            "INSERT INTO employee VALUES (?, ?, ?, ?)",
            (emp_id, name, salary, department)
        )

        self.con.commit()
        print("Employee added successfully!")

    def display_employee(self):
        self.cur.execute("SELECT * FROM employee")
        rows = self.cur.fetchall()

        if len(rows) == 0:
            print("No employee records found.")
        else:
            for row in rows:
                print(row)

    def search_employee(self):
        emp_id = int(input("Enter employee id to search: "))

        self.cur.execute(
            "SELECT * FROM employee WHERE id = ?",
            (emp_id,)
        )

        row = self.cur.fetchone()

        if row:
            print(row)
        else:
            print("Employee not found.")

    def update_employee(self):
        emp_id = int(input("Enter employee id to update: "))

        name = input("Enter new name: ")
        salary = float(input("Enter new salary: "))
        department = input("Enter new department: ")

        self.cur.execute("""
        UPDATE employee
        SET name = ?, salary = ?, department = ?
        WHERE id = ?
        """, (name, salary, department, emp_id))

        self.con.commit()

        if self.cur.rowcount > 0:
            print("Employee updated successfully!")
        else:
            print("Employee not found.")

    def delete_employee(self):
        emp_id = int(input("Enter employee id to delete: "))

        self.cur.execute(
            "DELETE FROM employee WHERE id = ?",
            (emp_id,)
        )

        self.con.commit()

        if self.cur.rowcount > 0:
            print("Employee deleted successfully!")
        else:
            print("Employee not found.")


obj = Employee()

while True:
    print("\n----- Employee Database -----")
    print("1. Add Employee")
    print("2. Display Employees")
    print("3. Search Employee")
    print("4. Update Employee")
    print("5. Delete Employee")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        obj.add_employee()

    elif choice == "2":
        obj.display_employee()

    elif choice == "3":
        obj.search_employee()

    elif choice == "4":
        obj.update_employee()

    elif choice == "5":
        obj.delete_employee()

    elif choice == "6":
        print("Program ended.")
        break

    else:
        print("Invalid choice.")