import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import os
# import the lex in lexer.py
from lexer import lex
# root app initialization
class LOLCodeInterpreterGUI:
    def __init__(self, master):
        self.master = master
        master.title("okay group 1 LOLTERPRETER")
        master.geometry("2000x1080")

        # Configure grid weights for resizing
        master.grid_rowconfigure(0, weight=4)  # Row 0 (Text Editor/Tables) gets more space
        master.grid_rowconfigure(2, weight=3)  # Row 2 (Console) gets less space
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        
        # File Explorer 
        self.file_explorer()

        # Text Editor, Lexemes Table, Symbol Table
        self.edit_lex_sym_container()

        # Execute Button Frame
        self.execute_button()

        # Console Frame
        self.create_console()

    def file_explorer(self):
        # for menu bar (file explorer)
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File explorer", menu=file_menu)
        file_menu.add_command(label="Open File", command=self.open_file)

    # container for the top part - text editor, lexemes, symbol table
    def edit_lex_sym_container(self):
        
        # Left side: Text Editor
        left_frame = tk.Frame(self.master, bd=2, relief=tk.SUNKEN)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        left_frame.grid_rowconfigure(0, weight=0)
        left_frame.grid_rowconfigure(1, weight=0)
        left_frame.grid_rowconfigure(2, weight=1) 
        left_frame.grid_columnconfigure(0, weight=1)
        # label 
        tk.Label(left_frame, text="Text Editor", font=('Arial', 10, 'bold')).grid(row=0, column=0, pady=2, sticky="ew")
        # filename
        self.file_name_label = tk.Label(
            left_frame,                              
            text="No file loaded", 
            font=('Arial', 9, 'italic'),             
            bg="#f2f1f1",                           
            anchor="w" 
        )
        # Place the label in Row 1, Column 0, spanning the full width
        self.file_name_label.grid(row=1, column=0, sticky="ew", padx=2, ipady=1)
        # text editor frame
        self.text_editor = ScrolledText(left_frame, wrap=tk.WORD, undo=True, height=20)
        self.text_editor.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        
        # Right Side: Lexemes & Symbol Table 
        right_frame = tk.Frame(self.master)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        right_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_columnconfigure(1, weight=1)
        
        # Lexemes
        token_frame = tk.Frame(right_frame, bd=2, relief=tk.SUNKEN)
        token_frame.grid(row=0, column=0, sticky="nsew", padx=2)
        tk.Label(token_frame, text="Lexemes", font=('Arial', 10, 'bold')).pack(pady=2)
        self.token_tree = self.create_table(token_frame, ('Lexeme', 'Classification'))
        self.token_tree.pack(fill="both", expand=True, padx=5, pady=5)

        #Symbol Table
        symbol_frame = tk.Frame(right_frame, bd=2, relief=tk.SUNKEN)
        symbol_frame.grid(row=0, column=1, sticky="nsew", padx=2)
        tk.Label(symbol_frame, text="Symbol Table", font=('Arial', 10, 'bold')).pack(pady=2)
        self.symbol_tree = self.create_table(symbol_frame, ('Identifier', 'Value', 'Classification'))
        self.symbol_tree.pack(fill="both", expand=True, padx=5, pady=5)
    
    # function to create table for the lexemes and symbol table
    def create_table(self, parent_frame, columns):
        """Helper function to create and configure a Treeview table."""
        tree = ttk.Treeview(parent_frame, columns=columns, show='headings')
        # Calculate the equal width share for each column
        column_count = len(columns)
        # The actual width will be scaled, but 100 provides a good base
        base_width = 100
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='w', minwidth=base_width, width=base_width, stretch=True)
        return tree

    # execute button
    def execute_button(self):
        execute_frame = tk.Frame(self.master)
        execute_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        self.execute_button = tk.Button(execute_frame, text="Execute", 
                                        command=self.execute_code, bg="#2BDB31", fg='white', font=('Arial', 12, 'bold'))
        self.execute_button.pack(padx=10)

    # console field
    def create_console(self):
        console_frame = tk.Frame(self.master, bd=2, relief=tk.SUNKEN)
        console_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        tk.Label(console_frame, text="Console", font=('Arial', 10, 'bold')).pack(pady=2)
        
        self.console = ScrolledText(console_frame, wrap=tk.WORD, height=10, state=tk.DISABLED, bg='black', fg='white')
        self.console.pack(fill="both", expand=True)

    # FUNCTIONALITIES
    # function for opening files of the computer
    def open_file(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".lol",
            filetypes=[("LOLCODE files", "*.lol")]
        )
        if file_path:
            with open(file_path, 'r') as file:
                code = file.read()
            self.text_editor.delete('1.0', tk.END)
            self.text_editor.insert('1.0', code)
            self.log_to_console(f"File loaded: {os.path.basename(file_path)}")
            self.file_name_label.config(text=f"{os.path.basename(file_path)}")

    # function for executing the lol code when the button is clicked
    # output is displayed in the console
    def execute_code(self):
        code = self.text_editor.get("1.0", tk.END).strip()
        self.log_to_console("--- Starting Execution ---")
        
        # check if the text editor has something in it
        if not code:
            self.log_to_console("Error: Text editor is empty.")
            return

        # call the lex function from lexer.py
        lexeme_table = lex(code)
        # 1. Lexical Analysis 
        self.update_lexeme_frame(lexeme_table)
        
        # 2. Variable/Symbol Tracking (Update Symbol Table)
        self.update_symbol_table(code) 
        

        self.log_to_console("--- Execution Complete ---")

    # function to write something on the console
    def log_to_console(self, message):
        # set to normal so the program can write in it
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END, f"{message}\n")
        self.console.see(tk.END)
        # disable again so the user cannot edit the console
        self.console.config(state=tk.DISABLED)

    # function for updating the lexeme table in the screen
    def update_lexeme_frame(self, lexemes):
        # Clear existing data
        for item in self.token_tree.get_children():
            self.token_tree.delete(item)
        
        # Fill the tree(table) with the values from the list returned from lex
        for lexeme, classification in lexemes:
            # ignore the IGNORE patterns
            if classification == "IGNORE_S_T":
                continue
            self.token_tree.insert('', tk.END, values=(lexeme, classification))

    # function for updating the symbol table in the screen   
    def update_symbol_table(self, code):
        # Clear existing data
        for item in self.symbol_tree.get_children():
            self.symbol_tree.delete(item)

        # Add simulated data based on the image's example
        symbols = [
            ("var", "nOOt nOOt 12", "Variable"),
            ("IT", "12", "Variable"), # 'IT' is the implicit variable
        ]

        for identifier, value, classification in symbols:
            self.symbol_tree.insert('', tk.END, values=(identifier, value, classification))


if __name__ == "__main__":
    root = tk.Tk()
    app = LOLCodeInterpreterGUI(root)
    root.mainloop()