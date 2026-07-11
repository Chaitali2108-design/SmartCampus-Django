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


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dashboard.models import CodingQuestion
from openai import OpenAI
from django.conf import settings
import json

client = OpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


@csrf_exempt
def submit_code_api(request):

    if request.method != "POST":
        return JsonResponse(
            {"success": False, "error": "POST request required."},
            status=405,
        )

    try:

        data = json.loads(request.body)

        question = CodingQuestion.objects.get(
            id=data["question_id"]
        )

        language = data["language"]
        code = data["code"]

        prompt = f"""
You are an online coding judge.

Evaluate the submitted solution.

Problem Title:
{question.title}

Problem Statement:
{question.statement}

Input Format:
{question.input_format}

Output Format:
{question.output_format}

Constraints:
{question.constraints}

Expected Output:
{question.expected_output}

Programming Language:
{language}

Candidate Code:
{code}

Rules:
1. Analyze the algorithm carefully.
2. Decide whether the solution correctly solves the problem.
3. Check if the algorithm satisfies the constraints.
4. Estimate time complexity.
5. Give marks out of {question.marks}.
6. Return ONLY valid JSON.

JSON Format:

{{
    "accepted": true,
    "marks": 50,
    "feedback": "Correct solution using HashMap.",
    "complexity": "O(n)"
}}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        result = json.loads(
            response.choices[0].message.content
        )

        return JsonResponse(
            {
                "success": result["accepted"],
                "verdict": "Accepted" if result["accepted"] else "Wrong Answer",
                "marks": result["marks"],
                "total_marks": question.marks,
                "feedback": result["feedback"],
                "complexity": result["complexity"],
            }
        )

    except Exception as e:

        return JsonResponse(
            {
                "success": False,
                "verdict": "Server Error",
                "feedback": str(e),
            }
        )