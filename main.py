# main.py
import os # env interacting tools
import sys # get access to cli
from dotenv import load_dotenv # tool to read .env files
from google import genai # get google generative ai tools
from google.genai import types # for prompt roles

from functions.call_function import call_function # for func calling

# Get env vars
load_dotenv() # read the .env file
api_key = os.environ.get("GEMINI_API_KEY") # get apikey from .env

# Create Google Generative AI client
client = genai.Client(api_key=api_key)

# send gen AI request
model = "gemini-2.0-flash-001"

# check if CLI prompt arg provided
if len(sys.argv) < 2:
    print("Please provide a prompt as an argument.") # log message
    sys.exit(1) # error code 1 to mean CLI failure
user_prompt = sys.argv[1] # use CLI input arg

# our message list
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
] # user role, prompt arg only

# hardcoded system prompt
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request:

1. You must use FUNCTION CALLS to perform any action (listing files, reading, writing, or executing Python files).
2. When planning, reason in steps and make function calls for each action, even if it is just to gather information.
3. Only provide an answer, explanation, or summary AFTER all necessary function calls and actions are complete.
4. Once finished with all tool use, output a brief, clear summary to the user.

All filesystem paths should be relative to the working directory. You do NOT need to specify the working directory argument—it will be set for you automatically.
"""

# get_files_info schema function declaration
schema_get_files_info = types.FunctionDeclaration( # func blueprint we store in a var
    name="get_files_info", # func name as LLM sees it
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.", # func description LLM sees
    parameters=types.Schema( # defines params the LLM needs
        type=types.Type.OBJECT, # provide func as object (like dict) to LLM
        properties={ # key-value pairs of object parameter
            "directory": types.Schema( # define directory parameter
                type=types.Type.STRING, # store value of "directory" as a string
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.", # tells LLM what type of string is expected
            ),
        },
    ),
)

# get_file_content schema function declaration
schema_get_file_content = types.FunctionDeclaration( # func blueprint we store in a var
    name="get_file_content", # func name as LLM sees it
    description="Reads file contents in the specified file path, constrained to the working directory.", # func description LLM sees
    parameters=types.Schema( # defines params the LLM needs
        type=types.Type.OBJECT, # provide func as object (like dict) to LLM
        properties={ # key-value pairs of object parameter
            "file_path": types.Schema( # define file_path parameter
                type=types.Type.STRING, # store value of "file_path" as a string
                description="The file path to file to read contents from, relative to the working directory", # tells LLM what type of string is expected
            ),
        },
    ),
)

# write_file schema function declaration
schema_write_file = types.FunctionDeclaration( # func blueprint we store in a var
    name="write_file", # func name as LLM sees it
    description="Write or overwrite file content in the specified file path, constrained to the working directory.", # func description LLM sees
    parameters=types.Schema( # defines params the LLM needs
        type=types.Type.OBJECT, # provide func as object (like dict) to LLM
        properties={ # key-value pairs of object parameter
            "file_path": types.Schema( # define file_path parameter
                type=types.Type.STRING, # store value of "file_path" as a string
                description="The file path to file to write content to, relative to the working directory", # tells LLM what type of string is expected
            ),
            "content": types.Schema( # define content parameter
                type=types.Type.STRING, # store value of "content" as a string
                description="The content to write to the file at the file path", # tells LLM what type of string is expected
            ),
        },
    ),
)

# run_python_file schema function declaration
schema_run_python_file = types.FunctionDeclaration( # func blueprint we store in a var
    name="run_python_file", # func name as LLM sees it
    description="Run python file at the specified file path using subprocess.run, constrained to the working directory.", # func description LLM sees
    parameters=types.Schema( # defines params the LLM needs
        type=types.Type.OBJECT, # provide func as object (like dict) to LLM
        properties={ # key-value pairs of object parameter
            "file_path": types.Schema( # define file_path parameter
                type=types.Type.STRING, # store value of "file_path" as a string
                description="The file path to file to run python code using subprocess.run, relative to the working directory", # tells LLM what type of string is expected
            ),
        },
    ),
)

# functions available to LLM
available_functions = types.Tool( # we provide the "tool"s for the LLM
    function_declarations=[ # list of func decls
        schema_get_files_info, # dir contents
        schema_get_file_content, # file content
        schema_write_file, # edit file
        schema_run_python_file, # execute file
    ]
)

# set verbose flag
if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
    verbose_flag = True
else:
    verbose_flag = False

# agent feedback loop
iter_count = 0 # init starting
iter_max = 20 # we limit to 20 loops

while iter_count < iter_max:
    # generate a response from Gemini
    GeminiResp = client.models.generate_content(
        model=model, # version of gemini
        contents=messages, # our messages to AI
        config=types.GenerateContentConfig( # system config
            tools=[available_functions], # funcs as tools for LLM
            system_instruction=system_prompt # hardcoded system prompt on how do do things
            ),
    )

    # loop resp candidates and always append to msg history
    for candidate in GeminiResp.candidates:
        messages.append(candidate.content) # add content to msg list

    # get gemini response most likely candidate response content
    content = GeminiResp.candidates[0].content # use first candidate for action

    # flag for function call handling
    func_call_flag = False # default false each loop

    # loop through each part of the most likely response content
    for part in content.parts:
        if part.function_call:  # check if func call
            func_call_flag = True # set flag to true as it's a function_call!

            # call the function
            call_result = call_function(part.function_call, verbose=verbose_flag) # function called
            messages.append(call_result) # append the result to messages list
            response = call_result.parts[0].function_response.response # get result from function called out of the response!

            # check if func response exists
            if not response:
                raise Exception("Function call response missing required structure!")
            
            # print result if success else the error! if both? print both!
            if "result" in response:
                print(f"-> {response['result']}") # success, result only
            elif "error" in response:
                print(f"-> {response['error']}") # failure, error only
            else:
                print(f"-> {response}") # result and error! just an edge case

    # after the INNER FOR LOOP
    # if no func call, break the loop
    if not func_call_flag:
        for part in content.parts:
            if part.text: # just the plain text response
                print(part.text) # print result only
        break

    # check verbose flag is true
    if verbose_flag: # extract result and error
        # token fields
        GeminiPromptTokens = GeminiResp.usage_metadata.prompt_token_count
        GeminiResponseTokens = GeminiResp.usage_metadata.candidates_token_count

        # do a verbose output with prompt and tokens
        print(f"User prompt: {user_prompt}") # print the user prompt
        print(f"Prompt tokens: {GeminiPromptTokens}") # tokens in the prompt
        print(f"Response tokens: {GeminiResponseTokens}") # tokens in the response

    # end of loop, incr
    iter_count += 1


