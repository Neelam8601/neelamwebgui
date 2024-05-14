
import tkinter as tk
from tkinter import ttk, Scrollbar
from constants import FILE_PATH, ICON_FILE
import xml.etree.ElementTree as ET

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("My Application")
        self.root.iconbitmap(ICON_FILE)
        self.root.geometry("900x800")

        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        # Menu setup
        my_menu = tk.Menu(self.root)
        self.root.config(menu=my_menu)

        # Create menu items
        file_menu = tk.Menu(my_menu, tearoff=False)
        my_menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New..", command=self.our_command)
        file_menu.add_command(label="Open..", command=self.our_command)
        file_menu.add_separator()
        file_menu.add_command(label="Save..", command=self.our_command)
        file_menu.add_command(label="Save as..", command=self.our_command)
        file_menu.add_separator()
        file_menu.add_command(label="Most recently used..", command=self.our_command)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # ... rest of the menu items ...
        # create an edit menu item
        edit_menu = tk.Menu(my_menu)
        my_menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Edit", command=self.our_command)
        edit_menu.add_separator()
        edit_menu.add_command(label="Remove", command=self.our_command)

        # create Settings item

        setting_menu = tk.Menu(my_menu)
        my_menu.add_cascade(label="Settings", menu=setting_menu)
        setting_menu.add_command(label="Set Protocol Dll Root...", command=self.our_command)
        setting_menu.add_command(label="Select Protocol..", command=self.our_command)
        setting_menu.add_separator()
        setting_menu.add_command(label="Edit on Create", command=self.our_command)
        setting_menu.add_command(label="Extended Info..", command=self.our_command)

        # create Tools item
        tool_menu = tk.Menu(my_menu)
        my_menu.add_cascade(label="Tools", menu=tool_menu)
        tool_menu.add_command(label="Binary / Hex Converter", command=self.our_command)

        # create helps item
        help_menu = tk.Menu(my_menu)
        my_menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Help F1", command=self.our_command)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.our_command)

    def create_widgets(self):
        # Frames and Widgets
        frame = ttk.Frame(self.root, borderwidth=5)
        frame.grid(sticky=tk.W, pady=10, padx=10)

        label = ttk.Label(frame, text="Available PDUs")
        label.grid()

        # Create a TreeView widget
        self.tree_view = ttk.Treeview(frame)
        self.tree_view.grid(padx=10, pady=10)

        # Add vertical scrollbar
        vsb = Scrollbar(frame, orient="vertical", command=self.tree_view.yview)
        vsb.grid(row=1, column=1, sticky='ns')
        self.tree_view.configure(yscrollcommand=vsb.set)

        # Add horizontal scrollbar
        hsb = Scrollbar(frame, orient="horizontal", command=self.tree_view.xview)
        hsb.grid(row=2, column=0, sticky='ew')
        self.tree_view.configure(xscrollcommand=hsb.set)

        # ... rest of the widgets ...
        # Create a frame for the table
        frame_table = ttk.Frame(root, borderwidth=5)
        frame_table.grid(row=0, column=3, sticky='E', pady=30)

        label = ttk.Label(frame_table, text="Predefined PDUs")
        label.grid()

        # Create the Treeview widget
        tree = ttk.Treeview(frame_table, columns=("Name", "Type", "Protocol"), show="headings")
        tree.grid()

        # Define column headings
        tree.heading("Name", text="Name")
        tree.heading("Type", text="Type")
        tree.heading("Protocol", text="Protocol")


        # Create a frame for the table
        Hex_frame = ttk.Frame(root, borderwidth=5)
        Hex_frame.grid(row=4)

        label = ttk.Label(Hex_frame, text="Hex Value:")
        label.grid(sticky='W')

        decode_button = tk.Button(root, text="Decode", command=self.load_xml_file)
        decode_button.grid(pady=10, sticky='S')

        # Create a button to open the XML file
        open_button = tk.Button(root, text="Open XML File", command=self.load_xml_file)
        open_button.grid(pady=10, sticky='S')

    def our_command(self):
        pass

    def load_xml_file(self):
        try:
            tree = ET.parse(FILE_PATH)
            xml_root = tree.getroot()
            self.display_xml_tree(xml_root)
        except ET.ParseError as e:
            print(f"Error parsing XML file: {e}")

    def display_xml_tree(self, xml_root):
        self.tree_view.delete(*self.tree_view.get_children())
        self.populate_tree(xml_root, "")

    def populate_tree(self, node, parent_id):
        item_id = parent_id
        for name, value in node.attrib.items():
            item_id=self.tree_view.insert(parent_id, 'end', text=value)
        for child in node:
            self.populate_tree(child, item_id)


if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()