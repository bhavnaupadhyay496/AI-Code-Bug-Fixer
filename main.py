from fastapi import FastAPI
from pydantic import BaseModel
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(
    api_key=HF_TOKEN
)


class CodeRequest(BaseModel):
    code: str
    language: str = "Python"


@app.get("/")
def home():
    return {
        "message": "AI Code Bug Fixer Backend is running"
    }


@app.post("/fix-code")
def fix_code(request: CodeRequest):

    prompt = f"""
You are an expert {request.language} developer and debugging assistant.

Analyze the user's code carefully.

Tasks:

1. Find syntax errors.
2. Find logical errors.
3. Find runtime-related problems if visible.
4. Provide the COMPLETE corrected code.
5. Explain the important corrections.
6. Identify the error type.
7. Identify the approximate error line.
8. Generate useful test cases.

Return ONLY this format:

ERROR_TYPE:
<syntax / logical / runtime / no error>

ERROR_LINE:
<line number or unknown>

FIXED_CODE:
<complete corrected code>

EXPLANATION:
<simple explanation>

TEST_CASES:
Test 1:
Input: <input>
Expected: <expected output>

Test 2:
Input: <input>
Expected: <expected output>

Test 3:
Input: <input>
Expected: <expected output>

Original code:

{request.code}
"""

    try:

        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-Coder-32B-Instruct",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert coding assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1500
        )

        result = response.choices[0].message.content

        error_type = "Unknown"
        error_line = "Unknown"
        fixed_code = result
        explanation = "AI returned the corrected code."
        test_cases = []

        if "ERROR_TYPE:" in result:
            error_type = (
                result.split("ERROR_TYPE:", 1)[1]
                .split("ERROR_LINE:", 1)[0]
                .strip()
            )

        if "ERROR_LINE:" in result:
            error_line = (
                result.split("ERROR_LINE:", 1)[1]
                .split("FIXED_CODE:", 1)[0]
                .strip()
            )

        if "FIXED_CODE:" in result:
            fixed_code = (
                result.split("FIXED_CODE:", 1)[1]
                .split("EXPLANATION:", 1)[0]
                .strip()
            )

        if "EXPLANATION:" in result:
            explanation = (
                result.split("EXPLANATION:", 1)[1]
                .split("TEST_CASES:", 1)[0]
                .strip()
            )

        if "TEST_CASES:" in result:
            test_cases_text = result.split(
                "TEST_CASES:", 1
            )[1].strip()

            test_cases = [
                line
                for line in test_cases_text.splitlines()
                if line.strip()
            ]

        return {
            "success": True,
            "error_type": error_type,
            "error_line": error_line,
            "fixed_code": fixed_code,
            "explanation": explanation,
            "test_cases": test_cases
        }

    except Exception as e:

        return {
            "success": False,
            "error_type": "AI Error",
            "error_line": "Unknown",
            "fixed_code": "",
            "explanation": str(e),
            "test_cases": []
        }