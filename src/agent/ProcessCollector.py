import time
import psutil
from typing import List, Dict

class ProcessCollector:
    def __init__(self):
        pass

    def list_processes(self) -> List[Dict]:
        proc_list = []
        for p in psutil.process_iter(['pid','name','username','cpu_percent','memory_info']):
            try:
                info = p.info
                proc_list.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return proc_list

class SpecAgentService:
    def __init__(self, interval: float = 5.0):
        self.interval = interval
        self.collector = ProcessCollector()
        self.running = False

    def run_once(self):
        procs = self.collector.list_processes()
        # einfache Ausgabe / später: normalisieren, DB, ML-Pipeline
        print(f"Gefundene Prozesse: {len(procs)}")
        for p in procs[:10]:
            print(p)

    def run(self):
        self.running = True
        while self.running:
            try:
                self.run_once()
                time.sleep(self.interval)
            except KeyboardInterrupt:
                self.running = False
            except Exception as e:
                # Fehler robust behandeln, Logging statt Absturz
                print("Fehler im Lauf: ", e)