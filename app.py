import os
import time
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from flask import Flask, jsonify, render_template

# Configuration
REPORT_DIR = './reports'
ARCHIVE_DIR = './archive'
UPDATE_INTERVAL = 60  # in seconds

app = Flask(__name__)
current_data = []
last_file_path = None

class ReportHandler(FileSystemEventHandler):
    def process(self, file_path):
        global current_data, last_file_path
        try:
            # Check if last file exists and archive it
            if last_file_path and os.path.exists(last_file_path):
                os.rename(last_file_path, os.path.join(ARCHIVE_DIR, os.path.basename(last_file_path)))

            # Read the new file
            df = pd.read_csv(file_path)
            current_data = df[df['status'] == 'IN'].to_dict(orient='records')
            last_file_path = file_path  # Update last file path
            print("Updated current_data:", current_data)  # Debugging line
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    def on_created(self, event):
        if event.is_directory:
            return
        # Ensure the file is fully written before processing
        time.sleep(5)  # Adjust the sleep duration as necessary
        self.process(event.src_path)

def start_observer():
    event_handler = ReportHandler()
    observer = Observer()
    observer.schedule(event_handler, REPORT_DIR, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    global current_data
    print("Serving current_data:", current_data)  # Debugging line
    return jsonify(current_data)

if __name__ == "__main__":
    from threading import Thread
    observer_thread = Thread(target=start_observer)
    observer_thread.daemon = True
    observer_thread.start()
    app.run(host='0.0.0.0', port=5000, debug=True)

