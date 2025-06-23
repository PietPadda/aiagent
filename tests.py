# tests.py

from functions.get_files_info import get_files_info 


# do all function calls for testing with direct execution in the main guard
if __name__ == "__main__":
    result = get_files_info("calculator", ".") # get all in the calculator dir
    print(result) # print to console
    result = get_files_info("calculator", "pkg") # get all in the pkg subfolder
    print(result) # print to console
    result = get_files_info("calculator", "/bin") # should err as /bin is an absolute path not in calc dir
    print(result) # print to console
    result = get_files_info("calculator", "../") # should err as prev dir is not inside calculator dir
    print(result) # print to console
