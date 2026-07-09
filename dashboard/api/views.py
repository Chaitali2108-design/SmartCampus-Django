from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .executor import CodeExecutor


@csrf_exempt
def run_code_api(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST requests are allowed."},
            status=405
        )

    try:
        data = json.loads(request.body)

        language = data.get("language")
        code = data.get("code")
        custom_input = data.get("input", "")

        result = CodeExecutor.execute(
            language=language,
            code=code,
            custom_input=custom_input
        )

        return JsonResponse(result)

    except Exception as e:
        return JsonResponse(
            {
                "success": False,
                "output": "",
                "error": str(e)
            },
            status=500
        )


@csrf_exempt
def submit_code_api(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST requests are allowed."},
            status=405
        )

    data = json.loads(request.body)

    return JsonResponse({
        "success": True,
        "message": "Submit API will be implemented in the next stage."
    })