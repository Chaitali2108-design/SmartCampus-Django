from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .executor import CodeExecutor
from dashboard.models import CodingQuestion


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


from dashboard.models import CodingQuestion
import json


@csrf_exempt
def submit_code_api(request):

    if request.method != "POST":
        return JsonResponse(
            {"success": False, "error": "POST request required."},
            status=405
        )

    try:

        data = json.loads(request.body)

        question_id = data.get("question_id")
        language = data.get("language")
        code = data.get("code")

        question = CodingQuestion.objects.get(id=question_id)

        result = CodeExecutor.execute(
            language=language,
            code=code,
            custom_input=question.official_input
        )

        if not result["success"]:
            return JsonResponse({
                "success": False,
                "verdict": "Runtime Error",
                "expected": question.expected_output,
                "received": result["error"]
            })

        expected = question.expected_output.strip()
        received = result["output"].strip()

        if expected == received:

            return JsonResponse({

                "success": True,

                "verdict": "Accepted",

                "marks": question.marks,

                "total_marks": question.marks

            })

        return JsonResponse({

            "success": False,

            "verdict": "Wrong Answer",

            "expected": expected,

            "received": received

        })

    except CodingQuestion.DoesNotExist:

        return JsonResponse({

            "success": False,

            "verdict": "Question Not Found"

        })

    except Exception as e:

        return JsonResponse({

            "success": False,

            "verdict": "Server Error",

            "received": str(e)

        })