import psutil
import threading
import time
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from django.conf import settings
logger = logging.getLogger(__name__)

class MetricsCollector(threading.Thread):
    def __init__(self, interval=1):
        super().__init__()
        self.interval = interval
        self.running = True
        self.metrics = []  # ← Aquí guardamos las métricas por segundo

    def run(self):
        while self.running:
            timestamp = time.strftime('%H:%M:%S')
            cpu = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory().percent
            disk = psutil.disk_io_counters().write_bytes  # Bytes escritos en disco

            self.metrics.append({
                "timestamp": timestamp,
                "cpu_percent": cpu,
                "memory_percent": mem,
                "disk_write_bytes": disk
            })

            time.sleep(self.interval)

    def stop(self):
        self.running = False

@csrf_exempt
def receive_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        collector = MetricsCollector(interval=1)
        collector.start()

        file = request.FILES['file']
        filename = file.name
        file_path = f"/tmp/{filename}"

        with open(file_path, 'wb+') as dest:
            print(f"Received file: {filename}")


        processed_data = {
            "filename": filename,
            "result": "success",
            "time": time.time(),
        }
        requests.post(f"{settings.STORAGE_URL}store/", data=processed_data)

        collector.stop()
        collector.join()

        # ¡Incluimos las métricas en la respuesta!
        return JsonResponse({
            "status": "received",
            "file": filename,
            "metrics": collector.metrics
        })

    return JsonResponse({"error": "No file provided"}, status=400)
