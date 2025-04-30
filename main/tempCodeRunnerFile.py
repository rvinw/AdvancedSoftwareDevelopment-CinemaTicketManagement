class ListingsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        for i in range(6):
            self.grid_columnconfigure(i, weight=1)
        for i in range(10):
            self.grid_rowconfigure(i, weight=1)


        # Header row with Film Listings label and Main Menu Button
        header_frame = tk.Frame(self, bg='#add8e6')
        header_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

        # Film Listings title
        tk.Label(header_frame, text="Film Listings", font=('Arial', 18), bg='#add8e6').pack(side='left', padx=10)

        # Main Menu button aligned to the right
        tk.Button(header_frame, text="Main Menu", font=('Arial', 12),
                  command=lambda: controller.show_frame("MainMenuPage")).pack(side='right', padx=10)

        # Container for scrollable content (movies list)
        container = tk.Frame(self, bg='white')
        container.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)

        container.grid_rowconfigure(0, weight=1)  # Allow vertical expansion
        container.grid_columnconfigure(0, weight=1)  # Allow horizontal expansion

        # Canvas for scrollable area
        canvas = tk.Canvas(container, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')

        # Bind scroll event to resize the scroll region
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw', width=680)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Layout for the canvas and scrollbar
        canvas.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='nsew')

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)