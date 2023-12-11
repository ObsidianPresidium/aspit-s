import tkinter as tk
import ctypes
from tkinter import ttk
from tkinter import messagebox
import danskcargo_sql as dcsql
import danskcargo_data as dcd
import danskcargo_func as dcf


window_name = "Danskcargo Container App"
even_row_color = "#cccccc"
odd_row_color = "#dddddd"
treeview_background = "#eeeeee"
treeview_foreground = "black"
treeview_selected = "#206030"
row_height = 24

ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Blurry display fix for Windows when display scaling is not 100%
main_window = tk.Tk()
main_window.title(window_name)
main_window.resizable(False, False)
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
        self.classparam = eval("dcd." + category_name.capitalize())
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
            if self.classparam != dcd.Container:  # containers have the weather entry also, we need to circumvent an error
                if len(values) != len(self.entries):
                    raise ValueError("There are either too many or too few values to insert into the entries in this category!")

                for entry in enumerate(self.entries):
                    entry[1].insert(0, values[entry[0]])
            else:
                self.entries[0].insert(0, values[0])
                self.entries[1].insert(0, values[1])
                self.entries[2].insert(0, values[2])

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
        result = dcsql.select_all(self.classparam)
        for record in result:
            if record.valid():
                if count % 2 == 0:
                    self.tree.insert(parent="", index="end", iid=str(count), text="", values=record.convert_to_tuple(), tags=("evenrow",))
                else:
                    self.tree.insert(parent="", index="end", iid=str(count), text="", values=record.convert_to_tuple(), tags=("oddrow",))
                count += 1

    def empty_tree(self):
        self.tree.delete(*self.tree.get_children())

    def refresh_tree(self):
        self.empty_tree()
        self.read_table()

    def create(self):
        record = dcd.convert_from_tuple(self.classparam, self.read_entries())
        if record.valid():
            dcsql.create_record(record)
            self.clear_entries()
            self.refresh_tree()
        else:
            messagebox.showwarning(window_name, "Either the Weight, Capacity, or Aircraft Id is missing or negative.")

    def update(self):
        test_record = dcd.convert_from_tuple(self.classparam, self.read_entries())
        if test_record.valid():
            dcsql.update_record(self.classparam, self.read_entries())
            self.refresh_tree()
        else:
            messagebox.showwarning(window_name, "Either the Weight, Capacity, or Aircraft Id is missing or negative.")

    def delete(self):
        transport_conflict = dcf.get_transport_conflict(self.classparam, int(self.entries[0].get()))
        if transport_conflict:
            messagebox.showwarning(window_name, f"Transport with id {transport_conflict.id} depends on this container or aircraft. Delete that transport first before deleting this record.")
        else:
            dcsql.delete_soft(self.classparam, self.read_entries())
            self.clear_entries()
            self.refresh_tree()


class CategoryContainer(Category):
    def __init__(self):
        super().__init__("container")
        self.tree["columns"] = ("id", "weight", "destination")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("id", anchor=tk.E, width=40)
        self.tree.column("weight", anchor=tk.E, width=80)
        self.tree.column("destination", anchor=tk.W, width=200)
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("id", text="Id", anchor=tk.CENTER)
        self.tree.heading("weight", text="Weight", anchor=tk.CENTER)
        self.tree.heading("destination", text="Destination", anchor=tk.CENTER)

        label_id = tk.Label(self.edit_frame, text="Id")
        label_id.grid(row=0, column=0, padx=padx, pady=pady)
        label_weight = tk.Label(self.edit_frame, text="Weight")
        label_weight.grid(row=0, column=1, padx=padx, pady=pady)
        label_destination = tk.Label(self.edit_frame, text="Destination")
        label_destination.grid(row=0, column=2, padx=padx, pady=pady)
        label_weather = tk.Label(self.edit_frame, text="Weather")
        label_weather.grid(row=0, column=3, padx=padx, pady=pady)
        entry_id = tk.Entry(self.edit_frame, width=4)
        entry_id.grid(row=1, column=0, padx=padx, pady=pady)
        entry_weight = tk.Entry(self.edit_frame, width=4)
        entry_weight.grid(row=1, column=1, padx=padx, pady=pady)
        entry_destination = tk.Entry(self.edit_frame, width=12)
        entry_destination.grid(row=1, column=2, padx=padx, pady=pady)
        entry_weather = tk.Entry(self.edit_frame, width=8)
        entry_weather.grid(row=1, column=3, padx=padx, pady=pady)

        self.entries = [entry_id, entry_weight, entry_destination, entry_weather]


class CategoryAircraft(Category):
    def __init__(self):
        super().__init__("aircraft")
        self.tree["columns"] = ("id", "maxweight", "registration")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("id", anchor=tk.E, width=40)
        self.tree.column("maxweight", anchor=tk.E, width=100)
        self.tree.column("registration", anchor=tk.W, width=100)
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("id", text="Id", anchor=tk.CENTER)
        self.tree.heading("maxweight", text="Max. Carg. Weight", anchor=tk.CENTER)
        self.tree.heading("registration", text="Registration", anchor=tk.CENTER)

        label_id = tk.Label(self.edit_frame, text="Id")
        label_id.grid(row=0, column=0, padx=padx, pady=pady)
        label_maxweight = tk.Label(self.edit_frame, text="Max.Carg.Wgt.")
        label_maxweight.grid(row=0, column=1, padx=padx, pady=pady)
        label_registration = tk.Label(self.edit_frame, text="Registration")
        label_registration.grid(row=0, column=2, padx=padx, pady=pady)
        entry_id = tk.Entry(self.edit_frame, width=4)
        entry_id.grid(row=1, column=0, padx=padx, pady=pady)
        entry_maxweight = tk.Entry(self.edit_frame, width=8)
        entry_maxweight.grid(row=1, column=1, padx=padx, pady=pady)
        entry_registration = tk.Entry(self.edit_frame, width=12)
        entry_registration.grid(row=1, column=2, padx=padx, pady=pady)

        self.entries = [entry_id, entry_maxweight, entry_registration]


class CategoryTransport(Category):
    def __init__(self):
        super().__init__("transport")
        self.tree["columns"] = ("id", "date", "containerid", "aircraftid")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("id", anchor=tk.E, width=40)
        self.tree.column("date", anchor=tk.E, width=80)
        self.tree.column("containerid", anchor=tk.E, width=70)
        self.tree.column("aircraftid", anchor=tk.E, width=70)
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("id", text="Id", anchor=tk.CENTER)
        self.tree.heading("date", text="Date", anchor=tk.CENTER)
        self.tree.heading("containerid", text="Container Id", anchor=tk.CENTER)
        self.tree.heading("aircraftid", text="Aircraft Id", anchor=tk.CENTER)

        label_id = tk.Label(self.edit_frame, text="Id")
        label_id.grid(row=0, column=0, padx=padx, pady=pady)
        label_date = tk.Label(self.edit_frame, text="Date")
        label_date.grid(row=0, column=1, padx=padx, pady=pady)
        label_containerid = tk.Label(self.edit_frame, text="Container Id")
        label_containerid.grid(row=0, column=2, padx=padx, pady=pady)
        label_aircraftid = tk.Label(self.edit_frame, text="Aircraft Id")
        label_aircraftid.grid(row=0, column=3, padx=padx, pady=pady)
        entry_id = tk.Entry(self.edit_frame, width=4)
        entry_id.grid(row=1, column=0, padx=padx, pady=pady)
        entry_date = tk.Entry(self.edit_frame, width=12)
        entry_date.grid(row=1, column=1, padx=padx, pady=pady)
        entry_containerid = tk.Entry(self.edit_frame, width=4)
        entry_containerid.grid(row=1, column=2, padx=padx, pady=pady)
        entry_aircraftid = tk.Entry(self.edit_frame, width=4)
        entry_aircraftid.grid(row=1, column=3, padx=padx, pady=pady)

        self.entries = [entry_id, entry_date, entry_containerid, entry_aircraftid]

    def check_and_return_transport(self):
        transport = dcd.convert_from_tuple(self.classparam, self.read_entries())
        capacity_ok = dcf.capacity_available(dcsql.get_record(dcd.Aircraft, self.entries[3].get()), self.entries[1].get(), dcsql.get_record(dcd.Container, self.entries[2].get()))  # self.entries[3] refers to target aircraft id, self.entries[1] refers to target date, self.entries[2] refers to target container id
        destination_ok = dcf.max_one_destination(dcsql.get_record(dcd.Aircraft, self.entries[3].get()), self.entries[1].get(), dcsql.get_record(dcd.Container, self.entries[2].get()))  # self.entries[3] refers to target aircraft id, self.entries[1] refers to target date, self.entries[2] refers to target container id
        if destination_ok:
            if capacity_ok:
                return transport
            else:
                messagebox.showwarning(window_name, "Not enough capacity on aircraft!")
        else:
            messagebox.showwarning(window_name, "Aircraft already has another destination!")

    def create(self):
        dcsql.create_record(self.check_and_return_transport())
        self.clear_entries()
        self.refresh_tree()

    def update(self):
        dcsql.update_record(dcd.Transport, self.check_and_return_transport().convert_to_tuple())
        self.clear_entries()
        self.refresh_tree()


container = CategoryContainer()
aircraft = CategoryAircraft()
transport = CategoryTransport()

if __name__ == "__main__":
    for category in categories:
        category.refresh_tree()
    main_window.mainloop()