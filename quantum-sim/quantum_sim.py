import tkinter as tk
import random
import datetime
import math
import hashlib # To create a more unique seed from multiple inputs

# --- Configuration ---
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
NUM_DIMENSIONS = 4 # Can be 4 or 5
NUM_POINTS = 50    # Number of points to simulate
SIMULATION_SPEED_MS = 50 # Milliseconds between simulation steps

# --- Projection Settings ---
# Simple perspective-like projection parameters (can be adjusted)
PROJECTION_DISTANCE_4D_TO_3D = 2.0
PROJECTION_DISTANCE_3D_TO_2D = 500.0 # Distance from viewer to screen

# --- Global Simulation State ---
points = []
CANVAS = None
ROOT = None
IS_RUNNING = False

# --- Functions to Influence Randomness ---

def get_random_seed(use_datetime=True, use_location=True, latitude=0.0, longitude=0.0):
    """Generates a seed for the random number generator."""
    seed_components = []

    if use_datetime:
        now = datetime.datetime.now()
        # Include microsecond for higher variability
        seed_components.append(str(now.timestamp()))

    if use_location:
        # Use latitude and longitude (replace with user input if desired)
        # Note: I am using placeholder values as I cannot use your actual location.
        # These are example coordinates (near a park in San Francisco)
        example_latitude = 37.7749
        example_longitude = -122.4194
        seed_components.append(f"{example_latitude},{example_longitude}")

    # Add some system-specific randomness if possible (though less reliable cross-platform)
    # seed_components.append(str(random.getrandbits(128))) # Can add more system entropy

    # Combine components and create a hash for a robust seed
    combined_string = "_".join(seed_components)
    if not combined_string:
        # Fallback if no components are used
        return random.getrandbits(128)
    else:
        # Use SHA-256 hash of the string as the seed
        return int(hashlib.sha256(combined_string.encode('utf-8')).hexdigest(), 16)

def initialize_randomness(use_datetime=True, use_location=True, latitude=0.0, longitude=0.0):
    """Initializes the random number generator with a seed."""
    seed = get_random_seed(use_datetime, use_location, latitude, longitude)
    random.seed(seed)
    print(f"Randomness seeded with: {seed}")

# --- 4D/5D Object Representation ---

def create_random_points(num_points, num_dimensions):
    """Creates a list of random points in the specified dimensions."""
    points = []
    for _ in range(num_points):
        point = [random.uniform(-1, 1) for _ in range(num_dimensions)] # Points within a unit hypercube
        points.append(point)
    return points

# --- Simple "Quantum Calculation" (Random Evolution) ---

def evolve_points_randomly(points, influence_factor=0.05):
    """
    Simulates a simple random evolution of the points.
    This is NOT a physical quantum calculation but meets the
    requirement of calculation based on randomness.
    """
    for point in points:
        for i in range(len(point)):
            # Add a small random change to each coordinate
            change = random.uniform(-influence_factor, influence_factor)
            point[i] += change
            # Optional: Add constraints, e.g., keep points within a bound
            # point[i] = max(-2, min(2, point[i]))

# --- Higher Dimension Projection ---

def project_4d_to_3d(point_4d, distance=PROJECTION_DISTANCE_4D_TO_3D):
    """Projects a 4D point to 3D using a simple perspective-like projection."""
    # Basic perspective projection: x_3d = x_4d / (distance - w)
    # Avoid division by zero or near-zero if distance == w
    w = point_4d[3]
    divisor = distance - w
    if abs(divisor) < 1e-6:
        divisor = 1e-6 # Avoid division by zero

    x_3d = point_4d[0] / divisor
    y_3d = point_4d[1] / divisor
    z_3d = point_4d[2] / divisor
    return [x_3d, y_3d, z_3d]

def project_5d_to_3d(point_5d, distance_w=PROJECTION_DISTANCE_4D_TO_3D, distance_v=PROJECTION_DISTANCE_4D_TO_3D):
    """Projects a 5D point to 3D in two steps (5D->4D->3D)."""
    # Project 5D to 4D first
    v = point_5d[4]
    divisor_v = distance_v - v
    if abs(divisor_v) < 1e-6:
         divisor_v = 1e-6

    x_4d = point_5d[0] / divisor_v
    y_4d = point_5d[1] / divisor_v
    z_4d = point_5d[2] / divisor_v
    w_4d = point_5d[3] / divisor_v
    point_4d = [x_4d, y_4d, z_4d, w_4d]

    # Then project 4D to 3D
    return project_4d_to_3d(point_4d, distance_w)


def project_3d_to_2d(point_3d, distance=PROJECTION_DISTANCE_3D_TO_2D, fov=1.0):
    """Projects a 3D point to 2D using a simple perspective projection."""
    # Simple perspective projection onto a 2D plane (screen)
    # x_2d = (x_3d * distance) / (z_3d + distance)
    # y_2d = (y_3d * distance) / (z_3d + distance)
    # We can simplify by scaling based on z_3d directly if distance is large

    # Scale the point based on its 'depth' (z_3d)
    # Add distance to z_3d to handle points behind the viewer
    z_scaled = point_3d[2] + distance
    if z_scaled < 1e-6: # Avoid division by zero or projecting points far behind
        z_scaled = 1e-6

    x_2d = (point_3d[0] * distance * fov) / z_scaled
    y_2d = (point_3d[1] * distance * fov) / z_scaled

    # Translate to screen coordinates
    screen_x = x_2d + WINDOW_WIDTH // 2
    screen_y = y_2d + WINDOW_HEIGHT // 2 # Invert y for screen coordinates (origin top-left)

    return [screen_x, screen_y]

def project_nd_to_2d(point, num_dimensions):
    """Handles projection from N dimensions down to 2D."""
    if num_dimensions == 4:
        point_3d = project_4d_to_3d(point)
    elif num_dimensions == 5:
        point_3d = project_5d_to_3d(point)
    else:
        # For 3D points or fewer, just use the available dimensions
        point_3d = point[:3] + [0]*(3 - len(point[:3])) # Pad with zeros if less than 3D

    point_2d = project_3d_to_2d(point_3d)
    return point_2d

# --- Rendering ---

def draw_points(canvas, points_2d):
    """Draws the projected 2D points on the canvas."""
    canvas.delete("all") # Clear previous frame
    for x, y in points_2d:
        # Draw a small circle for each point
        radius = 2
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="white", outline="")

# --- Simulation Loop ---

def update_simulation():
    """Updates the simulation state and redraws."""
    if not is_running:
        return

    global points
    evolve_points_randomly(points) # Perform the random evolution

    # Project points to 2D
    points_2d = [project_nd_to_2d(p, NUM_DIMENSIONS) for p in points]

    # Draw on canvas
    draw_points(canvas, points_2d)

    # Schedule the next update
    root.after(SIMULATION_SPEED_MS, update_simulation)

# --- GUI Setup ---

def start_simulation():
    """Starts the simulation loop."""
    global is_running
    is_running = True
    update_simulation()

def stop_simulation():
    """Stops the simulation loop."""
    global is_running
    is_running = False

def reset_simulation():
    """Resets the simulation with new initial conditions."""
    global points
    # Re-initialize randomness with potential new seed
    initialize_randomness(use_datetime=True, use_location=True) # Options can be made configurable

    # Create new initial points
    points = create_random_points(NUM_POINTS, NUM_DIMENSIONS)

    # Stop if running, then start again
    stop_simulation()
    start_simulation()


def setup_gui():
    """Sets up the main application window and widgets."""
    global root, canvas, points

    root = tk.Tk()
    root.title("Quantum-like Random Simulation")

    # Create canvas for drawing
    canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black")
    canvas.pack(pady=10)

    # Control buttons
    control_frame = tk.Frame(root)
    control_frame.pack(pady=5)

    start_button = tk.Button(control_frame, text="Start", command=start_simulation)
    start_button.grid(row=0, column=0, padx=5)

    stop_button = tk.Button(control_frame, text="Stop", command=stop_simulation)
    stop_button.grid(row=0, column=1, padx=5)

    reset_button = tk.Button(control_frame, text="Reset", command=reset_simulation)
    reset_button.grid(row=0, column=2, padx=5)

    # --- Options/Configuration (can be expanded with entry fields) ---
    # For this example, we'll keep options internal but the framework is here
    # to add widgets for toggling datetime/location influence, changing dimensions, etc.

    # Initial setup
    reset_simulation() # Initialize points and start simulation immediately

    root.mainloop()

# --- Main Execution ---

if __name__ == "__main__":
    # Example of how to use the randomness with explicit latitude/longitude
    # You could add GUI elements to input these values if desired.
    # initialize_randomness(use_datetime=True, use_location=True, latitude=34.0522, longitude=-118.2437)
    # Example LA coords

    setup_gui()
