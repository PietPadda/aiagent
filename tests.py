# tests.py

from functions.get_file_content import get_file_content


# do all function calls for testing with direct execution in the main guard
if __name__ == "__main__":
    result = get_file_content("calculator", "main.py")
    print(f"main.py:\n{result}\n") # print to console
    result = get_file_content("calculator", "pkg/calculator.py")
    print(f"pkg/calculator.py:\n{result}\n") # print to console
    result = get_file_content("calculator", "/bin/cat")
    print(f"/bin/cat:\n{result}\n") # print to console
