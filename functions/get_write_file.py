import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        

        # Comprobación de que el directorio padre existe para la creación.
        # de archivos
        os.makedirs(os.path.dirname(target_dir), exist_ok=True)
        

        # Apertura del archivo con with open y "w".
        with open(target_dir, "w") as f:
            f.write(content)
            
        
        # Retornar mensaje de éxito para el mismo agente.
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


    except Exception as e:
        return f"Error: {e}"


schema_get_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write the file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory"
                ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file"
                ),
        },
    ),
)
