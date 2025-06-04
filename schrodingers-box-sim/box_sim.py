import tkinter as tk
from tkinter import messagebox, scrolledtext
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk # Corrected import

print("Script started.")

class SchrodingersBox:
    """
    Simulates a simplified quantum system representing a Schrödinger's Box.
    Particles exist in a superposition of states until measured.
    """
    def __init__(self, states_amplitudes: dict):
        """
        Initializes the Schrödinger's Box with given states and their amplitudes.
        Amplitudes can be real or complex numbers.
        Example: {'Left': 1/np.sqrt(2), 'Right': 1j/np.sqrt(2)}
        """
        if not states_amplitudes:
            raise ValueError("States and amplitudes dictionary cannot be empty.")

        self.states = list(states_amplitudes.keys())
        # Ensure amplitudes are treated as complex numbers for generality
        self.amplitudes = np.array(list(states_amplitudes.values()), dtype=complex)

        # Normalize amplitudes to ensure sum of probabilities is 1
        # Sum of squared absolute values gives the total "probability mass"
        norm_factor_sq = np.sum(np.abs(self.amplitudes)**2)
        if norm_factor_sq == 0:
            raise ValueError("Sum of squared amplitudes is zero. Cannot normalize.")
        self.amplitudes /= np.sqrt(norm_factor_sq) # Normalize the amplitudes

        self.probabilities = np.abs(self.amplitudes)**2 # Probabilities are |amplitude|^2

    def measure(self) -> str:
        """
        Simulates a single measurement, causing the superposition to collapse.
        Returns the measured state based on the probabilities.
        """
        # np.random.choice automatically handles the weights (probabilities)
        chosen_state = np.random.choice(self.states, p=self.probabilities)
        return chosen_state

    def simulate_measurements(self, num_trials: int) -> dict:
        """
        Simulates multiple measurements and returns the counts of each outcome.
        """
        if num_trials <= 0:
            raise ValueError("Number of trials must be positive.")
        outcomes = [self.measure() for _ in range(num_trials)]
        return Counter(outcomes)

    def get_state_info(self) -> str:
        """Returns a formatted string of the box's configuration."""
        info = "--- Schrödinger's Box Configuration ---\n"
        info += "States and Amplitudes (Normalized):\n"
        for state, amp, prob in zip(self.states, self.amplitudes, self.probabilities):
            info += f"  {state}: Amplitude = {amp:.3f}, Probability = {prob:.3f}\n"
        info += f"Total Probability Sum: {np.sum(self.probabilities):.3f}\n"
        info += "-" * 37 + "\n"
        return info


class SchrodingerBoxGUI:
    def __init__(self, master):
        print("SchrödingerBoxGUI __init__ started.")
        self.master = master
        master.title("Schrödinger's Box Simulator")
        master.geometry("800x700") # Initial window size

        self.schrodinger_box = None # Will hold an instance of SchrödingersBox

        # --- 1. Box Configuration Frame ---
        print("Creating config frame.")
        self.config_frame = tk.LabelFrame(master, text="Define Quantum States", padx=10, pady=10)
        self.config_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(self.config_frame, text="States (comma-separated):").grid(row=0, column=0, sticky="w", pady=2)
        self.states_entry = tk.Entry(self.config_frame, width=50)
        self.states_entry.grid(row=0, column=1, padx=5, pady=2)
        self.states_entry.insert(0, "Left,Right") # Default example

        tk.Label(self.config_frame, text="Amplitudes (comma-separated):").grid(row=1, column=0, sticky="w", pady=2)
        self.amplitudes_entry = tk.Entry(self.config_frame, width=50)
        self.amplitudes_entry.grid(row=1, column=1, padx=5, pady=2)
        self.amplitudes_entry.insert(0, "1,1") # Default example (will be normalized to 1/sqrt(2), 1/sqrt(2))

        # Pylint disable added here
        self.set_box_button = tk.Button(self.config_frame, text="Set Box Configuration", command=self._set_box) # pylint: disable=no-member
        self.set_box_button.grid(row=2, column=0, columnspan=2, pady=10)
        self.box_info_text = scrolledtext.ScrolledText(self.config_frame, height=5, state='disabled', wrap=tk.WORD)
        self.box_info_text.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")

        # --- 2. Single Measurement Frame ---
        self.single_measure_frame = tk.LabelFrame(master, text="Single Measurement", padx=10, pady=10)
        self.single_measure_frame.pack(pady=10, padx=10, fill="x")

        # Pylint disable added here
        self.measure_one_button = tk.Button(self.single_measure_frame, text="Measure One (Open Box)", command=self._measure_one, state='disabled') # pylint: disable=no-member
        self.measure_one_button.pack(pady=5)

        self.last_measurement_label = tk.Label(self.single_measure_frame, text="Last Measurement Result: N/A", font=("Arial", 12))
        self.last_measurement_label.pack(pady=5)

        # --- 3. Many Measurements Frame ---
        self.many_measure_frame = tk.LabelFrame(master, text="Multiple Measurements (Statistical Outcome)", padx=10, pady=10)
        self.many_measure_frame.pack(pady=10, padx=10, fill="both", expand=True)

        tk.Label(self.many_measure_frame, text="Number of Trials:").grid(row=0, column=0, sticky="w", pady=2)
        self.num_trials_entry = tk.Entry(self.many_measure_frame, width=10)
        self.num_trials_entry.grid(row=0, column=1, padx=5, pady=2, sticky="w")
        self.num_trials_entry.insert(0, "1000") # Default trials
        # Pylint disable added here
        self.simulate_many_button = tk.Button(self.many_measure_frame, text="Simulate Many Trials", command=self._simulate_many, state='disabled') # pylint: disable=no-member
        self.simulate_many_button.grid(row=0, column=2, padx=10, pady=2, sticky="w")
        # Matplotlib plot area
        self.fig, self.ax = plt.subplots(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.many_measure_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=1, column=0, columnspan=3, pady=10, padx=5, sticky="nsew")

        # Add Matplotlib toolbar
        # IMPORTANT FIX: pack_toolbar=False to prevent default packing, then use grid()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.many_measure_frame, pack_toolbar=False)
        self.toolbar.update()
        # This line was missing or incomplete in your provided code, causing the crash:
        self.toolbar.grid(row=2, column=0, columnspan=3, sticky="ew") # Place toolbar below the canvas

        self.many_measure_frame.grid_rowconfigure(1, weight=1)
        self.many_measure_frame.grid_columnconfigure(1, weight=1) # Allow plot to expand

        # --- 4. Status Bar ---
        self.status_label = tk.Label(master, text="Ready.", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        # Initialize the box with default values on startup
        print("Calling _set_box from __init__.")
        self._set_box()
        print("SchrödingerBoxGUI __init__ finished.")

    def _update_status(self, message, is_error=False):
        """Updates the status bar with a message."""
        self.status_label.config(text=message, fg="red" if is_error else "black")

    def _update_box_info_text(self, text):
        """Updates the scrolled text widget with box configuration info."""
        self.box_info_text.config(state='normal') # Enable editing
        self.box_info_text.delete(1.0, tk.END) # Clear existing text
        self.box_info_text.insert(tk.END, text) # Insert new text
        self.box_info_text.config(state='disabled') # Disable editing

    def _set_box(self):
        """Attempts to set the Schrödinger's Box configuration based on user input."""
        states_str = self.states_entry.get()
        amplitudes_str = self.amplitudes_entry.get()

        if not states_str or not amplitudes_str:
            self._update_status("Error: Please enter both states and amplitudes.", is_error=True)
            return

        states = [s.strip() for s in states_str.split(',') if s.strip()]
        try:
            # Safely evaluate amplitudes to allow complex numbers (e.g., '1j', '0.5+0.5j')
            import ast
            amplitudes_raw = [ast.literal_eval(a.strip()) for a in amplitudes_str.split(',') if a.strip()]
        except (SyntaxError, NameError, ValueError) as e:
            self._update_status(f"Error parsing amplitudes: {e}. Ensure they are valid numbers.", is_error=True)
            return

        if len(states) != len(amplitudes_raw):
            self._update_status("Error: Number of states must match number of amplitudes.", is_error=True)
            return

        if not states:  # After stripping and splitting, lists might be empty
            self._update_status("Error: No valid states or amplitudes entered.", is_error=True)
            return

        states_amplitudes_dict = dict(zip(states, amplitudes_raw))

        try:
            self.schrodinger_box = SchrodingersBox(states_amplitudes_dict)
            self._update_status("Box configured successfully. Ready for measurements.")
            self._update_box_info_text(self.schrodinger_box.get_state_info())
            self.measure_one_button.config(state='normal')
            self.simulate_many_button.config(state='normal')
            self.last_measurement_label.config(text="Last Measurement Result: N/A")
            self.ax.clear()
            self.ax.set_title("Simulate Many Trials to see the distribution")
            self.ax.set_ylabel("Occurrences")
            self.canvas.draw()
        except ValueError as e:
            self._update_status(f"Configuration Error: {e}", is_error=True)
            self.measure_one_button.config(state='disabled')
            self.simulate_many_button.config(state='disabled')
            self.last_measurement_label.config(text="Last Measurement Result: N/A")
            self._update_box_info_text("Invalid configuration. Please check inputs.")
        except (TypeError, SyntaxError) as e:
            self._update_status(f"An unexpected error occurred during configuration: {e}", is_error=True)

    def _measure_one(self):
        """Performs a single measurement and updates the result label."""
        if self.schrodinger_box is None:
            messagebox.showerror("Error", "Please set the box configuration first.")
            return

        try:
            outcome = self.schrodinger_box.measure()
            self.last_measurement_label.config(text=f"Last Measurement Result: {outcome}")
            self._update_status(f"Measured: {outcome}")
        except (ValueError, RuntimeError) as e:
            self._update_status(f"Measurement Error: {e}", is_error=True)
            messagebox.showerror("Measurement Error", f"Could not perform measurement: {e}")

    def _simulate_many(self):
        """Simulates many measurements and displays results in a bar chart."""
        if self.schrodinger_box is None:
            messagebox.showerror("Error", "Please set the box configuration first.")
            return

        try:
            num_trials = int(self.num_trials_entry.get())
            if num_trials <= 0:
                raise ValueError("Number of trials must be a positive integer.")
        except ValueError:
            self._update_status("Error: Invalid number of trials. Please enter a positive integer.", is_error=True)
            return

        try:
            results_counts = self.schrodinger_box.simulate_measurements(num_trials)
            # Prepare data for plotting
            states_order = self.schrodinger_box.states # Maintain consistent order
            simulated_counts = [results_counts.get(state, 0) for state in states_order]
            expected_probabilities = [self.schrodinger_box.probabilities[self.schrodinger_box.states.index(state)] for state in states_order]
            expected_counts = [p * num_trials for p in expected_probabilities]

            # Clear previous plot
            self.ax.clear()

            x = np.arange(len(states_order))
            width = 0.35

            self.ax.bar(x - width/2, simulated_counts, width, label=f'Simulated Counts ({num_trials} trials)', color='skyblue')
            self.ax.bar(x + width/2, expected_counts, width, label='Expected Counts', color='lightcoral')

            self.ax.set_ylabel('Number of Occurrences')
            self.ax.set_title(f'Schrödinger\'s Box Outcomes over {num_trials} Measurements')
            self.ax.set_xticks(x)
            self.ax.set_xticklabels(states_order, rotation=45, ha='right')
            self.ax.legend()
            self.ax.grid(axis='y', linestyle='--', alpha=0.7)
            self.fig.tight_layout() # Adjust layout to prevent labels overlapping

            self.canvas.draw()
            self._update_status(f"Simulated {num_trials} trials. Results updated in chart.")
        except (ValueError, RuntimeError) as e:
            self._update_status(f"Simulation Error: {e}", is_error=True)
            messagebox.showerror("Simulation Error", f"Could not run simulation: {e}")

# Main execution
if __name__ == "__main__":
    print("Main execution block started.")
    try:
        root = tk.Tk()
        print("Tkinter root window created.")
        app = SchrodingerBoxGUI(root)
        print("SchrodingerBoxGUI instance created.")
        root.mainloop()
        print("Mainloop exited.")
    except (tk.TclError, RuntimeError) as e:
        print(f"An unexpected error occurred during main execution: {e}")
        import traceback
        traceback.print_exc()

print("Script finished.")
