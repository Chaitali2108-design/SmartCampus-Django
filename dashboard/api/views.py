from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def run_code_api(request):

    if request.method != "POST":
        return JsonResponse(
            {
                "message": "Only POST request allowed"
            },
            status=405
        )


    data = json.loads(request.body)

    return JsonResponse({

        "status": "received",

        "language": data.get("language"),

        "code": data.get("code"),

        "input": data.get("input", ""),

        "message": "Run Code API working"

    })



@csrf_exempt
def submit_code_api(request):

    if request.method != "POST":
        return JsonResponse(
            {
                "message": "Only POST request allowed"
            },
            status=405
        )


    data = json.loads(request.body)


    return JsonResponse({

        "status": "received",

        "question_id": data.get("question_id"),

        "language": data.get("language"),

        "message": "Submit API working"

    })