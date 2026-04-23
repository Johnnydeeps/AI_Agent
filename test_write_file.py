from functions.write_file import write_file


def main():

    cases = [
        ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
        ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
        ("calculator", "/tmp/temp.txt", "this should not be allowed"),
    ]

    for working_directory, file_path, content_to_add in cases:
        print(
            f"--- write_file({working_directory!r}, {file_path!r}, {content_to_add!r}) ---"
        )
        result = write_file(working_directory, file_path, content_to_add)
        print(result)
        print()


main()
