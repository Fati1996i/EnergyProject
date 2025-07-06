from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import subprocess
import time

# ---------------------- PERF TOOL ----------------------
class PerfInput(BaseModel):
    command: str = Field(..., description="Full command to run with perf")

class PerfTool(BaseTool):
    name: str = "Perf Tool"
    description: str = "Runs a command using perf to profile energy usage"
    args_schema: Type[BaseModel] = PerfInput

    def _run(self, command: str) -> str:
        try:
            result = subprocess.run(
                ["perf", "stat", "-e", "power/energy-pkg/"] + command.split(),
                capture_output=True,
                text=True,
                timeout=20
            )
            with open("perf_output.txt", "w") as f:
                f.write(result.stderr if result.stderr else "No perf output.")
            return result.stderr if result.stderr else "No perf output."
        except Exception as e:
            return f"Perf error: {e}"


# ---------------------- VALIDATION TOOL ----------------------
class ValidateInput(BaseModel):
    command: str = Field(..., description="Command to run the optimized code and validate functionality")

class SmartValidatorTool(BaseTool):
    name: str = "Smart Validator and Debugger"
    description: str = "Runs and debugs the optimized code until it runs correctly using LLM"
    args_schema: Type[BaseModel] = ValidateInput

    def _run(self, command: str) -> str:
        attempt = 0
        max_attempts = 5

        while attempt < max_attempts:
            attempt += 1
            try:
                result = subprocess.run(command.split(), capture_output=True, text=True, timeout=20)

                if result.returncode == 0:
                    return f"✅ Success on attempt {attempt}:\n{result.stdout}"
                else:
                    error_msg = result.stderr.strip()
                    print(f"[Attempt {attempt}] ❌ Error: {error_msg}")

                    fix = self.fix_code_with_llm(error_msg)
                    if fix:
                        with open("optimized_code.py", "w") as f:
                            f.write(fix)
                        time.sleep(1)
                        continue
                    else:
                        return f"❌ Could not fix the issue:\n{error_msg}"
            except Exception as e:
                return f"❌ Exception during execution: {e}"

        return f"❌ Failed after {max_attempts} attempts."

    def fix_code_with_llm(self, error_msg: str) -> str:
        try:
            with open("optimized_code.py", "r") as f:
                current_code = f.read()

            prompt = f"""
You are an expert Python debugger.
You are given the following code and error message.

--- CODE START ---
{current_code}
--- CODE END ---

--- ERROR MESSAGE ---
{error_msg}
--- ERROR END ---

Fix the code so that it runs correctly. Only return the **corrected full code**.
"""

            response = self.llm.invoke(prompt)
            return response.strip()

        except Exception as e:
            return None
        
class FileWriteInput(BaseModel):
    filename: str = Field(..., description="Name of the file to write")
    content: str = Field(..., description="Content to be written to the file")

class FileWriterTool(BaseTool):
    name: str = "File Writer Tool"
    description: str = "Writes content to a specified file"
    args_schema: Type[BaseModel] = FileWriteInput

    def _run(self, filename: str, content: str) -> str:
        try:
            with open(filename, "w") as f:
                f.write(content)
            return f"Content saved to {filename}"
        except Exception as e:
            return f"Failed to save content: {e}"
