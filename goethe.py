"""
Solve for "User limit of inotify watches reached" error
cat /proc/sys/fs/inotify/max_user_watches
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p
OR
fs.inotify.max_user_watches=100000
"""
import time
import datetime
from datetime import date
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from shutil import copyfile

def createFolder() -> Path:
    today = date.today()
    dir = Path("/home/ehab/Desktop")/f"{today}"
    dir.mkdir(exist_ok=True)
    return dir

def moveFile():
    #copyfile(event.on_any_event(), "/home/ehab/Desktop")
    pass

def run():
    DIRECTORY_TO_WATCH = "/home/ehab/Downloads"
    observer = Observer()
    event_handler = Handler()
    observer.schedule(event_handler, DIRECTORY_TO_WATCH, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(5)
    except:
        observer.stop()
        print ("error!")
    observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            current_time = datetime.datetime.now()  
            print ("Received created event -- {} -- {}." .format(current_time, event.src_path))
            src = str(event.src_path)
            return src

def test():
    h=Handler()
    return None 



if __name__ == '__main__':
    createFolder()
    run()
    test()