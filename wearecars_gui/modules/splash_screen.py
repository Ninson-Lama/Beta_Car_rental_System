"""
Splash Screen - Welcome Window
WeAreCars Car Rental System
"""

import tkinter as tk
from tkinter import ttk
from modules.styling import COLORS, FONTS, PADDING

class SplashScreen:
    def __init__(self, parent, on_continue):
        """Initialize the splash screen."""
        self.parent = parent
        self.on_continue = on_continue
        self.window = tk.Toplevel(parent)
        self.window.title("WeAreCars - Welcome")
        self.window.geometry("500x400")
        self.window.configure(bg=COLORS['background'])
        self.window.resizable(False, False)  # Disable resizing for simplicity
        
        # Center the window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.window.winfo_screenheight() // 2) - (400 // 2)
        self.window.geometry(f"500x400+{x}+{y}")
        
        # Window configuration for stability
        self.window.transient(parent)
        self.window.lift()
        self.window.focus_force()
        self.window.update_idletasks()
        
        # Prevent abnormal closing
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.setup_ui()
    
    def on_closing(self):
        """Handle window close event."""
        self.window.destroy()
        self.on_continue()
    
    def setup_ui(self):
        """Create the splash screen UI."""
        # Header Frame
        header_frame = tk.Frame(self.window, bg=COLORS['header'], height=100)
        header_frame.pack(fill='x', pady=0)
        header_frame.pack_propagate(False)
        
        # Logo/Title
        title_label = tk.Label(
            header_frame,
            text="🚗 WeAreCars",
            font=('Segoe UI', 32, 'bold'),
            bg=COLORS['header'],
            fg=COLORS['text_light']
        )
        title_label.pack(pady=25)
        
        # Main Content: scrollable area
        container = tk.Frame(self.window, bg=COLORS['background'])
        container.pack(fill='both', expand=True, padx=PADDING['xlarge'], pady=PADDING['large'])
        canvas = tk.Canvas(container, bg=COLORS['background'], highlightthickness=0)
        vsb = tk.Scrollbar(container, orient='vertical', command=canvas.yview)
        content_frame = tk.Frame(canvas, bg=COLORS['background'])
        content_frame_id = canvas.create_window((0, 0), window=content_frame, anchor='nw')
        canvas.configure(yscrollcommand=vsb.set)
        canvas.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')
        
        def _on_resize(event):
            canvas.itemconfigure(content_frame_id, width=event.width)
        def _on_configure(event):
            canvas.configure(scrollregion=canvas.bbox('all'))
        content_frame.bind('<Configure>', _on_configure)
        container.bind('<Configure>', _on_resize)
        
        # Welcome Message
        welcome_label = tk.Label(
            content_frame,
            text="Welcome to WeAreCars\nRental Management System",
            font=FONTS['subheader'],
            bg=COLORS['background'],
            fg=COLORS['text'],
            justify='center'
        )
        welcome_label.pack(pady=(20, 10))
        
        # Subtitle
        subtitle_label = tk.Label(
            content_frame,
            text="Professional Car Rental Solution",
            font=FONTS['normal'],
            bg=COLORS['background'],
            fg=COLORS['disabled']
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Features Frame
        features_frame = tk.Frame(content_frame, bg=COLORS['background'])
        features_frame.pack(pady=PADDING['medium'])
        
        features = [
            "✓ Easy Booking Process",
            "✓ Multiple Car Types",
            "✓ Flexible Rental Options",
            "✓ Professional Service"
        ]
        
        for feature in features:
            feature_label = tk.Label(
                features_frame,
                text=feature,
                font=FONTS['normal'],
                bg=COLORS['background'],
                fg=COLORS['text'],
                anchor='w'
            )
            feature_label.pack(anchor='w', pady=2)
        
        # Button Frame
        button_frame = tk.Frame(content_frame, bg=COLORS['background'])
        button_frame.pack(side='bottom', pady=PADDING['large'])
        
        # Instructions Button
        instructions_btn = tk.Button(
            button_frame,
            text="📖 View Instructions",
            command=self.show_instructions,
            bg=COLORS['border'],
            fg=COLORS['text'],
            font=FONTS['button'],
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=8
        )
        instructions_btn.pack(side='left', padx=5)
        
        # Start Button
        start_btn = tk.Button(
            button_frame,
            text="Start Application →",
            command=self.continue_to_login,
            bg=COLORS['button'],
            fg=COLORS['text_light'],
            font=FONTS['button'],
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=8
        )
        start_btn.pack(side='left', padx=5)

        # Exit Button
        exit_btn = tk.Button(
            button_frame,
            text="Exit",
            command=self.exit_application,
            bg=COLORS['error'],
            fg=COLORS['text_light'],
            font=FONTS['button'],
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=8
        )
        exit_btn.pack(side='left', padx=5)
        self.bind_hover_effect(exit_btn, COLORS['error'], '#c0392b')
        
        # Bind hover effects
        self.bind_hover_effect(instructions_btn, COLORS['border'], COLORS['disabled'])
        self.bind_hover_effect(start_btn, COLORS['button'], COLORS['button_hover'])
        
        # Bind Enter key
        self.window.bind('<Return>', lambda e: self.continue_to_login())
    
    def bind_hover_effect(self, button, normal_color, hover_color):
        """Add hover effect to button."""
        button.bind('<Enter>', lambda e: button.config(bg=hover_color))
        button.bind('<Leave>', lambda e: button.config(bg=normal_color))
    
    def show_instructions(self):
        """Show instructions dialog."""
        instructions_window = tk.Toplevel(self.window)
        instructions_window.title("Instructions")
        instructions_window.geometry("500x400")
        instructions_window.configure(bg=COLORS['background'])
        
        # Center the window
        instructions_window.update_idletasks()
        x = (instructions_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (instructions_window.winfo_screenheight() // 2) - (400 // 2)
        instructions_window.geometry(f"500x400+{x}+{y}")
        
        # Header
        header = tk.Label(
            instructions_window,
            text="How to Use WeAreCars",
            font=FONTS['header'],
            bg=COLORS['background'],
            fg=COLORS['text']
        )
        header.pack(pady=PADDING['large'])
        
        # Instructions Text
        instructions_text = tk.Text(
            instructions_window,
            wrap='word',
            font=FONTS['normal'],
            bg=COLORS['card'],
            fg=COLORS['text'],
            relief='flat',
            padx=PADDING['medium'],
            pady=PADDING['medium']
        )
        instructions_text.pack(fill='both', expand=True, padx=PADDING['large'], pady=(0, PADDING['medium']))
        
        instructions = """Welcome to WeAreCars Rental System!

Getting Started:
1. Login with your credentials
   - Username: sta001
   - Password: password

Main Dashboard:
• Create New Booking - Start a rental booking
• View Rented Cars - See all active rentals
• Reports/Statistics - View business metrics
• Logout - Exit to login screen

Creating a Booking:
1. Enter customer details (name, address, age)
2. Select rental period (1-28 days)
3. Choose car type and fuel preference
4. Add optional extras if needed
5. Review summary and confirm

Navigation Tips:
• Use the menu bar for quick access
• Click buttons to navigate between screens
• All changes are saved automatically
• Use search to find specific bookings

For assistance, contact support."""
        
        instructions_text.insert('1.0', instructions)
        instructions_text.config(state='disabled')
        
        # Close Button
        close_btn = tk.Button(
            instructions_window,
            text="Close",
            command=instructions_window.destroy,
            bg=COLORS['button'],
            fg=COLORS['text_light'],
            font=FONTS['button'],
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=8
        )
        close_btn.pack(pady=(0, PADDING['large']))
        
        self.bind_hover_effect(close_btn, COLORS['button'], COLORS['button_hover'])
    
    def continue_to_login(self):
        """Close splash and continue to login."""
        self.window.destroy()
        self.on_continue()

    def exit_application(self):
        """Exit the entire application from splash."""
        try:
            self.parent.quit()
        except Exception as e:
            print(f"Error exiting application: {e}")

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    splash = SplashScreen(root, lambda: print("Continue to login"))
    root.mainloop()