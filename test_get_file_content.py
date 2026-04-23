from functions.get_file_content import get_file_content


def main():

    print("--- get_file_content_test:'calculator', 'lorem.txt' ---")
    test = get_file_content("calculator", "lorem.txt")
    print(f"Content length: {len(test)}")
    print(f"Last 100 chars: {test[-100:]}")
    print()

    cases = [
        ("calculator", "main.py"),
        ("calculator", "pkg/calculator.py"),
        ("calculator", "/bin/cat"),
        ("calculator", "pkg/does_not_exist.py"),
    ]
    for wd, fp in cases:
        print(f"--- get_file_content({wd!r}, {fp!r}) ---")
        result = get_file_content(wd, fp)
        print(result)
        print()


main()
