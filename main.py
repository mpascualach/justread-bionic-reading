import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from output_builder import build_output

url = 'https://www.theguardian.com/world/2023/may/18/italy-worst-flooding-in-100-years-emilia-romagna'
# prompt user for url?

def main():
    build_output(url)

if __name__ == "__main__":
    main()
