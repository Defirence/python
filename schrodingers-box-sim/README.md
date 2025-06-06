# Schrödinger's Box Quantum Simulator

## Project Overview

This project provides a simple graphical user interface (GUI) application built with Python's `tkinter` and `matplotlib` to simulate a "Schrödinger's Box" quantum system. It demonstrates key concepts in quantum mechanics, such as superposition, measurement, and the probabilistic nature of quantum outcomes (Born rule).

The simulator allows users to define a quantum system with multiple possible states and their corresponding probability amplitudes. You can then perform either single measurements (observing a single "collapsed" outcome) or run many measurements to statistically observe the distribution of outcomes, comparing them against the theoretically predicted probabilities.

## Features

* **Customizable Quantum States:** Define any number of states for your system (e.g., "Alive", "Dead", "Left", "Right", "Spin Up", "Spin Down").
* **Amplitude Input:** Assign real or complex probability amplitudes to each state. The simulator automatically normalizes these to calculate the correct probabilities.
* **Single Measurement Simulation:** Click a button to "open the box" and see a single, definite outcome, simulating quantum collapse upon measurement.
* **Multiple Measurement Simulation:** Run a large number of trials to observe the statistical distribution of outcomes.
* **Interactive Visualization:** A `matplotlib` bar chart embedded in the GUI displays the simulated frequencies alongside the theoretically expected probabilities, demonstrating the convergence predicted by the Born rule.
* **Error Handling:** Robust input validation and error messages guide the user.

## Core Quantum Concepts Illustrated

* **Superposition:** Although not directly visualized, the input amplitudes represent the system existing in a superposition of states before measurement.
* **Measurement Problem / Collapse:** The "Measure One" button simulates the act of observation, which forces the system to "collapse" into a single classical state.
* **Born Rule:** The "Simulate Many Trials" feature demonstrates that the probability of measuring a particular state is proportional to the square of its amplitude ($P_i = |\psi_i|^2$). Over many trials, the observed frequencies converge to these probabilities.

## Installation

1.  **Clone the repository (or copy the code):**
    Clone:
    ```bash
    git clone [https://github.com/yourusername/schrodinger-box-simulator.git](https://github.com/yourusername/schrodinger-box-simulator.git)
    cd schrodinger-box-simulator
    ```
    Run with: `python schrodinger_box_simulator.py`.

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install numpy matplotlib
    ```
    `tkinter` is typically included with Python standard library installations.

## How to Run

After installing dependencies, simply run the Python script:

```bash
python schrodinger_box_simulator.py

Co-written and tested in orchestra with Google Gemini Flash 2.x
