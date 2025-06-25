# call_function.py

# import the call functions
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python_file import run_python_file

from google.genai import types # for prompt roles

def call_function(function_call_part, verbose=False):
    # get func vars
    func_name = function_call_part.name # string
    func_args = function_call_part.args # dict of args

    # if verbose flag is specific
    if verbose == True:
        print(f"Calling function: {func_name}({func_args})")
    else:
        print(f" - Calling function: {func_name}")

    # build a map for calling
    func_dict = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    # use map to call function
    func_call = func_dict.get(func_name) # .get safer as returns None if invalid

    # check result is None ie invalid function call
    if func_call is None:
        return types.Content( # comms with agent system
            role="tool", # content from a function
            parts=[ # content chunks
                types.Part.from_function_response( # use as func response
                    name=func_name, # function name attempted
                    response={"error": f"Unknown function: {func_name}"}, # func error
                )
            ],
        )
    
    # valid function call args
    func_args["working_directory"] = "./calculator" # manually set WD

    # call the function and get result using our WD dict of args
    func_result = func_call(**func_args) # call function

    # return the func result as a types.Conent
    return types.Content( # comms with agent system
    role="tool", # content from a function
    parts=[ # content chunks
        types.Part.from_function_response( # use as func response
            name=func_name, # function name attempted
            response={"result": func_result}, # func result string
        )
    ],
)
