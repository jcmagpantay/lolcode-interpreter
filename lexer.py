# Python lexer

import re


# Reads the file to be lexically analyzed
def read_file(directory) -> str:
    """
    Read file directory to be analyzed.

    Args:
        directory (str): Path of the file.

    Returns:
        list: File contents as list of string per line.
    """ 

    # Error safety check

    with open(directory) as f:
        file_content = f.read()
        lines = file_content.split('\n')

        for line in lines:
            lexeme_line = lexify(line)

    return lines

def lex(directory):
    """
    Top-level function for lexical analysis.
    Calls `lexify` and `read_file` to perform lexing line-by-line

    Args:
        directory (str): The file to be lexified.

    Returns:
        list: A lexeme table containing tuple pairs of format: (match, pair).
    """
    lexeme_table = []

    lines = read_file(directory)

    for line in lines:
        lexeme_line = lexify(line)
        lexeme_table.extend(lexeme_line)

    return lexeme_table
        

def lexify(line):
    """
    Tokenize the string line into lexemes based on RegEx patterns

    Args:
        line (str): The line to be tokenized into lexemes.

    Returns:
        list: List of tuples (match, pattern) of identified lexemes per line.
    """

    # The list to be returned
    lexemes = []

    # List of RegEx patterns to be matched against.
    # NOTE: Order is important. Place the patterns carefully in prioritization.
    regex_library = {
        "CODE DELIMITER": [r"\bHAI\b"],
        "ARITHMETIC OPERATOR": [r"\bSUM OF\b", r"\DIFF OF\b", r"\bPRODUKT OF\b", r"\bQUOSHUNT OF\b" ],
        "VARIABLE LIST DELIMITER" :[r"\bWAZZUP\b", r"\bBUHBYE\b"],
        "VARIABLE DECLARATION": [r"\bI HAS A\b"],
        "VARIABLE ASSIGNMENT (following I HAS A)": [r"\bITZ\b"],
        "VAR_IDENTIFIER": [r"[a-zA-Z][a-zA-Z0-9_]*"],
        "STRING DELIMITER":[r"\""],
        "NUMBAR_LITERAL": [r"-?[0-9]+\.[0-9]+"],
        "NUMBR_LITERAL": [r"-?[0-9]+"],
        "YARN_LITERAL": ["\".*\""],
        "TROOF_LITERAL": [r"WIN|FAIL"],
        "TYPE_LITERAL": [r"NUMBR|NUMBAR|YARN|TROOF"],
        "IGNORE_S_T": [r"[ \t\n]"],
        "NO_MATCH": [r".+"]
    }

    # Exhausts all patterns in library
    for pattern in regex_library:
        for regex in regex_library[pattern]:
            # Find all matches of specific pattern
            matches = re.findall(regex, line)
            # ignore the line if it match to the comment
            if matches and matches[0] != "BTW":
                # Then append it to the variable to be returned
                for match in matches:
                    lexemes.append((match, pattern))

            # Remove the specific pattern from line to avoid double-matching
            line = re.sub(regex, '', line)

    return lexemes

def display_table(table):
    
    # Formatting variables
    token_width = 16
    pattern_width = 24

    print(f"{'Token':>{token_width}}  {'Pattern':>{pattern_width}}")
    print("-" * (token_width + pattern_width + 2))

    for (token, pattern) in table:
        if pattern == "IGNORE_S_T":
            continue

        print(f"{token:>{token_width}}  ", end = "")
        print(f"{pattern:>{pattern_width}}")

def clean(token):
    """
    Clean the token by removing any noisy input.

    Args:
        token (str): The token to be cleaned.

    Returns:
        str: The cleaned token.
    """
    pass


def main():
    lexeme_table = lex("test/simple_test.lol")
    
    display_table(lexeme_table)

if __name__ == "__main__":
    main()
