from functions.get_write_file import write_file

print("Result for writing 'lorem.txt' file:")
print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))

print("\nResult for writing 'pkg/morelorem' file:")
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

print("\nResult for writing '/tmp/temp.txt' file:")
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
