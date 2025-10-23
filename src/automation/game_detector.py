import psutil
import time
import threading

class GameDetector:
    def is_game_running(self):
        for proc in psutil.process_iter(['name']):
            if 'League of Legends.exe' in proc.info.get('name', ''):
                return True
        return False
    
    def start_monitoring(self, callback):
        def monitor():
            while True:
                if self.is_game_running():
                    callback()
                time.sleep(5)
        threading.Thread(target=monitor, daemon=True).start()
