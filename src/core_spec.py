import time
import threading
from agent.ProcessCollector import ProcessCollector
import psutil


class ProcessWatcher(threading.Thread):
    def __init__(self, interval: float = 5.0):
        super().__init__(daemon=True)
        self.interval = interval
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            for proc in psutil.process_iter(['name']):
                try:
                    if proc.info['name'] == 'systemd':
                        print(f"⚡ SYSTEMD gefunden (PID: {proc.pid})")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            time.sleep(self.interval)

    def stop(self):
        self.running = False


if __name__ == "__main__":
    print("Start Spec Agent service")

    collector = ProcessCollector()
    processes = collector.list_processes()

    print(f"Gefundene Prozesse: {len(processes)}")
    for proc in processes[:5]:
        print(proc)

    watcher = ProcessWatcher(interval=30.0)
    watcher.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        watcher.stop()
        print("SpecAgent beendet.")
