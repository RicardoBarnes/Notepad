import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class Notepad(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Notepad")

        # Customize the colors
        self.configure(bg="black")
        self.text = tk.Text(self, wrap="word", font=("Arial", 12), bg="black", fg="white")
        self.text.pack(side="top", fill="both", expand=True)

        # Create a status bar with blue text
        self.status_bar = tk.Label(self, text="", bd=1, relief="sunken", anchor="w", bg="blue", fg="white")
        self.status_bar.pack(side="bottom", fill="x")

        # Create a menu with blue background
        self.menu = tk.Menu(self, bg="blue", fg="white")
        self.config(menu=self.menu)

        file_menu = tk.Menu(self.menu, bg="blue", fg="white")
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        edit_menu = tk.Menu(self.menu, bg="blue", fg="white")
        self.menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Cut", command=self.cut)
        edit_menu.add_command(label="Copy", command=self.copy)
        edit_menu.add_command(label="Paste", command=self.paste)
        edit_menu.add_separator()
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)

        # Track changes for undo/redo
        self.text.edit_modified(False)

    def new_file(self):
        self.text.delete("1.0", "end")
        self.title("Notepad")
        self.update_status_bar("New file created")

    def open_file(self):
        file = filedialog.askopenfile(parent=self, mode="r", title="Open a file")
        if file:
            contents = file.read()
            self.text.delete("1.0", "end")
            self.text.insert("1.0", contents)
            file.close()
            self.title(file.name + " - Notepad")
            self.update_status_bar("File opened: " + file.name)

    def save_file(self):
        file = filedialog.asksaveasfile(mode="w", defaultextension=".txt", filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])
        if file:
            contents = self.text.get("1.0", "end")
            file.write(contents)
            file.close()
            self.title(file.name + " - Notepad")
            self.text.edit_modified(False)
            self.update_status_bar("File saved: " + file.name)

    def cut(self):
        self.text.event_generate("<<Cut>>")
        self.update_status_bar("Text cut")

    def copy(self):
        self.text.event_generate("<<Copy>>")
        self.update_status_bar("Text copied")

    def paste(self):
        self.text.event_generate("<<Paste>>")
        self.update_status_bar("Text pasted")

    def undo(self):
        try:
            self.text.edit_undo()
        except tk.TclError:
            pass

    def redo(self):
        try:
            self.text.edit_redo()
        except tk.TclError:
            pass

    def update_status_bar(self, text):
        self.status_bar.config(text=text)

if __name__ == "__main__":
    notepad = Notepad()
    notepad.mainloop()
