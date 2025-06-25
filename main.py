# main.py
import os # env interacting tools
import sys # get access to cli
from dotenv import load_dotenv # tool to read .env files
from google import genai # get google generative ai tools
from google.genai import types # for prompt roles

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

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
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

# generate a response from Gemini
GeminiResp = client.models.generate_content(
    model=model, # version of gemini
    contents=messages, # our messages to AI
    config=types.GenerateContentConfig( # system config
        tools=[available_functions], # funcs as tools for LLM
        system_instruction=system_prompt # hardcoded system prompt on how do do things
        ),
)

# get gemini response most likely candidate response content
content = GeminiResp.candidates[0].content

# loop through each part of the most likely response content
for part in content.parts:
    if part.function_call:  # check if func call
        # get name and args of func call
        func_name = part.function_call.name # func called name
        func_args = part.function_call.args # args passed to func called

        # print the function call
        print(f"Calling function: {func_name}({func_args})")
    elif part.text: # check if text only
        print(part.text) # print text only

# token fields
GeminiPromptTokens = GeminiResp.usage_metadata.prompt_token_count
GeminiResponseTokens = GeminiResp.usage_metadata.candidates_token_count

# verbose flag to print extra info
if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
    # do a verbose output with prompt and tokens
    print(f"User prompt: {user_prompt}") # print the user prompt
    print(f"Prompt tokens: {GeminiPromptTokens}") # tokens in the prompt
    print(f"Response tokens: {GeminiResponseTokens}") # tokens in the response
