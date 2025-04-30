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