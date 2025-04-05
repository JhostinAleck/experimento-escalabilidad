from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def store_file(request):
    if request.method == 'POST':
        filename = request.POST.get('filename')
        size = request.POST.get('size')

        if not filename or not size:
            return JsonResponse({"error": "Missing filename or size"}, status=400)

        # Aquí podrías guardar esta info en la base de datos o loguearla
        return JsonResponse({
            "status": "stored",
            "filename": filename,
            "size": size
        })

    return JsonResponse({"error": "Invalid method"}, status=405)
