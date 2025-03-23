import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from pygments import lex
from pygments.lexers import get_lexer_by_name, TextLexer
from ttkthemes import ThemedTk
import os

class CodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Code Editor")
        self.root.geometry("1200x800")
        
        # Configure the grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Create main containers
        self.create_file_tree()
        self.create_editor_area()
        self.create_menu()
        
        # Initialize variables
        self.current_file = None
        self.current_lexer = None
        
        # Configure tags for syntax highlighting
        self.setup_tags()
        
    def setup_tags(self):
        # Configure syntax highlighting tags
        self.text.tag_configure("keyword", foreground="#ff79c6")
        self.text.tag_configure("string", foreground="#f1fa8c")
        self.text.tag_configure("comment", foreground="#6272a4")
        self.text.tag_configure("function", foreground="#50fa7b")
        self.text.tag_configure("number", foreground="#bd93f9")
        self.text.tag_configure("operator", foreground="#ff79c6")
        self.text.tag_configure("default", foreground="#f8f8f2")
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
    def create_file_tree(self):
        # Create file tree frame
        tree_frame = ttk.Frame(self.root, width=200)
        tree_frame.grid(row=0, column=0, sticky="nsew")
        tree_frame.grid_rowconfigure(0, weight=1)
        
        # Create tree view
        self.tree = ttk.Treeview(tree_frame)
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.heading("#0", text="Project Explorer")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Bind double-click event
        self.tree.bind("<Double-1>", self.on_file_select)
        
        # Populate the tree with current directory contents
        self.populate_tree()
        
    def create_editor_area(self):
        # Create editor frame
        editor_frame = ttk.Frame(self.root)
        editor_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        editor_frame.grid_rowconfigure(0, weight=1)
        editor_frame.grid_columnconfigure(0, weight=1)
        
        # Create text widget with line numbers
        self.text = ScrolledText(
            editor_frame,
            wrap=tk.NONE,
            undo=True,
            background="#282a36",
            foreground="#f8f8f2",
            insertbackground="#f8f8f2",
            selectbackground="#44475a",
            selectforeground="#f8f8f2",
            font=("Consolas", 11),
            padx=5,
            pady=5
        )
        self.text.grid(row=0, column=0, sticky="nsew")
        
        # Bind events
        self.text.bind("<KeyRelease>", self.on_text_change)
        
    def new_file(self):
        self.current_file = None
        self.text.delete(1.0, tk.END)
        self.root.title("Custom Code Editor - New File")
        
    def open_file(self):
        if not self.current_file:
            file_path = filedialog.askopenfilename(
                filetypes=[
                    ("Python Files", "*.py"),
                    ("JavaScript Files", "*.js"),
                    ("HTML Files", "*.html"),
                    ("All Files", "*.*")
                ]
            )
            if not file_path:
                return
            self.current_file = file_path
            
        try:
            with open(self.current_file, 'r', encoding='utf-8') as file:
                content = file.read()
                self.text.delete(1.0, tk.END)
                self.text.insert(1.0, content)
            self.root.title(f"Custom Code Editor - {os.path.basename(self.current_file)}")
            self.update_syntax_highlighting()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {str(e)}")
                
    def save_file(self):
        if not self.current_file:
            self.current_file = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[
                    ("Python Files", "*.py"),
                    ("JavaScript Files", "*.js"),
                    ("HTML Files", "*.html"),
                    ("All Files", "*.*")
                ]
            )
        if self.current_file:
            try:
                content = self.text.get(1.0, tk.END)
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    file.write(content)
                self.root.title(f"Custom Code Editor - {os.path.basename(self.current_file)}")
                messagebox.showinfo("Success", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {str(e)}")
                
    def on_text_change(self, event=None):
        self.update_syntax_highlighting()
        
    def update_syntax_highlighting(self):
        if not self.current_file:
            return
            
        # Remove existing tags
        for tag in self.text.tag_names():
            self.text.tag_remove(tag, "1.0", tk.END)
            
        # Get file extension
        ext = os.path.splitext(self.current_file)[1][1:].lower()
        
        # Map extensions to lexers
        lexer_map = {
            'py': 'python',
            'js': 'javascript',
            'html': 'html',
            'css': 'css',
            'json': 'json',
            'md': 'markdown'
        }
        
        try:
            # Get appropriate lexer
            lexer_name = lexer_map.get(ext, 'text')
            lexer = get_lexer_by_name(lexer_name)
            
            # Get current content
            content = self.text.get(1.0, tk.END)
            
            # Apply syntax highlighting
            token_source = lex(content, lexer)
            
            # Apply tags based on token types
            for token, value in token_source:
                token_type = str(token)
                tag = None
                
                if 'Keyword' in token_type:
                    tag = 'keyword'
                elif 'String' in token_type:
                    tag = 'string'
                elif 'Comment' in token_type:
                    tag = 'comment'
                elif 'Function' in token_type:
                    tag = 'function'
                elif 'Number' in token_type:
                    tag = 'number'
                elif 'Operator' in token_type:
                    tag = 'operator'
                else:
                    tag = 'default'
                    
                # Find the position to apply the tag
                start = self.text.search(value, "1.0", tk.END)
                if start:
                    end = f"{start}+{len(value)}c"
                    self.text.tag_add(tag, start, end)
                    
        except Exception as e:
            print(f"Error updating syntax highlighting: {str(e)}")
            
    def populate_tree(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Get current directory
        current_dir = os.getcwd()
        
        # Add root node
        root = self.tree.insert("", "end", text=os.path.basename(current_dir), values=[current_dir])
        
        # Recursively add files and directories
        self._populate_tree_recursive(root, current_dir)
        
    def _populate_tree_recursive(self, parent, path):
        try:
            # List directory contents
            for item in sorted(os.listdir(path)):
                item_path = os.path.join(path, item)
                
                # Skip hidden files and directories
                if item.startswith('.'):
                    continue
                    
                if os.path.isfile(item_path):
                    self.tree.insert(parent, "end", text=item, values=[item_path])
                elif os.path.isdir(item_path):
                    node = self.tree.insert(parent, "end", text=item, values=[item_path])
                    self._populate_tree_recursive(node, item_path)
        except PermissionError:
            pass  # Skip directories we don't have access to
            
    def on_file_select(self, event):
        try:
            selected_item = self.tree.selection()[0]
            item_values = self.tree.item(selected_item)['values']
            
            if item_values and len(item_values) > 0:
                file_path = item_values[0]
                if os.path.isfile(file_path):
                    self.current_file = file_path
                    self.open_file()
        except (IndexError, KeyError):
            pass  # Ignore if no valid selection

if __name__ == "__main__":
    root = ThemedTk(theme="equilux")
    app = CodeEditor(root)
    root.mainloop() 