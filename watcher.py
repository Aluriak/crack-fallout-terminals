"""Watcher, looking for PNG files in the home directory.

"""


import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class PNGhandler(FileSystemEventHandler):
    """Just intercept creation of png files, and call run_on with it"""
    def __init__(self, callback:callable):
        self.callback = callback

    def on_created(self, event):
        fname = event.src_path
        if os.path.splitext(fname)[1] == '.png':
            self.callback(fname)


def run_watchdog(callback:callable):
    """Blocking. Will call given callable when a new png file is detected"""
    target_dir = os.path.expanduser('~')
    observer = Observer()
    observer.schedule(PNGhandler(callback), target_dir)
    observer.start()
    print(f'Listening to PNG files in {target_dir}…')
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print(f'Finished!')


if __name__ == '__main__':
    run_watchdog(print)
