import tkinter as tk
import datetime
import tkinter.messagebox as messagebox

class CinemaBookingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Horizon Cinemas")
        self.geometry("700x700")
        self.configure(bg='#add8e6')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

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

        for i in range(10):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)

        self.header_frame = tk.Frame(self, bg='#add8e6')
        self.header_frame.grid(row=0, column=0, columnspan=10, sticky='nsew', padx=10, pady=10)

        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=1)
        self.header_frame.grid_columnconfigure(2, weight=1)

        self.user_label = tk.Label(self.header_frame, font=('Arial', 12), bg='#add8e6')
        self.user_label.grid(row=0, column=0, sticky='w')

        self.time_label = tk.Label(self.header_frame, font=('Arial', 12), bg='#add8e6')
        self.time_label.grid(row=0, column=1)

        self.logout_btn = tk.Button(self.header_frame, text="Log out", font=('Arial', 12), command=self.logout)
        self.logout_btn.grid(row=0, column=2, sticky='e')

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

        for i in range(6):
            self.grid_columnconfigure(i, weight=1)
        for i in range(10):
            self.grid_rowconfigure(i, weight=1)

        tk.Label(self, text="Login Screen", font=('Arial', 18), bg='#add8e6').grid(row=0, column=2, columnspan=2, pady=(20, 10))

        tk.Label(self, text="Username:", font=('Arial', 14), bg='#add8e6').grid(row=1, column=1, sticky='e', pady=5)
        self.username_entry = tk.Entry(self, font=('Arial', 14), width=25, fg='grey')
        self.username_entry.grid(row=1, column=2, columnspan=2, sticky='w', pady=5)
        self.set_placeholder(self.username_entry, "Enter username")

        tk.Label(self, text="Password:", font=('Arial', 14), bg='#add8e6').grid(row=2, column=1, sticky='e', pady=5)
        self.password_entry = tk.Entry(self, font=('Arial', 14), width=25, fg='grey')
        self.password_entry.grid(row=2, column=2, columnspan=2, sticky='w', pady=5)
        self.set_placeholder(self.password_entry, "Enter password", is_password=True)

        self.show_var = tk.BooleanVar()
        tk.Checkbutton(self, text="Show Password", variable=self.show_var,
                       command=self.toggle_password, bg='#add8e6').grid(row=3, column=2, sticky='w', pady=(5, 15))

        tk.Button(self, text='Log in', font=('Arial', 14),
                  command=self.login).grid(row=5, column=2, columnspan=2, sticky='nsew')

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
            self.password_entry.config(show='')
        else:
            if self.password_entry.get() != "Enter password":
                self.password_entry.config(show='*')

    def login(self):
        from db_queries.validate_user_login import validate_user_login

        username = self.username_entry.get()
        password = self.password_entry.get()

        if username != "Enter username" and password != "Enter password":
            usertype, user_forename = validate_user_login(username, password)
            if usertype:
                self.controller.logged_in_user = user_forename
                self.controller.user_type = usertype
                self.controller.show_frame("MainMenuPage")
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")


class BookingPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Label(self, text="Making a Booking", font=('Arial', 18), bg='#add8e6').grid(row=1, column=1, columnspan=4, pady=20, sticky='nsew')
        tk.Button(self, text="Main Menu", font=('Arial', 12),
                  command=lambda: controller.show_frame("MainMenuPage")).grid(row=0, column=5, sticky='nsew')


class ListingsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # Make the whole page responsive
        for i in range(6):
            self.grid_columnconfigure(i, weight=1)
        for i in range(10):
            self.grid_rowconfigure(i, weight=1)

        # header
        header_frame = tk.Frame(self, bg='#add8e6')
        header_frame.grid(row=1, column=0, columnspan=10, sticky='nsew', padx=10, pady=10)

        tk.Label(header_frame, text="Film Listings", font=('Arial', 18), bg='#add8e6').pack(side='left', padx=10)
        tk.Button(header_frame, text="Main Menu", font=('Arial', 12),
                  command=lambda: controller.show_frame("MainMenuPage")).pack(side='right', padx=10)

        #scroll container
        container = tk.Frame(self, bg='white')
        container.grid(row=2,rowspan=10, column=0, columnspan=12, sticky='nsew', padx=10, pady=10)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(container, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        from db_queries.show_listings import get_movies
        movies = get_movies()
        row_index = 0

        for movie in movies:
            frame = tk.Frame(scrollable_frame, bg='white', bd=1, relief='solid', padx=12, pady=10)
            frame.grid(row=row_index, column=0, sticky='nsew', pady=8)

            tk.Label(frame, text=movie["title"], font=('Arial', 14, 'bold'), bg='white').pack(anchor='w')
            tk.Label(frame, text=f"Directors: {movie['directors']}", font=('Arial', 11), bg='white').pack(anchor='w', pady=(2, 0))

            if movie.get("cast"):
                tk.Label(frame, text=f"Cast: {movie['cast']}", font=('Arial', 10), wraplength=640, justify='left', bg='white').pack(anchor='w', pady=(2, 0))

            tk.Label(frame, text=f"Genre: {movie['genre']}", font=('Arial', 10), bg='white').pack(anchor='w', pady=(2, 0))
            tk.Label(frame, text=f"Rating: {movie['rating']} | Age: {movie['age']} | Runtime: {movie['runTime']}", font=('Arial', 10), bg='white').pack(anchor='w', pady=(2, 0))
            tk.Label(frame, text=f"Synopsis: {movie['description']}", font=('Arial', 10), wraplength=640, justify='left', bg='white').pack(anchor='w', pady=(4, 0))

            row_index += 1

class CancelPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Label(self, text="Cancel a Booking", font=('Arial', 18), bg='#add8e6').grid(row=1, column=1, columnspan=4, pady=20, sticky='nsew')
        tk.Button(self, text="Main Menu", font=('Arial', 12),
                  command=lambda: controller.show_frame("MainMenuPage")).grid(row=1, column=5, sticky='nsew')


class MainMenuPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.menu_label = tk.Label(self, text="Main Menu", font=('Arial', 18), bg='#add8e6')
        self.menu_label.grid(row=1, column=2, columnspan=3, pady=20, sticky='nsew')

        self.book_btn = tk.Button(self, text="Book Tickets", font=('Arial', 14),
                                  command=lambda: controller.show_frame("BookingPage"))
        self.book_btn.grid(row=3, column=3, sticky='nsew')

        self.cancel_btn = tk.Button(self, text="Cancel Tickets", font=('Arial', 14),
                                    command=lambda: controller.show_frame("CancelPage"))
        self.cancel_btn.grid(row=4, column=3, sticky='nsew')

        self.listings_btn = tk.Button(self, text="Film Listings", font=('Arial', 14),
                                      command=lambda: controller.show_frame("ListingsPage"))
        self.listings_btn.grid(row=5, column=3, sticky='nsew')

        self.manager_widgets = []
        self.admin_widgets = []

    def update_header(self):
        super().update_header()
        self.update_content()

    def update_content(self):
        for widget in self.manager_widgets + self.admin_widgets:
            widget.grid_forget()

        self.manager_widgets.clear()
        self.admin_widgets.clear()

        user_type = self.controller.user_type

        # General options for all users
        if user_type in [1, 2, 3]:
            self.book_btn.grid(row=3, column=3, sticky='nsew')
            self.cancel_btn.grid(row=4, column=3, sticky='nsew')
            self.listings_btn.grid(row=5, column=3, sticky='nsew')

        # Additional options for Managers (user_type == 2)
        if user_type == 2:
            add_city_btn = tk.Button(self, text="Add City", font=('Arial', 14))
            add_cinema_btn = tk.Button(self, text="Add Cinema", font=('Arial', 14))

            add_city_btn.grid(row=6, column=3, sticky='nsew')
            add_cinema_btn.grid(row=7, column=3, sticky='nsew')

            self.manager_widgets.extend([add_city_btn, add_cinema_btn])

        # Additional options for Admins (user_type == 3)
        if user_type == 3:
            screening_btn = tk.Button(self, text="Manage Screening", font=('Arial', 14))
            settings_btn = tk.Button(self, text="Listing Settings", font=('Arial', 14))
            reports_btn = tk.Button(self, text="Reports", font=('Arial', 14))

            screening_btn.grid(row=6, column=3, sticky='nsew')
            settings_btn.grid(row=7, column=3, sticky='nsew')
            reports_btn.grid(row=8, column=3, sticky='nsew')

            self.admin_widgets.extend([screening_btn, settings_btn, reports_btn])
if __name__ == "__main__":
    app = CinemaBookingApp()
    app.mainloop()