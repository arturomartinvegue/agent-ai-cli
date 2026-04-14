import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs


        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'


        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        
        command = ["python", target_dir] 
        if args:
            command.extend(args)
        

        subprocess_complete = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)

        
        # Building a output string.
        output = ""

        if subprocess_complete.returncode != 0:
            output = f"Process exited with code {subprocess_complete.returncode}"
        if not subprocess_complete.stdout and not subprocess_complete.stderr:
            output = f"No output produced"
        else:
            if subprocess_complete.stdout:
                output += f"STDOUT: {subprocess_complete.stdout}"
            if subprocess_complete.stderr:
                output += f"STDERR: {subprocess_complete.stderr}"
    
        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the script of Python or .py in the working directory or relative to path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of arguments to pass to the Python file"
                ),
        },
    ),
)
