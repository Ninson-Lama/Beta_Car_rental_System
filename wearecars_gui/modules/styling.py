import tkinter as tk

# Centralized styling for the WeAreCars app

COLORS = {
    'background': '#0f172a',
    'header': '#1e293b',
    'card': '#111827',
    'border': '#334155',
    'text': '#e5e7eb',
    'text_light': '#f8fafc',
    'disabled': '#94a3b8',
    'primary': '#3b82f6',
    'primary_hover': '#2563eb',
    'secondary': '#64748b',
    'secondary_hover': '#475569',
    'danger': '#ef4444',
    'danger_hover': '#dc2626',
    # Compatibility keys used by some modules
    'button': '#3b82f6',
    'button_hover': '#2563eb',
    'error': '#ef4444',
    'success': '#22c55e',
    'success_hover': '#16a34a',
}

FONTS = {
    'header': ('Segoe UI', 28, 'bold'),
    'subheader': ('Segoe UI', 18, 'bold'),
    'normal': ('Segoe UI', 12),
    'label': ('Segoe UI', 11, 'bold'),
    'entry': ('Segoe UI', 11),
    'button': ('Segoe UI', 12, 'bold'),
    'small': ('Segoe UI', 10),
}

PADDING = {
    'small': 6,
    'medium': 10,
    'large': 16,
    'xlarge': 24,
}

def apply_button_style(button: tk.Button, style: str = 'primary') -> None:
    """Apply a consistent style to Tkinter buttons.

    style: 'primary' | 'secondary' | 'danger'
    """
    bg = COLORS['primary']
    activebg = COLORS['primary_hover']
    fg = COLORS['text_light']
    if style == 'secondary':
        bg = COLORS['secondary']
        activebg = COLORS['secondary_hover']
    elif style == 'danger':
        bg = COLORS['danger']
        activebg = COLORS['danger_hover']

    button.configure(
        bg=bg,
        activebackground=activebg,
        fg=fg,
        activeforeground=fg,
        relief='flat',
        bd=0,
        font=FONTS['normal'],
        cursor='hand2'
    )

def create_styled_frame(parent, bg_color: str = 'background') -> tk.Frame:
    """Create a frame using app color scheme."""
    color = COLORS.get(bg_color, COLORS['background'])
    frame = tk.Frame(parent, bg=color)
    return frame