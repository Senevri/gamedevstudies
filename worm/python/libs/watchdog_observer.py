# watchdog_observer.py

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from queue import Queue
import threading

import os

# Get the current script file path
current_script_path = os.path.abspath(__file__)

# Get the parent directory
parent_directory = os.path.dirname(current_script_path)


class MyHandler(FileSystemEventHandler):
    def __init__(self, change_queue: Queue):
        super().__init__()
        self.change_queue = change_queue
        self.delay = 1

    def set_delay(self, seconds):
        self.delay = seconds

    def on_modified(self, event):
        if event.is_directory:
            return
        file_path = event.src_path
        self.change_queue.put(file_path)


class FileMonitor:
    def __init__(self):
        self.observer = Observer()
        self.change_queue = Queue()

    def monitor_directory(self, path, change_queue, sleep_interval=1):
        event_handler = MyHandler(change_queue)
        event_handler.set_delay(sleep_interval)
        self.observer.schedule(event_handler, path, recursive=True)
        self.observer.start()

        try:
            while True:
                time.sleep(1)  # Adjust the sleep interval as needed
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

    def start(self, directory=parent_directory):
        monitored_path = f"{directory}"

        # Create a queue for inter-thread communication

        # Run the monitoring in a separate thread
        self.monitoring_thread = threading.Thread(
            target=self.monitor_directory, args=(monitored_path, self.change_queue, 1)
        )
        self.monitoring_thread.start()

        self.files_changed = set()

    def get_changed_files(self):
        # Check the queue for changes
        while not self.change_queue.empty():
            changed_file = self.change_queue.get()
            self.files_changed.add(changed_file)
        # Your main process logic goes here
        if self.files_changed:  # Maybe no need for 'if', if it's cheked on use.
            yield (self.files_changed)
            self.files_changed = set()
            # Stop the monitoring thread when the main process is terminated

    def stop(self):
        self.monitoring_thread.join()


# Watchdog observer test

if __name__ == "__main__":
    filemon = None
    try:
        filemon = FileMonitor()
        filemon.start()
        while True:
            changed_files = list(filemon.get_changed_files())
            if changed_files:
                print(changed_files)
                # Reload
            time.sleep(1)
    except KeyboardInterrupt:
        if filemon:
            filemon.stop()
