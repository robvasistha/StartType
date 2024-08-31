import tkinter as tk
from ui import TypingTestApp

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingTestApp(root)
    root.bind('<Control-Shift-E>', app.emergency_exit)  # Hidden command to exit
    root.mainloop()
