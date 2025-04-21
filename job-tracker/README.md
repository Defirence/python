# Thunderbird Email Analyzer

This project is a Python application that provides a graphical user interface (GUI) for analyzing emails from a specified Gmail label. It allows users to authenticate via Google, retrieve emails, extract dates from the email headers, and visualize the data through graphs.

## Features

- Parses email text files exported from Thunderbird or other email clients.
- Extracts dates from email headers.
- Visualizes email frequency over time using matplotlib.
- Simple GUI built with PyQt5 for easy interaction.

## Requirements

To run this project, you need to have Python installed along with the following dependencies:

- matplotlib
- PyQt5
- numpy
- scikit-learn

## Setup Instructions

1.  Clone the repository:

    ```
    git clone https://github.com/yourusername/python-gui-gmail-analyzer.git
    cd python-gui-gmail-analyzer
    ```
2.  Create a virtual environment (optional but recommended):

    ```
    python -m venv venv
    source venv/bin/activate   # On Linux or macOS
    venv\Scripts\activate  # On Windows
    ```
3.  Install the required packages:

    ```
    pip install -r requirements.txt
    ```

## Usage

1.  **Export your emails (Optional):** Export your emails from Thunderbird (or your email client) as a text file. Each email should be separated by an empty line.
2.  **Run the application:**

    ```
    python main.py
    ```
3.  **Select the Email Text File (Recommended):** Click the "Select Email Text File" button and choose the text file you exported.
4.  **Generate Graph:** Click the "Generate Graph" button to parse the file and display a graph showing the distribution of emails over time.  The graph will group emails by month and year, and display an average line.

## Notes

*   The application parses the 'Date' header in each email to extract the date.
*   Ensure that your email export format separates each email with an empty line for correct parsing.

## License

This project is licensed under the WTFPL License - see the [LICENSE](LICENSE) file for details.

## Screenshots
![Screenshot 1](screenshots/screenshot1.png)

![Screenshot 2](screenshots/screenshot2.png)

![Screenshot 3](screenshots/screenshot3.png)