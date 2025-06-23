# write_file.py

import os

def write_file(working_directory, file_path, content):
    # construct the file path
    target_path = os.path.join(working_directory, file_path)

    # get absolute paths
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(target_path)

    # write the file contents using try-except block
    try:
        # check if file in working dir
        if not abs_file_path.startswith(abs_working_directory):
            # file not in working dir str to LLM
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # check if file doesn't exist
        if not os.path.exists(target_path):
            # create folders for file_path (else can't write to it)
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        # write to file (even if it doesn't exist yet - will create one)
        with open(target_path, 'w') as file: # open and close when done
            file.write(content) # write content to the files

    # os operation had an error
    except Exception as e:
        return f"Error: {e}"

    # return success msg to LLM
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
