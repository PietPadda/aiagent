# run_python_file.py

import os
import subprocess

def run_python_file(working_directory, file_path):
    # construct the file path
    target_path = os.path.join(working_directory, file_path)

    # get absolute paths
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(target_path)

    # check if file in working dir
    if not abs_file_path.startswith(abs_working_directory):
        # file not in working dir str to LLM
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # check if file exists
    if not os.path.exists(target_path): # "" also evaluates to False
        # path doesn't exist str to LLM
        return f'Error: File "{file_path}" not found.'
    
    # check if python file
    _, ext = os.path.splitext(target_path)
    if ext != '.py': # check extension
        # wrong extension str to LLM
        return f'Error: "{file_path}" is not a Python file.'
    
    # execute command in try-except block to catch errors
    try:
        # run the file and return result
        result = subprocess.run(["python3", abs_file_path], # execute the file at path
                                cwd=abs_working_directory, # command working dir
                                capture_output=True, # capture stdout and stderr
                                text=True, # strings not bytes
                                timeout=30 # cmd timeout timer
                                )
        
        output = [] # init empty list for output
        
        # format stdout
        if result.stdout:
            output.append("STDOUT:"+result.stdout)
        
        # format stderr
        if result.stderr:
            output.append("STDERR:"+result.stderr)

        # exit code check
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        # empty output
        if not output:
            return "No output produced." # early return

    # capture any exceptions
    except Exception as e:
        return f"Error: executing Python file: {e}" # early return
    
    # return output
    return "\n".join(output)