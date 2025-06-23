# tests.py

from functions.write_file import write_file


# do all function calls for testing with direct execution in the main guard
if __name__ == "__main__":
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(f"lorem.txt:\n{result}\n") # print to console
    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(f"pkg/morelorem.txt:\n{result}\n") # print to console
    result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(f"/tmp/temp.txt:\n{result}\n") # print to console
