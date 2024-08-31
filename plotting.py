from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def plot_wpm_graph(ui) -> None:
    """
    Plot a graph of WPM and Raw WPM over time using Matplotlib, embedded directly into the Tkinter window.
    """
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(ui.logic.wpm_history, label='WPM')
    ax.plot(ui.logic.raw_wpm_history, label='Raw WPM')
    ax.set_xlabel('Words')
    ax.set_ylabel('WPM')
    ax.set_title('WPM and Raw WPM Over Time')
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=ui.root)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=20)
