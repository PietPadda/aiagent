# get_file_content.py

import os

def get_file_content(working_directory, file_path):
    # construct the file path
    target_path = os.path.join(working_directory, file_path)

    # get absolute paths
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(target_path)
    
    # check if file in working dir
    if not abs_file_path.startswith(abs_working_directory):
        # file not in working dir str to LLM
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    # check if file is a file
    if not os.path.isfile(target_path): # "" also evaluates to False
        # not a file str to LLM
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    # set char read limit
    MAX_CHARS = 10000
    
    # read the file contents using try-except block
    try:
        # open and close (via with) in read mode the file
        with open(target_path, "r") as file:
            content = file.read(MAX_CHARS+1)  # read the contents

        # modify content if over max chars
        if len(content) > MAX_CHARS:
            # truncate to max_chars and append with msg
            content = content[:MAX_CHARS] + f'[...File "{file_path}" truncated at 10000 characters]'

    # os operation had an error
    except Exception as e:
        return f"Error: {e}"
    
    return content

