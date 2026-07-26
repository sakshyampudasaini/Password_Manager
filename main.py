import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict
import crypto_storage
import password_gen

class PasswordManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("KeyVault - Secure Password Manager")
        self.geometry("680x700")
        self.minsize(600, 550)

        self.accounts: List[Dict[str, str]] = crypto_storage.load_accounts()
        self.dark_mode = False

        self.setup_styles()
        self.create_widgets()
        self.refresh_account_list()

    def setup_styles(self):
        self.themes = {
            "light": {
                "bg": "#f5f6fa",
                "card": "#ffffff",
                "fg": "#2f3640",
                "select_bg": "#dcdde1"
            },
            "dark": {
                "bg": "#1e272e",
                "card": "#2f3640",
                "fg": "#f5f6fa",
                "select_bg": "#485460"
            }
        }
        self.apply_theme()

    def apply_theme(self):
        theme_name = "dark" if self.dark_mode else "light"
        colors = self.themes[theme_name]
        
        self.configure(bg=colors["bg"])
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("Treeview", 
                        background=colors["card"], 
                        fieldbackground=colors["card"], 
                        foreground=colors["fg"],
                        rowheight=28)
        style.map("Treeview", background=[("selected", colors["select_bg"])])

        style.configure("TLabel", background=colors["bg"], foreground=colors["fg"], font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("TFrame", background=colors["bg"])
        style.configure("TLabelframe", background=colors["bg"], foreground=colors["fg"])
        style.configure("TLabelframe.Label", background=colors["bg"], foreground=colors["fg"], font=("Segoe UI", 10, "bold"))

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def create_widgets(self):
        # Header Row
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=15, pady=10)

        ttk.Label(top_frame, text="🔒 KeyVault Password Manager", style="Header.TLabel").pack(side=tk.LEFT)
        ttk.Button(top_frame, text="🌓 Toggle Theme", command=self.toggle_theme).pack(side=tk.RIGHT)

        # Entry & Generator Form
        form_frame = ttk.LabelFrame(self, text=" Add New Credential ", padding=10)
        form_frame.pack(fill=tk.X, padx=15, pady=5)

        ttk.Label(form_frame, text="Website / App:").grid(row=0, column=0, sticky=tk.W, pady=4)
        self.site_entry = ttk.Entry(form_frame, width=25)
        self.site_entry.grid(row=0, column=1, padx=5, pady=4, sticky=tk.EW)

        ttk.Label(form_frame, text="Username / Email:").grid(row=1, column=0, sticky=tk.W, pady=4)
        self.user_entry = ttk.Entry(form_frame, width=25)
        self.user_entry.grid(row=1, column=1, padx=5, pady=4, sticky=tk.EW)

        ttk.Label(form_frame, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=4)
        
        pass_subframe = ttk.Frame(form_frame)
        pass_subframe.grid(row=2, column=1, padx=5, pady=4, sticky=tk.EW)

        self.pass_entry = ttk.Entry(pass_subframe, width=18)
        self.pass_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Button(pass_subframe, text="🎲 Generate", command=self.generate_and_fill).pack(side=tk.LEFT, padx=(5, 0))

        # Generator Controls
        gen_opts_frame = ttk.Frame(form_frame)
        gen_opts_frame.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=2)

        ttk.Label(gen_opts_frame, text="Length:").pack(side=tk.LEFT)
        self.len_spin = ttk.Spinbox(gen_opts_frame, from_=8, to=32, width=4)
        self.len_spin.set(16)
        self.len_spin.pack(side=tk.LEFT, padx=5)

        self.num_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(gen_opts_frame, text="123", variable=self.num_var).pack(side=tk.LEFT, padx=5)

        self.sym_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(gen_opts_frame, text="#$&", variable=self.sym_var).pack(side=tk.LEFT, padx=5)

        ttk.Button(form_frame, text="💾 Save Account", command=self.add_account).grid(row=4, column=0, columnspan=2, pady=8, sticky=tk.EW)

        form_frame.columnconfigure(1, weight=1)

        # Search Bar
        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, padx=15, pady=8)

        ttk.Label(search_frame, text="🔍 Search Accounts:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_account_list())

        # Saved Accounts Table
        list_frame = ttk.Frame(self)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        cols = ("site", "username", "password")
        self.tree = ttk.Treeview(list_frame, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("site", text="Website / App")
        self.tree.heading("username", text="Username / Email")
        self.tree.heading("password", text="Password")

        self.tree.column("site", width=180)
        self.tree.column("username", width=200)
        self.tree.column("password", width=180)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Quick Actions
        action_frame = ttk.Frame(self)
        action_frame.pack(fill=tk.X, padx=15, pady=15)

        ttk.Button(action_frame, text="📋 Copy Password", command=self.copy_password).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_frame, text="📋 Copy Username", command=self.copy_username).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_frame, text="🗑 Delete Account", command=self.delete_account).pack(side=tk.RIGHT, padx=2)

    # --- Business Logic ---

    def generate_and_fill(self):
        try:
            length = int(self.len_spin.get())
        except ValueError:
            length = 16

        pwd = password_gen.generate_password(
            length=length, 
            include_numbers=self.num_var.get(), 
            include_symbols=self.sym_var.get()
        )
        self.pass_entry.delete(0, tk.END)
        self.pass_entry.insert(0, pwd)

    def add_account(self):
        site = self.site_entry.get().strip()
        user = self.user_entry.get().strip()
        pwd = self.pass_entry.get().strip()

        if not site or not user or not pwd:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        self.accounts.append({"site": site, "username": user, "password": pwd})
        crypto_storage.save_accounts(self.accounts)

        # Clear fields
        self.site_entry.delete(0, tk.END)
        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)

        self.refresh_account_list()
        messagebox.showinfo("Success", f"Credentials for '{site}' saved securely!")

    def refresh_account_list(self):
        self.tree.delete(*self.tree.get_children())
        query = self.search_entry.get().lower()

        for index, acc in enumerate(self.accounts):
            if query and (query not in acc["site"].lower() and query not in acc["username"].lower()):
                continue

            self.tree.insert("", tk.END, iid=str(index), values=(acc["site"], acc["username"], acc["password"]))

    def get_selected_index(self) -> int:
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Selection Needed", "Please select an account from the list.")
            return -1
        return int(selected[0])

    def copy_password(self):
        idx = self.get_selected_index()
        if idx != -1:
            pwd = self.accounts[idx]["password"]
            self.clipboard_clear()
            self.clipboard_append(pwd)
            messagebox.showinfo("Copied", "Password copied to clipboard!")

    def copy_username(self):
        idx = self.get_selected_index()
        if idx != -1:
            user = self.accounts[idx]["username"]
            self.clipboard_clear()
            self.clipboard_append(user)
            messagebox.showinfo("Copied", "Username copied to clipboard!")

    def delete_account(self):
        idx = self.get_selected_index()
        if idx != -1:
            site = self.accounts[idx]["site"]
            if messagebox.askyesno("Confirm Delete", f"Delete credentials for '{site}'?"):
                del self.accounts[idx]
                crypto_storage.save_accounts(self.accounts)
                self.refresh_account_list()

if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()