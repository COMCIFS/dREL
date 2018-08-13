#!/usr/bin/env python

# A simple code filter for Pandoc to extract only the code blocks in a file

from pandocfilters import toJSONFilter, Para, Str, Space, CodeBlock, RawBlock

def getcode(key,value,format,_):
    if key == 'CodeBlock' or key == 'RawBlock':
        mm,t = value
        return CodeBlock(mm,t)
    elif key in ['Para','OrderedList','Header']:
        return Para([Space()])

if __name__ == "__main__":
    toJSONFilter(getcode)
