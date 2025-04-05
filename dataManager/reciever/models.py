from django.http import JsonResponse
import requests
import os
import time
STORAGE_URL = "http://34.41.151.57:8000/store/"

def receive_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        filename = file.name

        with open(f"/tmp/{filename}", 'wb+') as dest:
            print(f"Received file: {filename}")
            # time

        data = {
            "filename": filename,
            "result": "success",
            "time": time.time(),
        }
        # Simulación de envío a almacenamiento
        with open(f"/tmp/{filename}", 'rb') as f:
            response = requests.post(STORAGE_URL, data=data)

        return JsonResponse({
            "received": filename,
            "sent_to_storage": response.status_code,
        })

    return JsonResponse({"error": "No file sent"}, status=400)
