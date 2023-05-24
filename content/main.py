import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from output_builder import build_output
from url_getter import get_url

url = 'https://www.theguardian.com/world/2023/may/18/italy-worst-flooding-in-100-years-emilia-romagna'
# prompt user for url?

class WatchForChanges(FileSystemEventHandler):
    def on_changes(self, event):
        if os.path.dirname(event.src_path) == os.path.dirname(os.path.absname(__file__)):
            print("Something has changed!")

def main():
    event_handler = WatchForChanges()
    observer = Observer()
    directory = os.path.dirname(os.path.abspath(__file__))
    observer.schedule(event_handler, directory, recursive = True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()

if __name__ == "__main__":
    # url_article = get_url()
    build_output()
    main()
