# -*- coding: utf-8 -*-
import os
import sys
import tempfile

#Q3: any better idea?
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

def start_parsing(filename, adding_token):
    print 'filename = %s, token = %s' % (filename, adding_token)
    # create a temp file to store the parsing result.
    fd, path = tempfile.mkstemp(prefix=filename)
    print fd, path
    #Q2 need to close the handle?
    with os.fdopen(fd, 'w', 65536) as writer:
        with open(filename, 'r') as reader:
            lines = reader.readlines()
            for line in lines:
                result = find_and_replace(line, '{', adding_token)
                writer.write(result)
    #Q1 : windows will cause exception when the file is existing.
    os.rename(path, filename + 'new')

def main():
    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)
    filename = ''
    adding_token = 'printf("%s", __func__);'
    #Q4: any better logic?
    if len(sys.argv) > 1: 
        filename = str(sys.argv[1])
    if len(sys.argv) > 2: 
        adding_token = str(sys.argv[2])

    start_parsing(filename, adding_token)

if __name__ == '__main__':
    main()