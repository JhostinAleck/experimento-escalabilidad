from django.http import JsonResponse
import os

def store_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        path = f"/tmp/almacenado_{file.name}"

        with open(path, 'wb+') as dest:
            for chunk in file.chunks():
                dest.write(chunk)

        return JsonResponse({"status": "stored", "file": file.name})

    return JsonResponse({"error": "No file received"}, status=400)
