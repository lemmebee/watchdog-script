"""
Solve for "User limit of inotify watches reached" error
cat /proc/sys/fs/inotify/max_user_watches
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p
OR
fs.inotify.max_user_watches=100000
"""

import datetime
from datetime import date
import time
import os 
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil


today = date.today()
newFolder = os.path.join("/home/ehab/Desktop/", str(today)) 
os.mkdir(newFolder) 
newFolder =str(newFolder)

class Watcher:
    DIRECTORY_TO_WATCH = "/home/ehab/Pictures"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print ("error!")
        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        global newFolder
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            src = str(event.src_path)
            FileName = src[20:]
            FileName = str(FileName)
            FileName = "/" + FileName
            dst = newFolder + FileName
            current_time = datetime.datetime.now()
            print("**************")
            print ("Received created event -- {} -- {}." .format(current_time, event.src_path))
            print(src)
            print(dst)
            shutil.move(src, dst)


if __name__ == '__main__':
    w=Watcher()
    w.run()
