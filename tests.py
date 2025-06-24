# tests.py

from functions.run_python_file import run_python_file


# do all function calls for testing with direct execution in the main guard
if __name__ == "__main__":
    result = run_python_file("calculator", "main.py")
    print(f"main.py:\n{result}\n") # print to console
    result = run_python_file("calculator", "tests.py")
    print(f"tests.py:\n{result}\n") # print to console
    result = run_python_file("calculator", "../main.py")
    print(f"../main.py:\n{result}\n") # print to console
    result = run_python_file("calculator", "nonexistent.py")
    print(f"nonexistent.py:\n{result}\n") # print to console
