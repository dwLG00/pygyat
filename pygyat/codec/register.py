#!/usr/bin/env python


import codecs, io, encodings
import sys
import traceback
from encodings import utf_8
from pygyat.parser import parse_file_contents

def pygyat_transform(stream):
    text = stream.read()
    return pygyat_transform_string(text)

def pygyat_transform_string(text):
    output = parse_file_contents(text)
    #return 'print("hi")\n'.encode('utf-8')
    return output.encode('utf-8')

def pygyat_decode(input, errors='strict'):
    return utf_8.decode(pygyat_transform_string(input), errors)

class PyGyatIncrementalDecoder(utf_8.IncrementalDecoder):
    def decode(self, input, final=False):
        self.buffer += input
        if final:
            buff = self.buffer
            #return super().decode(buff, final=True)
            #print('buffer: %s' % buff)
            gyatt_transformed = pygyat_transform_string(buff.decode('utf-8')).decode('utf-8')
            self.buffer = b''
            if gyatt_transformed == '\n':
                return ''
            return gyatt_transformed
        else:
            return ''

class PyGyatStreamReader(utf_8.StreamReader):
    def __init__(self, *args, **kwargs):
        codecs.StreamReader.__init__(self, *args, **kwargs)
        self.stream = io.StringIO(pygyat_transform(self.stream))

def search_function(encoding):
    if encoding != 'pygyat': return None
    utf8 = encodings.search_function('utf8')
    return codecs.CodecInfo(
        name = 'pygyat',
        encode=utf8.encode,
        #decode=utf8.decode,
        decode=pygyat_decode,
        incrementalencoder = utf8.incrementalencoder,
        #incrementaldecoder = utf8.incrementaldecoder,
        incrementaldecoder = PyGyatIncrementalDecoder,
        #streamreader = utf8.streamreader,
        streamreader = PyGyatStreamReader,
        #streamwriter = utf8.streamwriter
    )

codecs.register(search_function)

_USAGE = """\
Wraps a python command to allow it to recognize pygyat files with
no source modifications.

Usage:
    python -m pygyat.codec.register -m module.to.run [args...]
    python -m pygyat.codec.register path/to/script.py [args...]
"""

if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == '-m':
        mode = 'module'
        module = sys.argv[2]
        del sys.argv[1:3]
    elif len(sys.argv) >= 2:
        mode = 'script'
        script = sys.argv[1]
        sys.argv = sys.argv[1:]
    else:
        print((sys.stderr, _USAGE))
        sys.exit(1)

    if mode == 'module':
        import runpy
        runpy.run_module(module, run_name='__main__', alter_sys=True)
    elif mode == 'script':
        with open(script) as f:
            global __file__
            __file__ = script
            # Use globals as our "locals" dictionary so that something
            # that tries to import __main__ (e.g. the unittest module)
            # will see the right things.
            exec(f.read(), globals(), globals())
