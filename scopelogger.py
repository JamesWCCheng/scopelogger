# -*- coding: utf-8 -*-
import os
import sys
import tempfile

def find_and_replace(line, ch, adding_token):
    index = line.find('{')
    # e.g 'if (nullptr) { [](){}; }' , first '{' is in index 13.
    # Thus, line[:index + 1] equals to 'if (nullptr) {'
    # line[index + 1:] equals to ' [](){}; }', recursively call with the remaining string.
    if index != -1:
        # recursive call to finish the remaining '{'
        line = line[:index + 1] + adding_token + find_and_replace(line[index + 1:], '{', adding_token)
    else:
        return line
    return line

def find_occurences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]

def start_parsing(filepath, adding_token):
    print 'filepath = %s, token = %s' % (filepath, adding_token)
    adding_token = ' ' + adding_token
    # create a temp file to store the parsing result.
    fd, path = tempfile.mkstemp(prefix=filepath)
    previous_line = ' '
    with os.fdopen(fd, 'w', 65536) as writer:
        with open(filepath, 'r') as reader:
            lines = reader.readlines()
            for line in lines:
                   # no need to process 'namespace {' case.
                   # no need to process '{' which may be the next line of 'namespace xxx'
                   # avoid this case 'foo({ xxx, yyy});'.
                   # cannot handle the constructing by {}
                if (not line.lstrip().startswith('namespace'))\
                   and (not (previous_line.lstrip().startswith('namespace') and line.lstrip().startswith('{')))\
                   and '({' not in line:
                  result = find_and_replace(line, '{', adding_token)
                  writer.write(result)
                else:
                  writer.write(line)
                previous_line = line
    # remove the original file
    os.remove(filepath)
    # write the processed file back to the original name.
    os.rename(path, filepath)

def main():
    filepath = ''
    adding_token = 'printf("%s", __func__);'
    if len(sys.argv) > 1:
        filepath = str(sys.argv[1])
    if len(sys.argv) > 2:
        adding_token = str(sys.argv[2])

    start_parsing(filepath, adding_token)

if __name__ == '__main__':
    main()