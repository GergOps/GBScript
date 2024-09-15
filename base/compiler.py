import os
import sys

_funcs = {}
_gfuncs = []
_vars = {}
func = ""

main = open("main.gb", "r")


def print(s):
    os.system(f"echo {s}")


def var(s):
    global _vars
    global _funcs
    if s[3] in _funcs:
        print(f"ERROR: {s[3]} IS FUNCTION")
        sys.exit()
    if s[2] == "=":
        _vars[s[1]] = [getType(s[3]), getValue(s[3])]
    elif s[2] == "+=":
        if s[1] in _vars:
            if _vars[s[1]][0] == "str":
                _vars[s[1]][1] += f"{getValue(s[3])}"
            elif _vars[s[1]][0] == "int":
                if getType(s[3]) == "int":
                    _vars[s[1]][1] += getValue(s[3])
            elif _vars[s[1]][0] == "arr":
                if getType(s[3]) == "arr":
                    _vars[s[1]][1] += getValue(s[3])
                else:
                    _vars[s[1]][1].append(getValue(s[3]))
    elif s[2] == "-=":
        if _vars[s[1]][0] == "int":
            if getType(s[3]) == "int":
                _vars[s[1]][1] -= getValue(s[3])


def calling(s):
    global _funcs
    global _vars
    varss = _vars
    if not (s in _funcs):
        print(f"ERROR: FUNCTION {s} NOT FOUNDED")
        sys.exit()
    for i in _funcs[s]:
        if i[0] == "var":
            var(i)
        elif i[0] == "print":
            if i[1] in _vars:
                print(_vars[i[1]][1])
            else:
                print(getValue(i[1]))
        elif i[0] == "call":
            calling(i[1])
    if not s[0] in _gfuncs:
        _vars = varss


def getValue(var):
    if var in _vars:
        return _vars[var][1]
    if getType(var) == "str":
        return var[1:-1]
    if getType(var) == "int":
        return int(var)

    # todo Array
    """
    if var[0] == '[' and var[-1] == ']':
        return var[1:-1].split(", ")
    """

    # todo Dictionary
    """  
        if var[0] == '{' and var[-1] == "}":
            l = var[1:-1].split(", ")
            for k in l:
                n = k.split(": ")
    """


def getType(var):
    if var in _vars:
        return _vars[var]
    if var[0] == '"' and var[-1] == '"' or var[0] == "'" and var[-1] == "'":
        return "str"
    try:
        int(var)
        return "int"
    except:
        gg = False
    if var[0] == '[' and var[-1] == ']':
        return "arr"
    if var[0] == '{' and var[-1] == '}':
        return "dict"

    print("ERROR: TYPE ERROR")
    os.system("pause")
    sys.exit()


for line in main:
    s = []
    word = ""
    op = ""

    # Splitting line
    for i in range(len(line) - 1):
        if len(op) == 0:
            if line[i] == "'" or line[i] == '"' or line[i] == "[" or line[i] == "{":
                op += line[i]
                word += line[i]
            elif line[i] == "]" or line[i] == "}":
                print("ERROR: BRACKETS ERROR")
                os.system("pause")
                sys.exit()
            elif line[i] == " " and word != "":
                s.append(word)
                word = ""
            elif line[i] != " ":
                word += line[i]
                if i == len(line) - 2:
                    s.append(word)
        elif line[i] == "'" and op[-1] != "'" or line[i] == '"' and op[-1] != '"' or line[i] == "[" or line[i] == "{":
            op += line[i]
            word += line[i]
        elif line[i] == "'" or line[i] == '"' or line[i] == "]" and op[-1] == "[" or line[i] == "}" and op[-1] == "{":
            op = op[:-1]
            word += line[i]
            if i == len(line) - 2:
                if word != "":
                    s.append(word)
        elif line[i] == "]" or line[i] == "}":
            print("ERROR: BRACKETS ERROR")
            os.system("pause")
            sys.exit()
        else:
            word += line[i]
            if i == len(line) - 2:
                s.append(word)

    # Checking code
    if s[0] == "var":
        if func != "":
            _funcs[func].append(s)
            continue
        var(s)
    elif s[0] == "print":
        if func != "":
            _funcs[func].append(s)
            continue
        if s[1] in _vars:
            print(_vars[s[1]][1])
        else:
            print(getValue(s[1]))
    elif s[0] == "function":
        if func != "":
            print("ERROR: DECLARING FUNCTION IN FUNCTION")
            os.system("pause")
            sys.exit()
        if len(s) == 3 and s[1] == "global":
            func = s[2]
            _gfuncs.append(s[2])
        else:
            func = s[1]
        _funcs[func] = []
    elif s[0] == "endf":
        if func == "":
            print("ERROR: ENDING NO FUNCTION")
            os.system("pause")
            sys.exit()
        func = ""
    elif s[0] == "call":
        if func != "":
            _funcs[func].append(s)
            continue
        calling(s[1])

os.system("pause")
