import streamlit as st
import requests
import subprocess
import sys
import tempfile
import os
import shutil


# =========================
# PAGE CONFIGURATION
# =========================

st.set_page_config(
    page_title="AI Code Debugger",
    page_icon="💻",
    layout="wide"
)


# =========================
# TITLE
# =========================

st.title("💻 AI Code Bug Fixer & Explainer")
st.write("Fix code errors instantly and understand them with AI.")


# =========================
# LANGUAGE MAPPING
# =========================

syntax_map = {
    "Python": "python",
    "Java": "java",
    "JavaScript": "javascript",
    "C++": "cpp",
    "C": "c",
    "C#": "csharp",
    "PHP": "php",
    "Go": "go",
    "Kotlin": "kotlin",
    "TypeScript": "typescript",
    "SQL": "sql"
}


extension_map = {
    "Python": "py",
    "Java": "java",
    "JavaScript": "js",
    "C++": "cpp",
    "C": "c",
    "C#": "cs",
    "PHP": "php",
    "Go": "go",
    "Kotlin": "kt",
    "TypeScript": "ts",
    "SQL": "sql"
}


# =========================
# TWO COLUMNS
# =========================

col1, col2 = st.columns(2)


# =========================
# LEFT SIDE
# =========================

with col1:

    st.subheader("📥 Enter Your Code")

    language = st.selectbox(
        "Select Language:",
        [
            "Python",
            "Java",
            "JavaScript",
            "C++",
            "C",
            "C#",
            "PHP",
            "Go",
            "Kotlin",
            "TypeScript",
            "SQL"
        ]
    )

    broken_code = st.text_area(
        "Paste your incorrect code here:",
        height=300,
        placeholder='Example:\nif x > 5\n    print("Hello")'
    )

    submit_button = st.button(
        "Fix My Code 🚀",
        use_container_width=True
    )


# =========================
# RIGHT SIDE
# =========================

with col2:

    st.subheader("📤 AI Result")

    if submit_button:

        if not broken_code.strip():

            st.warning("Please enter some code first!")

        else:

            with st.spinner(
                "AI is analyzing and fixing your code..."
            ):

                try:

                    # =========================
                    # BACKEND URL
                    # =========================

                    backend_url = (
                        "http://127.0.0.1:8000/fix-code"
                    )


                    # =========================
                    # REQUEST DATA
                    # =========================

                    data = {
                        "code": broken_code,
                        "language": language
                    }


                    # =========================
                    # SEND REQUEST TO FASTAPI
                    # =========================

                    response = requests.post(
                        backend_url,
                        json=data,
                        timeout=60
                    )


                    # =========================
                    # RESPONSE CHECK
                    # =========================

                    if response.status_code == 200:

                        result = response.json()


                        if result.get("success"):

                            st.success(
                                "Code fixed successfully!"
                            )


                            # =========================
                            # ERROR ANALYSIS
                            # =========================

                            error_type = result.get(
                                "error_type",
                                "Unknown"
                            )

                            error_line = result.get(
                                "error_line",
                                "Unknown"
                            )

                            error_reason = result.get(
                                "error_reason",
                                "No error reason provided."
                            )


                            st.subheader(
                                "🔴 Error Analysis"
                            )

                            st.write(
                                f"**Error Type:** {error_type}"
                            )

                            st.write(
                                f"**Error Line:** {error_line}"
                            )

                            st.write(
                                f"**Error Reason:** {error_reason}"
                            )


                            # =========================
                            # CORRECT CODE
                            # =========================

                            st.subheader(
                                "✅ Correct Code"
                            )

                            fixed_code = result.get(
                                "fixed_code",
                                ""
                            )


                            # Remove markdown code fences
                            if fixed_code.startswith("```"):

                                lines = fixed_code.splitlines()

                                if (
                                    lines
                                    and lines[0].startswith("```")
                                ):
                                    lines = lines[1:]

                                if (
                                    lines
                                    and lines[-1].strip() == "```"
                                ):
                                    lines = lines[:-1]

                                fixed_code = "\n".join(
                                    lines
                                ).strip()


                            code_language = syntax_map.get(
                                language,
                                "text"
                            )


                            st.code(
                                fixed_code,
                                language=code_language
                            )


                            # =========================
                            # DOWNLOAD FIXED CODE
                            # =========================

                            extension = extension_map.get(
                                language,
                                "txt"
                            )


                            st.download_button(
                                "⬇️ Download Fixed Code",
                                fixed_code,
                                file_name=(
                                    f"fixed_code.{extension}"
                                ),
                                use_container_width=True
                            )


                            # =========================
                            # AI EXPLANATION
                            # =========================

                            explanation = result.get(
                                "explanation",
                                "No explanation provided."
                            )


                            st.subheader(
                                "💡 AI Explanation"
                            )

                            st.write(
                                explanation
                            )


                            # =========================
                            # SUGGESTIONS
                            # =========================

                            suggestions = result.get(
                                "suggestions",
                                "No suggestions provided."
                            )


                            st.subheader(
                                "🚀 Suggestions"
                            )

                            st.write(
                                suggestions
                            )


                            # ==================================================
                            # OUTPUT / CODE EXECUTION
                            # ==================================================

                            st.subheader(
                                "▶️ Output"
                            )


                            try:

                                # =========================
                                # PYTHON
                                # =========================

                                if language == "Python":

                                    with tempfile.NamedTemporaryFile(
                                        mode="w",
                                        suffix=".py",
                                        delete=False,
                                        encoding="utf-8"
                                    ) as temp_file:

                                        temp_file.write(
                                            fixed_code
                                        )

                                        file_path = (
                                            temp_file.name
                                        )


                                    execution = subprocess.run(
                                        [
                                            sys.executable,
                                            file_path
                                        ],
                                        capture_output=True,
                                        text=True,
                                        timeout=10
                                    )


                                    if execution.returncode == 0:

                                        st.success(
                                            "Execution Successful!"
                                        )

                                        if execution.stdout.strip():

                                            st.code(
                                                execution.stdout
                                            )

                                        else:

                                            st.info(
                                                "Program produced no output."
                                            )

                                    else:

                                        st.error(
                                            "Runtime Error"
                                        )

                                        st.code(
                                            execution.stderr
                                        )


                                    # Delete temporary file

                                    try:
                                        os.remove(file_path)
                                    except:
                                        pass


                                # =========================
                                # JAVASCRIPT
                                # =========================

                                elif language == "JavaScript":

                                    if not shutil.which("node"):

                                        st.error(
                                            "Node.js is not installed "
                                            "or not available in PATH."
                                        )

                                    else:

                                        with tempfile.NamedTemporaryFile(
                                            mode="w",
                                            suffix=".js",
                                            delete=False,
                                            encoding="utf-8"
                                        ) as temp_file:

                                            temp_file.write(
                                                fixed_code
                                            )

                                            file_path = (
                                                temp_file.name
                                            )


                                        execution = subprocess.run(
                                            [
                                                "node",
                                                file_path
                                            ],
                                            capture_output=True,
                                            text=True,
                                            timeout=10
                                        )


                                        if execution.returncode == 0:

                                            st.success(
                                                "Execution Successful!"
                                            )

                                            st.code(
                                                execution.stdout
                                                or
                                                "Program produced no output."
                                            )

                                        else:

                                            st.error(
                                                "Runtime Error"
                                            )

                                            st.code(
                                                execution.stderr
                                            )


                                # =========================
                                # JAVA
                                # =========================

                                elif language == "Java":

                                    if not shutil.which("javac"):

                                        st.error(
                                            "Java JDK is not installed "
                                            "or javac is not in PATH."
                                        )

                                    else:

                                        with tempfile.TemporaryDirectory() as temp_dir:

                                            java_file = os.path.join(
                                                temp_dir,
                                                "Main.java"
                                            )


                                            with open(
                                                java_file,
                                                "w",
                                                encoding="utf-8"
                                            ) as file:

                                                file.write(
                                                    fixed_code
                                                )


                                            compile_result = subprocess.run(
                                                [
                                                    "javac",
                                                    java_file
                                                ],
                                                capture_output=True,
                                                text=True,
                                                timeout=20
                                            )


                                            if (
                                                compile_result.returncode
                                                != 0
                                            ):

                                                st.error(
                                                    "Compilation Error"
                                                )

                                                st.code(
                                                    compile_result.stderr
                                                )

                                            else:

                                                run_result = subprocess.run(
                                                    [
                                                        "java",
                                                        "-cp",
                                                        temp_dir,
                                                        "Main"
                                                    ],
                                                    capture_output=True,
                                                    text=True,
                                                    timeout=10
                                                )


                                                if (
                                                    run_result.returncode
                                                    == 0
                                                ):

                                                    st.success(
                                                        "Execution Successful!"
                                                    )

                                                    st.code(
                                                        run_result.stdout
                                                        or
                                                        "Program produced no output."
                                                    )

                                                else:

                                                    st.error(
                                                        "Runtime Error"
                                                    )

                                                    st.code(
                                                        run_result.stderr
                                                    )


                                # =========================
                                # C
                                # =========================

                                elif language == "C":

                                    if not shutil.which("gcc"):

                                        st.error(
                                            "GCC is not installed "
                                            "or not available in PATH."
                                        )

                                    else:

                                        with tempfile.TemporaryDirectory() as temp_dir:

                                            source_file = os.path.join(
                                                temp_dir,
                                                "main.c"
                                            )

                                            output_file = os.path.join(
                                                temp_dir,
                                                "program.exe"
                                            )


                                            with open(
                                                source_file,
                                                "w",
                                                encoding="utf-8"
                                            ) as file:

                                                file.write(
                                                    fixed_code
                                                )


                                            compile_result = subprocess.run(
                                                [
                                                    "gcc",
                                                    source_file,
                                                    "-o",
                                                    output_file
                                                ],
                                                capture_output=True,
                                                text=True,
                                                timeout=20
                                            )


                                            if (
                                                compile_result.returncode
                                                != 0
                                            ):

                                                st.error(
                                                    "Compilation Error"
                                                )

                                                st.code(
                                                    compile_result.stderr
                                                )

                                            else:

                                                run_result = subprocess.run(
                                                    [
                                                        output_file
                                                    ],
                                                    capture_output=True,
                                                    text=True,
                                                    timeout=10
                                                )


                                                if (
                                                    run_result.returncode
                                                    == 0
                                                ):

                                                    st.success(
                                                        "Execution Successful!"
                                                    )

                                                    st.code(
                                                        run_result.stdout
                                                        or
                                                        "Program produced no output."
                                                    )

                                                else:

                                                    st.error(
                                                        "Runtime Error"
                                                    )

                                                    st.code(
                                                        run_result.stderr
                                                    )


                                # =========================
                                # C++
                                # =========================

                                elif language == "C++":

                                    if not shutil.which("g++"):

                                        st.error(
                                            "G++ is not installed "
                                            "or not available in PATH."
                                        )

                                    else:

                                        with tempfile.TemporaryDirectory() as temp_dir:

                                            source_file = os.path.join(
                                                temp_dir,
                                                "main.cpp"
                                            )

                                            output_file = os.path.join(
                                                temp_dir,
                                                "program.exe"
                                            )


                                            with open(
                                                source_file,
                                                "w",
                                                encoding="utf-8"
                                            ) as file:

                                                file.write(
                                                    fixed_code
                                                )


                                            compile_result = subprocess.run(
                                                [
                                                    "g++",
                                                    source_file,
                                                    "-o",
                                                    output_file
                                                ],
                                                capture_output=True,
                                                text=True,
                                                timeout=20
                                            )


                                            if (
                                                compile_result.returncode
                                                != 0
                                            ):

                                                st.error(
                                                    "Compilation Error"
                                                )

                                                st.code(
                                                    compile_result.stderr
                                                )

                                            else:

                                                run_result = subprocess.run(
                                                    [
                                                        output_file
                                                    ],
                                                    capture_output=True,
                                                    text=True,
                                                    timeout=10
                                                )


                                                if (
                                                    run_result.returncode
                                                    == 0
                                                ):

                                                    st.success(
                                                        "Execution Successful!"
                                                    )

                                                    st.code(
                                                        run_result.stdout
                                                        or
                                                        "Program produced no output."
                                                    )

                                                else:

                                                    st.error(
                                                        "Runtime Error"
                                                    )

                                                    st.code(
                                                        run_result.stderr
                                                    )


                                # =========================
                                # PHP
                                # =========================

                                elif language == "PHP":

                                    if not shutil.which("php"):

                                        st.error(
                                            "PHP is not installed "
                                            "or not available in PATH."
                                        )

                                    else:

                                        with tempfile.NamedTemporaryFile(
                                            mode="w",
                                            suffix=".php",
                                            delete=False,
                                            encoding="utf-8"
                                        ) as temp_file:

                                            temp_file.write(
                                                fixed_code
                                            )

                                            file_path = (
                                                temp_file.name
                                            )


                                        execution = subprocess.run(
                                            [
                                                "php",
                                                file_path
                                            ],
                                            capture_output=True,
                                            text=True,
                                            timeout=10
                                        )


                                        if execution.returncode == 0:

                                            st.success(
                                                "Execution Successful!"
                                            )

                                            st.code(
                                                execution.stdout
                                                or
                                                "Program produced no output."
                                            )

                                        else:

                                            st.error(
                                                "Runtime Error"
                                            )

                                            st.code(
                                                execution.stderr
                                            )


                                # =========================
                                # GO
                                # =========================

                                elif language == "Go":

                                    if not shutil.which("go"):

                                        st.error(
                                            "Go is not installed "
                                            "or not available in PATH."
                                        )

                                    else:

                                        with tempfile.TemporaryDirectory() as temp_dir:

                                            source_file = os.path.join(
                                                temp_dir,
                                                "main.go"
                                            )


                                            with open(
                                                source_file,
                                                "w",
                                                encoding="utf-8"
                                            ) as file:

                                                file.write(
                                                    fixed_code
                                                )


                                            execution = subprocess.run(
                                                [
                                                    "go",
                                                    "run",
                                                    source_file
                                                ],
                                                capture_output=True,
                                                text=True,
                                                timeout=20
                                            )


                                            if (
                                                execution.returncode
                                                == 0
                                            ):

                                                st.success(
                                                    "Execution Successful!"
                                                )

                                                st.code(
                                                    execution.stdout
                                                    or
                                                    "Program produced no output."
                                                )

                                            else:

                                                st.error(
                                                    "Runtime Error"
                                                )

                                                st.code(
                                                    execution.stderr
                                                )


                                # =========================
                                # OTHER LANGUAGES
                                # =========================

                                else:

                                    st.info(
                                        f"{language} code fixed successfully. "
                                        "Live execution is not configured "
                                        "for this language yet."
                                    )


                            except subprocess.TimeoutExpired:

                                st.error(
                                    "Execution timed out. "
                                    "Please check your code."
                                )


                            except Exception as execution_error:

                                st.error(
                                    f"Execution Error: "
                                    f"{execution_error}"
                                )


                        else:

                            st.error(
                                result.get(
                                    "message",
                                    "Unable to fix the code."
                                )
                            )


                    else:

                        st.error(
                            "Backend Error: "
                            f"{response.status_code}"
                        )


                # =========================
                # CONNECTION ERROR
                # =========================

                except requests.exceptions.ConnectionError:

                    st.error(
                        "Could not connect to backend. "
                        "Please make sure FastAPI server "
                        "is running."
                    )


                # =========================
                # TIMEOUT ERROR
                # =========================

                except requests.exceptions.Timeout:

                    st.error(
                        "Request timed out. "
                        "Please try again."
                    )


                # =========================
                # OTHER ERROR
                # =========================

                except Exception as app_error:

                    st.error(
                        f"Something went wrong: {app_error}"
                    )