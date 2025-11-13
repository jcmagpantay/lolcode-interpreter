# Python lexer

import re


# changed this to string param
# because of the implementation in the gui (executing line by line)
def lex(code_string):
    """
    Top-level function for lexical analysis.
    Calls `lexify` and `read_file` to perform lexing line-by-line

    Args:
        directory (str): The file to be lexified.

    Returns:
        list: A lexeme table containing tuple pairs of format: (match, pair).
    """
    lexeme_table = []

    lines = code_string.split('\n')

    skip_line = False #flag sana to ignore lines pero di ko pa napagana


    for idx,line in enumerate(lines):

        #if nasa loob ng  block comment, look for TLDR
        if skip_line:
            if "TLDR" in line:

                # resume AFTER TLDR on the same line
                line = line.split("TLDR", 1)[1]
                skip_line = False

            else:
                # still inside block, skip line
                continue

        #outside of a block: remove any OBTW, TLDR that might be on this same line
        #sensing the case of having multiple OBTW/TLDR pairs in one line; handle them iteratively.
        while True:

            start = line.find("OBTW")

            if start == -1:
                break

            end = line.find("TLDR", start + 4)

            if end == -1:
                #start block comment and keep only the part BEFORE OBTW
                line = line[:start]
                skip_line = True
                break

            else:
                #remove the OBTW...TLDR segment and keep both sides
                line = line[:start] + line[end + 4:]

        if skip_line:
            #when entered a block comment and no TLDR yet; skip the rest of this line
            continue

        # Ignore everything after
        if "BTW" in line:
            line = line.split("BTW")[0]  # keep only before BTW
        lexeme_line = lexify(line, idx + 1)
        lexeme_table.extend(lexeme_line)


    return lexeme_table       

def lexify(line, line_no):
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
        "CODE DELIMITER": [r"\bHAI\b",r"\bKTHXBYE\b"],
        "ARITHMETIC OPERATOR": [r"\bSUM OF\b", r"\DIFF OF\b", r"\bPRODUKT OF\b", r"\bQUOSHUNT OF\b", r"\bMOD OF\b", r"\bBIGGR OF\b", r"\bSMALLR OF\b"],
        "VARIABLE LIST DELIMITER" :[r"\bWAZZUP\b", r"\bBUHBYE\b"],
        "ASSIGNMENT R":[r"\ R\ "],
        "BOOLEAN OPERATOR": [r"\bBOTH OF\b", r"\bEITHER OF\b", r"\bWON OF\b", r"\bNOT\b", r"\bALL OF\b", r"\bANY OF\b"],
        "COMPARISON OPERATOR": [r"\bBOTH SAEM\b", r"\bDIFFRINT\b"],
        "FLOW CONTROL DELIMITER": [r"\bO RLY\?\b",r"\bWTF\?\b", r"\bOIC\b"],
        "IF OPERATOR": [r"\bYA RLY\b"],
        "ELSE OPERATOR":[r"\bNO WAI\b"],
        "CASE OPERATOR":[r"\bOMG\b",r"\bOMGWTF\b"],
        "LOOP DELIMITER": [r"\bIM IN\b", r"\bIM OUTTA\b", r"\bTIL\b", r"\bWILE\b"],
        "LOOP NEST":[r"\bMEBBE\b"],
        "NUM CAST OPERATOR":[r"\bUPPIN\b",r"\bNERFIN\b"],
        "PARAMETER": [r"\bYR\b"],
        "FUNCTION DELIMITER":[r"\bHOW IZ I\b", r"\bIF U SAY SO\b"],
        "FUNCTION CALL DELIMITER":[r"\bI IZ\b", r"\bMKAY\b"],
        "CONCAT OPERATOR" :[r"\bSMOOSH\b"],
        "TYPECAST OPERATOR": [r"\bMAEK\b"],
        "RECAST OPERATOR": [r"\b IS NOW A\b"],
        "RETURN KEYWORD": [r"\bFOUND\b",r"\bGTFO\b"],
        "OUTPUT KEYWORD": [r"\bVISIBLE\b"],
        "INPUT KEYWORD": [r"\bGIMMEH\b"],
        "PARAMETER SEPARATOR": [r"\bAN\b"],
        "VARIABLE DECLARATION": [r"\bI HAS A\b"],
        "VARIABLE ASSIGNMENT (following I HAS A)": [r"\bITZ\b"],
        "TYPECAST A": [r"\ A\ "],
        "NUMBAR LITERAL": [r"-?[0-9]+\.[0-9]+"],
        "NUMBR LITERAL": [r"-?[0-9]+"],
        "YARN LITERAL": [r"\"(.*?)\""],
        "VAR IDENTIFIER": [r"[a-zA-Z][a-zA-Z0-9_]*"],
        "TROOF LITERAL": [r"WIN|FAIL"],
        "TYPE LITERAL": [r"NUMBR|NUMBAR|YARN|TROOF"],

        # Ignore space and tabs
        "IGNORE_S_T": [r"[ \t\n]"],

        # Catch no matches
        "NO_MATCH": [r".+"]
    }

    matches_tuple = []

    # Exhausts all patterns in library
    for pattern in regex_library:
        for regex in regex_library[pattern]:
            # Find all matches of specific pattern
            matches = re.finditer(regex, line)
            # ignore the line if it match to the comment
            for match in matches:
                matches_tuple.append((match.start(), match.end(), match.group(), pattern))

    matches_tuple.sort(key=lambda m: m[0])

    # Filters duplicate tokens and intersecting tokens
    seen_tokens = set()
    for start, end, word, pattern in matches_tuple:
        overlapping = False
        new_tok = (start, end)

        if not seen_tokens:
            lexemes.append((word, pattern))
            seen_tokens.add((start, end))

        for seen in seen_tokens:
            if overlaps(new_tok, seen):
                overlapping = True

        if not overlapping:
            seen_tokens.add((start, end))
            lexemes.append((word, pattern))
    # to separate "" from yarns
    cleaned_lexemes = []
    for word, classification in lexemes:
        if classification == "YARN LITERAL":
            # get first "
            cleaned_lexemes.append((word[0], "STRING DELIMITER", line_no))
            # get word
            cleaned_lexemes.append((word[1:len(word)-1], classification, line_no))
            # get ending "
            cleaned_lexemes.append((word[-1], "STRING DELIMITER", line_no))
        else:
            cleaned_lexemes.append((word,classification,line_no))

        

    return cleaned_lexemes

def overlaps(x, y):
    """Return True if intervals x and y overlap."""
    return not (x[1] <= y[0] or y[1] <= x[0])

def display_table(table):
    
    # Formatting variables
    token_width = 16
    pattern_width = 48

    print(f"{'Token':>{token_width}}  {'Pattern':>{pattern_width}}")
    print("-" * (token_width + pattern_width + 2))

    for (token, pattern, line_no) in table:
        if pattern == "IGNORE_S_T":
            continue

        print(f"[{line_no}]{token:>{token_width}}  ", end = "")
        print(f"{pattern:>{pattern_width}}")


def main():
    # edited so this can still run properly
    with open("test/milestone1_test.lol", 'r') as f:
        code = f.read()
    lexeme_table = lex(code)
    
    display_table(lexeme_table)

if __name__ == "__main__":
    main()
