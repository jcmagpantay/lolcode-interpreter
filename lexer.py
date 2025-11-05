# Python lexer


# Reads the file to be lexically analyzed
def read_file(directory) -> str:
    """
    Read file directory to be analyzed.

    Args:
        directory (str): Path of the file.

    Returns:
        str: File contents as string.
    """ 

    # Error safety check

    with open(directory) as f:
      print(f.read())

def main():
    read_file("test/milestone1_test.lol")
if __name__ == "main":
    main()
