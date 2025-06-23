# get_files_info.py

import os

def get_files_info(working_directory, directory=None):
    # construct the directory path
    target_path = os.path.join(working_directory, directory)

    # check if dir is a dir
    if not os.path.isdir(target_path): # "" also evaluates to False
        # not a dir str to LLM
        return f'Error: "{directory}" is not a directory'
    
    # get absolute paths
    abs_working_directory = os.path.abspath(working_directory)
    abs_directory = os.path.abspath(target_path)
    
    # check if dir in working dir
    if not abs_directory.startswith(abs_working_directory):
        # dir not in working dir str to LLM
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    contents = [] # init empty list

    # use try-except block to catch errors
    try:
        # loop all files in dir and print out contents strs
        for filename in os.listdir(target_path):
            file_path = os.path.join(target_path, filename) # get filepath of content
            is_dir = False # init as False
            if os.path.isdir(file_path): # check if a a dir
                is_dir = True # is a dir
            file_size = os.path.getsize(file_path) # get file size
            file_string = f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}"

            contents.append(file_string) # add to contents list
    # os operation had an error
    except Exception as e:
        return f"Error: {e}"
    
    # build content string using the list of file_strings
    contents_string = "\n".join(contents)

    return contents_string


