# 🔐 Password Manager

> **A Secure Desktop Password Management Application Built with Python, Tkinter, and Cryptographic Storage**
 <img width="778" height="628" alt="image" src="https://github.com/user-attachments/assets/c17a8b4d-0710-49a8-8e7d-132adaeb8e0a" />


---

# 📖 Project Overview

**Password Manager** is a secure desktop application developed using **Python** and **Tkinter** that allows users to safely store, generate, and manage passwords through a simple graphical interface. Password data is encrypted before being stored, ensuring sensitive information remains protected while providing a convenient user experience.

The project was built to practice **Python programming**, **desktop GUI development**, **cryptography**, **secure file handling**, and **modular software architecture**. It demonstrates how encryption and password generation can be integrated into a real-world desktop application using Python.

---

# ✨ Features

### 🔐 Secure Password Storage

- Store website credentials securely
- Encrypt sensitive information before saving
- Load encrypted password data automatically
- Protect stored credentials using cryptographic techniques

### 🔑 Password Generator

- Generate strong random passwords
- High-entropy password generation
- Supports secure combinations of:
  - Uppercase letters
  - Lowercase letters
  - Numbers
  - Special characters

### 💾 Secure Data Persistence

- Encrypted local password database
- Automatic saving of password entries
- Automatic loading when the application starts
- JSON-based encrypted storage

  
<img width="378" height="259" alt="image" src="https://github.com/user-attachments/assets/a050f32c-3d15-4ae3-8427-a7d34d74e369" />


### 🎨 User Interface

- Clean Tkinter desktop interface
- Beginner-friendly layout
- Lightweight application
- Responsive controls

---

# 📂 Repository Structure

```text
password_manager/
│
├── crypto_storage.py      # Cryptographic abstraction & encrypted JSON storage
├── password_gen.py        # Secure password generation module
├── main.py                # Tkinter GUI and application workflow
├── passwords.json         # Encrypted password database (generated automatically)
├── README.md              # Project documentation
└── .gitignore
```

---

# 🏗 Architecture

```text
                    User
                      │
                      ▼
          ┌─────────────────────┐
          │    Tkinter GUI      │
          │     (main.py)       │
          └──────────┬──────────┘
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
┌──────────────────┐   ┌────────────────────┐
│ Password Manager │   │ Password Generator │
│ crypto_storage.py│   │ password_gen.py    │
└──────────┬───────┘   └────────────────────┘
           │
           ▼
    Encrypted JSON Storage
```

---

# 🚀 Core Functionalities

## 🔐 Save Passwords

Store account credentials securely using encrypted local storage.

---

## 🔑 Generate Strong Passwords

Create high-entropy passwords suitable for online accounts and services.

---

## 🔒 Encrypt Stored Data

Sensitive information is encrypted before being written to disk, helping protect stored credentials.

---

## 📂 Automatic Loading

Previously saved passwords are automatically loaded when the application starts.

---

## 💾 Persistent Storage

All password entries remain available between sessions through encrypted JSON storage.

---

## 🖥 Simple Desktop Interface

Manage passwords using an intuitive Tkinter-based graphical interface.

---

# 🛠 Technologies Used

| Technology | Purpose |
|------------|---------|
| Python 3 | Programming Language |
| Tkinter | Desktop GUI Framework |
| JSON | Local Data Storage |
| Cryptography | Secure Password Storage |
| Object-Oriented Programming | Modular Architecture |
| File Handling | Persistent Data Management |

---

# ▶️ Getting Started

## Prerequisites

- Python 3.10 or later

---

## Clone the Repository

```bash
git clone https://github.com/sakshyampudasaini/password_manager.git
```

> Replace the repository URL if your repository uses a different name.

---

## Navigate to the Project

```bash
cd password_manager
```

---

## Run the Application

```bash
python main.py
```

---

# 🎯 Learning Outcomes

This project demonstrates practical understanding of:

- Python Programming
- Tkinter GUI Development
- Cryptography Fundamentals
- Secure Password Storage
- Password Generation Algorithms
- JSON File Handling
- Object-Oriented Programming (OOP)
- Modular Application Design
- Desktop Application Development

---

# 🔮 Future Improvements

- Master password authentication
- AES-256 encryption support
- Password strength analyzer
- Copy password to clipboard
- Password editing and deletion
- Search saved credentials
- Auto-lock after inactivity
- Dark and Light themes
- Backup and restore encrypted vault
- Cloud synchronization

---

# 🤝 Contributing

Contributions, feature requests, and bug reports are welcome. Feel free to fork the repository, create a new branch, and submit a pull request.

---

# 📄 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Author

**Sakshyam Pudasaini**

GitHub: https://github.com/sakshyampudasaini

---

## ⭐ Support

If you found this project useful, consider giving it a **⭐ Star** on GitHub. Your support helps encourage future improvements and open-source development.
