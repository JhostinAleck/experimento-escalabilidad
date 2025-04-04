from django.http import JsonResponse
import requests
import os

STORAGE_URL = "http://<IP_VM_STORAGE>:8000/store/"

def receive_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        filename = file.name

        with open(f"/tmp/{filename}", 'wb+') as dest:
            for chunk in file.chunks():
                dest.write(chunk)

        data = {
            "filename": filename,
            "size": os.path.getsize(f"/tmp/{filename}")
            # "metadata": metadata, 
        }
        # Simulación de envío a almacenamiento
        with open(f"/tmp/{filename}", 'rb') as f:
            response = requests.post(STORAGE_URL, data=data)

        return JsonResponse({
            "received": filename,
            "sent_to_storage": response.status_code,
        })

    return JsonResponse({"error": "No file sent"}, status=400)
