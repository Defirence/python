import sys
import os
import email
from email.utils import parsedate_to_datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QFileDialog, QWidget
import matplotlib.pyplot as plt
from datetime import datetime

# %appdata%\Roaming\thunderbird\Profiles\xyz.default-release\ImapMail\imap.gmail.com\labelName.txt 

# The default path requires your unique path for the Thunderbird profile. 
# The labels that are synchronized through the Gmail IMAP server are stored as raw text files on Windows. I presume it's the same for Linux and MacOS.

# Required libraries
# matplotlib
# PyQt5
# numpy
# scikit-learn

class ThunderbirdAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thunderbird Email Analyzer")
        self.setGeometry(100, 100, 600, 400)

        # Main layout
        self.layout = QVBoxLayout()

        # Buttons and labels
        self.select_file_button = QPushButton("Select Email Text File")
        self.select_file_button.clicked.connect(self.select_text_file)
        self.layout.addWidget(self.select_file_button)

        self.graph_button = QPushButton("Generate Graph")
        self.graph_button.clicked.connect(self.generate_graph)
        self.graph_button.setEnabled(False)
        self.layout.addWidget(self.graph_button)

        self.status_label = QLabel("Status: No file selected")
        self.layout.addWidget(self.status_label)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        self.text_file_path = None
        self.dates = []

    def select_text_file(self):
        """Open a file dialog to select a text file."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Email Text File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_path:
            self.text_file_path = file_path
            self.status_label.setText(f"Status: Selected {os.path.basename(file_path)}")
            self.graph_button.setEnabled(True)

    def generate_graph(self):
        """Parse the text file and generate a graph."""
        if not self.text_file_path:
            self.status_label.setText("Status: Please select a text file first")
            return

        self.dates = self.parse_text_file(self.text_file_path)
        if not self.dates:
            self.status_label.setText("Status: No valid dates found in the text file")
            return

        self.plot_dates(self.dates)

    def parse_text_file(self, file_path):
        """Parse the text file and extract email dates."""
        dates = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                raw_email = ""
                for line in file:
                    if line.strip() == "":
                        # Empty line indicates end of an email
                        if raw_email:
                            try:
                                msg = email.message_from_string(raw_email)
                                if 'Date' in msg:
                                    date = msg['Date']
                                    parsed_date = parsedate_to_datetime(date)
                                    dates.append(parsed_date)
                            except email.errors.MessageError as e:
                                print(f"Error parsing email message: {e}")
                            except ValueError as e:
                                print(f"Error converting date: {e}")
                            except Exception as e:
                                print(f"Unexpected error parsing email: {e}")
                            raw_email = ""  # Reset for the next email
                    else:
                        raw_email += line
            return dates
        except FileNotFoundError:
            self.status_label.setText("Error: File not found.")
            return []
        except IOError as e:
            self.status_label.setText(f"Error reading file: {e}")
            return []

    def plot_dates(self, dates):
        """Plot the dates grouped by month over the years and include an average line."""
        from collections import Counter
        import numpy as np
        import matplotlib.pyplot as plt

        # Group dates by year and month
        month_year_counts = Counter((date.year, date.month) for date in dates)

        # Sort the data by year and month
        sorted_data = sorted(month_year_counts.items())

        # Prepare data for plotting
        labels = [f"{year}-{month:02d}" for (year, month), _ in sorted_data]
        counts = [count for _, count in sorted_data]

        # Ensure there is data to plot
        if not counts:
            self.status_label.setText("No data available to plot.")
            return

        # Calculate the average count
        average_count = np.mean(counts)

        # Debugging: Print counts and average
        print("Counts:", counts)
        print("Average Count:", average_count)

        # Plot the data
        plt.figure(figsize=(12, 6))
        plt.bar(labels, counts, color='green', edgecolor='black', label='Monthly Counts')
        plt.axhline(y=average_count, color='red', linestyle='--', label=f'Average ({average_count:.2f})')

        # Force y-axis to include the average
        plt.ylim(0, max(max(counts, default=0), average_count) + 5)

        plt.title("Job Application Emails by Month")
        plt.xlabel("Month-Year")
        plt.ylabel("Email Count")
        plt.xticks(rotation=45, fontsize=8)
        plt.legend()
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ThunderbirdAnalyzer()
    window.show()
    sys.exit(app.exec_())