import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# MySQL connection setup
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="product_management"
    )


def register_user():
    name = name_entry.get()
    contact = contact_entry.get()
    email = email_entry.get()
    gender = gender_var.get()
    city = city_combobox.get()
    state = state_combobox.get()
    role = role_combobox.get()

    if name and contact and email and gender and city and state and role:
        try:
            conn = connect_db()
            cursor = conn.cursor()
            query = """
                INSERT INTO users (name, contact, email, gender, city, state, role) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, contact, email, gender, city, state, role))
            conn.commit()
            cursor.close()
            conn.close()

            # Display success message
            messagebox.showinfo("Success", "Registration successful!")

            # Automatically log the user in and open the respective dashboard
            root.destroy()  # Close the registration window
            if role == "Manager":
                open_manager_dashboard()
            elif role == "Customer":
                open_customer_dashboard()

        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")
    else:
        messagebox.showerror("Error", "All fields are required!")



# Clear Registration Fields
def clear_registration_fields():
    name_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    city_combobox.set("")
    state_combobox.set("")
    gender_var.set("")
    role_combobox.set("")


# Login User Function
def login_user():
    email = email_entry_login.get()
    role = role_combobox_login.get()

    if email and role:
        try:
            conn = connect_db()
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE email=%s AND role=%s"
            cursor.execute(query, (email, role))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            if user:
                messagebox.showinfo("Login Success", f"Welcome {user[1]}!")
                login_window.destroy()  # Close login window
                if role == "Manager":
                    open_manager_dashboard()
                elif role == "Customer":
                    open_customer_dashboard()
            else:
                messagebox.showerror("Error", "Invalid email or role")
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")
    else:
        messagebox.showerror("Error", "All fields are required!")

# Manager Dashboard
def open_manager_dashboard():
    manager_window = tk.Tk()
    manager_window.title("Manager Dashboard")
    manager_window.geometry("600x400")

    tk.Label(manager_window, text="Manager Dashboard", font=("Arial", 16)).pack()

    # Buttons for stock operations
    tk.Button(manager_window, text="View All Stock", command=view_stock).pack(pady=10)
    tk.Button(manager_window, text="Add Stock", command=add_stock).pack(pady=10)
    tk.Button(manager_window, text="Edit Stock", command=edit_stock).pack(pady=10)
    tk.Button(manager_window, text="Delete Stock", command=delete_stock).pack(pady=10)

    manager_window.mainloop()


# Customer Dashboard
def open_customer_dashboard():
    customer_root = tk.Tk()
    customer_root.title("Customer Dashboard")
    customer_root.geometry("600x400")

    # Display all products
    def load_products():
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products")
            rows = cursor.fetchall()
            for i, row in enumerate(rows):
                product_table.insert("", "end", values=row)
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {e}")

    # Add product to the purchase list
    def purchase_product():
        selected_item = product_table.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a product to purchase.")
            return

        selected_product = product_table.item(selected_item[0], "values")
        product_id = selected_product[0]
        product_name = selected_product[1]
        price = selected_product[2]
        quantity = selected_product[3]

        try:
            conn = connect_db()
            cursor = conn.cursor()
            query = "INSERT INTO purchases (product_id, product_name, price, quantity) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (product_id, product_name, price, 1))  # Add 1 quantity by default
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", f"Product '{product_name}' added to your purchase list.")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {e}")

    # Table to display products
    columns = ("Product ID", "Name", "Price", "Quantity")
    product_table = ttk.Treeview(customer_root, columns=columns, show="headings", height=10)
    product_table.heading("Product ID", text="Product ID")
    product_table.heading("Name", text="Name")
    product_table.heading("Price", text="Price")
    product_table.heading("Quantity", text="Quantity")
    product_table.column("Product ID", width=100)
    product_table.column("Name", width=150)
    product_table.column("Price", width=100)
    product_table.column("Quantity", width=100)
    product_table.place(x=50, y=50)

    # Purchase Button
    purchase_button = tk.Button(customer_root, text="Purchase", bg="orange", fg="white", command=purchase_product)
    purchase_button.place(x=250, y=350)

    # Load products into the table
    load_products()

    customer_root.mainloop()



# Stock Operations

def view_stock():
    view_window = tk.Toplevel()
    view_window.title("View All Products")
    view_window.geometry("600x400")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    columns = ("ID", "Name", "Price", "Quantity")
    tree = ttk.Treeview(view_window, columns=columns, show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Price", text="Price")
    tree.heading("Quantity", text="Quantity")
    tree.column("ID", width=50)

    for row in rows:
        tree.insert("", tk.END, values=row)

    tree.pack(fill=tk.BOTH, expand=True)

    # Add Edit and Delete buttons
    tk.Button(view_window, text="Edit Selected", bg="blue", fg="white", command=lambda: edit_stock(tree)).pack(side=tk.LEFT, padx=10, pady=10)
    tk.Button(view_window, text="Delete Selected", bg="red", fg="white", command=lambda: delete_stock(tree)).pack(side=tk.RIGHT, padx=10, pady=10)


def add_stock():
    def save_product():
        name = name_entry.get()
        price = price_entry.get()
        quantity = quantity_entry.get()

        if name and price and quantity:
            try:
                conn = connect_db()
                cursor = conn.cursor()
                query = "INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)"
                cursor.execute(query, (name, float(price), int(quantity)))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Success", "Product added successfully!")
                add_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Database error: {e}")
        else:
            messagebox.showerror("Error", "All fields are required!")

    add_window = tk.Toplevel()
    add_window.title("Add Product")
    add_window.geometry("400x300")

    tk.Label(add_window, text="Product Name", font=("Arial", 12)).place(x=50, y=50)
    name_entry = tk.Entry(add_window, width=30)
    name_entry.place(x=150, y=50)

    tk.Label(add_window, text="Price", font=("Arial", 12)).place(x=50, y=100)
    price_entry = tk.Entry(add_window, width=30)
    price_entry.place(x=150, y=100)

    tk.Label(add_window, text="Quantity", font=("Arial", 12)).place(x=50, y=150)
    quantity_entry = tk.Entry(add_window, width=30)
    quantity_entry.place(x=150, y=150)

    tk.Button(add_window, text="Save", bg="green", fg="white", command=save_product).place(x=150, y=200)

    


def edit_stock(tree):
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror("Error", "No product selected!")
        return

    item_data = tree.item(selected_item, "values")
    product_id, name, price, quantity = item_data

    def update_product():
        new_name = name_entry.get()
        new_price = price_entry.get()
        new_quantity = quantity_entry.get()

        if new_name and new_price and new_quantity:
            try:
                conn = connect_db()
                cursor = conn.cursor()
                query = "UPDATE products SET name=%s, price=%s, quantity=%s WHERE id=%s"
                cursor.execute(query, (new_name, float(new_price), int(new_quantity), product_id))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Success", "Product updated successfully!")
                edit_window.destroy()
                tree.item(selected_item, values=(product_id, new_name, new_price, new_quantity))
            except Exception as e:
                messagebox.showerror("Error", f"Database error: {e}")
        else:
            messagebox.showerror("Error", "All fields are required!")

    edit_window = tk.Toplevel()
    edit_window.title("Edit Product")
    edit_window.geometry("400x300")

    tk.Label(edit_window, text="Product Name", font=("Arial", 12)).place(x=50, y=50)
    name_entry = tk.Entry(edit_window, width=30)
    name_entry.insert(0, name)
    name_entry.place(x=150, y=50)

    tk.Label(edit_window, text="Price", font=("Arial", 12)).place(x=50, y=100)
    price_entry = tk.Entry(edit_window, width=30)
    price_entry.insert(0, price)
    price_entry.place(x=150, y=100)

    tk.Label(edit_window, text="Quantity", font=("Arial", 12)).place(x=50, y=150)
    quantity_entry = tk.Entry(edit_window, width=30)
    quantity_entry.insert(0, quantity)
    quantity_entry.place(x=150, y=150)

    tk.Button(edit_window, text="Update", bg="green", fg="white", command=update_product).place(x=150, y=200)


def delete_stock(tree):
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror("Error", "No product selected!")
        return

    item_data = tree.item(selected_item, "values")
    product_id = item_data[0]

    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this product?"):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            query = "DELETE FROM products WHERE id=%s"
            cursor.execute(query, (product_id,))
            conn.commit()
            cursor.close()
            conn.close()
            tree.delete(selected_item)
            messagebox.showinfo("Success", "Product deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")
            
def view_stock_customer():
    view_window = tk.Toplevel()
    view_window.title("Available Products")
    view_window.geometry("600x400")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, price, quantity FROM products")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    columns = ("Name", "Price", "Quantity")
    tree = ttk.Treeview(view_window, columns=columns, show="headings")
    tree.heading("Name", text="Name")
    tree.heading("Price", text="Price")
    tree.heading("Quantity", text="Quantity")

    for row in rows:
        tree.insert("", tk.END, values=row)

    tree.pack(fill=tk.BOTH, expand=True)

    # Purchase button
    tk.Button(view_window, text="Purchase", bg="green", fg="white", command=lambda: purchase_stock(tree)).pack(pady=10)



def purchase_stock():
    messagebox.showinfo("Purchase Stock", "Purchase stock functionality here!")


# Open Login Window
def open_login_window():
    global login_window, email_entry_login, role_combobox_login

    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("400x300")

    tk.Label(login_window, text="Login", font=("Arial", 16)).pack()

    # Email
    tk.Label(login_window, text="Email", font=("Arial", 12)).place(x=50, y=80)
    email_entry_login = tk.Entry(login_window, width=30)
    email_entry_login.place(x=150, y=80)

    # Role
    tk.Label(login_window, text="Role", font=("Arial", 12)).place(x=50, y=120)
    role_combobox_login = ttk.Combobox(login_window, values=["Manager", "Customer"], width=27)
    role_combobox_login.place(x=150, y=120)

    # Login Button
    tk.Button(login_window, text="Login", command=login_user).place(x=150, y=180)

    login_window.mainloop()


# GUI for Registration
root = tk.Tk()
root.title("Product Management - Registration")
root.geometry("400x550")

tk.Label(root, text="Registration", font=("Arial", 16)).pack()

# Name
tk.Label(root, text="Name").place(x=50, y=50)
name_entry = tk.Entry(root, width=30)
name_entry.place(x=150, y=50)

# Contact
tk.Label(root, text="Contact").place(x=50, y=90)
contact_entry = tk.Entry(root, width=30)
contact_entry.place(x=150, y=90)

# Email
tk.Label(root, text="Email").place(x=50, y=130)
email_entry = tk.Entry(root, width=30)
email_entry.place(x=150, y=130)

# Gender
tk.Label(root, text="Gender").place(x=50, y=170)
gender_var = tk.StringVar()
tk.Radiobutton(root, text="Male", variable=gender_var, value="Male").place(x=150, y=170)
tk.Radiobutton(root, text="Female", variable=gender_var, value="Female").place(x=220, y=170)

# City
tk.Label(root, text="City").place(x=50, y=210)
city_combobox = ttk.Combobox(root, values=["City1", "City2", "City3"], width=27)
city_combobox.place(x=150, y=210)

# State
tk.Label(root, text="State").place(x=50, y=250)
state_combobox = ttk.Combobox(root, values=["State1", "State2", "State3"], width=27)
state_combobox.place(x=150, y=250)

# Role
tk.Label(root, text="Role").place(x=50, y=290)
role_combobox = ttk.Combobox(root, values=["Manager", "Customer"], width=27)
role_combobox.place(x=150, y=290)

# Register Button
tk.Button(root, text="Register", command=register_user).place(x=150, y=350)

# Login Link
tk.Button(root, text="Already registered? Login here", command=open_login_window).place(x=120, y=400)

root.mainloop()
