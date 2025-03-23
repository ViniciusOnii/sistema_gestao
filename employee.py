import pymongo
from tkinter import *
from tkinter import ttk, messagebox

# Conectar ao MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["employee_management"]
collection = db["employees"]


class EmployeeClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("850x500+300+150")
        self.root.title("Employee Management System")
        self.root.config(bg="white")

        self.create_widgets()
        self.update_table()

    def create_widgets(self):
        Label(self.root, text="Search Employee", font=("Arial", 10, "bold"), bg="white").place(x=20, y=10)

        self.search_by = ttk.Combobox(self.root, values=["Select", "Emp No.", "Name", "Email"], state="readonly")
        self.search_by.place(x=20, y=40, width=120)
        self.search_by.current(0)

        self.search_txt = Entry(self.root, bg="lightyellow")
        self.search_txt.place(x=150, y=40, width=180)

        Button(self.root, text="Search", bg="green", fg="white", command=self.search).place(x=340, y=38, width=80)

        Label(self.root, text="Employee Details", font=("Arial", 12, "bold"), bg="navy", fg="white").place(x=0, y=80, relwidth=1)

        self.fields = ["Emp No.", "Name", "Email", "Address", "Gender", "D.O.B", "Password", "Salary", "Contact No", "D.O.J", "User Type"]

        self.entries = {}
        for idx, field in enumerate(self.fields):
            x = 20 + (idx % 4) * 200
            y = 120 + (idx // 4) * 40

            Label(self.root, text=field, font=("Arial", 10), bg="white").place(x=x, y=y)

            if field in ["Gender", "User Type"]:
                options = ["Select", "Male", "Female"] if field == "Gender" else ["Select", "Admin", "Employee"]
                self.entries[field] = ttk.Combobox(self.root, values=options, state="readonly")
                self.entries[field].current(0)
            else:
                self.entries[field] = Entry(self.root, bg="lightyellow")

            self.entries[field].place(x=x + 80, y=y, width=100)

        Button(self.root, text="Save", command=self.add_employee, bg="blue", fg="white").place(x=300, y=250, width=80)
        Button(self.root, text="Update", command=self.update_employee, bg="green", fg="white").place(x=390, y=250, width=80)
        Button(self.root, text="Delete", command=self.delete_employee, bg="red", fg="white").place(x=480, y=250, width=80)
        Button(self.root, text="Clear", command=self.clear_fields, bg="gray", fg="white").place(x=570, y=250, width=80)

        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=0, y=300, relwidth=1, height=180)

        self.EmployeeTable = ttk.Treeview(emp_frame, columns=self.fields, show="headings")
        self.EmployeeTable.pack(fill=BOTH, expand=1)

        for field in self.fields:
            self.EmployeeTable.heading(field, text=field)
            self.EmployeeTable.column(field, width=100)

        self.EmployeeTable.bind("<ButtonRelease-1>", self.fill_fields)

    def add_employee(self):
        data = {field: self.entries[field].get() for field in self.fields}

        if any(v == "" or v == "Select" for v in data.values()):
            messagebox.showerror("Error", "All fields are required.", parent=self.root)
            return

        collection.insert_one(data)
        messagebox.showinfo("Success", "Employee added successfully.", parent=self.root)
        self.update_table()
        self.clear_fields()

    def update_table(self):
        self.EmployeeTable.delete(*self.EmployeeTable.get_children())
        for emp in collection.find({}, {"_id": 0}):
            self.EmployeeTable.insert("", END, values=tuple(emp.values()))

    def fill_fields(self, event):
        selected = self.EmployeeTable.focus()
        values = self.EmployeeTable.item(selected, "values")

        for idx, field in enumerate(self.fields):
            self.entries[field].delete(0, END)
            self.entries[field].insert(0, values[idx])

    def update_employee(self):
        selected = self.EmployeeTable.focus()
        if not selected:
            messagebox.showerror("Error", "Select an employee to update.", parent=self.root)
            return

        emp_id = self.EmployeeTable.item(selected, "values")[0]
        data = {field: self.entries[field].get() for field in self.fields}

        if any(v == "" or v == "Select" for v in data.values()):
            messagebox.showerror("Error", "All fields are required.", parent=self.root)
            return

        collection.update_one({"Emp No.": emp_id}, {"$set": data})
        messagebox.showinfo("Success", "Employee updated successfully.", parent=self.root)
        self.update_table()
        self.clear_fields()

    def delete_employee(self):
        selected = self.EmployeeTable.focus()
        if not selected:
            messagebox.showerror("Error", "Select an employee to delete.", parent=self.root)
            return

        emp_id = self.EmployeeTable.item(selected, "values")[0]
        collection.delete_one({"Emp No.": emp_id})
        messagebox.showinfo("Success", "Employee deleted successfully.", parent=self.root)
        self.update_table()

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, END)

    def search(self):
        field = self.search_by.get()
        value = self.search_txt.get()

        if field == "Select" or not value:
            messagebox.showerror("Error", "Please select a field and enter a value.", parent=self.root)
            return

        results = collection.find({field: value}, {"_id": 0})

        self.EmployeeTable.delete(*self.EmployeeTable.get_children())
        for emp in results:
            self.EmployeeTable.insert("", END, values=tuple(emp.values()))


if __name__ == "__main__":
    root = Tk()
    app = EmployeeClass(root)
    root.mainloop()
