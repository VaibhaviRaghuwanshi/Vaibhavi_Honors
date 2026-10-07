import csv
import os

class Employee:
    def __init__(self):
        self.file = "employee.csv"

    def add_employee(self):
        emp_id = input("Enter employee id: ")
        name = input("Enter employee name: ")
        salary = input("Enter salary: ")
        department = input("Enter department: ")

        file_exists = os.path.exists(self.file)

        with open(self.file, "a", newline="") as f:
            writer = csv.writer(f)

            if not file_exists:
                writer.writerow(["ID", "Name", "Salary", "Department"])

            writer.writerow([emp_id, name, salary, department])

        print("Employee added successfully!")

    def display_employee(self):
        try:
            with open(self.file, "r") as f:
                reader = csv.reader(f)

                for row in reader:
                    print(row)

        except FileNotFoundError:
            print("File not found.")

    def search_employee(self):
        emp_id = input("Enter employee id to search: ")

        try:
            with open(self.file, "r") as f:
                reader = csv.DictReader(f)

                found = False

                for row in reader:
                    if row["ID"] == emp_id:
                        print(row)
                        found = True

                if not found:
                    print("Employee not found.")

        except FileNotFoundError:
            print("File not found.")

    def update_employee(self):
        emp_id = input("Enter employee id to update: ")

        try:
            with open(self.file, "r") as f:
                rows = list(csv.DictReader(f))

            found = False

            for row in rows:
                if row["ID"] == emp_id:
                    row["Name"] = input("Enter new name: ")
                    row["Salary"] = input("Enter new salary: ")
                    row["Department"] = input("Enter new department: ")
                    found = True

            if found:
                with open(self.file, "w", newline="") as f:
                    fieldnames = ["ID", "Name", "Salary", "Department"]
                    writer = csv.DictWriter(f, fieldnames=fieldnames)

                    writer.writeheader()
                    writer.writerows(rows)

                print("Employee updated successfully!")
            else:
                print("Employee not found.")

        except FileNotFoundError:
            print("File not found.")

    def delete_employee(self):
        emp_id = input("Enter employee id to delete: ")

        try:
            with open(self.file, "r") as f:
                rows = list(csv.DictReader(f))

            new_rows = []
            found = False

            for row in rows:
                if row["ID"] == emp_id:
                    found = True
                else:
                    new_rows.append(row)

            if found:
                with open(self.file, "w", newline="") as f:
                    fieldnames = ["ID", "Name", "Salary", "Department"]
                    writer = csv.DictWriter(f, fieldnames=fieldnames)

                    writer.writeheader()
                    writer.writerows(new_rows)

                print("Employee deleted successfully!")
            else:
                print("Employee not found.")

        except FileNotFoundError:
            print("File not found.")


obj = Employee()

while True:
    print("\n----- Employee Menu -----")
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