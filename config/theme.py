# Color scheme
COLORS = {
    'background': '#1A365D',      # Dark blue background
    'secondary_bg': '#2D3748',    # Slightly lighter background
    'accent': '#4299E1',          # Bright blue accent
    'accent_hover': '#2B6CB0',    # Darker blue for hover states
    'text': '#E2E8F0',           # Light gray text
    'disabled': '#718096',        # Disabled state color
    'error': '#FC8181',          # Error color
    'success': '#68D391'         # Success color
}

# Style sheets
MAIN_STYLE = f"""
    QMainWindow, QDialog, QWidget {{
        background-color: {COLORS['background']};
    }}
    QLabel {{
        color: {COLORS['text']};
        font-size: 12px;
        margin: 2px;
    }}
    QPushButton {{
        background-color: {COLORS['accent']};
        color: {COLORS['text']};
        padding: 6px 12px;
        border-radius: 4px;
        border: none;
        min-width: 80px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {COLORS['accent_hover']};
    }}
    QPushButton:disabled {{
        background-color: {COLORS['disabled']};
    }}
"""

DIALOG_STYLE = f"""
    QDialog {{
        background-color: {COLORS['background']};
    }}
    QLabel {{
        color: {COLORS['text']};
    }}
"""

LIST_STYLE = f"""
    QListWidget {{
        border: 1px solid {COLORS['accent']};
        border-radius: 4px;
        background-color: {COLORS['secondary_bg']};
        color: {COLORS['text']};
    }}
"""

PROGRESS_STYLE = f"""
    QProgressBar {{
        border: 1px solid {COLORS['accent']};
        border-radius: 4px;
        text-align: center;
        background-color: {COLORS['secondary_bg']};
        color: {COLORS['text']};
    }}
    QProgressBar::chunk {{
        background-color: {COLORS['accent']};
    }}
"""

# Combined style for easy application
COMBINED_STYLE = "\n".join([MAIN_STYLE, LIST_STYLE, PROGRESS_STYLE])