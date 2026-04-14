from functions.run_python_file import run_python_file


print("Result of execute 'main.py' python file:")
print(run_python_file("calculator", "main.py"))


print("\nResult of execute 'main.py' + '['3 + 5']' argument:")
print(run_python_file("calculator", "main.py", ["3 + 5"]))


print("\nResult of execute 'tests.py' python file:")
print(run_python_file("calculator", "tests.py"))


print("\nResult of execute '../main.py' python file outside of working_directory")
print(run_python_file("calculator", "../main.py"))


print("\nResult of execute 'nonexistent.py' python file:")
print(run_python_file("calculator", "nonexistent.py"))


print("\nResult of trying to execute txt file 'lorem.txt':")
print(run_python_file("calculator", "lorem.txt"))
