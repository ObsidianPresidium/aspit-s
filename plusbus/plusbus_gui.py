import tkinter as tk
import ctypes
from tkinter import ttk, messagebox
import plusbus_sql as pbsql
import plusbus_data as pbd
import plusbus_func as pbf

window_name = "Plusbus Booking Management App"
even_row_color = "#cccccc"
odd_row_color = "#dddddd"
treeview_background = "#eeeeee"
treeview_foreground = "black"
treeview_selected = "#209bef"
row_height = 24

ctypes.windll.shcore.SetProcessDpiAwareness(1)
main_window = tk.Tk()
main_window.title(window_name)
# main_window.resizable(False, False)
padx=8
pady=4

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background=treeview_background, foreground=treeview_foreground, rowheight=row_height, fieldbackground=treeview_background)
style.map("Treeview", background=[("selected", treeview_selected)])

categories = []

class Category:
    def __init__(self, category_name):
        # region globals
        self.entries = []
        self.category_name = category_name
        self.classparam = eval("pbd." + category_name.capitalize())
        # endregion globals

        # region gui
        self.root_frame = tk.LabelFrame(main_window, text=category_name.capitalize())
        self.root_frame.grid(row=0, column=len(categories), padx=padx, pady=pady)

        self.tree_frame = tk.Frame(self.root_frame)
        self.tree_frame.grid(row=0, column=0, padx=padx, pady=pady)
        self.tree_scroll = tk.Scrollbar(self.tree_frame)
        self.tree_scroll.grid(row=0, column=1, padx=padx, pady=pady, sticky="ns")
        self.tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll.set, selectmode="browse")
        self.tree.grid(row=0, column=0, padx=0, pady=pady)
        self.tree_scroll.config(command=self.tree.yview)
        self.tree.tag_configure("oddrow", background=odd_row_color)
        self.tree.tag_configure("evenrow", background=even_row_color)
        self.tree.bind("<ButtonRelease-1>", lambda event: self.edit_tree(event))
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.heading("#0", text="", anchor=tk.W)

        self.controls_frame = tk.Frame(self.root_frame)
        self.controls_frame.grid(row=1, column=0, padx=padx, pady=pady)

        self.edit_frame = tk.Frame(self.controls_frame)
        self.edit_frame.grid(row=0, column=0, padx=padx, pady=pady)

        self.button_frame = tk.Frame(self.controls_frame)
        self.button_frame.grid(row=2, column=0, padx=padx, pady=pady)
        self.button_create = tk.Button(self.button_frame, text="Create", command=self.create)
        self.button_create.grid(row=0, column=0, padx=padx, pady=pady)
        self.button_update = tk.Button(self.button_frame, text="Update", command=self.update)
        self.button_update.grid(row=0, column=1, padx=padx, pady=pady)
        self.button_delete = tk.Button(self.button_frame, text="Delete", command=self.delete)
        self.button_delete.grid(row=0, column=2, padx=padx, pady=pady)
        self.button_clear = tk.Button(self.button_frame, text="Clear Entry Boxes", command=self.clear_entries)
        self.button_clear.grid(row=0, column=3, padx=padx, pady=pady)
        # endregion gui

        categories.append(self)

    def read_entries(self):
        out_tuple = ()
        for entry in self.entries:
            out_tuple += (entry.get(),)

        return out_tuple

    def write_entries(self, values):
        if len(values) != 0:
            if len(values) != len(self.entries):
                raise ValueError("There are either too many or too few values to insert into the entries in this category")
            for entry in enumerate(self.entries):
                entry[1].insert(0, values[entry[0]])

    def clear_entries(self):
        for entry in self.entries:
            entry.delete(0, tk.END)

    def edit_tree(self, event):
        index_selected = self.tree.focus()
        values = self.tree.item(index_selected, "values")
        self.clear_entries()
        self.write_entries(values)

    def read_table(self):
        count = 0
        result = pbsql.select_all(self.classparam)
        for record in result:
            if record.valid():
                if count % 2 == 0:
                    self.tree.insert(parent="", index="end", iid=str(count), text="", values=record.convert_to_tuple(),
                                     tags=("evenrow",))
                else:
                    self.tree.insert(parent="", index="end", iid=str(count), text="", values=record.convert_to_tuple(),
                                     tags=("oddrow",))
                count += 1

    def empty_tree(self):
        self.tree.delete(*self.tree.get_children())

    def refresh_tree(self):
        self.empty_tree()
        self.read_table()

    def create(self):
        record = pbd.convert_from_tuple(self.classparam, self.read_entries())
        if record.valid():
            pbsql.create_record(record)
            self.clear_entries()
            self.refresh_tree()
        else:
            messagebox.showwarning(window_name, "Either the Surname, Capacity, or Number of Passengers is missing or negative.")

    def update(self):
        test_record = pbd.convert_from_tuple(self.classparam, self.read_entries())
        if test_record.valid():
            pbsql.update_record(self.classparam, self.read_entries())
            self.refresh_tree()
        else:
            messagebox.showwarning(window_name,"Either the Surname, Capacity, or Number of Passengers is missing or negative.")

    def delete(self):
        pbsql.delete_soft(self.classparam, self.read_entries())
        self.clear_entries()
        self.refresh_tree()

class CategoryCustomer(Category):
    def __init__(self):
        super().__init__("customer")
        self.tree["columns"] = ("id", "name", "phone")
        self.tree.column("id", anchor=tk.W, width=40)
        self.tree.column("name", anchor=tk.W, width=150)
        self.tree.column("phone", anchor=tk.W, width=100)
        self.tree.heading("id", text="Id", anchor=tk.CENTER)
        self.tree.heading("name", text="Surname", anchor=tk.CENTER)
        self.tree.heading("phone", text="Phone No.", anchor=tk.CENTER)

        label_id = tk.Label(self.edit_frame, text="Id")
        label_id.grid(row=0, column=0, padx=padx, pady=pady)
        label_name = tk.Label(self.edit_frame, text="Surname")
        label_name.grid(row=0, column=1, padx=padx, pady=pady)
        label_phone = tk.Label(self.edit_frame, text="Phone No.")
        label_phone.grid(row=0, column=2, padx=padx, pady=pady)
        entry_id = tk.Entry(self.edit_frame, width=4)
        entry_id.grid(row=1, column=0, padx=padx, pady=pady)
        entry_name = tk.Entry(self.edit_frame, width=12)
        entry_name.grid(row=1, column=1, padx=padx, pady=pady)
        entry_phone = tk.Entry(self.edit_frame, width=10)
        entry_phone.grid(row=1, column=2, padx=padx, pady=pady)

        self.entries = [entry_id, entry_name, entry_phone]

class CategoryTrip(Category):
    def __init__(self):
        super().__init__("trip")
        self.tree["columns"] = ("id", "route", "departure", "capacity")
        self.tree.column("id", anchor=tk.W, width=40)
        self.tree.column("route", anchor=tk.W, width=120)
        self.tree.column("departure", anchor=tk.W, width=80)
        self.tree.column("capacity", anchor=tk.W, width=60)
        self.tree.heading("id", text="Id", anchor=tk.CENTER)
        self.tree.heading("route", text="Route", anchor=tk.CENTER)
        self.tree.heading("departure", text="Departure Time", anchor=tk.CENTER)
        self.tree.heading("capacity", text="Capacity", anchor=tk.CENTER)

        label_id = tk.Label(self.edit_frame, text="Id")
        label_id.grid(row=0, column=0, padx=padx, pady=pady)
        label_route = tk.Label(self.edit_frame, text="Route")
        label_route.grid(row=0, column=1, padx=padx, pady=pady)
        label_departure = tk.Label(self.edit_frame, text="Departure Time")
        label_departure.grid(row=0, column=2, padx=padx, pady=pady)
        label_capacity = tk.Label(self.edit_frame, text="Capacity")
        label_capacity.grid(row=0, column=3, padx=padx, pady=pady)
        entry_id = tk.Entry(self.edit_frame, width=4)
        entry_id.grid(row=1, column=0, padx=padx, pady=pady)
        entry_route = tk.Entry(self.edit_frame, width=12)
        entry_route.grid(row=1, column=1, padx=padx, pady=pady)
        entry_departure = tk.Entry(self.edit_frame, width=12)
        entry_departure.grid(row=1, column=2, padx=padx, pady=pady)
        entry_capacity = tk.Entry(self.edit_frame, width=8)
        entry_capacity.grid(row=1, column=3, padx=padx, pady=pady)

        self.entries = [entry_id, entry_route, entry_departure, entry_capacity]


class CategoryBookings(Category):
    def __init__(self):
        super().__init__("booking")
        self.root_frame.configure(text="Bookings")
        self.tree["columns"] = ("id", "customer_id", "trip_id", "num_passengers")
        self.tree.column("id", anchor=tk.W, width=80)
        self.tree.column("customer_id", anchor=tk.W, width=80)
        self.tree.column("trip_id", anchor=tk.W, width=80)
        self.tree.column("num_passengers", anchor=tk.W, width=80)
        self.tree.heading("id", text="Id", anchor=tk.CENTER)
        self.tree.heading("customer_id", text="Customer Id", anchor=tk.CENTER)
        self.tree.heading("trip_id", text="Trip Id", anchor=tk.CENTER)
        self.tree.heading("num_passengers", text="Passengers", anchor=tk.CENTER)

        label_id = tk.Label(self.edit_frame, text="Id")
        label_id.grid(row=0, column=0, padx=padx, pady=pady)
        label_customer_id = tk.Label(self.edit_frame, text="Customer Id")
        label_customer_id.grid(row=0, column=1, padx=padx, pady=pady)
        label_trip_id = tk.Label(self.edit_frame, text="Trip Id")
        label_trip_id.grid(row=0, column=2, padx=padx, pady=pady)
        label_num_passengers = tk.Label(self.edit_frame, text="Passengers")
        label_num_passengers.grid(row=0, column=3, padx=padx, pady=pady)
        entry_id = tk.Entry(self.edit_frame, width=4)
        entry_id.grid(row=1, column=0, padx=padx, pady=pady)
        entry_customer_id = tk.Entry(self.edit_frame, width=4)
        entry_customer_id.grid(row=1, column=1, padx=padx, pady=pady)
        entry_trip_id = tk.Entry(self.edit_frame, width=4)
        entry_trip_id.grid(row=1, column=2, padx=padx, pady=pady)
        entry_num_passengers = tk.Entry(self.edit_frame, width=6)
        entry_num_passengers.grid(row=1, column=3, padx=padx, pady=pady)

        self.entries = [entry_id, entry_customer_id, entry_trip_id, entry_num_passengers]

    def check_and_return_booking(self):
        entries = self.read_entries()
        if pbf.space_for_input_passengers(entries[3], entries[2]):
            return pbd.convert_from_tuple(pbd.Booking, entries)
        else:
            messagebox.showwarning(window_name, "There is not enough capacity on this trip for these passengers!")

    def create(self):
        pbsql.create_record(self.check_and_return_booking())
        self.clear_entries()
        self.refresh_tree()

    def update(self):
        pbsql.update_record(pbd.Booking, self.check_and_return_booking().convert_to_tuple())
        self.clear_entries()
        self.refresh_tree()

customer = CategoryCustomer()
trip = CategoryTrip()
bookings = CategoryBookings()

if __name__ == "__main__":
    for category in categories:
        category.refresh_tree()

    main_window.mainloop()