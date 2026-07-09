import subprocess
import tempfile
import os
import uuid


class CodeExecutor:

    @staticmethod
    def execute(language, code, custom_input=""):

        if language == "python":
            return CodeExecutor.run_python(code, custom_input)

        elif language == "cpp":
            return CodeExecutor.run_cpp(code, custom_input)

        elif language == "java":
            return CodeExecutor.run_java(code, custom_input)

        return {
            "success": False,
            "output": "",
            "error": "Unsupported language."
        }

    @staticmethod
    def run_python(code, custom_input):

        temp_dir = tempfile.mkdtemp()

        file_path = os.path.join(temp_dir, "main.py")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)

        try:

            result = subprocess.run(

                ["python", file_path],

                input=custom_input,

                text=True,

                capture_output=True,

                timeout=5

            )

            return {

                "success": result.returncode == 0,

                "output": result.stdout,

                "error": result.stderr

            }

        except subprocess.TimeoutExpired:

            return {

                "success": False,

                "output": "",

                "error": "Time Limit Exceeded"

            }

    @staticmethod
    def run_cpp(code, custom_input):

        temp_dir = tempfile.mkdtemp()

        cpp_file = os.path.join(temp_dir, "main.cpp")

        exe_file = os.path.join(temp_dir, "main.exe")

        with open(cpp_file, "w", encoding="utf-8") as f:
            f.write(code)

        compile_process = subprocess.run(

            ["g++", cpp_file, "-o", exe_file],

            text=True,

            capture_output=True

        )

        if compile_process.returncode != 0:

            return {

                "success": False,

                "output": "",

                "error": compile_process.stderr

            }

        try:

            result = subprocess.run(

                [exe_file],

                input=custom_input,

                text=True,

                capture_output=True,

                timeout=5

            )

            return {

                "success": result.returncode == 0,

                "output": result.stdout,

                "error": result.stderr

            }

        except subprocess.TimeoutExpired:

            return {

                "success": False,

                "output": "",

                "error": "Time Limit Exceeded"

            }

    @staticmethod
    def run_java(code, custom_input):

        temp_dir = tempfile.mkdtemp()

        java_file = os.path.join(temp_dir, "Main.java")

        with open(java_file, "w", encoding="utf-8") as f:
            f.write(code)

        compile_process = subprocess.run(

            ["javac", java_file],

            text=True,

            capture_output=True

        )

        if compile_process.returncode != 0:

            return {

                "success": False,

                "output": "",

                "error": compile_process.stderr

            }

        try:

            result = subprocess.run(

                ["java", "-cp", temp_dir, "Main"],

                input=custom_input,

                text=True,

                capture_output=True,

                timeout=5

            )

            return {

                "success": result.returncode == 0,

                "output": result.stdout,

                "error": result.stderr

            }

        except subprocess.TimeoutExpired:

            return {

                "success": False,

                "output": "",

                "error": "Time Limit Exceeded"

            }