"""
View Bookings Window - Display and Search Rental Bookings
WeAreCars Car Rental System
"""

import tkinter as tk
from tkinter import ttk, messagebox
import csv
from modules.styling import COLORS, FONTS, PADDING

class ViewBookings:
    def __init__(self, parent, database):
        """Initialize the view bookings window."""
        self.parent = parent
        self.database = database
        self.window = tk.Toplevel(parent)
        self.window.title("WeAreCars - View Bookings")
        self.window.geometry("1000x600")
        self.window.configure(bg=COLORS['background'])
        self.window.resizable(True, True)
        
        # Center the window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.window.winfo_screenheight() // 2) - (600 // 2)
        self.window.geometry(f"1000x600+{x}+{y}")
        
        # Window configuration for stability
        self.window.minsize(900, 500)
        self.window.transient(parent)
        self.window.lift()
        self.window.focus_force()
        self.window.update_idletasks()
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)
        
        self.setup_ui()
        self.load_bookings()
    
    def setup_ui(self):
        """Create the view bookings UI."""
        # Header Frame
        header_frame = tk.Frame(self.window, bg=COLORS['header'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="📋 Rental Bookings",
            font=('Segoe UI', 24, 'bold'),
            bg=COLORS['header'],
            fg=COLORS['text_light']
        )
        title_label.pack(pady=20)
        
        # Toolbar Frame
        toolbar = tk.Frame(self.window, bg=COLORS['background'])
        toolbar.pack(fill='x', padx=PADDING['large'], pady=PADDING['medium'])
        
        # Search Frame
        search_frame = tk.Frame(toolbar, bg=COLORS['background'])
        search_frame.pack(side='left', fill='x', expand=True)
        
        tk.Label(
            search_frame,
            text="🔍 Search:",
            font=FONTS['label'],
            bg=COLORS['background'],
            fg=COLORS['text']
        ).pack(side='left', padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.search_bookings())
        
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=FONTS['entry'],
            relief='solid',
            bd=1,
            width=40
        )
        search_entry.pack(side='left', ipady=5)
        
        # Buttons Frame
        buttons_frame = tk.Frame(toolbar, bg=COLORS['background'])
        buttons_frame.pack(side='right')
        
        refresh_btn = tk.Button(
            buttons_frame,
            text="🔄 Refresh",
            command=self.load_bookings,
            bg=COLORS['button'],
            fg=COLORS['text_light'],
            font=FONTS['button'],
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=5
        )
        refresh_btn.pack(side='left', padx=5)
        refresh_btn.bind('<Enter>', lambda e: refresh_btn.config(bg=COLORS['button_hover']))
        refresh_btn.bind('<Leave>', lambda e: refresh_btn.config(bg=COLORS['button']))
        
        export_btn = tk.Button(
            buttons_frame,
            text="📥 Export CSV",
            command=self.export_to_csv,
            bg=COLORS['success'],
            fg=COLORS['text_light'],
            font=FONTS['button'],
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=5
        )
        export_btn.pack(side='left', padx=5)
        export_btn.bind('<Enter>', lambda e: export_btn.config(bg='#229954'))
        export_btn.bind('<Leave>', lambda e: export_btn.config(bg=COLORS['success']))
        
        close_btn = tk.Button(
            buttons_frame,
            text="✕ Close",
            command=self.window.destroy,
            bg=COLORS['error'],
            fg=COLORS['text_light'],
            font=FONTS['button'],
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=5
        )
        close_btn.pack(side='left', padx=5)
        close_btn.bind('<Enter>', lambda e: close_btn.config(bg='#c0392b'))
        close_btn.bind('<Leave>', lambda e: close_btn.config(bg=COLORS['error']))
        
        # Table Frame
        table_frame = tk.Frame(self.window, bg=COLORS['card'])
        table_frame.pack(fill='both', expand=True, padx=PADDING['large'], pady=(0, PADDING['medium']))
        
        # Create Treeview with Scrollbars
        tree_scroll_y = tk.Scrollbar(table_frame, orient='vertical')
        tree_scroll_y.pack(side='right', fill='y')
        
        tree_scroll_x = tk.Scrollbar(table_frame, orient='horizontal')
        tree_scroll_x.pack(side='bottom', fill='x')
        
        # Configure Treeview Style
        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            'Treeview',
            background=COLORS['card'],
            foreground=COLORS['text'],
            rowheight=25,
            fieldbackground=COLORS['card'],
            font=FONTS['normal']
        )
        style.configure('Treeview.Heading', font=FONTS['button'], background=COLORS['button'], foreground=COLORS['text_light'])
        style.map('Treeview', background=[('selected', COLORS['button'])])
        
        # Create Treeview
        columns = ('ID', 'Customer', 'Car Type', 'Fuel', 'Days', 'Total', 'Booking Date', 'Start Date', 'End Date', 'Status')
        
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set,
            selectmode='browse'
        )
        
        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)
        
        # Define Headings
        column_widths = {
            'ID': 50,
            'Customer': 150,
            'Car Type': 100,
            'Fuel': 80,
            'Days': 60,
            'Total': 80,
            'Booking Date': 100,
            'Start Date': 90,
            'End Date': 90,
            'Status': 80
        }
        
        for col in columns:
            self.tree.heading(col, text=col, anchor='w')
            self.tree.column(col, width=column_widths.get(col, 100), anchor='w')
        
        self.tree.pack(fill='both', expand=True)
        
        # Bind double-click event
        self.tree.bind('<Double-1>', self.show_booking_details)
        
        # Status Bar
        status_frame = tk.Frame(self.window, bg=COLORS['border'], height=30)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready",
            font=FONTS['small'],
            bg=COLORS['border'],
            fg=COLORS['text'],
            anchor='w'
        )
        self.status_label.pack(side='left', padx=PADDING['medium'])
        
        self.count_label = tk.Label(
            status_frame,
            text="",
            font=FONTS['small'],
            bg=COLORS['border'],
            fg=COLORS['text'],
            anchor='e'
        )
        self.count_label.pack(side='right', padx=PADDING['medium'])
    
    def load_bookings(self):
        """Load all bookings from database."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch bookings
        bookings = self.database.get_all_bookings()
        
        # Insert into treeview
        for booking in bookings:
            # booking: (id, customer_name, car_type, fuel_type, days, total_cost,
            #           booking_date, start_date, end_date, status)
            self.tree.insert('', 'end', values=(
                booking[0],  # ID
                booking[1],  # Customer
                booking[2],  # Car Type
                booking[3],  # Fuel
                booking[4],  # Days
                f"£{booking[5]:.2f}",  # Total
                booking[6].split()[0] if booking[6] else '',  # Booking Date
                booking[7],  # Start Date
                booking[8],  # End Date
                booking[9]   # Status
            ))
        
        # Update status
        count = len(bookings)
        self.count_label.config(text=f"Total: {count} booking{'s' if count != 1 else ''}")
        self.status_label.config(text="Bookings loaded successfully")
    
    def search_bookings(self):
        """Search bookings based on search term."""
        search_term = self.search_var.get().strip()
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not search_term:
            self.load_bookings()
            return
        
        # Fetch matching bookings
        bookings = self.database.search_bookings(search_term)
        
        # Insert into treeview
        for booking in bookings:
            self.tree.insert('', 'end', values=(
                booking[0],
                booking[1],
                booking[2],
                booking[3],
                booking[4],
                f"£{booking[5]:.2f}",
                booking[6].split()[0] if booking[6] else '',
                booking[7],
                booking[8],
                booking[9]
            ))
        
        # Update status
        count = len(bookings)
        self.count_label.config(text=f"Found: {count} booking{'s' if count != 1 else ''}")
        self.status_label.config(text=f"Search results for '{search_term}'")
    
    def show_booking_details(self, event):
        """Show detailed view of selected booking."""
        selection = self.tree.selection()
        if not selection:
            return
        
        # Get booking data
        item = self.tree.item(selection[0])
        values = item['values']
        
        # Create details window
        details = tk.Toplevel(self.window)
        details.title(f"Booking Details - #{values[0]}")
        details.geometry("500x500")
        details.configure(bg=COLORS['background'])
        
        # Center the window
        details.update_idletasks()
        x = (details.winfo_screenwidth() // 2) - (500 // 2)
        y = (details.winfo_screenheight() // 2) - (500 // 2)
        details.geometry(f"500x500+{x}+{y}")
        
        # Header
        header = tk.Frame(details, bg=COLORS['header'], height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text=f"Booking #{values[0]}",
            font=FONTS['header'],
            bg=COLORS['header'],
            fg=COLORS['text_light']
        ).pack(pady=15)
        
        # Content
        content = tk.Frame(details, bg=COLORS['background'])
        content.pack(fill='both', expand=True, padx=PADDING['xlarge'], pady=PADDING['large'])
        
        # Create detail rows
        details_data = [
            ("Customer Name", values[1]),
            ("Car Type", values[2]),
            ("Fuel Type", values[3]),
            ("Rental Days", values[4]),
            ("Total Cost", values[5]),
            ("Booking Date", values[6]),
            ("Start Date", values[7]),
            ("End Date", values[8]),
            ("Status", values[9]),
        ]
        
        for label, value in details_data:
            row = tk.Frame(content, bg=COLORS['card'], relief='solid', bd=1)
            row.pack(fill='x', pady=5)
            
            tk.Label(
                row,
                text=label,
                font=FONTS['label'],
                bg=COLORS['card'],
                fg=COLORS['disabled'],
                anchor='w',
                width=15
            ).pack(side='left', padx=15, pady=10)
            
            tk.Label(
                row,
                text=value,
                font=FONTS['normal'],
                bg=COLORS['card'],
                fg=COLORS['text'],
                anchor='w'
            ).pack(side='left', padx=15, pady=10)
        
        # Close Button
        close_btn = tk.Button(
            content,
            text="Close",
            command=details.destroy,
            bg=COLORS['button'],
            fg=COLORS['text_light'],
            font=FONTS['button'],
            relief='flat',
            cursor='hand2',
            padx=30,
            pady=10
        )
        close_btn.pack(pady=(PADDING['large'], 0))
        close_btn.bind('<Enter>', lambda e: close_btn.config(bg=COLORS['button_hover']))
        close_btn.bind('<Leave>', lambda e: close_btn.config(bg=COLORS['button']))
    
    def export_to_csv(self):
        """Export bookings to CSV file."""
        try:
            from tkinter import filedialog
            
            # Ask for file location
            filename = filedialog.asksaveasfilename(
                parent=self.window,
                defaultextension='.csv',
                filetypes=[('CSV files', '*.csv'), ('All files', '*.*')],
                initialfile='wearecars_bookings.csv'
            )
            
            if not filename:
                return
            
            # Get all bookings
            bookings = self.database.get_all_bookings()
            
            # Write to CSV
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(['ID', 'Customer Name', 'Car Type', 'Fuel Type', 'Days', 
                               'Total Cost', 'Booking Date', 'Start Date', 'End Date', 'Status'])
                
                # Write data
                for booking in bookings:
                    writer.writerow(booking)
            
            messagebox.showinfo(
                "Export Successful",
                f"Bookings exported successfully to:\n{filename}",
                parent=self.window
            )
            self.status_label.config(text=f"Exported {len(bookings)} bookings to CSV")
            
        except Exception as e:
            messagebox.showerror(
                "Export Failed",
                f"Failed to export bookings:\n{str(e)}",
                parent=self.window
            )
