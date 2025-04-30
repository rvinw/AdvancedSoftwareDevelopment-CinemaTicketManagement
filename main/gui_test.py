from tkinter import ttk
import tkinter as tk
import datetime
import tkinter.messagebox as messagebox
from tkcalendar import DateEntry
from datetime import date, timedelta


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

        for F in (LoginPage, MainMenuPage, BookingPage, CancelPage, ListingsPage, AddCityPage, AddCinemaPage, AddMoviePage, ReportsPage, ManageScreeningPage, ListingSettingsPage):
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
        from db_queries.show_listings import get_title, get_cinema_name
        movie_list = get_title()
        cinema_name = get_cinema_name()
        
        tk.Label(self, text="Making a Booking", font=('Arial', 18), bg='#add8e6').grid(row=1, column=1, columnspan=4, pady=20, sticky='nsew')
        tk.Button(self, text="Main Menu", font=('Arial', 12),
                  command=lambda: controller.show_frame("MainMenuPage")).grid(row=0, column=5, sticky='nsew')
        tk.Label(self, text="Choose Film :", font=('Arial', 14)).grid(row=2, column=1, sticky='nsew')
        self.movie_combo = ttk.Combobox(self, values=movie_list, font=('Arial'))
        self.movie_combo.grid(row=2, column=2, sticky='nsew')
        
        tk.Label(self, text="Choose Cinema :", font=('Arial', 14)).grid(row=3, column=1, sticky='nsew')
        self.cinema_combo = ttk.Combobox(self, values=cinema_name, font=('Arial'))
        self.cinema_combo.grid(row=3, column=2, sticky='nsew')
        
        today = date.today()
        max_date = today + timedelta(days=7)
        tk.Label(self, text="Choose Date :", font=('Arial', 14)).grid(row=4, column=1, sticky='nsew')
        self.date_entry = DateEntry(self, font=('Arial'), mindate=today, maxdate=max_date, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=4, column=2, sticky='nsew')


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

        # Scroll container
        container = tk.Frame(self, bg='#add8e6')
        container.grid(row=2, rowspan=6, column=0, columnspan=10, sticky='nsew', padx=10, pady=10)

        # Make the canvas expand to fill the container
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Canvas (where the content will be placed)
        canvas = tk.Canvas(container, bg='#add8e6', highlightthickness=0)
        canvas.grid(row=0, column=0, sticky='nsew')

        # Scrollbar (right side, fixed width)
        scrollbar = tk.Scrollbar(container, orient='vertical', command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')  # This places the scrollbar in column 1

        scrollable_frame = tk.Frame(canvas, bg='#add8e6')

        # Create the window and keep reference to update its size
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor='n')

        # Ensure scroll region is updated on content resize
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        # Ensure the scrollable_frame always matches canvas width
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)

        scrollable_frame.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_canvas_configure)

        # Link the canvas scroll to the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        # Function to enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # Bind the mouse wheel event to scroll the canvas
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        from db_queries.show_listings import get_movies
        movies = get_movies()
        row_index = 0
        
        scrollable_frame.grid_columnconfigure(0, weight=1)

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
        self.controller = controller
        
        for i in range(6):
            self.grid_columnconfigure(i, weight=1)
        for i in range(10):
            self.grid_rowconfigure(i, weight=1)

        # Header
        header_frame = tk.Frame(self, bg='#add8e6')
        header_frame.grid(row=1, column=0, columnspan=10, sticky='nsew', padx=10, pady=10)
        tk.Label(header_frame, text="Cancel booking", font=('Arial', 18), bg='#add8e6').pack(side='left', padx=10)
        tk.Button(header_frame, text="Main Menu", font=('Arial', 12),
                  command=lambda: controller.show_frame("MainMenuPage")).pack(side='right', padx=10)

        # Booking ID
        tk.Label(self, text="Enter Booking ID:", font=('Arial', 14)).grid(row=2, column=2, sticky="e", padx=(10, 5), pady=10)
        self.booking_id_entry = tk.Entry(self, font=('Arial', 14))
        self.booking_id_entry.grid(row=2, column=3, sticky="ew", padx=(5, 5), pady=10)

        # Search button
        tk.Button(self, text="Search", font=('Arial', 14), command=self.search_booking).grid(
            row=2, column=4, sticky="w", padx=(5, 10), pady=10
        )

        # Booking data label
        self.booking_data_label = tk.Label(self, text="Booking Data will be shown here", font=('Arial', 12))
        self.booking_data_label.grid(row=3, column=3, columnspan=1, sticky="w", padx=(10, 5), pady=(10, 20))

          # Cancel Booking Button
        tk.Button(self, text="Cancel Booking", font=('Arial', 14), command=self.cancel_booking_action).grid(
            row=4, column=3, columnspan=1, sticky="nsew", padx=(5, 10), pady=15
        )

        # Uncancel Booking Button
        tk.Button(self, text="Uncancel Booking", font=('Arial', 14), command=self.handle_uncancel).grid(
            row=5, column=3,columnspan=1,sticky="nsew", padx=(5, 10), pady=15
        )

    def search_booking(self):
        from db_queries.cancel_booking import get_booking_info
        booking_id = self.booking_id_entry.get().strip()
        if not booking_id:
            messagebox.showerror("Input Error", "Please enter a Booking ID.")
            return

        result = get_booking_info(booking_id)

        if isinstance(result, str) and result.startswith("Error:"):
            messagebox.showerror("Error", result)
            return

        if result is None:
            self.booking_data_label.config(text="No booking found with this ID.")
        else:
            cancelled = "Yes" if result[5] else "No"
            self.booking_data_label.config(
                text=f"Booking ID: {result[0]}\nShow ID: {result[1]}\nShow Time: {result[2]}\nCancelled: {cancelled}"
            )

    def cancel_booking_action(self):
        from db_queries.cancel_booking import cancel_booking
        booking_id = self.booking_id_entry.get().strip()
        if not booking_id:
            messagebox.showerror("Input Error", "Please enter a Booking ID.")
            return
        cancel_booking(booking_id)
        self.search_booking()  # Refresh label

    def handle_uncancel(self):
        from db_queries.cancel_booking import uncancel_booking
        booking_id = self.booking_id_entry.get().strip()

        if not booking_id.isdigit():
            messagebox.showerror("Input Error", "Please enter a valid numeric Booking ID.")
            return

        success, msg = uncancel_booking(int(booking_id))
        
        if success:
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Failed", msg)
            
        
class AddCityPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Label(self, text="Add a City", font=('Arial', 18), bg='#add8e6').grid(row=1, column=1, columnspan=4, pady=20, sticky='nsew')
        tk.Button(self, text="Main Menu", font=('Arial', 12), command=lambda: controller.show_frame("MainMenuPage")).grid(row=1, column=5, sticky='nsew')
        
        tk.Label(self, text="City Name:", font=('Arial', 14), bg='#add8e6').grid(row=2, column=1, sticky='e', padx=10, pady=10)
        self.new_city_name = ttk.Entry(self, font=('Arial', 14), width=25)
        self.new_city_name.grid(row=2, column=2, columnspan=2, sticky='w')
        
        tk.Label(self, text="Base Price:", font=('Arial', 14), bg='#add8e6').grid(row=3, column=1, sticky='e', padx=10, pady=10)
        self.new_base_price = ttk.Entry(self, font=('Arial', 14), width=25)
        self.new_base_price.grid(row=3, column=2, columnspan=2, sticky='w')
        
        tk.Button(self, text="Create City", font=('Arial', 14), command=self.create_city).grid(row=4, column=2, columnspan=2, pady=20)     

    def create_city(self):
        from db_queries.add_city import add_city
        
        add_city(self.new_city_name.get(), self.new_base_price.get())
        
        self.controller.show_frame("MainMenuPage")
        
class AddCinemaPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        tk.Label(self, text="Add a Cinema", font=('Arial', 18), bg='#add8e6').grid(row=1, column=1, columnspan=4, pady=20, sticky='nsew')
        tk.Button(self, text="Main Menu", font=('Arial', 12), command=lambda: controller.show_frame("MainMenuPage")).grid(row=1, column=5, sticky='nsew')
        
        tk.Label(self, text="City Name :", font=('Arial', 14), bg='#add8e6').grid(row=2, column=1, sticky='e', padx=10, pady=10)
        self.new_city_name = ttk.Entry(self, font=('Arial', 14), width=25)
        self.new_city_name.grid(row=2, column=2, columnspan=2, sticky='w')
    
        tk.Label(self, text="Cinema Name :", font=('Arial', 14), bg='#add8e6').grid(row=3, column=1, sticky='e', padx=10, pady=10)
        self.new_cinema_name = ttk.Entry(self, font=('Arial', 14), width=25)
        self.new_cinema_name.grid(row=3, column=2, columnspan=2, sticky='w')

        tk.Label(self, text="Number of Screens :", font=('Arial', 14), bg='#add8e6').grid(row=4, column=1, sticky='e', padx=10, pady=10)
        self.number_of_screens = ttk.Combobox(self, font=('Arial', 14), width=22, state="readonly")
        self.number_of_screens['values'] = [str(i) for i in range(1, 7)]
        self.number_of_screens.current(0)
        self.number_of_screens.grid(row=4, column=2, columnspan=2, sticky='w')
        
        tk.Button(self, text="Create Cinema", font=('Arial', 14), command=self.create_cinema).grid(row=5, column=2, columnspan=2, pady=20)

    def create_cinema(self):
        from db_queries.add_cinema import add_cinema
        
        city_name = self.new_city_name.get()
        cinema_name = self.new_cinema_name.get()
        num_screens = self.number_of_screens.get()
        
        add_cinema(cinema_name, num_screens, city_name)
        
        self.controller.show_frame("MainMenuPage")


class AddMoviePage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # Title of the page
        tk.Label(self, text="Add a Movie", font=('Arial', 18), bg='#add8e6').grid(
            row=1, column=1, columnspan=4, pady=20, sticky='nsew'
        )
        
        # Main menu button
        tk.Button(self, text="Main Menu", font=('Arial', 12),
                  command=lambda: controller.show_frame("MainMenuPage")).grid(
            row=1, column=5, sticky='nsew'
        )

        # Labels for each field
        labels = [
            "Film Name", "Director", "Cast", "Synopsis",
            "Rating", "Genre", "Age Rating", "Runtime"
        ]

        self.entries = {}

        # Create input fields for each label
        for i, label_text in enumerate(labels):
            row = i + 3
            tk.Label(self, text=label_text, font=('Arial', 14), bg='#add8e6').grid(
                row=row, column=2, sticky='e', padx=10, pady=5
            )

            if label_text == "Age Rating":
                # Age rating combobox
                age_options = ["U", "PG", "12", "12A", "15", "18"]
                age_combobox = ttk.Combobox(self, values=age_options, font=('Arial', 14), width=22, state="readonly")
                age_combobox.current(0)
                age_combobox.grid(row=row, column=3, sticky='w', pady=5)
                self.entries["Age Rating"] = age_combobox
            else:
                # Regular entry fields
                entry = tk.Entry(self, font=('Arial', 14), width=25)
                entry.grid(row=row, column=3, sticky='w', pady=5)
                self.entries[label_text] = entry

        # Create the submit button
        tk.Button(self, text="Submit", font=('Arial', 14),
                  command=self.create_movie).grid(
            row=12, column=2, columnspan=2, pady=20
        )

        # Status label (added for error/success messages)
        self.status_label = tk.Label(self, text="", font=('Arial', 10), fg='red')
        self.status_label.grid(row=13, column=2, columnspan=2, sticky='w')

    def create_movie(self):
        from db_queries.add_movie import add_movie_func
        # Map display labels to DB column names
        field_mapping = {
            "Film Name": "title",
            "Director": "directors",
            "Cast": "cast",
            "Synopsis": "description",
            "Rating": "rating",
            "Genre": "genre",
            "Age Rating": "age",
            "Runtime": "runtime"
        }

        movie_data = {}

        # Loop through each entry and collect the data
        for label, entry in self.entries.items():
            value = entry.get().strip()
            if not value:
                self.status_label.config(text=f"'{label}' cannot be empty.", fg='red')
                return
            db_field = field_mapping[label]
            movie_data[db_field] = value

        try:
            # Convert rating to float
            movie_data["rating"] = float(movie_data["rating"])
        except ValueError:
            self.status_label.config(text="Rating must be a valid number.", fg='red')
            return

        try:
            # Add movie to the database
            add_movie_func(**movie_data)
            self.status_label.config(text="Movie added successfully!", fg='green')

            # Clear form inputs after successful submission
            for entry in self.entries.values():
                entry.delete(0, tk.END)
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", fg='red')


class ReportsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Label(self, text="Reports Page", font=('Arial', 18), bg='#add8e6').grid(row=1, column=1, columnspan=4, pady=20, sticky='nsew')
        tk.Button(self, text="Main Menu", font=('Arial', 12),
                  command=lambda: controller.show_frame("MainMenuPage")).grid(row=1, column=5, sticky='nsew')
 

class ManageScreeningPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Label(self, text="Cancel a Booking", font=('Arial', 18), bg='#add8e6').grid(row=1, column=1, columnspan=4, pady=20, sticky='nsew')
        tk.Button(self, text="Main Menu", font=('Arial', 12),
                  command=lambda: controller.show_frame("MainMenuPage")).grid(row=1, column=5, sticky='nsew')
        
        
class ListingSettingsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.menu_label = tk.Label(self, text="Main Menu", font=('Arial', 18), bg='#add8e6')
        self.menu_label.grid(row=1, column=2, columnspan=3, pady=20, sticky='nsew')

               
class MainMenuPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.menu_label = tk.Label(self, text="Main Menu", font=('Arial', 18), bg='#add8e6')
        self.menu_label.grid(row=1, column=2, columnspan=3, pady=20, sticky='nsew')

        # Connect buttons to new pages here
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

        # Manager specific options
        if user_type == 2:
            self.show_admin_widgets()
            self.show_manager_widgets()

        # Admin specific options
        if user_type == 3:
            self.show_admin_widgets()

    def show_manager_widgets(self):
        # Connecting manager buttons to their respective pages
        add_listing_btn = tk.Button(self, text="Add Movie", font=('Arial', 14),
                                 command=lambda: self.controller.show_frame("AddMoviePage"))
        add_city_btn = tk.Button(self, text="Add City", font=('Arial', 14),
                                   command=lambda: self.controller.show_frame("AddCityPage"))        
        add_cinema_btn = tk.Button(self, text="Add Cinema", font=('Arial', 14),
                                   command=lambda: self.controller.show_frame("AddCinemaPage"))

        add_listing_btn.grid(row=6, column=3, sticky='nsew')
        add_city_btn.grid(row=6, column=4, sticky='nsew')
        add_cinema_btn.grid(row=7, column=3, sticky='nsew')

        self.manager_widgets.extend([add_listing_btn, add_cinema_btn])

    def show_admin_widgets(self):
        # Connecting admin buttons to their respective pages
        screening_btn = tk.Button(self, text="Manage Screening", font=('Arial', 14),
                                  command=lambda: self.controller.show_frame("ManageScreeningPage"))
        settings_btn = tk.Button(self, text="Listing Settings", font=('Arial', 14),
                                 command=lambda: self.controller.show_frame("ListingSettingsPage"))
        reports_btn = tk.Button(self, text="Reports", font=('Arial', 14),
                                command=lambda: self.controller.show_frame("ReportsPage"))

        screening_btn.grid(row=3, column=4, sticky='nsew')
        settings_btn.grid(row=4, column=4, sticky='nsew')
        reports_btn.grid(row=5, column=4, sticky='nsew')

        self.admin_widgets.extend([screening_btn, settings_btn, reports_btn])


if __name__ == "__main__":
    app = CinemaBookingApp()
    app.mainloop()