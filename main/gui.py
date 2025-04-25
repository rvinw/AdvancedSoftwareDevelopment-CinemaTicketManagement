import tkinter as tk
from tkinter import *
import datetime

class CinemaBookingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cinema Booking System")
        self.geometry("700x300")
        self.configure(bg='#add8e6')

        for i in range(5):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i + 2, weight=1)

        self.frames = {}
        self.logged_in_user = "Guest"

        for F in (LoginPage, MainMenuPage, BookingPage, CancelPage, ListingsPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, "update_header"):
            frame.update_header()

class BasePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='#add8e6')
        self.controller = controller
        
        for i in range(5):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i + 2, weight=1)

        self.header_frame = tk.Frame(self, bg='#add8e6')
        self.header_frame.grid(row=0, column=0, columnspan=6, sticky='e', padx=10, pady=10)

        self.user_label = tk.Label(self.header_frame, font=('Arial', 12), bg='#add8e6')
        self.user_label.pack(side='left', padx=(0, 20))

        self.time_label = tk.Label(self.header_frame, font=('Arial', 12), bg='#add8e6')
        self.time_label.pack(side='left')

        self.logout_btn = tk.Button(self.header_frame, text="Log out", font=('Arial', 12), command=self.logout)
        self.logout_btn.pack(side='left', padx=(20, 0))

        self.update_clock()

    def update_clock(self):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=now)
        self.after(1000, self.update_clock)

    def update_header(self):
        self.user_label.configure(text=f"User: {self.controller.logged_in_user}")

    def logout(self):
        self.controller.logged_in_user = "Guest"
        self.controller.show_frame("LoginPage")

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='#add8e6')
        self.controller = controller

        for i in range(5):
            self.grid_columnconfigure(i, weight=1)

        tk.Label(self, text="Login Screen", font=('Arial', 18), bg='#add8e6').grid(row=0, column=2, pady=(20, 10))

        tk.Label(self, text="Username:", font=('Arial', 14), bg='#add8e6').grid(row=1, column=1, sticky='e', pady=5)
        self.username_entry = tk.Entry(self, font=('Arial', 14), width=25, fg='grey')
        self.username_entry.grid(row=1, column=2, sticky='w', pady=5)
        self.set_placeholder(self.username_entry, "Username")

        tk.Label(self, text="Password:", font=('Arial', 14), bg='#add8e6').grid(row=2, column=1, sticky='e', pady=5)
        self.password_entry = tk.Entry(self, font=('Arial', 14), width=25, fg='grey')
        self.password_entry.grid(row=2, column=2, sticky='w', pady=5)
        self.set_placeholder(self.password_entry, "Password", is_password=True)

        self.show_var = tk.BooleanVar()
        tk.Checkbutton(self, text="Show Password", variable=self.show_var,
                       command=self.toggle_password, bg='#add8e6').grid(row=3, column=2, sticky='w', pady=(5, 15))

        tk.Button(self, text='Log in', font=('Arial', 14),
                  command=self.login).grid(row=5, column=2, sticky='w')

    def set_placeholder(self, entry, placeholder, is_password=False):
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg='black')
                if is_password and not self.show_var.get():
                    entry.config(show='*')

        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(fg='grey')
                if is_password:
                    entry.config(show='')

        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def toggle_password(self):
        if self.show_var.get():
            if self.password_entry.get() != "Enter password":
                self.password_entry.config(show='')
        else:
            if self.password_entry.get() != "Enter password":
                self.password_entry.config(show='*')

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username != "Enter username" and password != "Enter password":
            self.controller.logged_in_user = username
            self.controller.show_frame("MainMenuPage")

class BookingPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Label(self, text="Making a Booking", font=('Arial', 18), bg='#add8e6').grid(row=1, column=1, pady=20)
        tk.Button(
            self,
            text="Main Menu",
            font=('Arial', 12),
            command=lambda: controller.show_frame("MainMenuPage")).grid(row=1, column=5)
        
class ListingsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Label(self, text="Film Listings", font=('Arial', 18), bg='#add8e6').grid(row=1, column=1, pady=20)
        tk.Button(
            self,
            text="Main Menu",
            font=('Arial', 12),
            command=lambda: controller.show_frame("MainMenuPage")).grid(row=1, column=5)
        
        
class CancelPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Label(self, text="Cancel a Booking", font=('Arial', 18), bg='#add8e6').grid(row=1, column=1, pady=20)
        tk.Button(
            self,
            text="Main Menu",
            font=('Arial', 12),
            command=lambda: controller.show_frame("MainMenuPage")).grid(row=1, column=5)
            
            

class MainMenuPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        tk.Label(self, text="Main Menu", font=('Arial', 18), bg='#add8e6').grid(row=1, column=1, pady=20)

        tk.Button(
            self,
            text="Book Tickets",
            font=('Arial', 14),
            command=lambda: controller.show_frame("BookingPage")).grid(row=3, column=3)
        
        tk.Button(
            self,
            text="Cancel Tickets",
            font=('Arial', 14),
            command=lambda: controller.show_frame("CancelPage")).grid(row=4, column=3)
        

        tk.Button(
            self,
            text="Film Listings",
            font=('Arial', 14),
            command=lambda: controller.show_frame("ListingsPage")).grid(row=5, column=3)

if __name__ == "__main__":
    app = CinemaBookingApp()
    app.mainloop()
