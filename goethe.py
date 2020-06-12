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

today = date.today()
dst = Path("/home/ehab/Desktop")/f"{today}"
dst.mkdir(exist_ok=True)
dst =str(dst)

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
        global dst
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            current_time = datetime.datetime.now()  
            print ("Received created event -- {} -- {}." .format(current_time, event.src_path))
            src = str(event.src_path)
            dstFileName = src[21:]
            dstFileName = "/" + dstFileName
            dstFileName = str(dstFileName)
            finaldst = dst + dstFileName
            print("**************")
            print(src)
            print(finaldst)
            print("**************")
            copyfile(src, finaldst)


if __name__ == '__main__':
    run()