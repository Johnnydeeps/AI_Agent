from functions.run_python_file import run_python_file


def main():

    cases = [
        ("calculator", "main.py"),
        ("calculator", "main.py", "3 + 5"),
        ("calculator", "../main.py"),
        ("calculator", "tests.py"),
        ("calculator", "nonexistent.py"),
        ("calculator", "lorem.txt"),
    ]

    for working_directory, file_path, *args in cases:
        print(
            f"--- run_python_file({working_directory!r}, {file_path!r}, {args!r}) ---"
        )
        result = run_python_file(working_directory, file_path, args)
        print(result)
        print()


main()
