"""
Booking Wizard - 4-Step Car Rental Booking Process
WeAreCars Car Rental System
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from modules.styling import COLORS, FONTS, PADDING

class BookingWizard:
    def __init__(self, parent, database, on_complete):
        """Initialize the booking wizard."""
        self.parent = parent
        self.database = database
        self.on_complete = on_complete
        self.window = tk.Toplevel(parent)
        self.window.title("WeAreCars - New Booking")
        self.window.geometry("800x750")
        self.window.configure(bg=COLORS['background'])
        self.window.resizable(True, True)
        
        # Center the window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.window.winfo_screenheight() // 2) - (750 // 2)
        self.window.geometry(f"800x750+{x}+{y}")
        
        # Window configuration for stability
        self.window.minsize(800, 650)
        self.window.transient(parent)
        self.window.lift()
        self.window.focus_force()
        self.window.update_idletasks()
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.cancel_booking)
        
        # Booking data
        self.booking_data = {
            'first_name': tk.StringVar(),
            'surname': tk.StringVar(),
            'address': tk.StringVar(),
            'age': tk.IntVar(value=25),
            'license_valid': tk.BooleanVar(value=True),
            'days': tk.IntVar(value=5),
            'car_type': tk.StringVar(value='City Car'),
            'fuel_type': tk.StringVar(value='Petrol'),
            'unlimited_mileage': tk.BooleanVar(value=False),
            'breakdown_cover': tk.BooleanVar(value=False),
        }
        
        # Pricing information
        self.base_rate = 25.0
        self.car_surcharges = {
            'City Car': 0,
            'Family Car': 50,
            'Sports Car': 75,
            'SUV': 65
        }
        self.fuel_surcharges = {
            'Petrol': 0,
            'Diesel': 0,
            'Hybrid': 30,
            'Electric': 50
        }
        
        self.setup_ui()
    
    def setup_ui(self):
        """Create the booking wizard UI."""
        # Header Frame
        header_frame = tk.Frame(self.window, bg=COLORS['header'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="📝 New Booking Wizard",
            font=('Segoe UI', 24, 'bold'),
            bg=COLORS['header'],
            fg=COLORS['text_light']
        )
        title_label.pack(pady=20)
        
        # Navigation Buttons Frame (pack first so it stays at bottom)
        nav_frame = tk.Frame(self.window, bg=COLORS['background'], height=60)
        nav_frame.pack(side='bottom', fill='x', padx=PADDING['large'], pady=PADDING['large'])
        nav_frame.pack_propagate(False)
        
        # Main Content
        content_frame = tk.Frame(self.window, bg=COLORS['background'])
        content_frame.pack(fill='both', expand=True, padx=PADDING['large'], pady=(PADDING['large'], 0))
        
        # Create Notebook (Tabbed Interface)
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background=COLORS['background'])
        style.configure('TNotebook.Tab', padding=[20, 10], font=FONTS['button'])
        
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Tab 1: Customer Details (scrollable)
        self.tab1 = tk.Frame(self.notebook, bg=COLORS['card'])
        self.notebook.add(self.tab1, text="1. Customer Details")
        self._make_scrollable_tab(self.tab1, self.create_customer_tab)
        
        # Tab 2: Rental Details (scrollable)
        self.tab2 = tk.Frame(self.notebook, bg=COLORS['card'])
        self.notebook.add(self.tab2, text="2. Rental Details")
        self._make_scrollable_tab(self.tab2, self.create_rental_tab)
        
        # Tab 3: Optional Extras
        self.tab3 = tk.Frame(self.notebook, bg=COLORS['card'])
        self.notebook.add(self.tab3, text="3. Optional Extras")
        self.create_extras_tab()
        
        # Tab 4: Summary & Confirm
        self.tab4 = tk.Frame(self.notebook, bg=COLORS['card'])
        self.notebook.add(self.tab4, text="4. Summary & Confirm")
        self.create_summary_tab()
        
        # Bind tab change to update summary
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed)
        
        # Navigation Buttons (already created above)
        self.prev_btn = tk.Button(
            nav_frame,
            text="← Previous",
            command=self.previous_tab,
            bg=COLORS['border'],
            fg=COLORS['text'],
            font=FONTS['button'],
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=8,
            state='disabled'
        )
        self.prev_btn.pack(side='left')
        
        self.next_btn = tk.Button(
            nav_frame,
            text="Next →",
            command=self.next_tab,
            bg=COLORS['button'],
            fg=COLORS['text_light'],
            font=FONTS['button'],
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=8
        )
        self.next_btn.pack(side='right')
        
        cancel_btn = tk.Button(
            nav_frame,
            text="Cancel",
            command=self.cancel_booking,
            bg=COLORS['error'],
            fg=COLORS['text_light'],
            font=FONTS['button'],
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=8
        )
        cancel_btn.pack(side='right', padx=10)
    
    def create_customer_tab(self):
        """Create customer details tab."""
        frame = self._current_scroll_frame
        frame.pack(fill='both', expand=True, padx=PADDING['xlarge'], pady=PADDING['large'])
        
        # Title
        title = tk.Label(
            frame,
            text="Customer Information",
            font=FONTS['subheader'],
            bg=COLORS['card'],
            fg=COLORS['text']
        )
        title.pack(anchor='w', pady=(0, PADDING['large']))
        
        # First Name
        tk.Label(frame, text="First Name: *", font=FONTS['label'], bg=COLORS['card'], fg=COLORS['text']).pack(anchor='w', pady=(10, 5))
        self.first_name_entry = tk.Entry(frame, textvariable=self.booking_data['first_name'], font=FONTS['entry'], relief='solid', bd=1)
        self.first_name_entry.pack(fill='x', ipady=8)
        
        # Surname
        tk.Label(frame, text="Surname: *", font=FONTS['label'], bg=COLORS['card'], fg=COLORS['text']).pack(anchor='w', pady=(15, 5))
        self.surname_entry = tk.Entry(frame, textvariable=self.booking_data['surname'], font=FONTS['entry'], relief='solid', bd=1)
        self.surname_entry.pack(fill='x', ipady=8)
        
        # Address
        tk.Label(frame, text="Address: *", font=FONTS['label'], bg=COLORS['card'], fg=COLORS['text']).pack(anchor='w', pady=(15, 5))
        self.address_text = tk.Text(frame, font=FONTS['entry'], relief='solid', bd=1, height=3)
        self.address_text.pack(fill='x')
        
        # Age
        tk.Label(frame, text="Age: *", font=FONTS['label'], bg=COLORS['card'], fg=COLORS['text']).pack(anchor='w', pady=(15, 5))
        age_frame = tk.Frame(frame, bg=COLORS['card'])
        age_frame.pack(fill='x')
        self.age_spinbox = tk.Spinbox(age_frame, from_=18, to=100, textvariable=self.booking_data['age'], font=FONTS['entry'], relief='solid', bd=1, width=10)
        self.age_spinbox.pack(side='left')
        tk.Label(age_frame, text="(18-100 years)", font=FONTS['small'], bg=COLORS['card'], fg=COLORS['disabled']).pack(side='left', padx=10)
        
        # License Valid
        self.license_check = tk.Checkbutton(
            frame,
            text="✓ Valid Driving License",
            variable=self.booking_data['license_valid'],
            font=FONTS['normal'],
            bg=COLORS['card'],
            fg=COLORS['text'],
            selectcolor=COLORS['card'],
            activebackground=COLORS['card']
        )
        self.license_check.pack(anchor='w', pady=(20, 0))
        
        # Validation note
        note = tk.Label(
            frame,
            text="* All fields are required",
            font=FONTS['small'],
            bg=COLORS['card'],
            fg=COLORS['error']
        )
        note.pack(anchor='w', pady=(20, 0))
    
    def create_rental_tab(self):
        """Create rental details tab."""
        frame = self._current_scroll_frame
        frame.pack(fill='both', expand=True, padx=PADDING['xlarge'], pady=PADDING['large'])
        
        # Title
        title = tk.Label(
            frame,
            text="Rental Configuration",
            font=FONTS['subheader'],
            bg=COLORS['card'],
            fg=COLORS['text']
        )
        title.pack(anchor='w', pady=(0, PADDING['large']))
        
        # Days Slider
        days_label = tk.Label(frame, text="Rental Period (Days): *", font=FONTS['label'], bg=COLORS['card'], fg=COLORS['text'])
        days_label.pack(anchor='w', pady=(10, 5))
        
        days_frame = tk.Frame(frame, bg=COLORS['card'])
        days_frame.pack(fill='x', pady=(0, 10))
        
        self.days_scale = tk.Scale(
            days_frame,
            from_=1,
            to=28,
            orient='horizontal',
            variable=self.booking_data['days'],
            font=FONTS['normal'],
            bg=COLORS['card'],
            fg=COLORS['text'],
            highlightthickness=0,
            length=500,
            command=lambda x: self.update_days_label()
        )
        self.days_scale.pack(side='left', fill='x', expand=True)
        
        self.days_value_label = tk.Label(days_frame, text="5 days", font=FONTS['subheader'], bg=COLORS['card'], fg=COLORS['button'], width=10)
        self.days_value_label.pack(side='left', padx=10)
        
        # Car Type
        tk.Label(frame, text="Car Type: *", font=FONTS['label'], bg=COLORS['card'], fg=COLORS['text']).pack(anchor='w', pady=(20, 10))
        
        car_frame = tk.Frame(frame, bg=COLORS['card'])
        car_frame.pack(fill='x')
        
        cars = [
            ('🏙️ City Car (+£0)', 'City Car'),
            ('👨‍👩‍👧‍👦 Family Car (+£50)', 'Family Car'),
            ('🏎️ Sports Car (+£75)', 'Sports Car'),
            ('🚙 SUV (+£65)', 'SUV')
        ]
        
        for i, (text, value) in enumerate(cars):
            rb = tk.Radiobutton(
                car_frame,
                text=text,
                variable=self.booking_data['car_type'],
                value=value,
                font=FONTS['normal'],
                bg=COLORS['card'],
                fg=COLORS['text'],
                selectcolor=COLORS['card'],
                activebackground=COLORS['card']
            )
            rb.grid(row=i//2, column=i%2, sticky='w', padx=10, pady=5)
        
        # Fuel Type
        tk.Label(frame, text="Fuel Type: *", font=FONTS['label'], bg=COLORS['card'], fg=COLORS['text']).pack(anchor='w', pady=(20, 10))
        
        fuel_frame = tk.Frame(frame, bg=COLORS['card'])
        fuel_frame.pack(fill='x')
        
        fuels = [
            ('⛽ Petrol (+£0)', 'Petrol'),
            ('🛢️ Diesel (+£0)', 'Diesel'),
            ('🔋 Hybrid (+£30)', 'Hybrid'),
            ('⚡ Electric (+£50)', 'Electric')
        ]
        
        for i, (text, value) in enumerate(fuels):
            rb = tk.Radiobutton(
                fuel_frame,
                text=text,
                variable=self.booking_data['fuel_type'],
                value=value,
                font=FONTS['normal'],
                bg=COLORS['card'],
                fg=COLORS['text'],
                selectcolor=COLORS['card'],
                activebackground=COLORS['card']
            )
            rb.grid(row=i//2, column=i%2, sticky='w', padx=10, pady=5)
    
    def create_extras_tab(self):
        """Create optional extras tab."""
        frame = tk.Frame(self.tab3, bg=COLORS['card'])
        frame.pack(fill='both', expand=True, padx=PADDING['xlarge'], pady=PADDING['large'])
        
        # Title
        title = tk.Label(
            frame,
            text="Optional Extras",
            font=FONTS['subheader'],
            bg=COLORS['card'],
            fg=COLORS['text']
        )
        title.pack(anchor='w', pady=(0, PADDING['large']))
        
        subtitle = tk.Label(
            frame,
            text="Enhance your rental experience with these optional extras:",
            font=FONTS['normal'],
            bg=COLORS['card'],
            fg=COLORS['disabled']
        )
        subtitle.pack(anchor='w', pady=(0, PADDING['large']))
        
        # Unlimited Mileage
        mileage_card = tk.Frame(frame, bg=COLORS['background'], relief='solid', bd=1)
        mileage_card.pack(fill='x', pady=10)
        
        mileage_inner = tk.Frame(mileage_card, bg=COLORS['card'])
        mileage_inner.pack(padx=2, pady=2, fill='both')
        
        mileage_check = tk.Checkbutton(
            mileage_inner,
            text="🌍 Unlimited Mileage (+£10/day)",
            variable=self.booking_data['unlimited_mileage'],
            font=FONTS['normal'],
            bg=COLORS['card'],
            fg=COLORS['text'],
            selectcolor=COLORS['card'],
            activebackground=COLORS['card']
        )
        mileage_check.pack(anchor='w', padx=15, pady=10)
        
        mileage_desc = tk.Label(
            mileage_inner,
            text="Drive without limits! No mileage restrictions on your rental.",
            font=FONTS['small'],
            bg=COLORS['card'],
            fg=COLORS['disabled']
        )
        mileage_desc.pack(anchor='w', padx=35, pady=(0, 10))
        
        # Breakdown Cover
        breakdown_card = tk.Frame(frame, bg=COLORS['background'], relief='solid', bd=1)
        breakdown_card.pack(fill='x', pady=10)
        
        breakdown_inner = tk.Frame(breakdown_card, bg=COLORS['card'])
        breakdown_inner.pack(padx=2, pady=2, fill='both')
        
        breakdown_check = tk.Checkbutton(
            breakdown_inner,
            text="🛡️ Breakdown Cover (+£2/day)",
            variable=self.booking_data['breakdown_cover'],
            font=FONTS['normal'],
            bg=COLORS['card'],
            fg=COLORS['text'],
            selectcolor=COLORS['card'],
            activebackground=COLORS['card']
        )
        breakdown_check.pack(anchor='w', padx=15, pady=10)
        
        breakdown_desc = tk.Label(
            breakdown_inner,
            text="24/7 roadside assistance and peace of mind.",
            font=FONTS['small'],
            bg=COLORS['card'],
            fg=COLORS['disabled']
        )
        breakdown_desc.pack(anchor='w', padx=35, pady=(0, 10))
        
        # Note
        note = tk.Label(
            frame,
            text="💡 Tip: Extras are optional and can be added to enhance your experience.",
            font=FONTS['small'],
            bg=COLORS['card'],
            fg=COLORS['warning']
        )
        note.pack(anchor='w', pady=(20, 0))
    
    def create_summary_tab(self):
        """Create summary and confirmation tab."""
        # Create scrollable frame
        canvas = tk.Canvas(self.tab4, bg=COLORS['card'], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.tab4, orient='vertical', command=canvas.yview)
        self.summary_frame = tk.Frame(canvas, bg=COLORS['card'])
        
        self.summary_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas.create_window((0, 0), window=self.summary_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Will be populated in update_summary
        self.price_label = None
    
    def update_summary(self):
        """Update the summary tab with current booking data."""
        # Clear existing content
        for widget in self.summary_frame.winfo_children():
            widget.destroy()
        
        frame = tk.Frame(self.summary_frame, bg=COLORS['card'])
        frame.pack(fill='both', expand=True, padx=PADDING['xlarge'], pady=PADDING['large'])
        
        # Title
        title = tk.Label(
            frame,
            text="Booking Summary",
            font=FONTS['header'],
            bg=COLORS['card'],
            fg=COLORS['text']
        )
        title.pack(anchor='w', pady=(0, PADDING['large']))
        
        # Customer Details Section
        self.add_summary_section(frame, "👤 Customer Details", [
            f"Name: {self.booking_data['first_name'].get()} {self.booking_data['surname'].get()}",
            f"Address: {self.address_text.get('1.0', 'end-1c')}",
            f"Age: {self.booking_data['age'].get()} years",
            f"Valid License: {'✓ Yes' if self.booking_data['license_valid'].get() else '✗ No'}"
        ])
        
        # Rental Details Section
        self.add_summary_section(frame, "🚗 Rental Details", [
            f"Duration: {self.booking_data['days'].get()} days",
            f"Car Type: {self.booking_data['car_type'].get()}",
            f"Fuel Type: {self.booking_data['fuel_type'].get()}",
            f"Start Date: {datetime.now().strftime('%Y-%m-%d')}"
        ])
        
        # Extras Section
        extras = []
        if self.booking_data['unlimited_mileage'].get():
            extras.append("✓ Unlimited Mileage")
        if self.booking_data['breakdown_cover'].get():
            extras.append("✓ Breakdown Cover")
        if not extras:
            extras.append("No extras selected")
        
        self.add_summary_section(frame, "🎁 Optional Extras", extras)
        
        # Price Calculation
        days = self.booking_data['days'].get()
        base_cost = self.base_rate * days
        car_surcharge = self.car_surcharges[self.booking_data['car_type'].get()]
        fuel_surcharge = self.fuel_surcharges[self.booking_data['fuel_type'].get()]
        
        mileage_cost = (10 * days) if self.booking_data['unlimited_mileage'].get() else 0
        breakdown_cost = (2 * days) if self.booking_data['breakdown_cover'].get() else 0
        extras_cost = mileage_cost + breakdown_cost
        
        total_cost = base_cost + car_surcharge + fuel_surcharge + extras_cost
        
        # Price Breakdown
        price_frame = tk.Frame(frame, bg=COLORS['background'], relief='solid', bd=2)
        price_frame.pack(fill='x', pady=(PADDING['large'], 0))
        
        price_inner = tk.Frame(price_frame, bg=COLORS['card'])
        price_inner.pack(padx=2, pady=2, fill='both')
        
        tk.Label(
            price_inner,
            text="💰 Price Breakdown",
            font=FONTS['subheader'],
            bg=COLORS['card'],
            fg=COLORS['text']
        ).pack(anchor='w', padx=15, pady=(15, 10))
        
        # Cost items
        costs = [
            (f"Base Cost: £{self.base_rate:.2f} × {days} days", f"£{base_cost:.2f}"),
            (f"Car Surcharge ({self.booking_data['car_type'].get()})", f"+£{car_surcharge:.2f}"),
            (f"Fuel Surcharge ({self.booking_data['fuel_type'].get()})", f"+£{fuel_surcharge:.2f}"),
        ]
        
        if mileage_cost > 0:
            costs.append((f"Unlimited Mileage", f"+£{mileage_cost:.2f}"))
        if breakdown_cost > 0:
            costs.append((f"Breakdown Cover", f"+£{breakdown_cost:.2f}"))
        
        for label, value in costs:
            item_frame = tk.Frame(price_inner, bg=COLORS['card'])
            item_frame.pack(fill='x', padx=30, pady=2)
            tk.Label(item_frame, text=label, font=FONTS['normal'], bg=COLORS['card'], fg=COLORS['text'], anchor='w').pack(side='left')
            tk.Label(item_frame, text=value, font=FONTS['normal'], bg=COLORS['card'], fg=COLORS['text'], anchor='e').pack(side='right')
        
        # Separator
        tk.Frame(price_inner, bg=COLORS['border'], height=2).pack(fill='x', padx=30, pady=10)
        
        # Total
        total_frame = tk.Frame(price_inner, bg=COLORS['card'])
        total_frame.pack(fill='x', padx=30, pady=(0, 15))
        tk.Label(total_frame, text="TOTAL:", font=FONTS['subheader'], bg=COLORS['card'], fg=COLORS['text'], anchor='w').pack(side='left')
        self.price_label = tk.Label(total_frame, text=f"£{total_cost:.2f}", font=('Segoe UI', 20, 'bold'), bg=COLORS['card'], fg=COLORS['success'], anchor='e')
        self.price_label.pack(side='right')
        
        # Confirm Button
        confirm_btn = tk.Button(
            frame,
            text="✓ Confirm Booking",
            command=self.confirm_booking,
            bg=COLORS['success'],
            fg=COLORS['text_light'],
            font=('Segoe UI', 14, 'bold'),
            relief='flat',
            cursor='hand2',
            padx=30,
            pady=15
        )
        confirm_btn.pack(pady=(PADDING['large'], 0))
        confirm_btn.bind('<Enter>', lambda e: confirm_btn.config(bg='#229954'))
        confirm_btn.bind('<Leave>', lambda e: confirm_btn.config(bg=COLORS['success']))
    
    def add_summary_section(self, parent, title, items):
        """Add a section to the summary."""
        section = tk.Frame(parent, bg=COLORS['card'])
        section.pack(fill='x', pady=(0, PADDING['medium']))
        
        tk.Label(
            section,
            text=title,
            font=FONTS['subheader'],
            bg=COLORS['card'],
            fg=COLORS['text']
        ).pack(anchor='w', pady=(0, 5))
        
        for item in items:
            tk.Label(
                section,
                text=f"  • {item}",
                font=FONTS['normal'],
                bg=COLORS['card'],
                fg=COLORS['disabled']
            ).pack(anchor='w', pady=2)
    
    def update_days_label(self):
        """Update the days value label."""
        days = self.booking_data['days'].get()
        self.days_value_label.config(text=f"{days} day{'s' if days > 1 else ''}")
    
    def validate_customer_details(self):
        """Validate customer details before proceeding."""
        if not self.booking_data['first_name'].get().strip():
            messagebox.showerror("Validation Error", "Please enter first name.", parent=self.window)
            self.first_name_entry.config(bg='#ffcccc')
            return False
        
        if not self.booking_data['surname'].get().strip():
            messagebox.showerror("Validation Error", "Please enter surname.", parent=self.window)
            self.surname_entry.config(bg='#ffcccc')
            return False
        
        address = self.address_text.get('1.0', 'end-1c').strip()
        if not address:
            messagebox.showerror("Validation Error", "Please enter address.", parent=self.window)
            self.address_text.config(bg='#ffcccc')
            return False
        
        if not self.booking_data['license_valid'].get():
            messagebox.showerror("Validation Error", "Customer must have a valid driving license.", parent=self.window)
            return False
        
        # Reset backgrounds if validation passes
        self.first_name_entry.config(bg='white')
        self.surname_entry.config(bg='white')
        self.address_text.config(bg='white')
        
        # Store address in booking data
        self.booking_data['address'].set(address)
        
        return True
    
    def next_tab(self):
        """Move to next tab."""
        current = self.notebook.index(self.notebook.select())
        
        # Validate before moving from customer tab
        if current == 0 and not self.validate_customer_details():
            return
        
        if current < 3:
            self.notebook.select(current + 1)
            self.update_navigation_buttons()
    
    def previous_tab(self):
        """Move to previous tab."""
        current = self.notebook.index(self.notebook.select())
        if current > 0:
            self.notebook.select(current - 1)
            self.update_navigation_buttons()
    
    def on_tab_changed(self, event):
        """Handle tab change event."""
        current = self.notebook.index(self.notebook.select())
        if current == 3:  # Summary tab
            self.update_summary()
        self.update_navigation_buttons()
    
    def update_navigation_buttons(self):
        """Update navigation button states."""
        current = self.notebook.index(self.notebook.select())
        
        # Previous button
        if current == 0:
            self.prev_btn.config(state='disabled')
        else:
            self.prev_btn.config(state='normal')
        
        # Next button
        if current == 3:
            self.next_btn.config(state='disabled')
        else:
            self.next_btn.config(state='normal')
    
    def confirm_booking(self):
        """Confirm and save the booking."""
        # Validate all data
        if not self.validate_customer_details():
            self.notebook.select(0)
            return
        
        try:
            # Add customer to database
            customer_id = self.database.add_customer(
                self.booking_data['first_name'].get(),
                self.booking_data['surname'].get(),
                self.booking_data['address'].get(),
                self.booking_data['age'].get(),
                1 if self.booking_data['license_valid'].get() else 0
            )
            
            # Calculate costs
            days = self.booking_data['days'].get()
            base_cost = self.base_rate * days
            car_surcharge = self.car_surcharges[self.booking_data['car_type'].get()]
            fuel_surcharge = self.fuel_surcharges[self.booking_data['fuel_type'].get()]
            
            mileage_cost = (10 * days) if self.booking_data['unlimited_mileage'].get() else 0
            breakdown_cost = (2 * days) if self.booking_data['breakdown_cover'].get() else 0
            extras_cost = mileage_cost + breakdown_cost
            
            total_cost = base_cost + car_surcharge + fuel_surcharge + extras_cost
            
            # Add booking to database
            booking_id = self.database.add_booking(
                customer_id,
                f"{self.booking_data['first_name'].get()} {self.booking_data['surname'].get()}",
                self.booking_data['car_type'].get(),
                self.booking_data['fuel_type'].get(),
                days,
                1 if self.booking_data['unlimited_mileage'].get() else 0,
                1 if self.booking_data['breakdown_cover'].get() else 0,
                base_cost,
                car_surcharge,
                fuel_surcharge,
                extras_cost,
                total_cost,
                datetime.now().strftime('%Y-%m-%d')
            )
            
            # Success message
            messagebox.showinfo(
                "Booking Confirmed!",
                f"Booking #{booking_id} has been successfully created!\n\n"
                f"Customer: {self.booking_data['first_name'].get()} {self.booking_data['surname'].get()}\n"
                f"Total Cost: £{total_cost:.2f}\n"
                f"Duration: {days} days",
                parent=self.window
            )
            
            self.window.destroy()
            self.on_complete()
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to create booking: {str(e)}",
                parent=self.window
            )
    
    def cancel_booking(self):
        """Cancel the booking process."""
        if messagebox.askyesno("Cancel Booking", "Are you sure you want to cancel this booking?", parent=self.window):
            self.window.destroy()
