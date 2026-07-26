import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Optional
import crypto_storage
import password_gen

AUTO_LOCK_SECONDS = 120  # Auto-locks after 2 minutes of inactivity

class MasterLoginDialog(tk.Toplevel):
    def __init__(self, parent, storage: crypto_storage.VaultStorage):
        super().__init__(parent)
        self.storage = storage
        self.authenticated = False
        self.title("KeyVault - Authentication")
        self.geometry("380x230")
        self.resizable(False, False)
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.center_window()
        self.create_widgets()

    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (190)
        y = (self.winfo_screenheight() // 2) - (115)
        self.geometry(f"+{x}+{y}")

    def create_widgets(self):
        is_new = not self.storage.vault_exists()
        header_text = "Create Master Password" if is_new else "Unlock Your Vault"
        
        ttk.Label(self, text=header_text, font=("Segoe UI", 14, "bold")).pack(pady=15)
        
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Master Password:").pack(anchor=tk.W, pady=(0, 2))
        self.pwd_entry = ttk.Entry(frame, show="•", width=30)
        self.pwd_entry.pack(fill=tk.X, pady=(0, 10))
        self.pwd_entry.focus()
        self.pwd_entry.bind("<Return>", lambda e: self.submit())

        btn_text = "Create Vault" if is_new else "Unlock Vault"
        ttk.Button(frame, text=btn_text, command=self.submit).pack(fill=tk.X, pady=5)

    def submit(self):
        pwd = self.pwd_entry.get().strip()
        if not pwd:
            messagebox.showwarning("Error", "Master password cannot be empty.", parent=self)
            return

        if not self.storage.vault_exists():
            self.storage.initialize_vault(pwd)
            self.authenticated = True
            self.destroy()
        else:
            if self.storage.verify_and_unlock(pwd):
                self.authenticated = True
                self.destroy()
            else:
                messagebox.showerror("Access Denied", "Incorrect master password.", parent=self)
                self.pwd_entry.delete(0, tk.END)

    def on_close(self):
        self.authenticated = False
        self.destroy()


class PasswordManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("KeyVault Pro")
        self.geometry("780x740")
        self.minsize(700, 600)

        self.storage = crypto_storage.VaultStorage()
        self.accounts: List[Dict[str, str]] = []
        self.editing_index: Optional[int] = None
        self.dark_mode = False
        self.passwords_visible = False

        self.withdraw()  # Hide main window during login
        if not self.authenticate_user():
            self.destroy()
            return

        self.deiconify()  # Show main window
        self.accounts = self.storage.load_accounts()

        self.setup_styles()
        self.create_widgets()
        self.refresh_account_list()
        
        # Setup Auto-lock listeners
        self.last_activity_timer = None
        self.bind_all("<Any-KeyPress>", self.reset_inactivity_timer)
        self.bind_all("<Any-Button>", self.reset_inactivity_timer)
        self.reset_inactivity_timer()

    def authenticate_user(self) -> bool:
        login_dialog = MasterLoginDialog(self, self.storage)
        self.wait_window(login_dialog)
        return login_dialog.authenticated

    def reset_inactivity_timer(self, event=None):
        if self.last_activity_timer:
            self.after_cancel(self.last_activity_timer)
        self.last_activity_timer = self.after(AUTO_LOCK_SECONDS * 1000, self.auto_lock)

    def auto_lock(self):
        messagebox.showinfo("Auto-Lock", "Vault locked due to inactivity.")
        self.withdraw()
        self.storage.fernet = None
        if self.authenticate_user():
            self.accounts = self.storage.load_accounts()
            self.deiconify()
            self.refresh_account_list()
            self.reset_inactivity_timer()
        else:
            self.destroy()

    def setup_styles(self):
        self.themes = {
            "light": {"bg": "#f5f6fa", "card": "#ffffff", "fg": "#2f3640", "select_bg": "#dcdde1"},
            "dark": {"bg": "#1e272e", "card": "#2f3640", "fg": "#f5f6fa", "select_bg": "#485460"}
        }
        self.apply_theme()

    def apply_theme(self):
        colors = self.themes["dark" if self.dark_mode else "light"]
        self.configure(bg=colors["bg"])
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("Treeview", background=colors["card"], fieldbackground=colors["card"], foreground=colors["fg"], rowheight=28)
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

        ttk.Label(top_frame, text="🔒 KeyVault Pro", style="Header.TLabel").pack(side=tk.LEFT)
        ttk.Button(top_frame, text="🌓 Toggle Theme", command=self.toggle_theme).pack(side=tk.RIGHT, padx=2)
        ttk.Button(top_frame, text="🔒 Lock Vault", command=self.auto_lock).pack(side=tk.RIGHT, padx=2)

        # Form Section
        self.form_frame = ttk.LabelFrame(self, text=" Add / Edit Credential ", padding=10)
        self.form_frame.pack(fill=tk.X, padx=15, pady=5)

        ttk.Label(self.form_frame, text="Website / App:").grid(row=0, column=0, sticky=tk.W, pady=4)
        self.site_entry = ttk.Entry(self.form_frame, width=25)
        self.site_entry.grid(row=0, column=1, padx=5, pady=4, sticky=tk.EW)

        ttk.Label(self.form_frame, text="Username / Email:").grid(row=1, column=0, sticky=tk.W, pady=4)
        self.user_entry = ttk.Entry(self.form_frame, width=25)
        self.user_entry.grid(row=1, column=1, padx=5, pady=4, sticky=tk.EW)

        ttk.Label(self.form_frame, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=4)
        
        pass_subframe = ttk.Frame(self.form_frame)
        pass_subframe.grid(row=2, column=1, padx=5, pady=4, sticky=tk.EW)

        self.pass_entry = ttk.Entry(pass_subframe, width=18, show="•")
        self.pass_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.pass_entry.bind("<KeyRelease>", lambda e: self.update_strength_meter())

        self.toggle_pass_btn = ttk.Button(pass_subframe, text="👁️", width=3, command=self.toggle_field_password)
        self.toggle_pass_btn.pack(side=tk.LEFT, padx=2)

        ttk.Button(pass_subframe, text="🎲 Generate", command=self.generate_and_fill).pack(side=tk.LEFT, padx=(2, 0))

        # Strength Meter Display
        ttk.Label(self.form_frame, text="Strength:").grid(row=3, column=0, sticky=tk.W, pady=2)
        
        meter_subframe = ttk.Frame(self.form_frame)
        meter_subframe.grid(row=3, column=1, sticky=tk.EW, padx=5, pady=2)

        self.strength_bar = ttk.Progressbar(meter_subframe, length=150, mode="determinate")
        self.strength_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.strength_lbl = ttk.Label(meter_subframe, text="None", font=("Segoe UI", 9, "bold"))
        self.strength_lbl.pack(side=tk.LEFT, padx=(10, 0))

        # Generator Controls
        gen_opts = ttk.Frame(self.form_frame)
        gen_opts.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=4)

        ttk.Label(gen_opts, text="Length:").pack(side=tk.LEFT)
        self.len_spin = ttk.Spinbox(gen_opts, from_=8, to=32, width=4)
        self.len_spin.set(16)
        self.len_spin.pack(side=tk.LEFT, padx=5)

        self.num_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(gen_opts, text="123", variable=self.num_var).pack(side=tk.LEFT, padx=5)

        self.sym_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(gen_opts, text="#$&", variable=self.sym_var).pack(side=tk.LEFT, padx=5)

        # Form Action Buttons
        btn_box = ttk.Frame(self.form_frame)
        btn_box.grid(row=5, column=0, columnspan=2, pady=8, sticky=tk.EW)

        self.save_btn = ttk.Button(btn_box, text="💾 Save Credential", command=self.save_account)
        self.save_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        self.cancel_btn = ttk.Button(btn_box, text="✖ Cancel Edit", command=self.cancel_edit)

        self.form_frame.columnconfigure(1, weight=1)

        # Search Bar & Visibility Toggle
        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, padx=15, pady=8)

        ttk.Label(search_frame, text="🔍 Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_account_list())

        self.toggle_table_vis_btn = ttk.Button(search_frame, text="👁️ Show Passwords", command=self.toggle_table_passwords)
        self.toggle_table_vis_btn.pack(side=tk.RIGHT, padx=(10, 0))

        # Accounts Treeview Table
        list_frame = ttk.Frame(self)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        cols = ("site", "username", "password")
        self.tree = ttk.Treeview(list_frame, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("site", text="Website / App")
        self.tree.heading("username", text="Username / Email")
        self.tree.heading("password", text="Password")

        self.tree.column("site", width=200)
        self.tree.column("username", width=220)
        self.tree.column("password", width=200)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Actions Toolbar
        action_frame = ttk.Frame(self)
        action_frame.pack(fill=tk.X, padx=15, pady=15)

        ttk.Button(action_frame, text="📋 Copy Password", command=self.copy_password).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_frame, text="📋 Copy Username", command=self.copy_username).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_frame, text="✏️ Edit", command=self.load_account_for_edit).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_frame, text="🗑 Delete Entry", command=self.delete_account).pack(side=tk.RIGHT, padx=2)

    # --- UI & Business Logic ---

    def toggle_field_password(self):
        current = self.pass_entry.cget("show")
        self.pass_entry.configure(show="" if current == "•" else "•")

    def toggle_table_passwords(self):
        self.passwords_visible = not self.passwords_visible
        label = "🙈 Hide Passwords" if self.passwords_visible else "👁️ Show Passwords"
        self.toggle_table_vis_btn.configure(text=label)
        self.refresh_account_list()

    def update_strength_meter(self):
        pwd = self.pass_entry.get()
        score, label, color = password_gen.calculate_strength(pwd)
        self.strength_bar["value"] = score
        self.strength_lbl.configure(text=label)

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
        self.update_strength_meter()

    def save_account(self):
        site = self.site_entry.get().strip()
        user = self.user_entry.get().strip()
        pwd = self.pass_entry.get().strip()

        if not site or not user or not pwd:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        account_data = {"site": site, "username": user, "password": pwd}

        if self.editing_index is not None:
            self.accounts[self.editing_index] = account_data
            messagebox.showinfo("Updated", f"Updated entry for '{site}'!")
            self.cancel_edit()
        else:
            self.accounts.append(account_data)
            messagebox.showinfo("Saved", f"Saved credentials for '{site}'!")

        self.storage.save_accounts(self.accounts)
        self.clear_form()
        self.refresh_account_list()

    def load_account_for_edit(self):
        idx = self.get_selected_index()
        if idx == -1:
            return

        acc = self.accounts[idx]
        self.editing_index = idx

        self.site_entry.delete(0, tk.END)
        self.site_entry.insert(0, acc["site"])

        self.user_entry.delete(0, tk.END)
        self.user_entry.insert(0, acc["username"])

        self.pass_entry.delete(0, tk.END)
        self.pass_entry.insert(0, acc["password"])

        self.update_strength_meter()
        self.save_btn.configure(text="💾 Update Credential")
        self.cancel_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

    def cancel_edit(self):
        self.editing_index = None
        self.clear_form()
        self.save_btn.configure(text="💾 Save Credential")
        self.cancel_btn.pack_forget()

    def clear_form(self):
        self.site_entry.delete(0, tk.END)
        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)
        self.update_strength_meter()

    def refresh_account_list(self):
        self.tree.delete(*self.tree.get_children())
        query = self.search_entry.get().lower()

        for index, acc in enumerate(self.accounts):
            if query and (query not in acc["site"].lower() and query not in acc["username"].lower()):
                continue

            disp_pwd = acc["password"] if self.passwords_visible else "••••••••••••"
            self.tree.insert("", tk.END, iid=str(index), values=(acc["site"], acc["username"], disp_pwd))

    def get_selected_index(self) -> int:
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Selection Required", "Please select an account from the list.")
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
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete credentials for '{site}'?"):
                del self.accounts[idx]
                self.storage.save_accounts(self.accounts)
                self.refresh_account_list()

if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()
