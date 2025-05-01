from tkinter import ttk
import tkinter as tk
import datetime
from tkinter import simpledialog
import tkinter.messagebox as messagebox
from tkcalendar import DateEntry
from datetime import date, timedelta
import sqlite3


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

        for F in (LoginPage, MainMenuPage, BookingPage, CancelPage, ListingsPage, AddCityPage, AddCinemaPage, AddMoviePage, ReportsPage, ManageScreeningPage, ScreeningSettingsPage, CreateNewUser):
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

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if username == "Enter username" or password == "Enter password":
            messagebox.showerror("Input Error", "Please enter both username and password.")
            return

        usertype = validate_user_login(username, password)

        if usertype:
            self.controller.logged_in_user = username
            self.controller.user_type = usertype
            self.controller.show_frame("MainMenuPage")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")


class BookingPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.controller = controller
        self.selected_seats = set()
        self.seat_buttons = {}
        self.seat_matrix = []
        self.seat_frame = None

        header_frame = tk.Frame(self, bg='#add8e6')
        header_frame.grid(row=1, column=0, columnspan=10, sticky='nsew', padx=10, pady=10)

        tk.Label(header_frame, text="Book a ticket", font=('Arial', 18), bg='#add8e6').pack(side='left', padx=10)
        tk.Button(header_frame, text="Main Menu", font=('Arial', 12),
                  command=lambda: controller.show_frame("MainMenuPage")).pack(side='right', padx=10)

        tk.Label(self, text="Show ID:", font=('Arial', 14)).grid(row=2, column=1, sticky='nsew')
        self.show_id_entry = tk.Entry(self, font=('Arial', 14), width=25)
        self.show_id_entry.grid(row=2, column=2, sticky='nsew')

        tk.Label(self, text="Choose Date:", font=('Arial', 14)).grid(row=3, column=1, sticky='nsew')
        today = date.today()
        max_date = today + timedelta(days=7)
        self.date_entry = DateEntry(self, font=('Arial'), mindate=today, maxdate=max_date, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=3, column=2, sticky='nsew')

        tk.Button(self, text="Load Seats", font=('Arial', 12),
                  command=self.prepare_and_load_seats).grid(row=4, column=1, columnspan=2, pady=10)

        tk.Button(self, text="Confirm Booking", font=('Arial', 12),
                  command=self.confirm_booking).grid(row=5, column=1, columnspan=2, pady=10)

    def prepare_and_load_seats(self):
        try:
            from db_queries.return_seat_info import get_seat_matrix

            show_id = int(self.show_id_entry.get().strip())
            self.seat_matrix = get_seat_matrix(show_id)
            self.create_seat_selector()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid Show ID.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load seat data:\n{e}")

    def create_seat_selector(self):
        if self.seat_frame:
            self.seat_frame.destroy()

        self.seat_frame = tk.Frame(self)
        self.seat_frame.grid(row=6, column=0, columnspan=10, pady=20)

        self.selected_seats.clear()
        self.seat_buttons.clear()

        for r, row in enumerate(self.seat_matrix):
            for c, (seatID, seatType, available) in enumerate(row):
                try:
                    numeric_seat_id = seatID  
                except ValueError:
                    continue  

                color = self.get_seat_color(seatType) if available else "gray"
                state = "normal" if available else "disabled"

                btn = tk.Button(
                    self.seat_frame,
                    text=seatID,
                    width=4,
                    bg=color,
                    state=state,
                    command=lambda sid=numeric_seat_id, st=seatType: self.toggle_seat_selection(sid, st)
                )
                btn.grid(row=r, column=c, padx=2, pady=2)
                self.seat_buttons[numeric_seat_id] = (btn, seatType)

        self.create_color_legend()

    def toggle_seat_selection(self, seatID, seatType):
        btn, _ = self.seat_buttons[seatID]
        if seatID in self.selected_seats:
            btn.config(bg=self.get_seat_color(seatType))
            self.selected_seats.remove(seatID)
        else:
            btn.config(bg="red")
            self.selected_seats.add(seatID)

    def get_seat_color(self, seat_type):
        return {
            "lower": "lightblue",
            "upper": "lightgreen",
            "vip": "gold"
        }.get(seat_type, "gray")

    def create_color_legend(self):
        legend_frame = tk.Frame(self, bg='#add8e6')
        legend_frame.grid(row=7, column=1, columnspan=4, pady=(10, 20))

        legend_items = [
            ("Lower", "lightblue"),
            ("Upper", "lightgreen"),
            ("VIP", "gold"),
            ("Booked", "gray"),
            ("Selected", "red")
        ]

        for i, (label, color) in enumerate(legend_items):
            tk.Label(legend_frame, text=label, bg=color, width=10, relief='groove').grid(row=0, column=i, padx=5)

    def confirm_booking(self):
        try:
            from db_queries.add_booking import add_booking
            from db_queries.return_seat_info import get_seat_matrix

            show_id = int(self.show_id_entry.get().strip())
            if not self.selected_seats:
                messagebox.showwarning("No Seats", "Please select at least one seat.")
                return

            staff_id = self.controller.user_type
            seat_ids = list(self.selected_seats)

            add_booking(show_id, seat_ids, staff_id)

            self.seat_matrix = get_seat_matrix(show_id)
            self.create_seat_selector()
            self.selected_seats.clear()

            messagebox.showinfo("Success", "Booking completed!")

        except ValueError:
            messagebox.showerror("Error", "Invalid Show ID.")
        except Exception as e:
            messagebox.showerror("Error", f"Booking failed:\n{e}")
            
class ListingsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

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

        header_frame = tk.Frame(self, bg='#add8e6')
        header_frame.grid(row=1, column=0, columnspan=10, sticky='nsew', padx=10, pady=10)

        tk.Label(header_frame, text="Cancel a Ticket", font=('Arial', 18), bg='#add8e6').pack(side='left', padx=10)
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
        header_frame = tk.Frame(self, bg='#add8e6')
        header_frame.grid(row=1, column=0, columnspan=10, sticky='nsew', padx=10, pady=10)

        tk.Label(header_frame, text="Add a city", font=('Arial', 18), bg='#add8e6').pack(side='left', padx=10)
        tk.Button(header_frame, text="Main Menu", font=('Arial', 12),
                  command=lambda: controller.show_frame("MainMenuPage")).pack(side='right', padx=10)
        
        tk.Label(self, text="City Name:", font=('Arial', 14), bg='#add8e6').grid(row=2, column=1, sticky='e', padx=10, pady=10)
        self.new_city_name = ttk.Entry(self, font=('Arial', 14), width=25)
        self.new_city_name.grid(row=2, column=2, columnspan=2, sticky='w')
        
        tk.Label(self, text="Base Price:", font=('Arial', 14), bg='#add8e6').grid(row=3, column=1, sticky='e', padx=10, pady=10)
        self.new_base_price = ttk.Entry(self, font=('Arial', 14), width=25)
        self.new_base_price.grid(row=3, column=2, columnspan=2, sticky='w')
                    
        tk.Button(self, text="Add City", font=('Arial', 14), command=self.create_city).grid(row=4, column=2, columnspan=2, pady=20)     

    def create_city(self):
        from db_queries.add_city import add_city

        city_name = self.new_city_name.get().strip()
        base_price = self.new_base_price.get().strip()

        if city_name and base_price:
            success = add_city(city_name, base_price)
            if success:
                self.new_city_name.delete(0, tk.END)
                self.new_base_price.delete(0, tk.END)
                self.controller.show_frame("MainMenuPage")

        
class AddCinemaPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        header_frame = tk.Frame(self, bg='#add8e6')
        header_frame.grid(row=1, column=0, columnspan=10, sticky='nsew', padx=10, pady=10)

        tk.Label(header_frame, text="Add a cinema", font=('Arial', 18), bg='#add8e6').pack(side='left', padx=10)
        tk.Button(header_frame, text="Main Menu", font=('Arial', 12),
                  command=lambda: controller.show_frame("MainMenuPage")).pack(side='right', padx=10)
        
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

        header_frame = tk.Frame(self, bg='#add8e6')
        header_frame.grid(row=1, column=0, columnspan=10, sticky='nsew', padx=10, pady=10)

        tk.Label(header_frame, text="Add a movie", font=('Arial', 18), bg='#add8e6').pack(side='left', padx=10)
        tk.Button(header_frame, text="Main Menu", font=('Arial', 12),
                  command=lambda: controller.show_frame("MainMenuPage")).pack(side='right', padx=10)

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

        header_frame = tk.Frame(self, bg='#add8e6')
        header_frame.grid(row=1, column=0, columnspan=10, sticky='nsew', padx=10, pady=10)

        tk.Label(header_frame, text="Reports page", font=('Arial', 18), bg='#add8e6').pack(side='left', padx=10)
        tk.Button(header_frame, text="Main Menu", font=('Arial', 12),
                  command=lambda: controller.show_frame("MainMenuPage")).pack(side='right', padx=10)

        button_frame = tk.Frame(self)
        button_frame.grid(row=2, column=0, pady=20, padx=10)

        reports = [
            ("Bookings per Listing", self.report_bookings_per_listing),
            ("Monthly Revenue per Cinema", self.report_monthly_revenue_per_cinema),
            ("Top Revenue Generating Film", self.report_top_revenue_film),
            ("Monthly Staff Bookings (Sorted)", self.report_monthly_staff_bookings),
        ]

        for i, (label, command) in enumerate(reports):
            tk.Button(button_frame, text=label, font=('Arial', 12), width=30, command=command).grid(row=i, column=0, pady=5)

    def get_month_year_input(self):
        month = simpledialog.askinteger("Input", "Enter month (1-12):")
        year = simpledialog.askinteger("Input", "Enter year (e.g., 2025):")
        if not (month and year):
            return None, None
        return f"{year}-{month:02d}", year  # formatted month-year string for SQL
    
    def report_bookings_per_listing(self):
        con = sqlite3.connect("HorizonCinema.db")
        cur = con.cursor()

        cur.execute('''
            SELECT show.showID, movie.title, COUNT(*) AS num_bookings
            FROM booking
            JOIN show ON booking.showID = show.showID
            JOIN movie ON show.movieID = movie.movieID
            WHERE cancelled = 0
            GROUP BY show.showID
            ORDER BY num_bookings DESC
        ''')
        rows = cur.fetchall()
        con.close()

        self.display_report_window("Bookings per Listing", rows, ["Show ID", "Movie Title", "Bookings"])

    def report_monthly_revenue_per_cinema(self):
        month_year, _ = self.get_month_year_input()
        if not month_year:
            return

        con = sqlite3.connect("HorizonCinema.db")
        cur = con.cursor()

        cur.execute('''
            SELECT cinema.cinemaName, 
                strftime('%Y-%m', show.showDateTime) AS month, 
                SUM(booking.price) AS revenue
            FROM booking
            JOIN show ON booking.showID = show.showID
            JOIN screen ON show.screenID = screen.screenID
            JOIN cinema ON screen.cinemaID = cinema.cinemaID
            WHERE cancelled = 0
            AND strftime('%Y-%m', show.showDateTime) = ?
            GROUP BY cinema.cinemaName
            ORDER BY revenue DESC
        ''', (month_year,))
        rows = cur.fetchall()
        con.close()

        self.display_report_window(f"Revenue for {month_year}", rows, ["Cinema", "Month", "Revenue (£)"])

    def report_top_revenue_film(self):
        con = sqlite3.connect("HorizonCinema.db")
        cur = con.cursor()

        cur.execute('''
            SELECT movie.title, SUM(booking.price) AS total_revenue
            FROM booking
            JOIN show ON booking.showID = show.showID
            JOIN movie ON show.movieID = movie.movieID
            WHERE cancelled = 0
            GROUP BY movie.title
            ORDER BY total_revenue DESC
            LIMIT 1
        ''')
        rows = cur.fetchall()
        con.close()

        self.display_report_window("Top Revenue Generating Film", rows, ["Movie Title", "Total Revenue (£)"])

    def report_monthly_staff_bookings(self):
        month_year, _ = self.get_month_year_input()
        if not month_year:
            return

        con = sqlite3.connect("HorizonCinema.db")
        cur = con.cursor()

        try:
            cur.execute('''
                SELECT s.userForename || ' ' || s.userSurname AS staff_name,
                    strftime('%Y-%m', sh.showDateTime) AS month,
                    COUNT(*) AS bookings
                FROM booking b
                JOIN show sh ON b.showID = sh.showID
                JOIN staff s ON b.staffID = s.userID
                WHERE b.cancelled = 0
                AND strftime('%Y-%m', sh.showDateTime) = ?
                GROUP BY staff_name
                ORDER BY bookings DESC
            ''', (month_year,))
            rows = cur.fetchall()
        except sqlite3.OperationalError:
            rows = [("Missing staffID in booking table", "", "")]

        con.close()
        self.display_report_window(f"Staff Bookings for {month_year}", rows, ["Staff Name", "Month", "Bookings"])

    def display_report_window(self, title, rows, headers):
        window = tk.Toplevel(self)
        window.title(title)
        window.geometry("700x400")

        canvas = tk.Canvas(window)
        scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Headers
        for col, header in enumerate(headers):
            tk.Label(scroll_frame, text=header, font=('Arial', 12, 'bold'), borderwidth=2, relief='groove').grid(row=0, column=col, sticky='nsew', padx=2, pady=2)

        # Rows
        for row_idx, row in enumerate(rows, start=1):
            for col_idx, val in enumerate(row):
                tk.Label(scroll_frame, text=str(val), font=('Arial', 11), borderwidth=1, relief='ridge').grid(row=row_idx, column=col_idx, sticky='nsew', padx=1, pady=1)
    
class ManageScreeningPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        self.entries = {}

        self.timeslot_mapping = {
            1: "12:00:00",
            2: "15:30:00",
            3: "19:00:00"
        }

        self.movies = self.get_movies()

        header_frame = tk.Frame(self, bg='#add8e6')
        header_frame.grid(row=1, column=0, columnspan=10, sticky='nsew', padx=10, pady=10)

        tk.Label(header_frame, text="Manage screening", font=('Arial', 18), bg='#add8e6').pack(side='left', padx=10)
        tk.Button(header_frame, text="Main Menu", font=('Arial', 12),
                  command=lambda: controller.show_frame("MainMenuPage")).pack(side='right', padx=10)

        tk.Label(self, text="Cinema ID:", font=('Arial', 14)).grid(row=2, column=0, sticky='e', padx=10, pady=5)
        self.cinema_id_entry = ttk.Entry(self, font=('Arial', 14), width=30)
        self.cinema_id_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self, text="Screen (1–6):", font=('Arial', 14)).grid(row=3, column=0, sticky='e', padx=10, pady=5)
        self.screen_combo = ttk.Combobox(self, font=('Arial', 14), values=list(range(1, 7)), state="readonly", width=28)
        self.screen_combo.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self, text="Select Date:", font=('Arial', 14)).grid(row=4, column=0, sticky='e', padx=10, pady=5)
        self.date_picker = DateEntry(self, font=('Arial', 14), width=28, mindate=date.today(), date_pattern='yyyy-mm-dd')
        self.date_picker.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self, text="Timeslot (1–3):", font=('Arial', 14)).grid(row=5, column=0, sticky='e', padx=10, pady=5)
        self.timeslot_combo = ttk.Combobox(self, font=('Arial', 14), values=[1, 2, 3], state="readonly", width=28)
        self.timeslot_combo.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(self, text="Movie:", font=('Arial', 14)).grid(row=6, column=0, sticky='e', padx=10, pady=5)
        self.movie_combo = ttk.Combobox(self, font=('Arial', 14), values=[m[1] for m in self.movies], state="readonly", width=28)
        self.movie_combo.grid(row=6, column=1, padx=5, pady=5)

        tk.Button(self, text="Add Show", font=('Arial', 14),
                  command=self.add_screening).grid(row=7, column=0, columnspan=2, pady=20)

    def get_movies(self):
        try:
            con = sqlite3.connect("HorizonCinema.db")
            cur = con.cursor()
            cur.execute("SELECT movieID, title FROM movie")
            movies = cur.fetchall()
            con.close()
            return movies
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load movies: {e}")
            return []

    def add_screening(self):
        from db_queries.add_show import add_show, validate_datetime

        def get_screen_id(cinema_id, screen_number):
            con = sqlite3.connect("HorizonCinema.db")
            cur = con.cursor()
            cur.execute('''
                SELECT screenID FROM screen
                WHERE cinemaID = ? AND screenName = ?
            ''', (cinema_id, screen_number))
            result = cur.fetchone()
            con.close()
            return result[0] if result else None

        try:
            cinema_id = int(self.cinema_id_entry.get().strip())
            screen_number = int(self.screen_combo.get())
            timeslot = int(self.timeslot_combo.get())
            date_obj = self.date_picker.get_date()
            movie_title = self.movie_combo.get()

            movie_id = next((m[0] for m in self.movies if m[1] == movie_title), None)
            if movie_id is None:
                messagebox.showerror("Error", "Invalid movie selected.")
                return

            screen_id = get_screen_id(cinema_id, screen_number)
            if screen_id is None:
                messagebox.showerror("Error", f"Screen {screen_number} not found for cinema {cinema_id}.")
                return

            show_time = self.timeslot_mapping[timeslot]
            show_datetime = f"{date_obj.strftime('%Y-%m-%d')} {show_time[:5]}"

            add_show(movie_id, show_datetime, screen_id)

            messagebox.showinfo("Success", "Screening added.")

        except ValueError:
            messagebox.showerror("Input Error", "Please fill in all fields correctly.")


                  
class ScreeningSettingsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        header_frame = tk.Frame(self, bg='#add8e6')
        header_frame.grid(row=1, column=0, columnspan=10, sticky='nsew', padx=10, pady=10)

        tk.Label(header_frame, text="Screen setting", font=('Arial', 18), bg='#add8e6').pack(side='left', padx=10)
        tk.Button(header_frame, text="Main Menu", font=('Arial', 12),
                  command=lambda: controller.show_frame("MainMenuPage")).pack(side='right', padx=10)

        # Screen Name
        tk.Label(self, text="Cinema ID:", font=('Arial', 14), bg='#add8e6').grid(row=3, column=0, sticky='e', padx=10, pady=5)
        self.screen_name_entry = ttk.Entry(self, font=('Arial', 14), width=30)
        self.screen_name_entry.grid(row=3, column=1, padx=10, pady=5)

        # Cinema ID
        tk.Label(self, text="Screen Name:", font=('Arial', 14), bg='#add8e6').grid(row=4, column=0, sticky='e', padx=10, pady=5)
        self.cinema_id_entry = ttk.Entry(self, font=('Arial', 14), width=30)
        self.cinema_id_entry.grid(row=4, column=1, padx=10, pady=5)

        # Capacity
        tk.Label(self, text="Capacity:", font=('Arial', 14), bg='#add8e6').grid(row=5, column=0, sticky='e', padx=10, pady=5)
        self.capacity_entry = ttk.Entry(self, font=('Arial', 14), width=30)
        self.capacity_entry.grid(row=5, column=1, padx=10, pady=5)

        # Add Screen Button
        tk.Button(self, text="Add Screen", font=('Arial', 14), command=self.add_screen).grid(row=6, column=0, columnspan=2, pady=15)

        # Screen List
        self.screen_list_label = tk.Label(self, text="Screens List", font=('Arial', 16), bg='#add8e6')
        self.screen_list_label.grid(row=7, column=0, columnspan=2, pady=20)

        # Screen Table
        self.screen_table = ttk.Treeview(self, columns=("ScreenID", "CinemaID", "Screen Name", "Capacity"), show="headings")
        self.screen_table.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        # Defining columns
        self.screen_table.heading("ScreenID", text="ScreenID")
        self.screen_table.heading("CinemaID", text="CinemaID")
        self.screen_table.heading("Screen Name", text="Screen Name")
        self.screen_table.heading("Capacity", text="Capacity")

        # Load screens
        self.load_screens()

    def add_screen(self):

        from db_queries.add_screening import add_screen 
        
        cinema_id = self.cinema_id_entry.get().strip()
        screen_name = self.screen_name_entry.get().strip()
        capacity = self.capacity_entry.get().strip()

        if not cinema_id or not screen_name or not capacity:
            messagebox.showerror("Input Error", "All fields must be filled.")
            return

        # Add screen
        success, msg = add_screen(cinema_id, screen_name, capacity)
        messagebox.showinfo("Result", msg)

        if success:
            self.load_screens()  # Reload the screen list after adding a new one

    def load_screens(self):
        from db_queries.add_screening import get_all_screens
        # Clear the table first
        for row in self.screen_table.get_children():
            self.screen_table.delete(row)

        # Get all screens and display them
        screens = get_all_screens()
        for screen in screens:
            self.screen_table.insert("", "end", values=screen)
               
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
        settings_btn = tk.Button(self, text="Screen Settings", font=('Arial', 14),
                                 command=lambda: self.controller.show_frame("ScreeningSettingsPage"))
        reports_btn = tk.Button(self, text="Reports", font=('Arial', 14),
                                command=lambda: self.controller.show_frame("ReportsPage"))
        user_btn = tk.Button(self, text="User creation", font=('Arial', 14),
                                command=lambda: self.controller.show_frame("CreateNewUser"))

        screening_btn.grid(row=3, column=4, sticky='nsew')
        settings_btn.grid(row=4, column=4, sticky='nsew')
        reports_btn.grid(row=5, column=4, sticky='nsew')
        user_btn.grid(row=7, column=4, sticky='nsew')


        self.admin_widgets.extend([screening_btn, settings_btn, reports_btn, user_btn])

class CreateNewUser(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        from db_queries.add_user import add_user
        self.controller = controller
        self.entries = {}

        header_frame = tk.Frame(self, bg='#add8e6')
        header_frame.grid(row=1, column=0, columnspan=10, sticky='nsew', padx=10, pady=10)

        tk.Label(header_frame, text="Create a User", font=('Arial', 18), bg='#add8e6').pack(side='left', padx=10)
        tk.Button(header_frame, text="Main Menu", font=('Arial', 12),
                  command=lambda: controller.show_frame("MainMenuPage")).pack(side='right', padx=10)

        tk.Label(self, text="Add New User", font=('Arial', 18), bg='#add8e6').grid(row=3, column=0, columnspan=4, pady=20)

        labels = ["Username", "Forename", "Surname", "User Type", "Password", "Cinema ID"]
        keys = ["username", "forename", "surname", "user_type", "password", "cinema_id"]

        for i, (label, key) in enumerate(zip(labels, keys)):
            tk.Label(self, text=label + ":", font=('Arial', 14)).grid(row=i+4, column=0, sticky='e', padx=10, pady=5)

            if label == "User Type":
                entry = ttk.Combobox(self, font=('Arial', 14), width=30, values=[1, 2, 3], state="readonly")
            else:
                entry = ttk.Entry(self, font=('Arial', 14), width=30, show='*' if label == "Password" else '')

            entry.grid(row=i+4, column=1, padx=5, pady=5)
            self.entries[key] = entry

        tk.Button(self, text="Create User", font=('Arial', 14),
                  command=self.create_user).grid(row=len(labels)+5, column=0, columnspan=2, pady=20)

    def create_user(self):
        from db_queries.add_user import add_user
        
        try:
            user_type = int(self.entries['user_type'].get())
            if user_type not in [1, 2, 3]:
                raise ValueError("User type must be 1, 2, or 3.")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return

        add_user(
            self.entries['username'].get(),
            self.entries['password'].get(),
            self.entries['forename'].get(),
            self.entries['surname'].get(),
            user_type,
            self.entries['cinema_id'].get()
        )

if __name__ == "__main__":
    app = CinemaBookingApp()
    app.mainloop()