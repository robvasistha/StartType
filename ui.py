import tkinter as tk
from logic import TypingTestLogic
from plotting import plot_wpm_graph
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class TypingTestApp:
    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the TypingTestApp with the main window, setting up the UI,
        loading texts, and setting the default theme.

        Args:
            root (tk.Tk): The main Tkinter root window.
        """
        self.root = root
        self.root.title("Typing Test")
        self.root.attributes("-topmost", True)  # Keep on top

        self.logic = TypingTestLogic(self)  # Initialize the logic handler

        self.current_theme = "dark"
        self.set_theme(self.current_theme)  # Initialize theme colors here
        self.texts = []
        self.start_time = None  # Initialize start_time for auto-start

        self.logic.load_texts()

        if not self.texts:
            self.show_text_input_window()
        else:
            self.start_main_window()

    def set_theme(self, theme: str) -> None:
        """
        Set the theme of the application to either dark or light mode.
        """
        if theme == "dark":
            self.root.configure(bg="#2E2E2E")
            self.theme_colors = {"bg": "#2E2E2E", "fg": "#FFFFFF", "entry_bg": "#3E3E3E", "entry_fg": "#FFFFFF"}
        else:
            self.root.configure(bg="#FFFFFF")
            self.theme_colors = {"bg": "#FFFFFF", "fg": "#000000", "entry_bg": "#FFFFFF", "entry_fg": "#000000"}

    def toggle_theme(self) -> None:
        """
        Toggle between light and dark themes.
        """
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.set_theme(self.current_theme)
        self.apply_theme()

    def apply_theme(self) -> None:
        """
        Apply the current theme to all UI elements.
        """
        for widget in self.root.winfo_children():
            if isinstance(widget, (tk.Label, tk.Button)):
                widget.config(bg=self.theme_colors["bg"], fg=self.theme_colors["fg"])
            elif isinstance(widget, tk.Entry):
                widget.config(bg=self.theme_colors["entry_bg"], fg=self.theme_colors["entry_fg"], insertbackground=self.theme_colors["fg"])
            elif isinstance(widget, tk.Text):
                widget.config(bg=self.theme_colors["bg"], fg=self.theme_colors["fg"], insertbackground=self.theme_colors["bg"])

    def show_text_input_window(self) -> None:
        """
        Display the initial window where the user is prompted to input text for the typing test.
        """
        self.clear_window()

        self.label = tk.Label(self.root, text="Please input text to train", font=("Helvetica", 16))
        self.label.pack(pady=20)

        self.text_entry = tk.Entry(self.root, width=50, font=("Helvetica", 14))
        self.text_entry.pack(pady=10)

        self.save_button = tk.Button(self.root, text="Submit", command=self.logic.save_text, font=("Helvetica", 14))
        self.save_button.pack(pady=20)

        self.apply_theme()

    def start_main_window(self) -> None:
        """
        Start the main typing test window where the user sees the text and starts the typing test.
        """
        self.clear_window()

        self.set_theme(self.current_theme)
        self.current_text = self.texts[0]
        self.words = self.current_text.split()  # Split the text into words
        self.logic.initialize_test()  # Initialize logic-related variables

        # Use Text widget for display
        self.text_display = tk.Text(self.root, height=10, font=("Helvetica", 16), wrap="word", bd=0, insertwidth=0)
        self.text_display.pack(pady=10)
        self.text_display.insert(tk.END, self.current_text)
        self.text_display.config(state=tk.DISABLED)

        # Use Entry widget for input with slim cursor
        self.entry = tk.Entry(self.root, width=50, font=("Helvetica", 14), insertwidth=1)
        self.entry.pack(pady=10)
        self.entry.bind("<KeyPress>", self.logic.start_test_on_type)
        self.entry.bind("<KeyRelease>", self.logic.update_displayed_text)
        self.entry.bind("<Tab>", self.focus_reset_button)  # Bind Tab to focus the Reset button

        self.wpm_label = tk.Label(self.root, text="WPM: 0", font=("Helvetica", 14))
        self.wpm_label.pack(pady=10)

        self.raw_wpm_label = tk.Label(self.root, text="Raw WPM: 0", font=("Helvetica", 14))
        self.raw_wpm_label.pack(pady=10)

        self.timer_label = tk.Label(self.root, text="Time: 0", font=("Helvetica", 14))
        self.timer_label.pack(pady=10)

        # Add Reset button
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_test, font=("Helvetica", 14))
        self.reset_button.pack(pady=10)
        self.reset_button.bind("<Return>", self.reset_test)  # Bind Enter to trigger reset

        # Add Edit Text button
        self.edit_text_button = tk.Button(self.root, text="Edit Text", command=self.show_text_input_window, font=("Helvetica", 14))
        self.edit_text_button.pack(pady=10)

        self.theme_toggle_button = tk.Button(self.root, text="Toggle Light/Dark Mode", command=self.toggle_theme, font=("Helvetica", 10))
        self.theme_toggle_button.pack(pady=10)

        self.apply_theme()

    def focus_reset_button(self, event=None) -> None:
        """
        Focus the Reset button when Tab is pressed.
        """
        self.reset_button.focus_set()

    def show_summary(self, wpm: float, raw_wpm: float, accuracy: float) -> None:
        """
        Display a summary window with WPM, Raw WPM, accuracy, and a graph of WPM over time.

        Args:
            wpm (float): The words per minute achieved in the current test.
            raw_wpm (float): The raw words per minute including all typed characters.
            accuracy (float): The accuracy percentage achieved in the current test.
        """
        self.clear_window()

        summary_label = tk.Label(self.root, text=f"Test Completed!\nWPM: {wpm:.2f}\nRaw WPM: {raw_wpm:.2f}\nAccuracy: {accuracy:.2f}%", font=("Helvetica", 16))
        summary_label.pack(pady=20)

        plot_wpm_graph(self)

        restart_button = tk.Button(self.root, text="Restart", command=self.start_main_window, font=("Helvetica", 14))
        restart_button.pack(pady=20)
        restart_button.bind("<Tab>", self.focus_reset_button)  # Bind Tab to focus the Reset button

        self.apply_theme()

    def clear_window(self) -> None:
        """
        Clear all widgets from the current window.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

    def reset_test(self, event=None) -> None:
        """
        Reset the typing test, clearing the current progress and restarting the test.
        """
        self.start_main_window()

    def emergency_exit(self, event=None) -> None:
        """
        Handle the emergency exit by closing the application.
        """
        self.root.destroy()
